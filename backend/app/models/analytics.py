"""SQLAlchemy Models for Phase 31: Business Intelligence, Portfolio Analytics & Organizational Learning System."""

import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    Float,
    Integer,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class MetricStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DRAFT = "DRAFT"
    EXPERIMENTAL = "EXPERIMENTAL"


class InsightCategory(str, Enum):
    SALES = "SALES"
    MARKETING = "MARKETING"
    ESTIMATION = "ESTIMATION"
    DELIVERY = "DELIVERY"
    QUALITY = "QUALITY"
    SUPPORT = "SUPPORT"
    CLIENT_SUCCESS = "CLIENT_SUCCESS"
    AI = "AI"
    OPERATIONS = "OPERATIONS"
    FINANCE = "FINANCE"
    PRODUCTIVITY = "PRODUCTIVITY"


class InsightStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class RecommendationStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IMPLEMENTED = "IMPLEMENTED"
    SUPERSEDED = "SUPERSEDED"


class ExperimentStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EVALUATED = "EVALUATED"


class ModelStatus(str, Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    VALIDATING = "VALIDATING"
    APPROVED = "APPROVED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class DataQualityStatus(str, Enum):
    GOOD = "GOOD"
    WARNING = "WARNING"
    POOR = "POOR"
    UNKNOWN = "UNKNOWN"


# ==============================================================================
# 1. Analytics & Metrics Registry Models
# ==============================================================================

class AnalyticsMetric(Base):
    """Centralized definition of business and operational metrics."""
    __tablename__ = "analytics_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    metric_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(InsightCategory), nullable=False, default=InsightCategory.OPERATIONS)
    formula = Column(Text, nullable=False)
    source_tables = Column(JSON, nullable=False, default=list)  # list of strings
    dimensions = Column(JSON, nullable=False, default=list)  # list of dimension keys
    time_window_default = Column(String(50), nullable=False, default="30d")
    version = Column(String(20), nullable=False, default="v1.0")
    owner = Column(String(100), nullable=False, default="system")
    status = Column(SQLEnum(MetricStatus), nullable=False, default=MetricStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    versions = relationship("AnalyticsMetricVersion", back_populates="metric", cascade="all, delete-orphan")


class AnalyticsMetricVersion(Base):
    """Immutable audit versioning for metrics formulas and definitions."""
    __tablename__ = "analytics_metric_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    metric_id = Column(String(36), ForeignKey("analytics_metrics.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    formula = Column(Text, nullable=False)
    change_reason = Column(Text, nullable=True)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    metric = relationship("AnalyticsMetric", back_populates="versions")


class AnalyticsDimension(Base):
    """Analytics dimensions (e.g., industry, service, channel, stage)."""
    __tablename__ = "analytics_dimensions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dimension_type = Column(String(100), nullable=False, index=True)  # DIM_INDUSTRY, DIM_SERVICE, DIM_CHANNEL, etc.
    dimension_key = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    attributes = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AnalyticsFact(Base):
    """Event & fact analytical records for multi-dimensional querying."""
    __tablename__ = "analytics_facts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    fact_type = Column(String(100), nullable=False, index=True)  # FACT_LEAD, FACT_PROJECT, FACT_SUPPORT, FACT_AI_USAGE, etc.
    entity_id = Column(String(36), nullable=True, index=True)
    dimensions = Column(JSON, nullable=False, default=dict)  # {"industry": "real_estate", "service": "crm"}
    numeric_values = Column(JSON, nullable=False, default=dict)  # {"estimated_hours": 40.0, "actual_hours": 46.5}
    status = Column(String(50), nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AnalyticsSnapshot(Base):
    """Periodic snapshots of portfolio performance & health."""
    __tablename__ = "analytics_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    snapshot_type = Column(String(100), nullable=False, index=True)  # EXECUTIVE_WEEKLY, SALES_FUNNEL, CLIENT_HEALTH
    time_window = Column(String(50), nullable=False)  # 7d, 30d, 90d, 365d
    metrics_data = Column(JSON, nullable=False, default=dict)
    sample_sizes = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AnalyticsAggregation(Base):
    """Aggregated cache for fast multi-dimensional analytical queries."""
    __tablename__ = "analytics_aggregations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    aggregation_key = Column(String(150), nullable=False, index=True)  # "sales_by_industry_30d"
    time_window = Column(String(50), nullable=False)
    granularity = Column(String(50), nullable=False, default="daily")  # daily, weekly, monthly
    results = Column(JSON, nullable=False, default=dict)
    sample_size = Column(Integer, nullable=False, default=0)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 2. Organizational Learning: Insights & Recommendations
# ==============================================================================

class BusinessInsight(Base):
    """Structured organizational insights with strict evidence grounding."""
    __tablename__ = "business_insights"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(InsightCategory), nullable=False, index=True)
    confidence = Column(SQLEnum(ConfidenceLevel), nullable=False, default=ConfidenceLevel.MEDIUM)
    sample_size = Column(Integer, nullable=False, default=0)
    time_window = Column(String(50), nullable=False, default="30d")
    affected_entities = Column(JSON, nullable=False, default=dict)  # {"services": ["ai_systems"], "industries": ["retail"]}
    recommended_action = Column(Text, nullable=True)
    status = Column(SQLEnum(InsightStatus), nullable=False, default=InsightStatus.DRAFT, index=True)
    created_by = Column(String(100), nullable=False, default="bi_learning_agent")
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    evidence_items = relationship("BusinessInsightEvidence", back_populates="insight", cascade="all, delete-orphan")
    recommendations = relationship("BusinessRecommendation", back_populates="insight")


class BusinessInsightEvidence(Base):
    """Audit-proof empirical evidence items backing a business insight."""
    __tablename__ = "business_insight_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    insight_id = Column(String(36), ForeignKey("business_insights.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type = Column(String(100), nullable=False)  # "PROJECT_VARIANCE", "LEAD_SCORE_ACCURACY", "QA_DEFECT_LEAKAGE"
    sample_count = Column(Integer, nullable=False, default=0)
    baseline_value = Column(Float, nullable=True)
    observed_value = Column(Float, nullable=True)
    variance_pct = Column(Float, nullable=True)
    details = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    insight = relationship("BusinessInsight", back_populates="evidence_items")


class BusinessRecommendation(Base):
    """Prescriptive suggestions requiring human review and explicit decision."""
    __tablename__ = "business_recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    insight_id = Column(String(36), ForeignKey("business_insights.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    recommendation = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    expected_benefit = Column(Text, nullable=False)
    potential_downside = Column(Text, nullable=False)
    confidence = Column(SQLEnum(ConfidenceLevel), nullable=False, default=ConfidenceLevel.MEDIUM)
    affected_workflow = Column(String(100), nullable=False)  # "ESTIMATION", "REQUIREMENTS", "DISCOVERY"
    status = Column(SQLEnum(RecommendationStatus), nullable=False, default=RecommendationStatus.PENDING_APPROVAL, index=True)
    decision_reason = Column(Text, nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    insight = relationship("BusinessInsight", back_populates="recommendations")
    reviews = relationship("RecommendationReview", back_populates="recommendation", cascade="all, delete-orphan")


class RecommendationReview(Base):
    """Historical record of human reviews on recommendations."""
    __tablename__ = "recommendation_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    recommendation_id = Column(String(36), ForeignKey("business_recommendations.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)  # "APPROVE", "REJECT", "IMPLEMENT", "SUPERSEDE"
    notes = Column(Text, nullable=True)
    policy_impact = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    recommendation = relationship("BusinessRecommendation", back_populates="reviews")


# ==============================================================================
# 3. Continuous Improvement: Hypotheses & Experiments
# ==============================================================================

class Experiment(Base):
    """Continuous improvement experiment framework."""
    __tablename__ = "experiments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    target_workflow = Column(String(100), nullable=False)  # "REQUIREMENTS", "ESTIMATION", "OUTREACH"
    target_metric = Column(String(100), nullable=False)  # "scope_change_frequency", "response_rate"
    baseline_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=False, default=0.0)
    sample_target = Column(Integer, nullable=False, default=10)
    current_sample_count = Column(Integer, nullable=False, default=0)
    status = Column(SQLEnum(ExperimentStatus), nullable=False, default=ExperimentStatus.DRAFT, index=True)
    created_by = Column(String(100), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    conclusion = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    metrics = relationship("ExperimentMetric", back_populates="experiment", cascade="all, delete-orphan")
    results = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan")


class ExperimentMetric(Base):
    """Tracking measurements for an experiment."""
    __tablename__ = "experiment_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    is_primary = Column(Boolean, nullable=False, default=True)
    baseline_value = Column(Float, nullable=False, default=0.0)
    current_value = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), nullable=False, default="count")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    experiment = relationship("Experiment", back_populates="metrics")


