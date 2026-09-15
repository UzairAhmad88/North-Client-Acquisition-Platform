from typing import Callable, Generator, List, Optional, Set

import jwt
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.security import SecurityRepository
from app.security.engine import AuthorizationDecision, AuthorizationEngine
from app.security.principals import AuthorizationContext, Principal, PrincipalStatus, PrincipalType, SecurityContext
from app.security.roles import get_role_permissions
from app.services.auth import AuthService

security_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> User:
    if not credentials or not credentials.credentials:
        raise UnauthorizedError("Authentication required")

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Authentication token has expired")
    except jwt.PyJWTError:
        raise UnauthorizedError("Invalid authentication token")

    return AuthService.get_user_from_token(db, payload)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UnauthorizedError("Account is inactive")
    return current_user


def get_security_context(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
) -> SecurityContext:
    """Build ambient security context from authenticated user session."""
    repo = SecurityRepository(db)
    roles = repo.get_user_roles(current_user.id)
    if not roles:
        roles = [current_user.role]

    permissions: Set[str] = set()
    for role in roles:
        permissions.update(get_role_permissions(role))

    principal_type = PrincipalType.CLIENT if any("CLIENT" in r for r in roles) else PrincipalType.USER
    default_tenant = repo.get_or_create_default_tenant()
    resolved_tenant_id = x_tenant_id or str(default_tenant.id)

    principal = Principal(
        id=str(current_user.id),
        type=principal_type,
        tenant_id=resolved_tenant_id,
        email=current_user.email,
        display_name=current_user.full_name,
        status=PrincipalStatus.ACTIVE if current_user.is_active else PrincipalStatus.SUSPENDED,
    )

    return SecurityContext(
        principal=principal,
        tenant_id=resolved_tenant_id,
        roles=roles,
        permissions=permissions,
        is_authenticated=True,
        auth_method="TOKEN",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        correlation_id=get_request_id(request),
    )


def require_permission(permission: str) -> Callable:
    """FastAPI dependency enforcing a granular permission check."""
    def _dependency(
        security_ctx: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        auth_ctx = AuthorizationContext(
            resource_type=permission.split(".")[0] if "." in permission else "system",
            action=permission,
            resource_tenant_id=security_ctx.tenant_id,
        )
        decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
        if not decision.allowed:
            raise ForbiddenError(decision.message)
        return security_ctx

    return _dependency


def require_role(role: str) -> Callable:
    """FastAPI dependency enforcing a specific role requirement."""
    def _dependency(
        security_ctx: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        if not security_ctx.has_role(role) and not security_ctx.has_role("OWNER"):
            raise ForbiddenError(f"Operation requires '{role}' role.")
        return security_ctx

    return _dependency
