"""Pydantic API schemas for Lead Qualifications."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QualificationResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    business_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    agent_run_id: Optional[uuid.UUID] = None
    decision: str
    confidence: str
    summary: Optional[str] = None
    factors: List[Dict[str, Any]] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    outreach_readiness: str
    recommended_internal_action: Optional[str] = None
    qualification_version: str
    is_stale: bool
    human_override_decision: Optional[str] = None
    human_override_reason: Optional[str] = None
    overridden_by_user_id: Optional[uuid.UUID] = None
    overridden_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QualificationOverrideRequest(BaseModel):
    decision: str  # QUALIFIED, POTENTIALLY_QUALIFIED, NEEDS_REVIEW, NOT_QUALIFIED, INSUFFICIENT_DATA
    reason: str


class QualificationHistoryResponse(BaseModel):
    lead_id: uuid.UUID
    total_qualifications: int
    latest_qualification: Optional[QualificationResponse] = None
    qualifications: List[QualificationResponse] = Field(default_factory=list)
