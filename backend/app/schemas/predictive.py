"""Pydantic schemas for Phase 32: Advanced AI/ML Decision Intelligence & Predictive Operations API."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# =============================================================================
# 1. Predictions & Explanations Schemas
# =============================================================================

class PredictionExplanationSchema(BaseModel):
    summary_text: str
    key_drivers: List[Dict[str, Any]]
    safety_notes: List[str]

    class Config:
        from_attributes = True


class PredictionOutcomeSchema(BaseModel):
    actual_numeric_outcome: float
    outcome_label: str
    error_magnitude: Optional[float]
    recorded_by: str
    recorded_at: datetime

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    id: str
    tenant_id: str
    model_id: str
    prediction_type: str
    entity_id: str
    probability: float
    risk_band: str
    confidence_interval: Dict[str, float]
    model_version: str
    inference_timestamp: datetime
    created_at: datetime
    explanation: Optional[PredictionExplanationSchema] = None
    outcome: Optional[PredictionOutcomeSchema] = None

    class Config:
        from_attributes = True


class PredictionCreateRequest(BaseModel):
    prediction_type: str = Field(..., description="LEAD_CONVERSION, PROJECT_DELAY, PROJECT_EFFORT_VARIANCE, CLIENT_RETENTION")
    entity_id: str
    features: Dict[str, Any] = Field(default_factory=dict)


class OutcomeRecordRequest(BaseModel):
    actual_numeric_outcome: float = Field(..., description="1.0 for Won/Delayed or 0.0 for Lost/On-Time or actual hours")
    outcome_label: str = Field(..., description="e.g. 'CLOSED_WON', 'DELIVERED_ON_TIME'")
    recorded_by: str = Field(default="user")


# =============================================================================
# 2. Decision Support & Human Review Schemas
# =============================================================================

class DecisionOverrideSchema(BaseModel):
    id: str
    original_recommendation: str
    chosen_action: str
    override_reason: str
    operator: str
    created_at: datetime

    class Config:
        from_attributes = True


class DecisionSupportResponse(BaseModel):
    id: str
    tenant_id: str
    prediction_id: str
    title: str
    recommended_action: str
    tradeoff_analysis: str
    urgency: str
    state: str
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime
    overrides: List[DecisionOverrideSchema] = []

    class Config:
        from_attributes = True


class DecisionReviewRequest(BaseModel):
    action: str = Field(..., description="ACCEPT, OVERRIDE, REJECT")
    reviewer: str = Field(default="user")
    notes: Optional[str] = None
    override_reason: Optional[str] = None
    chosen_action: Optional[str] = None


# =============================================================================
# 3. Model Registry & Drift Monitoring Schemas
# =============================================================================

class ModelGovernanceResponse(BaseModel):
    id: str
    tenant_id: str
    model_key: str
    name: str
    prediction_type: str
    algorithm: str
    current_version: str
    status: str
    thresholds: Dict[str, Any]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ModelApproveRequest(BaseModel):
    approved_by: str


class ForecastResponse(BaseModel):
    id: str
    tenant_id: str
    forecast_type: str
    time_horizon: str
    model_version: str
    predictions_payload: Dict[str, Any]
    confidence_intervals: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class ModelDriftEventResponse(BaseModel):
    id: str
    tenant_id: str
    model_key: str
    drift_type: str
    drift_metric_value: float
    drift_status: str
    details: Dict[str, Any]
    detected_at: datetime

    class Config:
        from_attributes = True
