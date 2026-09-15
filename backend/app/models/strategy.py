"""
ORM models for Phase 51: Autonomous Business Strategy, Planning & Goal Optimization Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class StrategicPillarModel(BaseModel):
    """Organization-level strategic pillars (e.g. Growth, Profitability, AI, Reliability)."""

    __tablename__ = "strategic_pillars"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    pillar_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class StrategicPlanModel(BaseModel):
    """High-level strategic plan container governing objectives and initiatives over a planning horizon."""

    __tablename__ = "strategic_plans"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    plan_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    vision_statement: Mapped[str] = mapped_column(Text, nullable=False)
    mission_statement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    planning_horizon: Mapped[str] = mapped_column(String(50), default="MEDIUM_TERM", nullable=False)  # SHORT_TERM, MEDIUM_TERM, LONG_TERM, STRATEGIC
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False, index=True)  # DRAFT, OPTIMIZED, REVIEW, APPROVED, ACTIVE, ARCHIVED
    total_budget_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class StrategicPlanVersionModel(BaseModel):
    """Immutable version history of approved and revised strategic plans."""

    __tablename__ = "strategic_plan_versions"

    plan_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    plan_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    change_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)


class StrategicObjectiveModel(BaseModel):
    """Measurable strategic objective anchored in a pillar and strategic plan."""

    __tablename__ = "strategic_objectives"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="SET NULL"), nullable=True, index=True
    )
    pillar_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_pillars.id", ondelete="SET NULL"), nullable=True, index=True
    )
    objective_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    strategic_pillar: Mapped[str] = mapped_column(String(100), default="GROWTH", nullable=False)
    owner: Mapped[str] = mapped_column(String(100), default="executive_team", nullable=False)
    priority: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    target_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # DRAFT, ACTIVE, ON_TRACK, AT_RISK, OFF_TRACK, ACHIEVED, MISSED
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class KeyResultModel(BaseModel):
    """Quantitative OKR key result underpinning an objective."""

    __tablename__ = "key_results"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    objective_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kr_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="PERCENT", nullable=False)
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    measurement_method: Mapped[str] = mapped_column(String(100), default="AUTOMATED_TELEMETRY", nullable=False)
    source_metric: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class StrategicInitiativeModel(BaseModel):
    """Funded, scheduled strategic initiative designed to accomplish objectives."""

    __tablename__ = "strategic_initiatives"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="SET NULL"), nullable=True, index=True
    )
    primary_objective_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_objectives.id", ondelete="SET NULL"), nullable=True, index=True
    )
    initiative_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), default="GROWTH", nullable=False)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IDEA", nullable=False, index=True)  # IDEA, EVALUATION, SIMULATION, PRIORITIZATION, APPROVED, PLANNING, EXECUTION, MONITORING, COMPLETED, CANCELLED
    expected_value_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    required_fte_capacity: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    estimated_duration_weeks: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    feasibility_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    is_funded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class InitiativeDependencyModel(BaseModel):
    """Dependency links between initiatives, projects, and resources."""

    __tablename__ = "initiative_dependencies"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    source_initiative_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_initiative_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dependency_type: Mapped[str] = mapped_column(String(50), default="FINISH_TO_START", nullable=False)
    is_critical_path: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    lag_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class StrategicConstraintModel(BaseModel):
    """Hard and soft operational, budget, and capacity constraints for strategic optimization."""

    __tablename__ = "strategic_constraints"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True
    )
    constraint_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="BUDGET", nullable=False)  # BUDGET, CAPACITY, HEADCOUNT, TIMELINE, COMPLIANCE, SECURITY, AI_CAPACITY
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    operator: Mapped[str] = mapped_column(String(20), default="LTE", nullable=False)  # LTE, GTE, EQ
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False)
    is_hard_constraint: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class StrategicAssumptionModel(BaseModel):
    """Explicitly declared assumptions governing strategic plans and optimization models."""

    __tablename__ = "strategic_assumptions"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True
    )
    assumption_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    parameter_name: Mapped[str] = mapped_column(String(100), nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    assumed_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    source_basis: Mapped[str] = mapped_column(String(100), default="HISTORICAL_ANALYTICS", nullable=False)


class OptimizationRunModel(BaseModel):
    """Mathematical optimization run generating Pareto-optimal initiative portfolios."""

    __tablename__ = "optimization_runs"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_plans.id", ondelete="CASCADE"), nullable=True, index=True
    )
    run_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    optimization_type: Mapped[str] = mapped_column(String(100), default="MULTI_OBJECTIVE_LINEAR", nullable=False)
    objective_weights: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    solver_name: Mapped[str] = mapped_column(String(100), default="EXACT_SIMPLEX_HEURISTIC", nullable=False)
    runtime_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)
    score_achieved: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    selected_initiative_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    explanation: Mapped[Text] = mapped_column(Text, nullable=False)


class ParetoFrontierModel(BaseModel):
    """Set of non-dominated strategic plans balancing competing business objectives."""

    __tablename__ = "pareto_frontiers"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    optimization_run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("optimization_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    frontier_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    plans_payload: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    tradeoff_summary: Mapped[Text] = mapped_column(Text, nullable=False)


class StrategicRiskAssessmentModel(BaseModel):
    """Comprehensive strategic risk assessment evaluating threats across 10 categories."""

    __tablename__ = "strategy_risk_assessments"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    initiative_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategic_initiatives.id", ondelete="CASCADE"), nullable=True, index=True
    )
    risk_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), default="OPERATIONAL", nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    likelihood: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    impact: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.1, nullable=False)
    mitigation_strategy: Mapped[Text] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)


class StrategicScorecardModel(BaseModel):
    """10-dimension strategic health scorecard."""

    __tablename__ = "strategy_scorecards"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    scorecard_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(50), default="CURRENT_QUARTER", nullable=False)
    composite_health_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    growth_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    profitability_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    delivery_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    ai_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    security_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    compliance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    reliability_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    dimensions_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class StrategicAlertModel(BaseModel):
    """Alerts triggered for goal divergence, strategic drift, budget overruns, or critical blockers."""

    __tablename__ = "strategy_alerts"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    alert_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    alert_type: Mapped[str] = mapped_column(String(100), default="STRATEGIC_DRIFT", nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="WARNING", nullable=False)  # INFO, WARNING, HIGH, CRITICAL
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    affected_objective_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class StrategicDecisionRecordModel(BaseModel):
    """Immutable human strategic decision record preserving options, rationale, and authority."""

    __tablename__ = "strategy_decisions"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    decision_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    question: Mapped[str] = mapped_column(String(255), nullable=False)
    context_summary: Mapped[Text] = mapped_column(Text, nullable=False)
    selected_option: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    rejected_options: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_owner: Mapped[str] = mapped_column(String(100), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    plan_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class StrategicOutcomeModel(BaseModel):
    """Observed real-world performance against planned strategic milestones."""

    __tablename__ = "strategy_outcomes"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    decision_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("strategy_decisions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    outcome_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    observed_period: Mapped[str] = mapped_column(String(50), nullable=False)
    planned_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    actual_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    variance_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    model_prediction_error: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class StrategicDriftEventModel(BaseModel):
    """Events indicating divergence between strategic expectations and operational reality."""

    __tablename__ = "strategy_drift_events"
    __table_args__ = {"extend_existing": True}

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    drift_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    drift_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    recommended_action: Mapped[Text] = mapped_column(Text, nullable=False)
    is_adapted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

