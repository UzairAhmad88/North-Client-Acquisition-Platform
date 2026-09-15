"""Central Authorization Engine enforcing RBAC, ABAC, Tenant Isolation, and High-Risk Safety Policies."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
import uuid

from app.security.audit import SecurityEventRecord, SecurityEventType, SecuritySeverity
from app.security.permissions import PERMISSION_REGISTRY, RiskLevel, SystemPermissions, get_permission
from app.security.principals import AuthorizationContext, Principal, PrincipalStatus, PrincipalType, SecurityContext
from app.security.roles import ROLE_PERMISSIONS_MAP, get_role_permissions


class ReasonCode:
    """Standardized decision reason codes."""

    ALLOWED = "ALLOWED"
    PRINCIPAL_INACTIVE = "PRINCIPAL_INACTIVE"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"
    TENANT_MISMATCH = "TENANT_MISMATCH"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    ROLE_DENIED = "ROLE_DENIED"
    PROJECT_MEMBERSHIP_REQUIRED = "PROJECT_MEMBERSHIP_REQUIRED"
    CLIENT_ACCESS_BOUNDARY_VIOLATION = "CLIENT_ACCESS_BOUNDARY_VIOLATION"
    MFA_REQUIRED = "MFA_REQUIRED"
    STEP_UP_REQUIRED = "STEP_UP_REQUIRED"
    AGENT_PROHIBITED_ACTION = "AGENT_PROHIBITED_ACTION"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    POLICY_BLOCKED = "POLICY_BLOCKED"


@dataclass
class AuthorizationDecision:
    """Structured result of an authorization evaluation."""

    allowed: bool
    principal_id: str
    tenant_id: str
    action: str
    resource: Optional[str] = None
    resource_id: Optional[str] = None
    reason_code: str = ReasonCode.ALLOWED
    message: str = "Access granted"
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    policy_version: int = 1
    required_gates: List[str] = field(default_factory=list)


# Prohibited actions for AI Agents at the platform level
AGENT_PROHIBITED_ACTIONS: Set[str] = {
    SystemPermissions.OUTREACH_SEND,
    SystemPermissions.PROPOSAL_SEND,
    SystemPermissions.CONTRACT_SIGN,
    SystemPermissions.PRICE_CHANGE,
    SystemPermissions.RELEASE_APPROVE,
    SystemPermissions.AI_MODEL_PROMOTE,
    SystemPermissions.AI_KILL_SWITCH,
    SystemPermissions.USER_MANAGE,
    SystemPermissions.ROLE_MANAGE,
    SystemPermissions.TENANT_MANAGE,
    SystemPermissions.API_KEY_MANAGE,
    SystemPermissions.PROJECT_DELETE,
    SystemPermissions.BUSINESS_DELETE,
    SystemPermissions.LEAD_DELETE,
}


class AuthorizationEngine:
    """Authoritative authorization engine for the platform."""

    POLICY_VERSION = 1

    @classmethod
    def evaluate(
        cls,
        security_ctx: SecurityContext,
        auth_ctx: AuthorizationContext,
    ) -> AuthorizationDecision:
        """Evaluate an operation against RBAC, ABAC, tenant boundary, and policy gates."""
        principal = security_ctx.principal
        action = auth_ctx.action or f"{auth_ctx.resource_type}.{auth_ctx.action}"

        # 1. Evaluate Principal Status
        if not principal.is_active:
            return AuthorizationDecision(
                allowed=False,
                principal_id=principal.id,
                tenant_id=security_ctx.tenant_id,
                action=action,
                resource=auth_ctx.resource_type,
                resource_id=auth_ctx.resource_id,
                reason_code=ReasonCode.ACCOUNT_SUSPENDED if principal.status == PrincipalStatus.SUSPENDED else ReasonCode.PRINCIPAL_INACTIVE,
                message=f"Principal '{principal.id}' is not active ({principal.status.value}).",
                policy_version=cls.POLICY_VERSION,
            )

        # 2. Evaluate Tenant Isolation
        if auth_ctx.resource_tenant_id and auth_ctx.resource_tenant_id != security_ctx.tenant_id:
            # Special check for internal superusers/system
            if not (security_ctx.has_role("OWNER") and security_ctx.tenant_id == "primary_tenant"):
                return AuthorizationDecision(
                    allowed=False,
                    principal_id=principal.id,
                    tenant_id=security_ctx.tenant_id,
                    action=action,
                    resource=auth_ctx.resource_type,
                    resource_id=auth_ctx.resource_id,
                    reason_code=ReasonCode.TENANT_MISMATCH,
                    message="Cross-tenant access attempt strictly denied.",
                    policy_version=cls.POLICY_VERSION,
                )

        # 3. Evaluate AI Agent Prohibitions
        if principal.type == PrincipalType.AGENT:
            if action in AGENT_PROHIBITED_ACTIONS:
                return AuthorizationDecision(
                    allowed=False,
                    principal_id=principal.id,
                    tenant_id=security_ctx.tenant_id,
                    action=action,
                    resource=auth_ctx.resource_type,
                    resource_id=auth_ctx.resource_id,
                    reason_code=ReasonCode.AGENT_PROHIBITED_ACTION,
                    message=f"Agent principal is strictly prohibited from executing '{action}'.",
                    policy_version=cls.POLICY_VERSION,
                )

        # 4. Evaluate Client Access Boundary
        if principal.type == PrincipalType.CLIENT:
            # Client users cannot access internal-only resources or actions
            if not auth_ctx.is_client_visible and auth_ctx.resource_type in {
                "ai_trace", "estimate_internal", "cost_model", "security", "role", "tenant"
            }:
                return AuthorizationDecision(
                    allowed=False,
                    principal_id=principal.id,
                    tenant_id=security_ctx.tenant_id,
                    action=action,
                    resource=auth_ctx.resource_type,
                    resource_id=auth_ctx.resource_id,
                    reason_code=ReasonCode.CLIENT_ACCESS_BOUNDARY_VIOLATION,
                    message="Client principals cannot access internal-only resources.",
                    policy_version=cls.POLICY_VERSION,
                )

        # 5. Evaluate RBAC Permission
        # Compute effective permissions: explicit permissions + permissions from roles
        effective_permissions = set(security_ctx.permissions)
        for role in security_ctx.roles:
            effective_permissions.update(get_role_permissions(role))

        # Check if action is granted (OWNER has wildcard bypass for internal operations)
        is_owner = security_ctx.has_role("OWNER")
        if not is_owner and action not in effective_permissions:
            return AuthorizationDecision(
                allowed=False,
                principal_id=principal.id,
                tenant_id=security_ctx.tenant_id,
                action=action,
                resource=auth_ctx.resource_type,
                resource_id=auth_ctx.resource_id,
                reason_code=ReasonCode.PERMISSION_DENIED,
                message=f"Principal lacks required permission '{action}'.",
                policy_version=cls.POLICY_VERSION,
            )

        # 6. Evaluate ABAC Rules: Project Membership
        if auth_ctx.project_id:
            user_projects = auth_ctx.attributes.get("assigned_project_ids", [])
            # If principal is DEVELOPER, QA, DESIGNER or CLIENT, they must be assigned to the project
            assigned_roles = {"DEVELOPER", "QA", "DESIGNER", "CLIENT_MEMBER", "CLIENT_REVIEWER", "CLIENT_VIEWER"}
            if any(r in assigned_roles for r in security_ctx.roles) and not is_owner and not security_ctx.has_role("ADMIN"):
                if auth_ctx.project_id not in user_projects:
                    return AuthorizationDecision(
                        allowed=False,
                        principal_id=principal.id,
                        tenant_id=security_ctx.tenant_id,
                        action=action,
                        resource=auth_ctx.resource_type,
                        resource_id=auth_ctx.resource_id,
                        reason_code=ReasonCode.PROJECT_MEMBERSHIP_REQUIRED,
                        message=f"Operation requires membership in project '{auth_ctx.project_id}'.",
                        policy_version=cls.POLICY_VERSION,
                    )

        # 7. Evaluate High-Risk Policy Gates
        perm_def = get_permission(action)
        required_gates = []
        if perm_def:
            if perm_def.requires_mfa and not security_ctx.is_mfa_authenticated:
                return AuthorizationDecision(
                    allowed=False,
                    principal_id=principal.id,
                    tenant_id=security_ctx.tenant_id,
                    action=action,
                    resource=auth_ctx.resource_type,
                    resource_id=auth_ctx.resource_id,
                    reason_code=ReasonCode.MFA_REQUIRED,
                    message=f"Action '{action}' requires multi-factor authentication (MFA).",
                    policy_version=cls.POLICY_VERSION,
                    required_gates=["MFA"],
                )

            if perm_def.requires_step_up and not auth_ctx.attributes.get("has_valid_step_up", False):
                required_gates.append("STEP_UP")

            if perm_def.requires_human_approval:
                required_gates.append("HUMAN_APPROVAL_GATE")

        # Decision: ALLOW
        return AuthorizationDecision(
            allowed=True,
            principal_id=principal.id,
            tenant_id=security_ctx.tenant_id,
            action=action,
            resource=auth_ctx.resource_type,
            resource_id=auth_ctx.resource_id,
            reason_code=ReasonCode.ALLOWED,
            message="Operation authorized.",
            policy_version=cls.POLICY_VERSION,
            required_gates=required_gates,
        )
