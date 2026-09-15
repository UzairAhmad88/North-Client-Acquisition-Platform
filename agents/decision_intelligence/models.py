"""Pydantic data structures for Predictive and Decision Intelligence Subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FeatureVector(BaseModel):
    entity_id: str
    feature_snapshot: Dict[str, Any] = Field(default_factory=dict)
    as_of_timestamp: str = Field(..., description="ISO timestamp for point-in-time leakage defense")


class PredictionDraft(BaseModel):
    prediction_type: str
    entity_id: str
    probability: float = Field(..., ge=0.0, le=1.0)
    risk_band: str = Field(default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL, UNKNOWN
    confidence_interval: Dict[str, float] = Field(default_factory=dict)  # {"lower": 0.60, "upper": 0.80}
    model_version: str = Field(default="v1.0")
    key_drivers: List[Dict[str, Any]] = Field(default_factory=list)
    summary_text: str = Field(...)
    safety_notes: List[str] = Field(default_factory=list)


class DecisionSupportDraft(BaseModel):
    prediction_type: str
    entity_id: str
    title: str
    recommended_action: str
    tradeoff_analysis: str
    urgency: str = Field(default="MEDIUM")
    governing_policy: str = Field(default="DEFAULT_POLICY")
    deterministic_override_applied: bool = Field(default=False)
    deterministic_rule_notes: Optional[str] = None


class HumanDecisionRequest(BaseModel):
    action: str = Field(..., description="ACCEPT, OVERRIDE, REJECT")
    reviewer: str = Field(default="user")
    notes: Optional[str] = None
    override_reason: Optional[str] = None
    chosen_action: Optional[str] = None


class ForecastRequest(BaseModel):
    forecast_type: str = Field(..., description="SUPPORT_VOLUME, AI_COST, WORKLOAD_DEMAND")
    time_horizon: str = Field(default="30d")
    context_filters: Dict[str, Any] = Field(default_factory=dict)
