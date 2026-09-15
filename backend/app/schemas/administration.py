"""Pydantic request and response schemas for Phase 44 Administration API."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.administration.base import (
    AdminHealthReport,
    AdminHealthStatus,
    ApprovalStatus,
    ChangeRiskLevel,
    ChangeStatus,
    ConfigItem,
    ConfigScope,
    ConfigStatus,
    ConfigType,
    DriftItem,
    DriftSeverity,
    EnvironmentType,
    FeatureFlagItem,
    FlagStatus,
    KillSwitchItem,
    KillSwitchLevel,
    KillSwitchState,
    MaintenanceMode,
    PolicyDomain,
    PolicyEvaluationResult,
    PolicyItem,
    PolicyRule,
    PolicyScope,
    PolicyStatus,
    RolloutType,
)
from app.administration.environments import EnvironmentDefinition, EnvironmentPromotionRequest
from app.administration.integrations import ProviderConfiguration
from app.administration.maintenance import MaintenanceWindow


class ConfigCreateRequest(BaseModel):
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


class ConfigChangeProposalRequest(BaseModel):
    key: str
    new_value: Any
    reason: str
    risk_level: ChangeRiskLevel = ChangeRiskLevel.MEDIUM


class ConfigRollbackRequest(BaseModel):
    key: str
    target_version: int
    reason: str


class PolicyCreateRequest(BaseModel):
    policy_id: str
    name: str
    domain: PolicyDomain
    description: str
    scope: PolicyScope = PolicyScope.GLOBAL
    priority: int = 100
    rules: List[PolicyRule] = Field(default_factory=list)


class PolicyEvaluateRequest(BaseModel):
    domain: PolicyDomain
    action: str
    actor_type: str = "user"
    context: Dict[str, Any] = Field(default_factory=dict)
    amount: Optional[float] = None


class FeatureFlagCreateRequest(BaseModel):
    key: str
    name: str
    description: str
    status: FlagStatus = FlagStatus.DISABLED
    rollout_type: RolloutType = RolloutType.BOOLEAN
    rollout_percentage: int = 0
    allowed_tiers: List[str] = Field(default_factory=list)
    environment: EnvironmentType = EnvironmentType.PRODUCTION


class FeatureFlagStatusUpdateRequest(BaseModel):
    status: FlagStatus


class FeatureFlagRolloutUpdateRequest(BaseModel):
    rollout_type: RolloutType
    rollout_percentage: int = 0
    allowed_tiers: List[str] = Field(default_factory=list)


class KillSwitchActionRequest(BaseModel):
    reason: str


class MaintenanceStartRequest(BaseModel):
    mode: MaintenanceMode
    title: str
    description: str
    internal_banner: str
    client_banner: str = ""
    affected_services: List[str] = Field(default_factory=list)


class EnvironmentPromotionCreateRequest(BaseModel):
    source_env: EnvironmentType
    target_env: EnvironmentType
    keys: List[str]


class AdminOverviewResponse(BaseModel):
    health: Dict[str, Any]
    configs_count: int
    policies_count: int
    feature_flags_count: int
    providers_count: int
    environments_count: int
    kill_switches_count: int
    maintenance_mode: str
