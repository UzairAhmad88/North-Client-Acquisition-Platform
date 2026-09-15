import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ComponentScoreResponse(BaseModel):
    component: str
    score: float
    weight: float
    weighted_contribution: float
    reasons: List[str]
    evidence: List[str]
    status: str = "SCORED"


class LeadScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    business_id: uuid.UUID
    audit_id: Optional[uuid.UUID] = None
    score_version: str
    total_score: float
    band: str
    website_need_score: float
    online_presence_score: float
    lead_capture_score: float
    automation_potential_score: float
    business_activity_score: float
    contactability_score: float
    service_fit_score: float
    explanation: str
    evidence: Dict[str, Any]
    breakdown: Dict[str, Any]
    confidence: str
    is_stale: bool
    calculated_at: datetime
    calculated_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


class LeadScoreHistoryResponse(BaseModel):
    lead_id: uuid.UUID
    total_scores: int
    latest_score: Optional[LeadScoreResponse] = None
    history: List[LeadScoreResponse] = Field(default_factory=list)
