"""Data models and structures for recommendation engine context and signal evaluation."""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.audit import AuditFinding, BusinessAudit
from app.models.business import Business
from app.models.lead import Lead
from app.models.research import ResearchRecord
from app.models.score import LeadScore
from app.models.service import LeadService, Service


class RecommendationSignal(BaseModel):
    """Internal signal representation traceable to evidence."""

    signal: str
    source: str  # audit, research, business, lead, scoring
    source_id: Optional[str] = None
    strength: float = Field(default=50.0, ge=0.0, le=100.0)
    confidence: str = "MEDIUM"
    description: str = ""


class ComponentScoreResult(BaseModel):
    """Calculated result for a single recommendation dimension."""

    component_name: str
    weight: float
    raw_score: float = Field(default=0.0, ge=0.0, le=100.0)
    weighted_contribution: float = 0.0
    signals: List[RecommendationSignal] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)


class CandidateRecommendation(BaseModel):
    """Engine result for a single recommended service."""

    service_id: uuid.UUID
    service_name: str
    service_slug: str
    category: str
    recommendation_version: str = "1.0"
    relevance_score: float
    band: str
    priority: str
    confidence: str
    reasons: List[str]
    evidence: List[Dict[str, Any]]
    limitations: List[str]
    component_scores: Dict[str, ComponentScoreResult]


class RecommendationContext(BaseModel):
    """Full snapshot of business, lead, research, audit, score, and service context."""

    lead: Lead
    business: Business
    research_records: List[ResearchRecord] = Field(default_factory=list)
    audit: Optional[BusinessAudit] = None
    findings: List[AuditFinding] = Field(default_factory=list)
    lead_score: Optional[LeadScore] = None
    existing_lead_services: List[LeadService] = Field(default_factory=list)
    available_services: List[Service] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)
