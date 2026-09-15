"""SQLAlchemy Models for Phase 32: Advanced AI/ML Decision Intelligence & Predictive Operations."""

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


class PredictionType(str, Enum):
    LEAD_CONVERSION = "LEAD_CONVERSION"
    LEAD_PRIORITY = "LEAD_PRIORITY"
    PROJECT_DELAY = "PROJECT_DELAY"
    PROJECT_EFFORT_VARIANCE = "PROJECT_EFFORT_VARIANCE"
    PROJECT_SCOPE_CHANGE = "PROJECT_SCOPE_CHANGE"
    SUPPORT_VOLUME = "SUPPORT_VOLUME"
    INCIDENT_RISK = "INCIDENT_RISK"
    CLIENT_RETENTION = "CLIENT_RETENTION"
    CLIENT_EXPANSION = "CLIENT_EXPANSION"
    AI_FAILURE = "AI_FAILURE"
    AI_COST = "AI_COST"
    WORKLOAD = "WORKLOAD"
    PIPELINE_FORECAST = "PIPELINE_FORECAST"


class ModelLifecycleStatus(str, Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    VALIDATING = "VALIDATING"
    APPROVED = "APPROVED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class RiskBand(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class DecisionState(str, Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    ACCEPTED = "ACCEPTED"
    OVERRIDDEN = "OVERRIDDEN"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class DriftStatus(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


# ==============================================================================
# 1. Feature Store & Feature Registry
# ==============================================================================

class FeatureDefinition(Base):
    """Central catalog of approved engineered features with lineage and privacy rating."""
    __tablename__ = "feature_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    feature_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    data_source = Column(String(100), nullable=False)  # "leads", "projects", "support_requests", "qa"
    formula = Column(Text, nullable=False)
    data_type = Column(String(50), nullable=False, default="float")  # float, int, categorical, boolean
    freshness_window = Column(String(50), nullable=False, default="24h")
    privacy_level = Column(String(50), nullable=False, default="INTERNAL_BUSINESS")
    owner = Column(String(100), nullable=False, default="ml_engineering")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    versions = relationship("FeatureVersion", back_populates="feature", cascade="all, delete-orphan")


class FeatureVersion(Base):
    """Versioned transformations for a feature."""
    __tablename__ = "feature_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    feature_id = Column(String(36), ForeignKey("feature_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)  # "v1.0", "v1.1"
    transformation_logic = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    feature = relationship("FeatureDefinition", back_populates="versions")


class FeatureValue(Base):
    """Point-in-time engineered feature values computed for entities."""
    __tablename__ = "feature_values"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    feature_id = Column(String(36), ForeignKey("feature_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)  # lead_id, project_id, etc.
    value_numeric = Column(Float, nullable=True)
    value_text = Column(String(255), nullable=True)
    value_json = Column(JSON, nullable=False, default=dict)
    as_of_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 2. Training Datasets & Runs
# ==============================================================================

class TrainingDataset(Base):
    """Immutable datasets assembled for model training with strict data leakage prevention."""
    __tablename__ = "training_datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dataset_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    prediction_type = Column(SQLEnum(PredictionType), nullable=False, index=True)
    feature_keys = Column(JSON, nullable=False, default=list)  # list of feature_key strings
    target_label = Column(String(100), nullable=False)
    data_window_start = Column(DateTime, nullable=False)
    data_window_end = Column(DateTime, nullable=False)
    row_count = Column(Integer, nullable=False, default=0)
    leakage_check_passed = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    runs = relationship("TrainingRun", back_populates="dataset")


class TrainingRun(Base):
    """Execution run training a specific candidate or experimental model."""
    __tablename__ = "training_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dataset_id = Column(String(36), ForeignKey("training_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    algorithm = Column(String(100), nullable=False)  # "logistic_regression", "gradient_boosting", "deterministic_baseline"
    hyperparameters = Column(JSON, nullable=False, default=dict)
    evaluation_metrics = Column(JSON, nullable=False, default=dict)  # {"accuracy": 0.82, "roc_auc": 0.88, "mae": 4.2}
    training_duration_seconds = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("TrainingDataset", back_populates="runs")


# ==============================================================================
# 3. Model Governance, Deployments & Monitoring
# ==============================================================================

class PredictionModel(Base):
    """Model governance record with approval and lifecycle status."""
    __tablename__ = "prediction_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    prediction_type = Column(SQLEnum(PredictionType), nullable=False, index=True)
    algorithm = Column(String(100), nullable=False)
    current_version = Column(String(20), nullable=False, default="v1.0")
    status = Column(SQLEnum(ModelLifecycleStatus), nullable=False, default=ModelLifecycleStatus.EXPERIMENTAL, index=True)
    thresholds = Column(JSON, nullable=False, default=dict)  # {"low": 0.39, "medium": 0.69, "high": 0.89}
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    deployments = relationship("ModelDeployment", back_populates="model", cascade="all, delete-orphan")
    predictions = relationship("PredictionRecord", back_populates="model")


class ModelDeployment(Base):
    """Historical record of model deployment activations with rollback tracking."""
    __tablename__ = "model_deployments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_id = Column(String(36), ForeignKey("prediction_models.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    deployed_by = Column(String(100), nullable=False)
    deployment_mode = Column(String(50), nullable=False, default="PRODUCTION")  # PRODUCTION, SHADOW
    deployed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    retired_at = Column(DateTime, nullable=True)

    model = relationship("PredictionModel", back_populates="deployments")


# ==============================================================================
# 4. Prediction Store, Explanations & Real-World Outcomes
# ==============================================================================

class PredictionRecord(Base):
    """Audit-proof prediction generated at a specific point in time."""
    __tablename__ = "prediction_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_id = Column(String(36), ForeignKey("prediction_models.id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_type = Column(SQLEnum(PredictionType), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)  # lead_id, project_id, client_account_id
    probability = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_band = Column(SQLEnum(RiskBand), nullable=False, default=RiskBand.MEDIUM)
    confidence_interval = Column(JSON, nullable=False, default=dict)  # {"lower": 0.65, "upper": 0.85}
    model_version = Column(String(20), nullable=False)
    inference_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    model = relationship("PredictionModel", back_populates="predictions")
    explanation = relationship("PredictionExplanation", back_populates="prediction", uselist=False, cascade="all, delete-orphan")
    outcome = relationship("PredictionOutcome", back_populates="prediction", uselist=False, cascade="all, delete-orphan")
    decision_support = relationship("DecisionSupportRecord", back_populates="prediction", uselist=False)


class PredictionExplanation(Base):
    """Calibrated feature attribution and human-readable drivers for a prediction."""
    __tablename__ = "prediction_explanations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    prediction_id = Column(String(36), ForeignKey("prediction_records.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    summary_text = Column(Text, nullable=False)
    key_drivers = Column(JSON, nullable=False, default=list)  # [{"feature": "blocked_tasks", "impact": "+0.32", "value": 4}]
    safety_notes = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prediction = relationship("PredictionRecord", back_populates="explanation")


class PredictionOutcome(Base):
    """Authoritative real-world outcome recorded against a historical prediction."""
    __tablename__ = "prediction_outcomes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    prediction_id = Column(String(36), ForeignKey("prediction_records.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    actual_numeric_outcome = Column(Float, nullable=False)  # 1.0 (Won/Delayed) or 0.0 (Lost/OnTime) or actual hours
    outcome_label = Column(String(100), nullable=False)  # "CLOSED_WON", "DELIVERED_ON_TIME", "OVERRUN"
    error_magnitude = Column(Float, nullable=True)  # abs(actual - predicted)
    recorded_by = Column(String(100), nullable=False, default="system_outcome_collector")
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prediction = relationship("PredictionRecord", back_populates="outcome")


# ==============================================================================
# 5. Decision Intelligence Layer & Human Review
# ==============================================================================

class DecisionPolicy(Base):
    """Versioned business policies mapping predictions and rules to human decision workflows."""
    __tablename__ = "decision_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    policy_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    prediction_type = Column(SQLEnum(PredictionType), nullable=False)
    rules_logic = Column(JSON, nullable=False, default=dict)
    version = Column(String(20), nullable=False, default="v1.0")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionPolicyVersion(Base):
    """Audit log of policy versions and changes."""
    __tablename__ = "decision_policy_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    policy_id = Column(String(36), ForeignKey("decision_policies.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    rules_logic = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)



class DecisionSupportRecord(Base):
    """Central human decision queue record: AI Recommends -> You Decide."""
    __tablename__ = "decision_support_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    prediction_id = Column(String(36), ForeignKey("prediction_records.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    recommended_action = Column(Text, nullable=False)
    tradeoff_analysis = Column(Text, nullable=False)
    urgency = Column(SQLEnum(RiskBand), nullable=False, default=RiskBand.MEDIUM)
    state = Column(SQLEnum(DecisionState), nullable=False, default=DecisionState.PENDING_REVIEW, index=True)
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    prediction = relationship("PredictionRecord", back_populates="decision_support")
    reviews = relationship("DecisionReview", back_populates="decision_record", cascade="all, delete-orphan")
    overrides = relationship("DecisionOverride", back_populates="decision_record", cascade="all, delete-orphan")


class DecisionReview(Base):
    """Audit log of human decisions recorded on decision support items."""
    __tablename__ = "decision_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    decision_record_id = Column(String(36), ForeignKey("decision_support_records.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)  # "ACCEPT", "REJECT", "OVERRIDE"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    decision_record = relationship("DecisionSupportRecord", back_populates="reviews")


class DecisionOverride(Base):
    """Valuable feedback records capturing why a human operator chose to override model advice."""
    __tablename__ = "decision_overrides"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    decision_record_id = Column(String(36), ForeignKey("decision_support_records.id", ondelete="CASCADE"), nullable=False, index=True)
    original_recommendation = Column(Text, nullable=False)
    chosen_action = Column(Text, nullable=False)
    override_reason = Column(Text, nullable=False)
    operator = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    decision_record = relationship("DecisionSupportRecord", back_populates="overrides")


# ==============================================================================
# 6. Forecasts, Model Drift Events & Monitoring Alerts
# ==============================================================================

class ForecastRun(Base):
    """Periodic multi-horizon operational and financial workload forecasts."""
    __tablename__ = "forecast_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    forecast_type = Column(String(100), nullable=False, index=True)  # "SUPPORT_VOLUME", "AI_COST", "WORKLOAD_DEMAND"
    time_horizon = Column(String(50), nullable=False, default="30d")
    model_version = Column(String(20), nullable=False)
    predictions_payload = Column(JSON, nullable=False, default=dict)
    confidence_intervals = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class ModelDriftEvent(Base):
    """Statistical drift detection events triggering human review alerts."""
    __tablename__ = "model_drift_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    model_key = Column(String(100), nullable=False, index=True)
    drift_type = Column(String(50), nullable=False)  # "FEATURE_DRIFT", "PREDICTION_DRIFT", "CALIBRATION_DRIFT"
    drift_metric_value = Column(Float, nullable=False)
    drift_status = Column(SQLEnum(DriftStatus), nullable=False, default=DriftStatus.WARNING)
    details = Column(JSON, nullable=False, default=dict)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
