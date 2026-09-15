"""Security Principals, Contexts, and Identity Definitions."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import uuid


class PrincipalType(str, Enum):
    """Types of security principals recognized by the platform."""

    USER = "USER"
    CLIENT = "CLIENT"
    AGENT = "AGENT"
    SERVICE = "SERVICE"
    WORKER = "WORKER"
    SYSTEM = "SYSTEM"
    INTEGRATION = "INTEGRATION"


class PrincipalStatus(str, Enum):
    """Operational lifecycle status of a principal."""

    INVITED = "INVITED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    LOCKED = "LOCKED"
    DISABLED = "DISABLED"
    DELETED = "DELETED"


@dataclass
class Principal:
    """Represents an entity requesting an operation."""

    id: str
    type: PrincipalType
    tenant_id: str
    organization_id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    status: PrincipalStatus = PrincipalStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.status == PrincipalStatus.ACTIVE

    @property
    def is_human(self) -> bool:
        return self.type in (PrincipalType.USER, PrincipalType.CLIENT)

    @property
    def is_client(self) -> bool:
        return self.type == PrincipalType.CLIENT

    @property
    def is_agent(self) -> bool:
        return self.type == PrincipalType.AGENT


@dataclass
class SecurityContext:
    """Ambient security context established during request authentication."""

    principal: Principal
    session_id: Optional[str] = None
    tenant_id: str = "default_tenant"
    roles: List[str] = field(default_factory=list)
    permissions: Set[str] = field(default_factory=set)
    is_authenticated: bool = True
    auth_method: str = "PASSWORD"  # PASSWORD, TOKEN, API_KEY, SERVICE_ACCOUNT, SYSTEM
    auth_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_mfa_authenticated: bool = False
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def has_role(self, role: str) -> bool:
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions


@dataclass
class AuthorizationContext:
    """Contextual metadata evaluated by RBAC and ABAC policy rules."""

    resource_type: str
    resource_id: Optional[str] = None
    action: str = ""
    resource_tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    organization_id: Optional[str] = None
    resource_owner_id: Optional[str] = None
    is_client_visible: bool = False
    risk_level: str = "LOW"  # INFO, LOW, MEDIUM, HIGH, CRITICAL
    workflow_id: Optional[str] = None
    environment: str = "production"
    attributes: Dict[str, Any] = field(default_factory=dict)