class ExperimentResult(Base):
    """Individual cohort/trial outcomes recorded against an experiment."""
    __tablename__ = "experiment_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(String(36), nullable=True)  # project_id or lead_id
    observed_value = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    experiment = relationship("Experiment", back_populates="results")


# ==============================================================================
# 4. Model Registry & ML Governance
# ==============================================================================

class ModelRegistry(Base):
    """Registry and governance for predictive baselines and ML models."""
    __tablename__ = "model_registry"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_key = Column(String(100), nullable=False, unique=True, index=True)  # "lead_conversion_baseline_v1"
    name = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    version = Column(String(20), nullable=False, default="v1.0")
    model_type = Column(String(50), nullable=False, default="deterministic_baseline")  # deterministic_baseline, regression, classifier
    features = Column(JSON, nullable=False, default=list)
    training_window = Column(String(50), nullable=False, default="90d")
    evaluation_metrics = Column(JSON, nullable=False, default=dict)  # {"mae": 0.12, "accuracy": 0.85}
    status = Column(SQLEnum(ModelStatus), nullable=False, default=ModelStatus.EXPERIMENTAL, index=True)
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    evaluations = relationship("ModelEvaluation", back_populates="model", cascade="all, delete-orphan")
    predictions = relationship("ModelPrediction", back_populates="model", cascade="all, delete-orphan")


