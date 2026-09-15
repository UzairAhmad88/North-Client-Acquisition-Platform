"""Unified Identity, RBAC, Permissions, and Access Control Module."""

from app.security.audit import SecurityEventRecord, SecurityEventType, SecuritySeverity
from app.security.engine import AuthorizationDecision, AuthorizationEngine, ReasonCode
from app.security.mfa import MFAService
from app.security.password import hash_password, validate_password_policy, verify_password
from app.security.permissions import (
    PERMISSION_REGISTRY,
    PermissionDefinition,
    RiskLevel,
    SystemPermissions,
    get_permission,
    list_permissions,
)
from app.security.principals import (
    AuthorizationContext,
    Principal,
    PrincipalStatus,
    PrincipalType,
    SecurityContext,
)
from app.security.roles import ROLE_PERMISSIONS_MAP, RoleDefinition, SystemRole, get_role_permissions
from app.security.sessions import SessionInfo, SessionManager

__all__ = [
    "Principal",
    "PrincipalType",
    "PrincipalStatus",
    "SecurityContext",
    "AuthorizationContext",
    "RiskLevel",
    "PermissionDefinition",
    "SystemPermissions",
    "PERMISSION_REGISTRY",
    "get_permission",
    "list_permissions",
    "SystemRole",
    "RoleDefinition",
    "ROLE_PERMISSIONS_MAP",
    "get_role_permissions",
    "hash_password",
    "verify_password",
    "validate_password_policy",
    "SessionInfo",
    "SessionManager",
    "MFAService",
    "SecurityEventType",
    "SecuritySeverity",
    "SecurityEventRecord",
    "ReasonCode",
    "AuthorizationDecision",
    "AuthorizationEngine",
    "SecurityOperationsService",
]

try:
    from app.security.service import SecurityOperationsService
except ImportError:
    from backend.app.security.service import SecurityOperationsService
