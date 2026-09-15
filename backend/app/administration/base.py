"""Base models and enums for Phase 44 — Unified Platform Administration & Control Center."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ConfigType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    ENUM = "ENUM"
    JSON = "JSON"
    LIST = "LIST"
    DURATION = "DURATION"
    URL = "URL"
    CURRENCY = "CURRENCY"
    PERCENTAGE = "PERCENTAGE"
    SECRET_REFERENCE = "SECRET_REFERENCE"


class ConfigScope(str, Enum):
    GLOBAL = "GLOBAL"
    ORGANIZATION = "ORGANIZATION"
    BUSINESS_UNIT = "BUSINESS_UNIT"
    ENVIRONMENT = "ENVIRONMENT"
    SERVICE = "SERVICE"
    FEATURE = "FEATURE"


class ConfigStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    SCHEDULED = "SCHEDULED"
    ROLLED_BACK = "ROLLED_BACK"
    ARCHIVED = "ARCHIVED"


class PolicyDomain(str, Enum):
    AI = "AI"
    SECURITY = "SECURITY"
    COMMUNICATION = "COMMUNICATION"
    FINANCE = "FINANCE"
    DATA = "DATA"
    WORKFLOW = "WORKFLOW"
    CLIENT = "CLIENT"
    PROJECT = "PROJECT"
    SUPPORT = "SUPPORT"
    RELIABILITY = "RELIABILITY"
    ADMINISTRATION = "ADMINISTRATION"


class PolicyScope(str, Enum):
    GLOBAL = "GLOBAL"
    ORGANIZATION = "ORGANIZATION"
    BUSINESS_UNIT = "BUSINESS_UNIT"
    PROJECT = "PROJECT"
    RESOURCE = "RESOURCE"


class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


class PolicyEvaluationResult(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class FlagStatus(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    SHADOW = "SHADOW"
    CANARY = "CANARY"


class RolloutType(str, Enum):
    BOOLEAN = "BOOLEAN"
    PERCENTAGE = "PERCENTAGE"
    TENANT_TIER = "TENANT_TIER"
    USER_LIST = "USER_LIST"


class EnvironmentType(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    DR = "DR"


class MaintenanceMode(str, Enum):
    NORMAL = "NORMAL"
    MAINTENANCE = "MAINTENANCE"
    READ_ONLY = "READ_ONLY"
    DEGRADED = "DEGRADED"
    EMERGENCY = "EMERGENCY"


class KillSwitchLevel(str, Enum):
    GLOBAL = "GLOBAL"
    DOMAIN = "DOMAIN"
    SERVICE = "SERVICE"
    PROVIDER = "PROVIDER"
    AGENT = "AGENT"
    MODEL = "MODEL"
    TOOL = "TOOL"
    WORKFLOW = "WORKFLOW"


class KillSwitchState(str, Enum):
    DISARMED = "DISARMED"
    ACTIVE = "ACTIVE"


class ChangeStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


class ChangeRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DriftSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AdminHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    STABLE = "STABLE"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"


# Pydantic schema models

class ConfigItem(BaseModel):
    key: str
    display_name: str
    description: str
    config_type: ConfigType
    category: str
    scope: ConfigScope = ConfigScope.GLOBAL
    default_value: Any
    current_value: Any
    validation_rules: Dict[str, Any] = Field(default_factory=dict)
    sensitive: bool = False
    mutable: bool = True
    restart_required: bool = False
    policy_controlled: bool = False
    version: int = 1
    status: ConfigStatus = ConfigStatus.ACTIVE
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PolicyRule(BaseModel):
    rule_id: str
    name: str
    condition: str
    action: PolicyEvaluationResult
    reason: str
    is_mandatory_security: bool = False


class PolicyItem(BaseModel):
    policy_id: str
    name: str
    domain: PolicyDomain
    description: str
    scope: PolicyScope = PolicyScope.GLOBAL
    priority: int = 100
    version: int = 1
    status: PolicyStatus = PolicyStatus.ACTIVE
    rules: List[PolicyRule] = Field(default_factory=list)
    effective_from: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    effective_until: Optional[datetime] = None
    approval_required: bool = False
    created_by: str = "system"


class FeatureFlagItem(BaseModel):
    key: str
    name: str
    description: str
    status: FlagStatus = FlagStatus.DISABLED
    rollout_type: RolloutType = RolloutType.BOOLEAN
    rollout_percentage: int = 0
    allowed_tiers: List[str] = Field(default_factory=list)
    environment: EnvironmentType = EnvironmentType.PRODUCTION
    owner: str = "platform_admin"
    version: int = 1
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdminChangeRequest(BaseModel):
    change_id: str
    key: str
    old_value: Any
    new_value: Any
    reason: str
    requested_by: str
    reviewed_by: Optional[str] = None
    approved_by: Optional[str] = None
    risk_level: ChangeRiskLevel = ChangeRiskLevel.MEDIUM
    status: ChangeStatus = ChangeStatus.PENDING_APPROVAL
    effective_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class KillSwitchItem(BaseModel):
    switch_id: str
    name: str
    level: KillSwitchLevel
    target_identifier: str
    state: KillSwitchState = KillSwitchState.DISARMED
    reason: Optional[str] = None
    activated_by: Optional[str] = None
    activated_at: Optional[datetime] = None


class DriftItem(BaseModel):
    drift_id: str
    key: str
    expected_value: Any
    actual_value: Any
    severity: DriftSeverity
    environment: EnvironmentType
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False


class AdminHealthReport(BaseModel):
    status: AdminHealthStatus
    configuration_validity_score: float
    policy_consistency_score: float
    integration_health_score: float
    drift_count: int
    pending_approvals_count: int
    active_kill_switches_count: int
    active_maintenance_mode: MaintenanceMode
    details: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
