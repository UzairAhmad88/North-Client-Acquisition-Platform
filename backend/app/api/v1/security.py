"""REST API endpoints for Security, Identity, Sessions, RBAC, API Keys, and Audit."""

from typing import List
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db, get_security_context, require_permission, require_role
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.security import (
    APIKeyCreatedResponse,
    APIKeyCreateRequest,
    APIKeyResponse,
    MFASetupResponse,
    MFAVerifyRequest,
    PermissionResponse,
    RevokeSessionRequest,
    RoleResponse,
    SecurityEventResponse,
    SecurityMetricsResponse,
    SessionResponse,
    StepUpAuthRequest,
    StepUpAuthResponse,
    UserInviteRequest,
    UserProfileResponse,
    UserRoleAssignmentRequest,
)
from app.security.permissions import list_permissions
from app.security.principals import SecurityContext
from app.security.roles import ROLE_PERMISSIONS_MAP
from app.services.security import SecurityService

router = APIRouter(prefix="/security", tags=["Security & Identity"])


# 1. User Directory & Identity Management
@router.get("/users", response_model=DataResponse[List[UserProfileResponse]])
def list_users(
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("user.read")),
):
    """List all registered users with their assigned roles."""
    service = SecurityService(db)
    users = service.list_users()
    return DataResponse(data=users)


@router.post("/users/invite", response_model=DataResponse[UserProfileResponse], status_code=status.HTTP_201_CREATED)
def invite_user(
    req: UserInviteRequest,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("user.manage")),
):
    """Invite a new internal team or client user."""
    service = SecurityService(db)
    user = service.invite_user(req, inviter_id=security_ctx.principal.id)
    return DataResponse(data=user)


@router.post("/users/{user_id}/suspend", response_model=DataResponse[UserProfileResponse])
def suspend_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("user.manage")),
):
    """Suspend user account and revoke all active sessions immediately."""
    service = SecurityService(db)
    user = service.suspend_user(user_id, actor_id=security_ctx.principal.id)
    return DataResponse(data=user)


@router.post("/users/{user_id}/activate", response_model=DataResponse[UserProfileResponse])
def activate_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("user.manage")),
):
    """Reactivate suspended user account."""
    service = SecurityService(db)
    user = service.activate_user(user_id, actor_id=security_ctx.principal.id)
    return DataResponse(data=user)


# 2. Session Management
@router.get("/sessions", response_model=DataResponse[List[SessionResponse]])
def list_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List active sessions for current authenticated user."""
    service = SecurityService(db)
    sessions = service.list_sessions(current_user.id)
    return DataResponse(data=sessions)


@router.post("/sessions/revoke", response_model=DataResponse[dict])
def revoke_session(
    req: RevokeSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Revoke a specific session."""
    service = SecurityService(db)
    success = service.revoke_session(uuid.UUID(req.session_id), actor_id=str(current_user.id))
    return DataResponse(data={"revoked": success})


@router.post("/sessions/revoke-all", response_model=DataResponse[dict])
def revoke_all_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Global logout: Revoke all active sessions for current user."""
    service = SecurityService(db)
    count = service.revoke_all_sessions(current_user.id, actor_id=str(current_user.id))
    return DataResponse(data={"revoked_count": count})


# 3. Roles & Permissions Catalog
@router.get("/roles", response_model=DataResponse[List[RoleResponse]])
def get_roles(
    security_ctx: SecurityContext = Depends(get_security_context),
):
    """List all available system roles with mapped permissions."""
    roles = []
    for role_name, perms in ROLE_PERMISSIONS_MAP.items():
        roles.append(
            RoleResponse(
                name=role_name,
                description=f"Predefined {role_name} role",
                is_internal="CLIENT" not in role_name,
                permissions=sorted(list(perms)),
            )
        )
    return DataResponse(data=roles)


@router.get("/permissions", response_model=DataResponse[List[PermissionResponse]])
def get_permissions(
    security_ctx: SecurityContext = Depends(get_security_context),
):
    """List all registered system permissions."""
    perms = list_permissions()
    res = [
        PermissionResponse(
            name=p.name,
            resource=p.resource,
            action=p.action,
            description=p.description,
            risk_level=p.risk_level.value,
        )
        for p in perms
    ]
    return DataResponse(data=res)


# 4. MFA & Step-Up Authentication
@router.post("/mfa/setup", response_model=DataResponse[MFASetupResponse])
def setup_mfa(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Generate TOTP secret and backup recovery codes."""
    service = SecurityService(db)
    setup = service.setup_mfa(current_user.id)
    return DataResponse(data=setup)


@router.post("/step-up", response_model=DataResponse[StepUpAuthResponse])
def verify_step_up(
    req: StepUpAuthRequest,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(get_security_context),
):
    """Re-authenticate to receive short-lived step-up token for high-risk actions."""
    service = SecurityService(db)
    res = service.verify_step_up_auth(
        user_id=uuid.UUID(security_ctx.principal.id),
        password=req.password,
        tenant_id=security_ctx.tenant_id,
    )
    return DataResponse(data=res)


# 5. API Keys
@router.get("/api-keys", response_model=DataResponse[List[APIKeyResponse]])
def list_api_keys(
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("api_key.manage")),
):
    """List active and revoked API keys."""
    service = SecurityService(db)
    keys = service.list_api_keys()
    return DataResponse(data=keys)


@router.post("/api-keys", response_model=DataResponse[APIKeyCreatedResponse], status_code=status.HTTP_201_CREATED)
def create_api_key(
    req: APIKeyCreateRequest,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("api_key.manage")),
):
    """Generate a scoped API key."""
    service = SecurityService(db)
    created = service.create_api_key(uuid.UUID(security_ctx.principal.id), req)
    return DataResponse(data=created)


@router.delete("/api-keys/{key_id}", response_model=DataResponse[dict])
def revoke_api_key(
    key_id: uuid.UUID,
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("api_key.manage")),
):
    """Revoke an active API key."""
    service = SecurityService(db)
    success = service.revoke_api_key(key_id, actor_id=security_ctx.principal.id)
    return DataResponse(data={"revoked": success})


# 6. Security Metrics & Audit Logs
@router.get("/metrics", response_model=DataResponse[SecurityMetricsResponse])
def get_security_metrics(
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("security.audit_read")),
):
    """Get high-level security posture snapshot and metric counters."""
    service = SecurityService(db)
    metrics = service.get_security_metrics()
    return DataResponse(data=metrics)


@router.get("/events", response_model=DataResponse[List[SecurityEventResponse]])
def list_security_events(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    security_ctx: SecurityContext = Depends(require_permission("security.audit_read")),
):
    """Query immutable security audit log."""
    service = SecurityService(db)
    events = service.list_security_events(limit=limit)
    return DataResponse(data=events)
