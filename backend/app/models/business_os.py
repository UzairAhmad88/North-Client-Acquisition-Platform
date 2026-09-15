"""SQLAlchemy ORM Models for Unified Business Operating System (Business OS) & Executive Intelligence."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base

JSON_TYPE = JSON


class StrategicObjectiveModel(Base):
    """Strategic objectives defining organizational direction."""
    __tablename__ = "strategic_objectives"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), nullable=False, default="default_org", index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    timeframe = Column(String(50), nullable=False, default="FY2026")
    priority = Column(String(50), nullable=False, default="P1_HIGH")
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)
    owner = Column(String(100), nullable=False, default="Executive Team")
    progress_pct = Column(Numeric(5, 2), nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    key_results = relationship("app.models.business_os.KeyResultModel", back_populates="objective", cascade="all, delete-orphan")
    initiatives = relationship("InitiativeModel", back_populates="objective", cascade="all, delete-orphan")


class KeyResultModel(Base):
    """Measurable Key Results attached to Strategic Objectives (OKRs)."""
    __tablename__ = "key_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    objective_id = Column(String(36), ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    target_value = Column(Numeric(18, 2), nullable=False)
    current_value = Column(Numeric(18, 2), nullable=False, default=0.0)
    unit = Column(String(50), nullable=False, default="%")
    status = Column(String(50), nullable=False, default="NOT_STARTED")
    owner = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    objective = relationship("app.models.business_os.StrategicObjectiveModel", back_populates="key_results")


class InitiativeModel(Base):
    """Execution initiatives converting strategy into delivery actions."""
    __tablename__ = "initiatives"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    objective_id = Column(String(36), ForeignKey("strategic_objectives.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    owner = Column(String(100), nullable=False)
    budget = Column(Numeric(18, 2), nullable=False, default=0.0)
    priority = Column(String(50), nullable=False, default="P1_HIGH")
    status = Column(String(50), nullable=False, default="PLANNED", index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    objective = relationship("app.models.business_os.StrategicObjectiveModel", back_populates="initiatives")
    milestones = relationship("app.models.business_os.InitiativeMilestoneModel", back_populates="initiative", cascade="all, delete-orphan")
    dependencies = relationship("app.models.business_os.InitiativeDependencyModel", back_populates="initiative", cascade="all, delete-orphan")


class InitiativeMilestoneModel(Base):
    """Milestones supporting an initiative."""
    __tablename__ = "initiative_milestones"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    initiative_id = Column(String(36), ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    due_date = Column(String(50), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    initiative = relationship("app.models.business_os.InitiativeModel", back_populates="milestones")


class InitiativeDependencyModel(Base):
    """Dependencies across people, budget, technology, or other initiatives."""
    __tablename__ = "initiative_dependencies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    initiative_id = Column(String(36), ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    dependency_type = Column(String(50), nullable=False)  # PEOPLE, BUDGET, TECHNOLOGY, VENDOR
    state = Column(String(50), nullable=False, default="AVAILABLE")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    initiative = relationship("app.models.business_os.InitiativeModel", back_populates="dependencies")


class KPIDefinitionModel(Base):
    """Centralized KPI registry definition."""
    __tablename__ = "kpi_definitions"

    id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # FINANCIAL, SALES, CLIENT, DELIVERY, SUPPORT, AI, OPERATIONS
    description = Column(Text, nullable=True)
    unit = Column(String(50), nullable=False, default="")
    currency = Column(String(10), nullable=False, default="PKR")
    source_domain = Column(String(100), nullable=False)
    formula = Column(Text, nullable=False)
    target_value = Column(Numeric(18, 2), nullable=True)
    warning_threshold = Column(Numeric(18, 2), nullable=True)
    critical_threshold = Column(Numeric(18, 2), nullable=True)
    freshness_max_seconds = Column(Integer, nullable=False, default=3600)
    version = Column(String(20), nullable=False, default="1.0")
    is_higher_better = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class KPIValueSnapshotModel(Base):
    """Historical snapshot values for metrics."""
    __tablename__ = "kpi_value_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    kpi_id = Column(String(100), ForeignKey("kpi_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    value = Column(Numeric(18, 2), nullable=False)
    target_value = Column(Numeric(18, 2), nullable=True)
    variance = Column(Numeric(18, 2), nullable=True)
    status = Column(String(50), nullable=False, default="ON_TRACK")
    calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ScorecardRecordModel(Base):
    """Departmental and organizational scorecards."""
    __tablename__ = "scorecard_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    department_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    overall_status = Column(String(50), nullable=False, default="ON_TRACK")
    scorecard_items_json = Column(JSON_TYPE, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class BusinessHealthSnapshotModel(Base):
    """10-dimension composite organizational health snapshots."""
    __tablename__ = "business_health_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    overall_health_score = Column(Numeric(5, 2), nullable=False)
    overall_status = Column(String(50), nullable=False, default="HEALTHY", index=True)
    dimensions_json = Column(JSON_TYPE, nullable=False)
    key_strengths_json = Column(JSON_TYPE, nullable=True)
    critical_risks_json = Column(JSON_TYPE, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class OrganizationalRiskModel(Base):
    """Enterprise risk register records."""
    __tablename__ = "organizational_risks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    probability = Column(String(50), nullable=False, default="POSSIBLE")
    impact = Column(String(50), nullable=False, default="MODERATE")
    risk_score = Column(Integer, nullable=False, default=9)
    severity = Column(String(50), nullable=False, default="MEDIUM", index=True)
    owner = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="ASSESSED", index=True)
    evidence_signals_json = Column(JSON_TYPE, nullable=True)
    mitigation_strategy = Column(Text, nullable=True)
    contingency_plan = Column(Text, nullable=True)
    due_date = Column(String(50), nullable=True)
    identified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_reviewed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DecisionRecordModel(Base):
    """Executive decision records and governance lifecycle."""
    __tablename__ = "decision_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    business_question = Column(Text, nullable=False)
    context_summary = Column(Text, nullable=False)
    priority = Column(String(50), nullable=False, default="P1_HIGH")
    status = Column(String(50), nullable=False, default="DECISION_REQUIRED", index=True)
    ai_recommendation = Column(Text, nullable=True)
    ai_recommendation_rationale = Column(Text, nullable=True)
    chosen_option_id = Column(String(50), nullable=True)
    chosen_option_title = Column(String(255), nullable=True)
    decision_rationale = Column(Text, nullable=True)
    decided_by = Column(String(100), nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    expected_outcome = Column(Text, nullable=True)
    actual_outcome = Column(Text, nullable=True)
    outcome_variance_analysis = Column(Text, nullable=True)
    lessons_learned_json = Column(JSON_TYPE, nullable=True)
    evidence_signals_json = Column(JSON_TYPE, nullable=True)
    review_due_date = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ScenarioModel(Base):
    """Scenario model configurations and simulation runs."""
    __tablename__ = "scenario_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    scenario_type = Column(String(50), nullable=False, default="CUSTOM")
    simulated_revenue = Column(Numeric(18, 2), nullable=False)
    simulated_profit = Column(Numeric(18, 2), nullable=False)
    simulated_margin_pct = Column(Numeric(5, 2), nullable=False)
    capacity_utilization_pct = Column(Numeric(5, 2), nullable=False)
    cash_requirement = Column(Numeric(18, 2), nullable=False)
    risk_level = Column(String(50), nullable=False, default="LOW")
    assumptions_json = Column(JSON_TYPE, nullable=True)
    sensitivity_json = Column(JSON_TYPE, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExecutiveBriefingModel(Base):
    """Archived executive briefings."""
    __tablename__ = "executive_briefings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    frequency = Column(String(50), nullable=False, default="DAILY", index=True)
    title = Column(String(255), nullable=False)
    summary_paragraph = Column(Text, nullable=False)
    key_metrics_json = Column(JSON_TYPE, nullable=True)
    what_changed_json = Column(JSON_TYPE, nullable=True)
    top_decisions_json = Column(JSON_TYPE, nullable=True)
    critical_risks_json = Column(JSON_TYPE, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class BusinessCalendarEventModel(Base):
    """Strategic calendar events across renewals, milestones, and reviews."""
    __tablename__ = "business_calendar_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False, index=True)
    event_date = Column(String(50), nullable=False, index=True)
    related_entity_id = Column(String(100), nullable=False)
    related_entity_name = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False, default="NORMAL")
    owner = Column(String(100), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExecutiveAlertModel(Base):
    """Executive priority alerts."""
    __tablename__ = "executive_alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False, default="HIGH", index=True)  # INFO, LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), nullable=False, default="TRIGGERED", index=True)  # TRIGGERED, ACKNOWLEDGED, RESOLVED, DISMISSED
    source_domain = Column(String(100), nullable=False)
    acknowledged_by = Column(String(100), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
