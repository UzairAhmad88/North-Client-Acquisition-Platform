"""
Pydantic Schemas for Phase 50:
Unified Digital Twin, Business Simulation, Scenario Intelligence & Strategic What-If Engine.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StateSnapshotCreateRequest(BaseModel):
    title: str = "Enterprise Point-in-Time Snapshot"
    source_snapshot_id: Optional[str] = None


class StateSnapshotResponse(BaseModel):
    id: Optional[str] = None
    snapshot_code: str
    tenant_id: str
    title: str
    snapshot_timestamp: datetime
    commercial_state: Dict[str, Any] = Field(default_factory=dict)
    delivery_state: Dict[str, Any] = Field(default_factory=dict)
    operational_state: Dict[str, Any] = Field(default_factory=dict)
    financial_state: Dict[str, Any] = Field(default_factory=dict)
    ai_state: Dict[str, Any] = Field(default_factory=dict)
    reliability_state: Dict[str, Any] = Field(default_factory=dict)
    risk_state: Dict[str, Any] = Field(default_factory=dict)
    composite_health_score: float
    state_hash: str
    is_valid: bool = True


class ScenarioCreateRequest(BaseModel):
    name: str
    twin_model_id: str = "primary_twin_model"
    scenario_type: str = "GROWTH"
    time_horizon: str = "12_MONTHS"
    simulation_method: str = "MONTE_CARLO"
    parameter_overrides: Dict[str, float] = Field(default_factory=dict)
    custom_assumptions: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)


class ScenarioResponse(BaseModel):
    id: Optional[str] = None
    scenario_code: str
    tenant_id: str
    twin_model_id: str
    name: str
    description: Optional[str] = None
    scenario_type: str
    time_horizon: str
    simulation_method: str
    parameter_overrides: Dict[str, float] = Field(default_factory=dict)
    assumptions: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)
    status: str
    created_by: str
    version: int


class SimulationRunRequest(BaseModel):
    scenario_name: Optional[str] = None
    parameter_overrides: Dict[str, float] = Field(default_factory=dict)
    simulation_method: str = "MONTE_CARLO"
    time_horizon: str = "12_MONTHS"
    iterations: int = 1000
    random_seed: Optional[int] = 42


class SimulationResponse(BaseModel):
    simulation_code: str
    scenario_id: str
    method: str
    iterations: int
    runtime_seconds: float
    metrics_summary: Dict[str, Any] = Field(default_factory=dict)
    uncertainty_distribution: Dict[str, Any] = Field(default_factory=dict)
    constraint_violations: List[str] = Field(default_factory=list)
    is_sandboxed: bool = True
    assumptions_applied: List[Dict[str, Any]] = Field(default_factory=list)


class ScenarioCompareRequest(BaseModel):
    baseline_scenario_name: str = "Current Baseline"
    baseline_overrides: Dict[str, float] = Field(default_factory=dict)
    scenarios: List[Dict[str, Any]] = Field(default_factory=list)
    iterations: int = 1000


class ScenarioCompareResponse(BaseModel):
    baseline: Dict[str, Any]
    alternatives: List[Dict[str, Any]]


class SensitivityRequest(BaseModel):
    target_metric: str = "cumulative_revenue_usd"
    parameter_overrides: Dict[str, float] = Field(default_factory=dict)
    sweep_percentage: float = 0.25


class SensitivityRankingResponse(BaseModel):
    parameter_code: str
    parameter_name: str
    target_metric: str
    sensitivity_score: float
    impact_level: str
    low_impact_value: float
    high_impact_value: float


class CounterfactualRequest(BaseModel):
    historical_event_id: str
    hypothetical_condition: str
    historical_actual_metrics: Dict[str, Any]
    hypothetical_parameter_overrides: Dict[str, float]


class CounterfactualResponse(BaseModel):
    counterfactual_code: str
    historical_event_id: str
    hypothetical_condition: str
    historical_actual: Dict[str, Any]
    simulated_alternative: Dict[str, Any]
    divergence_summary: str
    limitations: str


class DecisionOptionResponse(BaseModel):
    id: Optional[str] = None
    option_code: str
    title: str
    scenario_id: str
    expected_benefit_usd: float
    expected_cost_usd: float
    risk_score: float
    confidence_score: float
    tradeoff_summary: str


class DecisionRecordCreateRequest(BaseModel):
    question: str
    rationale: str
    decision_owner: str
    selected_option_id: Optional[str] = None


class DecisionRecordResponse(BaseModel):
    id: Optional[str] = None
    decision_code: str
    question: str
    selected_option_id: Optional[str] = None
    rationale: str
    decision_owner: str
    approved_at: datetime
    scenario_version: int
    status: str


class OutcomeRecordCreateRequest(BaseModel):
    observed_period: str
    predicted_metrics: Dict[str, Any]
    actual_metrics: Dict[str, Any]
    decision_id: Optional[str] = None
    scenario_id: Optional[str] = None


class OutcomeRecordResponse(BaseModel):
    id: Optional[str] = None
    decision_id: Optional[str] = None
    scenario_id: Optional[str] = None
    observed_period: str
    predicted_metrics: Dict[str, Any]
    actual_metrics: Dict[str, Any]
    variance_percentage: float
    model_error: float


class CalibrationReportResponse(BaseModel):
    calibrations_count: int
    parameter_updates: List[Dict[str, Any]] = Field(default_factory=list)
    average_prediction_error: float
    summary: str


class CopilotQueryRequest(BaseModel):
    query: str
    tenant_id: str = "default_tenant"


class CopilotQueryResponse(BaseModel):
    query: str
    intent: str
    scenario_generated: Optional[Dict[str, Any]] = None
    simulation_result: Optional[Dict[str, Any]] = None
    explanation: str
    confidence: float
    governance_notice: str = "Simulations are estimates. Strategic decisions require human executive signoff."
