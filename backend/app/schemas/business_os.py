"""Pydantic V2 Schemas for Business OS, Strategy, KPIs, Decisions, and Executive Intelligence."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.business_os.base import (
    AlertSeverity,
    AlertStatus,
    BriefingFrequency,
    BusinessHealthStatus,
    DecisionPriority,
    DecisionStatus,
    InitiativeStatus,
    KPICategory,
    KeyResultStatus,
    ObjectivePriority,
    ObjectiveStatus,
    RiskCategory,
    RiskImpact,
    RiskLifecycleStatus,
    RiskProbability,
    RiskSeverity,
    ScenarioType,
    ScorecardStatus,
    StrategicDependencyState,
)


# --- Strategy & OKR Schemas ---

class KeyResultCreate(BaseModel):
    title: str
    target_value: Decimal
    current_value: Decimal = Decimal("0.00")
    unit: str = "%"
    owner: Optional[str] = None


class KeyResultResponse(BaseModel):
    kr_id: str
    objective_id: str
    title: str
    target_value: Decimal
    current_value: Decimal
    unit: str
    status: KeyResultStatus
    progress_pct: Decimal
    owner: Optional[str] = None


class InitiativeCreate(BaseModel):
    title: str
    owner: str
    budget: Decimal = Decimal("0.00")
    priority: ObjectivePriority = ObjectivePriority.P1_HIGH


class InitiativeResponse(BaseModel):
    initiative_id: str
    objective_id: str
    title: str
    owner: str
    budget: Decimal
    priority: ObjectivePriority
    status: InitiativeStatus
    progress_pct: Decimal
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    dependencies: List[Dict[str, Any]] = Field(default_factory=list)


class StrategicObjectiveCreate(BaseModel):
    title: str
    description: Optional[str] = None
    timeframe: str = "FY2026"
    priority: ObjectivePriority = ObjectivePriority.P1_HIGH
    owner: str = "Executive Team"


class StrategicObjectiveResponse(BaseModel):
    objective_id: str
    title: str
    description: Optional[str] = None
    timeframe: str
    priority: ObjectivePriority
    status: ObjectiveStatus
    owner: str
    overall_progress_pct: Decimal
    key_results: List[KeyResultResponse] = Field(default_factory=list)
    initiatives: List[InitiativeResponse] = Field(default_factory=list)


# --- KPI & Scorecard Schemas ---

class KPIDefinitionCreate(BaseModel):
    kpi_id: str
    name: str
    category: KPICategory
    description: str
    unit: str = ""
    currency: str = "PKR"
    source_domain: str
    formula: str
    target_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    freshness_max_seconds: int = 3600
    is_higher_better: bool = True


class KPISnapshotResponse(BaseModel):
    kpi_id: str
    name: str
    category: KPICategory
    value: Decimal
    previous_value: Optional[Decimal] = None
    target_value: Optional[Decimal] = None
    variance: Optional[Decimal] = None
    variance_pct: Optional[Decimal] = None
    unit: str
    currency: str
    source_domain: str
    version: str
    freshness_seconds: int
    is_stale: bool
    status: ScorecardStatus
    calculated_at: datetime


class ScorecardItemResponse(BaseModel):
    kpi_id: str
    name: str
    category: KPICategory
    target: Decimal
    actual: Decimal
    variance: Decimal
    variance_pct: Optional[Decimal]
    unit: str
    currency: str
    trend: str
    status: ScorecardStatus
    owner: str


class DepartmentScorecardResponse(BaseModel):
    department_name: str
    category: KPICategory
    overall_status: ScorecardStatus
    scorecard_items: List[ScorecardItemResponse]
    generated_at: datetime


class CrossDomainReconciliationRequest(BaseModel):
    finance_revenue: Decimal
    crm_closed_won_revenue: Decimal
    active_contracts_count: int
    active_billing_profiles_count: int


# --- Business Health Schemas ---

class HealthDimensionScoreResponse(BaseModel):
    dimension_name: str
    score: Decimal
    weight_pct: Decimal
    status: BusinessHealthStatus
    positive_drivers: List[str]
    negative_drivers: List[str]
    signals_count: int


class BusinessHealthReportResponse(BaseModel):
    overall_health_score: Decimal
    overall_status: BusinessHealthStatus
    dimensions: Dict[str, HealthDimensionScoreResponse]
    key_strengths: List[str]
    critical_risks: List[str]
    reconciliation_alerts: List[str]
    evaluated_at: datetime


# --- Risk Register Schemas ---

class RiskCreate(BaseModel):
    title: str
    description: str
    category: RiskCategory
    probability: RiskProbability = RiskProbability.POSSIBLE
    impact: RiskImpact = RiskImpact.MODERATE
    owner: str
    evidence_signals: List[str] = Field(default_factory=list)
    mitigation_strategy: str = ""
    contingency_plan: str = ""
    due_date: Optional[str] = None


class RiskResponse(BaseModel):
    risk_id: str
    title: str
    description: str
    category: RiskCategory
    probability: RiskProbability
    impact: RiskImpact
    risk_score: int
    severity: RiskSeverity
    owner: str
    status: RiskLifecycleStatus
    identified_at: datetime
    due_date: Optional[str] = None
    evidence_signals: List[str]
    mitigation_strategy: str
    contingency_plan: str
    last_reviewed_at: datetime


# --- Decision Queue Schemas ---

class DecisionCreate(BaseModel):
    title: str
    business_question: str
    context_summary: str
    priority: DecisionPriority = DecisionPriority.P1_HIGH
    evidence_signals: List[str] = Field(default_factory=list)
    expected_outcome: str = ""
    review_due_date: Optional[str] = None


class DecisionRecordAction(BaseModel):
    chosen_option_id: str
    decision_rationale: str
    decided_by: str


class DecisionOutcomeRecordAction(BaseModel):
    actual_outcome: str
    outcome_variance_analysis: str
    lessons_learned: List[str]


class DecisionResponse(BaseModel):
    decision_id: str
    title: str
    business_question: str
    context_summary: str
    priority: DecisionPriority
    status: DecisionStatus
    candidate_options: List[Dict[str, Any]]
    ai_recommendation: Optional[str] = None
    ai_recommendation_rationale: Optional[str] = None
    chosen_option_id: Optional[str] = None
    chosen_option_title: Optional[str] = None
    decision_rationale: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None
    evidence_signals: List[str]
    expected_outcome: str
    actual_outcome: Optional[str] = None
    outcome_variance_analysis: Optional[str] = None
    lessons_learned: List[str]
    created_at: datetime
    review_due_date: Optional[str] = None


# --- Scenario Planning Schemas ---

class ScenarioRunRequest(BaseModel):
    scenario_name: str
    scenario_type: ScenarioType = ScenarioType.CUSTOM
    base_revenue: Decimal = Decimal("4000000.00")
    base_cost: Decimal = Decimal("1400000.00")
    base_capacity_hours: Decimal = Decimal("160.0")
    base_committed_hours: Decimal = Decimal("140.0")
    price_change_pct: Decimal = Decimal("0.0")
    conversion_change_pct: Decimal = Decimal("0.0")
    client_churn_revenue: Decimal = Decimal("0.0")
    new_hires_count: int = 0
    additional_project_hours: Decimal = Decimal("0.0")


class ScenarioResponse(BaseModel):
    scenario_id: str
    scenario_name: str
    scenario_type: ScenarioType
    simulated_revenue: Decimal
    simulated_profit: Decimal
    simulated_margin_pct: Decimal
    capacity_utilization_pct: Decimal
    cash_requirement: Decimal
    risk_level: str
    assumptions_applied: Dict[str, Any]
    sensitivity_rankings: List[Dict[str, Any]]
    generated_at: datetime
    is_production_isolated: bool


# --- Briefings, Calendar & Copilot Schemas ---

class ExecutiveBriefingResponse(BaseModel):
    briefing_id: str
    frequency: BriefingFrequency
    title: str
    summary_paragraph: str
    key_metrics_snapshot: Dict[str, Any]
    what_changed_summary: List[str]
    top_decisions_required: List[Dict[str, Any]]
    critical_risks: List[Dict[str, Any]]
    upcoming_deadlines: List[Dict[str, Any]]
    recommended_attention_areas: List[str]
    generated_at: datetime


class BusinessCalendarEventResponse(BaseModel):
    event_id: str
    title: str
    event_type: str
    event_date: str
    related_entity_id: str
    related_entity_name: str
    severity: str
    owner: str
    is_completed: bool


class CopilotQueryRequest(BaseModel):
    query: str
    user_role: str = "EXECUTIVE"


class CopilotQueryResponse(BaseModel):
    query_id: str
    user_query: str
    intent: str
    answer_markdown: str
    confidence: str
    evidence_sources: List[Dict[str, Any]]
    suggested_followups: List[str]
    action_prohibited: bool
    prohibited_reason: Optional[str] = None
    answered_at: datetime
