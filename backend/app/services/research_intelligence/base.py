"""
Base domain types and schemas for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ResearchStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    RESEARCHING = "RESEARCHING"
    VALIDATING = "VALIDATING"
    SYNTHESIZING = "SYNTHESIZING"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    MONITORING = "MONITORING"
    ARCHIVED = "ARCHIVED"


class ResearchType(str, Enum):
    MARKET = "MARKET"
    COMPETITIVE = "COMPETITIVE"
    TECHNOLOGY = "TECHNOLOGY"
    PRODUCT = "PRODUCT"
    CUSTOMER = "CUSTOMER"
    INDUSTRY = "INDUSTRY"
    BUSINESS = "BUSINESS"
    AI = "AI"
    SECURITY = "SECURITY"
    REGULATORY = "REGULATORY"
    VENDOR = "VENDOR"
    TREND = "TREND"
    STRATEGIC = "STRATEGIC"


class SourceTrustLevel(str, Enum):
    PRIMARY = "PRIMARY"
    OFFICIAL = "OFFICIAL"
    GOVERNMENT = "GOVERNMENT"
    ACADEMIC = "ACADEMIC"
    PROFESSIONAL = "PROFESSIONAL"
    SECONDARY = "SECONDARY"
    COMMUNITY = "COMMUNITY"
    UNKNOWN = "UNKNOWN"


class FactStatus(str, Enum):
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    CORROBORATED = "CORROBORATED"
    CONFLICTED = "CONFLICTED"
    OUTDATED = "OUTDATED"
    REJECTED = "REJECTED"


class ClaimVerificationStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    CONFLICTED = "CONFLICTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class IntelligenceEventType(str, Enum):
    NEW = "NEW"
    CHANGED = "CHANGED"
    REMOVED = "REMOVED"
    EMERGING = "EMERGING"
    DECLINING = "DECLINING"
    CONFLICT = "CONFLICT"
    RISK = "RISK"
    OPPORTUNITY = "OPPORTUNITY"


class SignificanceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ResearchSource(BaseModel):
    id: str
    workspace_id: str
    url_or_reference: str
    source_type: SourceTrustLevel = SourceTrustLevel.SECONDARY
    publisher: Optional[str] = None
    author: Optional[str] = None
    authority_score: float = Field(default=0.7, ge=0.0, le=1.0)
    reliability: str = "MEDIUM_TRUST"
    freshness: str = "CURRENT"
    content_hash: Optional[str] = None
    status: str = "VALIDATED"


class ResearchFact(BaseModel):
    id: str
    workspace_id: str
    source_id: Optional[str] = None
    claim: str
    value_extracted: Optional[str] = None
    fact_status: FactStatus = FactStatus.VERIFIED
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    provenance: Optional[str] = None
    observed_date: Optional[str] = None


class ResearchClaim(BaseModel):
    id: str
    workspace_id: str
    claim_text: str
    verification_status: ClaimVerificationStatus = ClaimVerificationStatus.SUPPORTED
    independent_sources_count: int = 1
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)


class ResearchConflict(BaseModel):
    id: str
    workspace_id: str
    topic: str
    source_a_id: str
    claim_a: str
    source_b_id: str
    claim_b: str
    possible_explanation: Optional[str] = None
    resolution_status: str = "SURFACED"


class IntelligenceEvent(BaseModel):
    id: str
    event_type: IntelligenceEventType
    target_entity: str
    summary: str
    significance: SignificanceLevel = SignificanceLevel.MEDIUM
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence_payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
