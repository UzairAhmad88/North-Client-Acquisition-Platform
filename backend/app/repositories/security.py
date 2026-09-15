"""Repository layer for Security, Identity, Sessions, API Keys, and Audit Logs."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import uuid

from sqlalchemy import and_, desc, or_, select
from sqlalchemy.orm import Session

from app.models.security import (
    APIKey,
    AgentIdentity,
    AgentPermissionAssignment,
    Organization,
    OrganizationMember,
    Permission,
    ProjectMembership,
    Role,
    RolePermission,
    SecurityEvent,
    ServiceAccount,
    Tenant,
    UserCredential,
    UserMFAMethod,
    UserRole,
    UserSession,
)
from app.models.user import User


class SecurityRepository:
    """Encapsulates database access for Identity, RBAC, Sessions, and Security Audit."""

    def __init__(self, db: Session):
        self.db = db

    # 1. Tenant Operations
    def get_or_create_default_tenant(self) -> Tenant:
        stmt = select(Tenant).where(Tenant.slug == "default-tenant")
        tenant = self.db.scalars(stmt).first()
        if not tenant:
            tenant = Tenant(
                name="North's Primary Tenant",
                slug="default-tenant",
                tenant_type="INTERNAL",
                status="ACTIVE",
                config={},
            )
            self.db.add(tenant)
            self.db.commit()
            self.db.refresh(tenant)
        return tenant

    def get_tenant_by_id(self, tenant_id: str) -> Optional[Tenant]:
        try:
            uid = uuid.UUID(tenant_id)
            return self.db.get(Tenant, uid)
        except (ValueError, TypeError):
            return None

    # 2. Session Operations
    def create_session(
        self,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        is_mfa: bool = False,
    ) -> UserSession:
        now = datetime.now(timezone.utc)
        session = UserSession(
            user_id=user_id,
            tenant_id=tenant_id,
            token_hash=token_hash,
            expires_at=expires_at,
            last_seen_at=now,
            ip_address=ip_address,
            user_agent=user_agent,
            is_mfa_authenticated=is_mfa,
            is_revoked=False,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_by_token_hash(self, token_hash: str) -> Optional[UserSession]:
        stmt = select(UserSession).where(
            and_(UserSession.token_hash == token_hash, UserSession.is_revoked == False)
        )
        return self.db.scalars(stmt).first()

    def list_user_sessions(self, user_id: uuid.UUID) -> List[UserSession]:
        stmt = (
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .order_by(desc(UserSession.last_seen_at))
        )
        return list(self.db.scalars(stmt).all())

    def revoke_session(self, session_id: uuid.UUID, reason: str = "USER_LOGOUT") -> Optional[UserSession]:
        session = self.db.get(UserSession, session_id)
        if session:
            session.is_revoked = True
            session.revoked_at = datetime.now(timezone.utc)
            session.revocation_reason = reason
            self.db.commit()
            self.db.refresh(session)
        return session

    def revoke_all_user_sessions(self, user_id: uuid.UUID, reason: str = "GLOBAL_LOGOUT") -> int:
        stmt = select(UserSession).where(
            and_(UserSession.user_id == user_id, UserSession.is_revoked == False)
        )
        sessions = list(self.db.scalars(stmt).all())
        now = datetime.now(timezone.utc)
        for s in sessions:
            s.is_revoked = True
            s.revoked_at = now
            s.revocation_reason = reason
        self.db.commit()
        return len(sessions)

    # 3. Roles & Permissions Operations
    def list_roles(self) -> List[Role]:
        stmt = select(Role).order_by(Role.name)
        return list(self.db.scalars(stmt).all())

    def get_role_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name)
        return self.db.scalars(stmt).first()

    def list_permissions(self) -> List[Permission]:
        stmt = select(Permission).order_by(Permission.resource, Permission.action)
        return list(self.db.scalars(stmt).all())

    def get_user_roles(self, user_id: uuid.UUID) -> List[str]:
        stmt = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        return list(self.db.scalars(stmt).all())

    def assign_user_role(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scope_type: str = "GLOBAL",
        scope_id: Optional[str] = None,
        assigned_by: Optional[uuid.UUID] = None,
    ) -> UserRole:
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            tenant_id=tenant_id,
            scope_type=scope_type,
            scope_id=scope_id,
            assigned_by=assigned_by,
        )
        self.db.add(user_role)
        self.db.commit()
        self.db.refresh(user_role)
        return user_role

    def remove_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> bool:
        stmt = select(UserRole).where(
            and_(UserRole.user_id == user_id, UserRole.role_id == role_id)
        )
        user_role = self.db.scalars(stmt).first()
        if user_role:
            self.db.delete(user_role)
            self.db.commit()
            return True
        return False

    # 4. API Key Operations
    def create_api_key(
        self,
        tenant_id: uuid.UUID,
        name: str,
        key_prefix: str,
        key_hash: str,
        scopes: List[str],
        user_id: Optional[uuid.UUID] = None,
        expires_at: Optional[datetime] = None,
    ) -> APIKey:
        api_key = APIKey(
            tenant_id=tenant_id,
            user_id=user_id,
            name=name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            scopes=scopes,
            expires_at=expires_at,
            is_revoked=False,
        )
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    def list_api_keys(self, tenant_id: uuid.UUID) -> List[APIKey]:
        stmt = select(APIKey).where(APIKey.tenant_id == tenant_id).order_by(desc(APIKey.created_at))
        return list(self.db.scalars(stmt).all())

    def revoke_api_key(self, key_id: uuid.UUID) -> Optional[APIKey]:
        key = self.db.get(APIKey, key_id)
        if key:
            key.is_revoked = True
            self.db.commit()
            self.db.refresh(key)
        return key

    # 5. Security Audit Logging
    def record_security_event(
        self,
        event_type: str,
        severity: str,
        principal_id: str,
        principal_type: str = "USER",
        tenant_id: str = "default_tenant",
        action: Optional[str] = None,
        resource: Optional[str] = None,
        resource_id: Optional[str] = None,
        result: str = "ALLOW",
        reason_code: str = "SUCCESS",
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> SecurityEvent:
        event = SecurityEvent(
            event_type=event_type,
            severity=severity,
            principal_id=principal_id,
            principal_type=principal_type,
            tenant_id=tenant_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            result=result,
            reason_code=reason_code,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            occurred_at=datetime.now(timezone.utc),
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def list_security_events(
        self,
        tenant_id: Optional[str] = None,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 50,
    ) -> List[SecurityEvent]:
        query = select(SecurityEvent)
        conditions = []
        if tenant_id:
            conditions.append(SecurityEvent.tenant_id == tenant_id)
        if event_type:
            conditions.append(SecurityEvent.event_type == event_type)
        if severity:
            conditions.append(SecurityEvent.severity == severity)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(SecurityEvent.occurred_at)).limit(limit)
        return list(self.db.scalars(query).all())