class ModelEvaluation(Base):
    """Periodic evaluation runs tracking model performance and calibration."""
    __tablename__ = "model_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_id = Column(String(36), ForeignKey("model_registry.id", ondelete="CASCADE"), nullable=False, index=True)
    evaluation_type = Column(String(50), nullable=False)  # "CALIBRATION", "ACCURACY", "DRIFT"
    sample_size = Column(Integer, nullable=False, default=0)
    metrics_result = Column(JSON, nullable=False, default=dict)
    drift_detected = Column(Boolean, nullable=False, default=False)
    drift_details = Column(JSON, nullable=False, default=dict)
    evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    model = relationship("ModelRegistry", back_populates="evaluations")


class ModelPrediction(Base):
    """Audit log of predictive inferences with confidence intervals."""
    __tablename__ = "model_predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_id = Column(String(36), ForeignKey("model_registry.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(String(36), nullable=True, index=True)  # lead_id, project_id
    prediction_value = Column(Float, nullable=False)
    confidence_interval = Column(JSON, nullable=False, default=dict)  # {"lower": 0.65, "upper": 0.85}
    features_snapshot = Column(JSON, nullable=False, default=dict)
    actual_outcome = Column(Float, nullable=True)
    outcome_recorded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    model = relationship("ModelRegistry", back_populates="predictions")


# ==============================================================================
# 5. Data Quality, Semantic Queries & Audit Reports
# ==============================================================================

class DataQualityCheck(Base):
    """Data quality rules and health verification checks."""
    __tablename__ = "data_quality_checks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    check_name = Column(String(150), nullable=False)
    target_table = Column(String(100), nullable=False)
    rule_type = Column(String(100), nullable=False)  # "MISSING_OUTCOME", "IMPOSSIBLE_TIMESTAMP", "STALE_RECORD"
    status = Column(SQLEnum(DataQualityStatus), nullable=False, default=DataQualityStatus.GOOD)
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DataQualityResult(Base):
    """Results of periodic data quality checks."""
    __tablename__ = "data_quality_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    check_id = Column(String(36), ForeignKey("data_quality_checks.id", ondelete="CASCADE"), nullable=False, index=True)
    total_records = Column(Integer, nullable=False, default=0)
    failed_records = Column(Integer, nullable=False, default=0)
    status = Column(SQLEnum(DataQualityStatus), nullable=False, default=DataQualityStatus.GOOD)
    anomalies = Column(JSON, nullable=False, default=list)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AnalyticsQueryRun(Base):
    """Audit log of parameterized semantic queries executed via AI or UI."""
    __tablename__ = "analytics_query_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    query_name = Column(String(150), nullable=False)
    parameter_payload = Column(JSON, nullable=False, default=dict)
    executed_by = Column(String(100), nullable=False)
    execution_time_ms = Column(Float, nullable=False, default=0.0)
    result_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AnalyticsReport(Base):
    """Weekly, monthly, or quarterly executive BI reports."""
    __tablename__ = "analytics_reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    report_type = Column(String(50), nullable=False)  # "WEEKLY_OPERATIONAL", "MONTHLY_PERFORMANCE", "QUARTERLY_STRATEGIC"
    title = Column(String(255), nullable=False)
    time_window = Column(String(50), nullable=False)
    report_summary = Column(Text, nullable=False)
    report_data = Column(JSON, nullable=False, default=dict)
    created_by = Column(String(100), nullable=False, default="bi_agent")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
