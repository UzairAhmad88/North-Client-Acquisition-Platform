"""
Pydantic Schemas for Phase 51:
Autonomous Business Strategy, Planning & Goal Optimization Engine.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ObjectiveCreateRequest(BaseModel):
    name: str
    target_value: float
    unit: str = "USD"
    baseline_value: float = 0.0
    strategic_pillar: str = "GROWTH"
    owner: str = "executive_team"
    priority: str = "HIGH"
    description: Optional[str] = None


class ObjectiveProgressUpdateRequest(BaseModel):
    current_value: float
    evidence_summary: Optional[str] = None


class ObjectiveResponse(BaseModel):
    id: Optional[str] = None
    objective_code: str
    name: str
    description: Optional[str] = None
    strategic_pillar: str
    owner: str
    priority: str
    start_date: datetime
    target_date: datetime
    baseline_value: float
    target_value: float
    current_value: float
    unit: str
    status: str
    confidence_score: float
    progress_percentage: float
    evidence_summary: Optional[str] = None
    version: int


class KeyResultCreateRequest(BaseModel):
    objective_id: str
    name: str
    target_value: float
    unit: str = "PERCENT"
    baseline_value: float = 0.0
    owner: str = "team_lead"


class KeyResultResponse(BaseModel):
    id: Optional[str] = None
    kr_code: str
    objective_id: str
    name: str
    baseline_value: float
    target_value: float
    current_value: float
    unit: str
    progress_percentage: float
    measurement_method: str
    source_metric: Optional[str] = None
    owner: str
    confidence: float
    deadline: datetime


class InitiativeCreateRequest(BaseModel):
    title: str
    owner: str
    category: str = "GROWTH"
    expected_value_usd: float = 50000.0
    estimated_cost_usd: float = 15000.0
    required_fte_capacity: float = 1.5
    estimated_duration_weeks: float = 6.0
    description: Optional[str] = None


class InitiativeResponse(BaseModel):
    id: Optional[str] = None
    initiative_code: str
    title: str
    description: Optional[str] = None
    category: str
    owner: str
    status: str
    expected_value_usd: float
    estimated_cost_usd: float
    required_fte_capacity: float
    estimated_duration_weeks: float
    priority_score: float
    risk_score: float
    feasibility_score: float
    is_funded: bool
    version: int


class OptimizationRunRequest(BaseModel):
    budget_limit_usd: float = 100000.0
    capacity_limit_fte: float = 8.0
    max_acceptable_risk: float = 0.50
    initiatives: Optional[List[InitiativeCreateRequest]] = None


class OptimizationResponse(BaseModel):
    run_code: str
    status: str
    runtime_seconds: float
    budget_limit_usd: float
    allocated_budget_usd: float
    budget_utilization_percentage: float
    capacity_limit_fte: float
    allocated_capacity_fte: float
    capacity_utilization_percentage: float
    total_expected_value_usd: float
    net_expected_benefit_usd: float
    selected_initiatives: List[Dict[str, Any]]
    binding_constraints: List[str]
    explanation: str


class ParetoPlanResponse(BaseModel):
    plan_code: str
    title: str
    growth_score: float
    profitability_score: float
    risk_score: float
    selected_initiatives: List[str]
    total_cost_usd: float
    expected_net_benefit_usd: float
    is_pareto_optimal: bool


class FeasibilityResponse(BaseModel):
    objective_code: str
    objective_name: str
    feasibility_level: str
    feasibility_score: float
    required_growth_percentage: float
    historical_growth_rate_pct: float
    capacity_factor: float
    confidence: float
    rationale: str


class GapAnalysisResponse(BaseModel):
    objective_code: str
    objective_name: str
    strategic_pillar: str
    current_value: float
    target_value: float
    gap_value: float
    gap_percentage: float
    estimated_budget_needed_usd: float
    estimated_fte_needed: float
    urgency: str


class CriticalPathResponse(BaseModel):
    total_timeline_weeks: float
    critical_path_length: int
    critical_path_initiatives: List[Dict[str, Any]]
    summary: str


class ScorecardResponse(BaseModel):
    scorecard_code: str
    period: str
    composite_health_score: float
    composite_health_percentage: float
    dimensions: Dict[str, float]
    evaluation_time: str


class DriftCheckRequest(BaseModel):
    metric_name: str = "monthly_recurring_revenue_usd"
    expected_value: float
    actual_value: float
    drift_tolerance_pct: float = 10.0


class DriftCheckResponse(BaseModel):
    has_drift: bool
    drift_event: Optional[Dict[str, Any]] = None


class DecisionRecordCreateRequest(BaseModel):
    question: str
    context_summary: str
    selected_option: Dict[str, Any]
    rationale: str
    decision_owner: str
    rejected_options: List[Dict[str, Any]] = Field(default_factory=list)


class DecisionRecordResponse(BaseModel):
    id: Optional[str] = None
    decision_code: str
    question: str
    context_summary: str
    selected_option: Dict[str, Any]
    rejected_options: List[Dict[str, Any]]
    rationale: str
    decision_owner: str
    approved_at: datetime
    plan_version: int


class StrategyCopilotQueryRequest(BaseModel):
    query: str
    tenant_id: str = "default_tenant"


class StrategyCopilotQueryResponse(BaseModel):
    query: str
    intent: str
    explanation: str
    recommendations: List[str]
    confidence: float
    governance_notice: str = "AI produces strategic recommendations. All decisions and resource commitments require authorized human executive approval."
