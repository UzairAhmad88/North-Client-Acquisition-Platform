"""Security Audit Logging & Immutable Security Event Records."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class SecurityEventType(str, Enum):
    """Classifies security events across authentication, authorization, and tenant isolation."""

    # Authentication
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    LOGOUT = "LOGOUT"
    PASSWORD_CHANGED = "PASSWORD_CHANGED"
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED"
    PASSWORD_RESET_COMPLETED = "PASSWORD_RESET_COMPLETED"
    EMAIL_VERIFIED = "EMAIL_VERIFIED"
    MFA_ENABLED = "MFA_ENABLED"
    MFA_DISABLED = "MFA_DISABLED"
    MFA_CHALLENGE_FAILED = "MFA_CHALLENGE_FAILED"
    SESSION_CREATED = "SESSION_CREATED"
    SESSION_REVOKED = "SESSION_REVOKED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"

    # Authorization & Access Control
    AUTHORIZATION_GRANTED = "AUTHORIZATION_GRANTED"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    PRIVILEGE_ESCALATION_ATTEMPT = "PRIVILEGE_ESCALATION_ATTEMPT"
    CROSS_TENANT_ACCESS_ATTEMPT = "CROSS_TENANT_ACCESS_ATTEMPT"
    AGENT_PERMISSION_DENIED = "AGENT_PERMISSION_DENIED"
    WORKFLOW_PERMISSION_DENIED = "WORKFLOW_PERMISSION_DENIED"
    SENSITIVE_ACTION_BLOCKED = "SENSITIVE_ACTION_BLOCKED"
    BREAK_GLASS_ACCESSED = "BREAK_GLASS_ACCESSED"
    API_KEY_CREATED = "API_KEY_CREATED"
    API_KEY_REVOKED = "API_KEY_REVOKED"


class SecuritySeverity(str, Enum):
    """Severity ratings for security events."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SecurityEventRecord:
    """Immutable audit record for a security event."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: SecurityEventType = SecurityEventType.AUTHORIZATION_GRANTED
    severity: SecuritySeverity = SecuritySeverity.INFO
    principal_id: str = "anonymous"
    principal_type: str = "USER"
    tenant_id: str = "default_tenant"
    action: Optional[str] = None
    resource: Optional[str] = None
    resource_id: Optional[str] = None
    result: str = "ALLOW"  # ALLOW, DENY, BLOCK, ERROR
    reason_code: str = "SUCCESS"
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[str] = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
