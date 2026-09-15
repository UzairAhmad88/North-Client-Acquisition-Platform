"""Business service layer for Identity, Sessions, RBAC, MFA, API Keys, and Security Audit."""

from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Any, Dict, List, Optional, Tuple
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError, ValidationError
from app.models.security import APIKey, Role, SecurityEvent, Tenant, UserSession
from app.models.user import User
from app.repositories.security import SecurityRepository
from app.schemas.security import (
    APIKeyCreatedResponse,
    APIKeyCreateRequest,
    MFASetupResponse,
    SecurityMetricsResponse,
    StepUpAuthResponse,
    UserInviteRequest,
    UserProfileResponse,
)
from app.security.audit import SecurityEventType, SecuritySeverity
from app.security.mfa import MFAService
from app.security.password import hash_password, validate_password_policy, verify_password
from app.security.permissions import PERMISSION_REGISTRY, SystemPermissions, list_permissions
from app.security.principals import Principal, PrincipalStatus, PrincipalType, SecurityContext
from app.security.roles import ROLE_PERMISSIONS_MAP, SystemRole, get_role_permissions
from app.security.sessions import SessionManager


class SecurityService:
    """Provides high-level security operations and identity orchestration."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = SecurityRepository(db)

    # 1. User & Identity Management
    def invite_user(self, req: UserInviteRequest, inviter_id: str) -> UserProfileResponse:
        existing = self.db.query(User).filter(User.email == req.email.lower()).first()
        if existing:
            raise ValidationError(f"User with email '{req.email}' already exists.")

        temp_password = secrets.token_urlsafe(12)
        valid, msg = validate_password_policy(temp_password)
        pw_hash = hash_password(temp_password)

        default_tenant = self.repo.get_or_create_default_tenant()

        user = User(
            email=req.email.lower(),
            password_hash=pw_hash,
            full_name=req.full_name,
            is_active=True,
            is_verified=False,
            role=req.role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Assign Role
        role_obj = self.repo.get_role_by_name(req.role)
        if not role_obj:
            role_obj = Role(name=req.role, description=f"{req.role} role", is_internal=True)
            self.db.add(role_obj)
            self.db.commit()
            self.db.refresh(role_obj)

        self.repo.assign_user_role(
            user_id=user.id,
            role_id=role_obj.id,
            tenant_id=default_tenant.id,
            scope_type="GLOBAL",
            assigned_by=uuid.UUID(inviter_id) if inviter_id != "system" else None,
        )

        self.repo.record_security_event(
            event_type=SecurityEventType.USER_READ.value if hasattr(SecurityEventType, "USER_READ") else "USER_INVITED",
            severity=SecuritySeverity.INFO.value,
            principal_id=inviter_id,
            action="user.invite",
            resource="user",
            resource_id=str(user.id),
            result="ALLOW",
            details={"email": req.email, "role": req.role},
        )

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
            roles=[user.role],
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )

    def list_users(self) -> List[UserProfileResponse]:
        users = self.db.query(User).order_by(User.email).all()
        results = []
        for u in users:
            roles = self.repo.get_user_roles(u.id)
            if not roles:
                roles = [u.role]
            results.append(
                UserProfileResponse(
                    id=u.id,
                    email=u.email,
                    full_name=u.full_name,
                    is_active=u.is_active,
                    is_verified=u.is_verified,
                    role=u.role,
                    roles=roles,
                    created_at=u.created_at,
                    last_login_at=u.last_login_at,
                )
            )
        return results

    def suspend_user(self, user_id: uuid.UUID, actor_id: str, reason: str = "ADMIN_SUSPENSION") -> UserProfileResponse:
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = False
        self.db.commit()

        # Invalidate all active sessions immediately
        self.repo.revoke_all_user_sessions(user_id, reason=reason)

        self.repo.record_security_event(
            event_type=SecurityEventType.ACCOUNT_SUSPENDED.value,
            severity=SecuritySeverity.HIGH.value,
            principal_id=actor_id,
            action="user.suspend",
            resource="user",
            resource_id=str(user_id),
            result="ALLOW",
            details={"reason": reason},
        )

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
            roles=[user.role],
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )

    def activate_user(self, user_id: uuid.UUID, actor_id: str) -> UserProfileResponse:
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = True
        self.db.commit()

        self.repo.record_security_event(
            event_type="ACCOUNT_ACTIVATED",
            severity=SecuritySeverity.INFO.value,
            principal_id=actor_id,
            action="user.activate",
            resource="user",
            resource_id=str(user_id),
            result="ALLOW",
            details={"email": user.email},
        )

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
            roles=[user.role],
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )

    # 2. Session Management
    def list_sessions(self, user_id: uuid.UUID) -> List[UserSession]:
        return self.repo.list_user_sessions(user_id)

    def revoke_session(self, session_id: uuid.UUID, actor_id: str) -> bool:
        session = self.repo.revoke_session(session_id, reason=f"REVOKED_BY_{actor_id}")
        if session:
            self.repo.record_security_event(
                event_type=SecurityEventType.SESSION_REVOKED.value,
                severity=SecuritySeverity.INFO.value,
                principal_id=actor_id,
                action="session.revoke",
                resource="session",
                resource_id=str(session_id),
                result="ALLOW",
            )
            return True
        return False

    def revoke_all_sessions(self, user_id: uuid.UUID, actor_id: str) -> int:
        count = self.repo.revoke_all_user_sessions(user_id, reason=f"REVOKED_ALL_BY_{actor_id}")
        self.repo.record_security_event(
            event_type=SecurityEventType.SESSION_REVOKED.value,
            severity=SecuritySeverity.MEDIUM.value,
            principal_id=actor_id,
            action="session.revoke_all",
            resource="user_sessions",
            resource_id=str(user_id),
            result="ALLOW",
            details={"revoked_count": count},
        )
        return count

    # 3. MFA & Step-Up Authentication
    def setup_mfa(self, user_id: uuid.UUID) -> MFASetupResponse:
        secret = MFAService.generate_totp_secret()
        backup_codes = MFAService.generate_backup_codes()
        qr_uri = f"otpauth://totp/Uzaii:{user_id}?secret={secret}&issuer=Uzaii"
        return MFASetupResponse(secret=secret, backup_codes=backup_codes, qr_code_uri=qr_uri)

    def verify_step_up_auth(self, user_id: uuid.UUID, password: str, tenant_id: str) -> StepUpAuthResponse:
        user = self.db.get(User, user_id)
        if not user or not verify_password(password, user.password_hash):
            self.repo.record_security_event(
                event_type="STEP_UP_FAILED",
                severity=SecuritySeverity.MEDIUM.value,
                principal_id=str(user_id),
                result="DENY",
                reason_code="INVALID_PASSWORD",
            )
            raise UnauthorizedError("Invalid credentials for step-up authentication.")

        token = MFAService.create_step_up_token(str(user_id), tenant_id)
        self.repo.record_security_event(
            event_type="STEP_UP_SUCCESS",
            severity=SecuritySeverity.INFO.value,
            principal_id=str(user_id),
            result="ALLOW",
            reason_code="VERIFIED",
        )
        return StepUpAuthResponse(step_up_token=token)

    # 4. API Keys
    def create_api_key(self, user_id: uuid.UUID, req: APIKeyCreateRequest) -> APIKeyCreatedResponse:
        default_tenant = self.repo.get_or_create_default_tenant()
        prefix = f"uz_{secrets.token_hex(4)}"
        secret_part = secrets.token_urlsafe(32)
        full_key = f"{prefix}_{secret_part}"
        key_hash = hashlib.sha256(full_key.encode("utf-8")).hexdigest()

        expires_at = None
        if req.expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=req.expires_in_days)

        api_key = self.repo.create_api_key(
            tenant_id=default_tenant.id,
            name=req.name,
            key_prefix=prefix,
            key_hash=key_hash,
            scopes=req.scopes,
            user_id=user_id,
            expires_at=expires_at,
        )

        self.repo.record_security_event(
            event_type=SecurityEventType.API_KEY_CREATED.value,
            severity=SecuritySeverity.MEDIUM.value,
            principal_id=str(user_id),
            action="api_key.create",
            resource="api_key",
            resource_id=str(api_key.id),
            result="ALLOW",
            details={"name": req.name, "scopes": req.scopes},
        )

        return APIKeyCreatedResponse(
            id=api_key.id,
            name=api_key.name,
            key_prefix=prefix,
            secret_key=full_key,
            scopes=req.scopes,
            expires_at=expires_at,
        )

    def list_api_keys(self) -> List[APIKey]:
        default_tenant = self.repo.get_or_create_default_tenant()
        return self.repo.list_api_keys(default_tenant.id)

    def revoke_api_key(self, key_id: uuid.UUID, actor_id: str) -> bool:
        key = self.repo.revoke_api_key(key_id)
        if key:
            self.repo.record_security_event(
                event_type=SecurityEventType.API_KEY_REVOKED.value,
                severity=SecuritySeverity.HIGH.value,
                principal_id=actor_id,
                action="api_key.revoke",
                resource="api_key",
                resource_id=str(key_id),
                result="ALLOW",
            )
            return True
        return False

    # 5. Security Metrics & Audit
    def get_security_metrics(self) -> SecurityMetricsResponse:
        default_tenant = self.repo.get_or_create_default_tenant()
        now = datetime.now(timezone.utc)
        since_24h = now - timedelta(hours=24)

        active_sessions = self.db.query(UserSession).filter(
            UserSession.is_revoked == False, UserSession.expires_at > now
        ).count()
        total_users = self.db.query(User).count()
        events_24h = self.db.query(SecurityEvent).filter(SecurityEvent.occurred_at >= since_24h).count()
        failed_logins_24h = self.db.query(SecurityEvent).filter(
            SecurityEvent.occurred_at >= since_24h,
            SecurityEvent.event_type == SecurityEventType.LOGIN_FAILURE.value,
        ).count()
        active_keys = self.db.query(APIKey).filter(APIKey.is_revoked == False).count()

        return SecurityMetricsResponse(
            active_sessions_count=active_sessions,
            users_count=total_users,
            security_events_last_24h=events_24h,
            failed_logins_last_24h=failed_logins_24h,
            mfa_enabled_users_count=0,
            api_keys_active_count=active_keys,
        )

    def list_security_events(self, limit: int = 50) -> List[SecurityEvent]:
        return self.repo.list_security_events(limit=limit)
