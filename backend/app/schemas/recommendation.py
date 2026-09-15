import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class RecommendationEvidenceRead(BaseModel):
    source: str
    source_id: Optional[str] = None
    type: str
    description: str
    strength: float
    confidence: str


class ServiceRecommendationRead(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    business_id: uuid.UUID
    service_id: uuid.UUID
    service_name: Optional[str] = None
    service_slug: Optional[str] = None
    recommendation_version: str
    relevance_score: float
    band: str
    priority: str
    confidence: str
    status: str
    reasons: List[str]
    evidence: List[Dict[str, Any]]
    limitations: List[str]
    rejection_reason: Optional[str] = None
    rejected_by: Optional[uuid.UUID] = None
    rejected_at: Optional[datetime] = None
    accepted_by: Optional[uuid.UUID] = None
    accepted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecommendationRejectRequest(BaseModel):
    reason: Optional[str] = Field(default=None, max_length=1000)


class ServiceRecommendationListResponse(BaseModel):
    data: List[ServiceRecommendationRead]
    total: int
