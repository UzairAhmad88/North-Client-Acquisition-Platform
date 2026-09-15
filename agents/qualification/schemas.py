"""Pydantic schemas for Phase 17 Qualification Agent requests, factors, evidence, and results."""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QualificationFactorItem(BaseModel):
    name: str  # SERVICE_FIT, BUSINESS_NEED, DIGITAL_GAP, AUTOMATION_OPPORTUNITY, BUSINESS_ACTIVITY, CONTACTABILITY, DATA_QUALITY, TIMING_SIGNAL, RISK
    status: str  # STRONG, MODERATE, WEAK, UNKNOWN, NOT_APPLICABLE
    assessment: str
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW
    evidence: List[Dict[str, Any]] = Field(default_factory=list)


class QualificationEvidenceItem(BaseModel):
    source: str  # RESEARCH, AUDIT, SCORE, RECOMMENDATION, CRM
    source_id: Optional[str] = None
    finding_id: Optional[str] = None
    confidence: str = "HIGH"
    details: str


class QualificationAgentResult(BaseModel):
    decision: str  # QUALIFIED, POTENTIALLY_QUALIFIED, NEEDS_REVIEW, NOT_QUALIFIED, INSUFFICIENT_DATA
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW
    summary: str
    factors: List[QualificationFactorItem] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    evidence: List[QualificationEvidenceItem] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    outreach_readiness: str = "NOT_READY"  # OUTREACH_READY, NEEDS_VERIFICATION, NOT_READY, OUTREACH_BLOCKED
    recommended_internal_action: str = "REVIEW_LEAD"  # RESEARCH_MORE, VERIFY_CONTACT, REVIEW_LEAD, PREPARE_OUTREACH, HOLD, ARCHIVE, MERGE_DUPLICATE
    qualification_version: str = "1.0"


class HumanOverrideInput(BaseModel):
    decision: str  # QUALIFIED, POTENTIALLY_QUALIFIED, NEEDS_REVIEW, NOT_QUALIFIED, INSUFFICIENT_DATA
    reason: str
