"""
Canonical base types, enums, and domain schemas for Phase 50: Unified Digital Twin & Simulation.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class EntityDomain(str, Enum):
    ORGANIZATION = "ORGANIZATION"
    COMMERCIAL = "COMMERCIAL"
    DELIVERY = "DELIVERY"
    OPERATIONS = "OPERATIONS"
    FINANCE = "FINANCE"
    AI_OPERATIONS = "AI_OPERATIONS"
    RELIABILITY = "RELIABILITY"
    SECURITY = "SECURITY"
    GOVERNANCE = "GOVERNANCE"
    PROCESS = "PROCESS"
    RISK = "RISK"


class ScenarioType(str, Enum):
    GROWTH = "GROWTH"
    PRICING = "PRICING"
    RESOURCE = "RESOURCE"
    PROJECT = "PROJECT"
    CLIENT = "CLIENT"
    PROCESS = "PROCESS"
    FINANCE = "FINANCE"
    AI_SCALING = "AI_SCALING"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    RISK_DISRUPTION = "RISK_DISRUPTION"


class ScenarioStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIGURED = "CONFIGURED"
    VALIDATED = "VALIDATED"
    READY_FOR_SIMULATION = "READY_FOR_SIMULATION"
    SIMULATING = "SIMULATING"
    COMPLETED = "COMPLETED"
    ANALYZED = "ANALYZED"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    DECISION = "DECISION"
    CANCELLED = "CANCELLED"


class SimulationMethod(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    MONTE_CARLO = "MONTE_CARLO"
    DISCRETE_EVENT = "DISCRETE_EVENT"
    AGENT_BASED = "AGENT_BASED"
    SYSTEM_DYNAMICS = "SYSTEM_DYNAMICS"


class TimeHorizon(str, Enum):
    MONTH_1 = "1_MONTH"
    MONTH_3 = "3_MONTHS"
    MONTH_6 = "6_MONTHS"
    MONTH_12 = "12_MONTHS"
    MONTH_24 = "24_MONTHS"
    CUSTOM = "CUSTOM"


class SensitivityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"


class DecisionStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"


# Pydantic Schemas

class TwinEntity(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    entity_code: str
    entity_type: str
    source_domain: EntityDomain = EntityDomain.COMMERCIAL
    source_entity_id: str
    name: str
    state_payload: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class TwinRelationship(BaseModel):
    id: Optional[str] = None
    twin_model_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    weight: float = 1.0
    properties: Dict[str, Any] = Field(default_factory=dict)


class TwinState(BaseModel):
    snapshot_code: str = Field(default_factory=lambda: f"SNAP-{uuid.uuid4().hex[:8].upper()}")
    tenant_id: str = "default_tenant"
    title: str = "Enterprise State Snapshot"
    snapshot_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    commercial_state: Dict[str, Any] = Field(default_factory=dict)
    delivery_state: Dict[str, Any] = Field(default_factory=dict)
    operational_state: Dict[str, Any] = Field(default_factory=dict)
    financial_state: Dict[str, Any] = Field(default_factory=dict)
    ai_state: Dict[str, Any] = Field(default_factory=dict)
    reliability_state: Dict[str, Any] = Field(default_factory=dict)
    risk_state: Dict[str, Any] = Field(default_factory=dict)
    composite_health_score: float = 1.0
    state_hash: str = ""


class Assumption(BaseModel):
    id: Optional[str] = None
    assumption_code: str = Field(default_factory=lambda: f"ASM-{uuid.uuid4().hex[:6].upper()}")
    name: str
    description: str
    parameter_code: str
    baseline_value: float
    assumed_value: float
    delta_percentage: float
    source_basis: str = "HISTORICAL_ANALYTICS"
    confidence_score: float = 0.8


class Parameter(BaseModel):
    id: Optional[str] = None
    parameter_code: str
    name: str
    category: str = "COMMERCIAL"
    current_value: float
    unit: str = "RATIO"
    min_bound: Optional[float] = None
    max_bound: Optional[float] = None
    confidence: float = 1.0
    version: int = 1


class Scenario(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    twin_model_id: str
    scenario_code: str = Field(default_factory=lambda: f"SCEN-{uuid.uuid4().hex[:6].upper()}")
    name: str
    description: Optional[str] = None
    scenario_type: ScenarioType = ScenarioType.GROWTH
    time_horizon: TimeHorizon = TimeHorizon.MONTH_12
    simulation_method: SimulationMethod = SimulationMethod.MONTE_CARLO
    baseline_snapshot_id: Optional[str] = None
    parameter_overrides: Dict[str, float] = Field(default_factory=dict)
    assumptions: List[Assumption] = Field(default_factory=list)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)
    status: ScenarioStatus = ScenarioStatus.CONFIGURED
    created_by: str = "system"
    version: int = 1


class SimulationResult(BaseModel):
    simulation_code: str
    scenario_id: str
    method: SimulationMethod
    iterations: int
    runtime_seconds: float
    metrics_summary: Dict[str, Any] = Field(default_factory=dict)
    uncertainty_distribution: Dict[str, Any] = Field(default_factory=dict)  # Expected, P10, P25, P50, P75, P90, Min, Max
    constraint_violations: List[str] = Field(default_factory=list)
    is_sandboxed: bool = True
    assumptions_applied: List[Dict[str, Any]] = Field(default_factory=list)


class SensitivityRanking(BaseModel):
    parameter_code: str
    parameter_name: str
    target_metric: str = "REVENUE"
    sensitivity_score: float
    impact_level: SensitivityLevel = SensitivityLevel.HIGH
    low_impact_value: float
    high_impact_value: float


class CounterfactualResult(BaseModel):
    counterfactual_code: str
    historical_event_id: str
    hypothetical_condition: str
    historical_actual: Dict[str, Any]
    simulated_alternative: Dict[str, Any]
    divergence_summary: str
    limitations: str = "Historical dependencies assumed invariant."


class DecisionOption(BaseModel):
    id: Optional[str] = None
    option_code: str = Field(default_factory=lambda: f"OPT-{uuid.uuid4().hex[:6].upper()}")
    title: str
    scenario_id: str
    expected_benefit_usd: float
    expected_cost_usd: float
    risk_score: float
    confidence_score: float
    tradeoff_summary: str


class DecisionRecord(BaseModel):
    id: Optional[str] = None
    decision_code: str = Field(default_factory=lambda: f"DEC-{uuid.uuid4().hex[:6].upper()}")
    question: str
    selected_option_id: Optional[str] = None
    rationale: str
    decision_owner: str
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scenario_version: int = 1
    status: DecisionStatus = DecisionStatus.APPROVED


class OutcomeRecord(BaseModel):
    id: Optional[str] = None
    decision_id: Optional[str] = None
    scenario_id: Optional[str] = None
    observed_period: str
    predicted_metrics: Dict[str, Any]
    actual_metrics: Dict[str, Any]
    variance_percentage: float
    model_error: float


class CalibrationReport(BaseModel):
    calibrations_count: int
    parameter_updates: List[Dict[str, Any]] = Field(default_factory=list)
    average_prediction_error: float
    summary: str
