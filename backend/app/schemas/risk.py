"""Pydantic schemas for Risk & Quality API endpoints."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskCheckRequest(BaseModel):
    artifact_id: str
    artifact_type: str = "OUTREACH"


class RiskOverrideRequest(BaseModel):
    decision: str = Field(description="Decision: ACCEPTED, REJECTED")
    reason: str = Field(min_length=3, description="Reason for override")


class RiskFindingSchema(BaseModel):
    id: uuid.UUID
    rule_id: str
    category: str
    severity: str
    message: str
    evidence_reference: Optional[str] = None
    remediation: Optional[str] = None

    class Config:
        from_attributes = True


class QualityCheckSchema(BaseModel):
    id: uuid.UUID
    check_type: str
    status: str
    score: float
    details: Dict[str, Any]

    class Config:
        from_attributes = True


class RiskAssessmentResponse(BaseModel):
    id: uuid.UUID
    artifact_id: str
    artifact_type: str
    business_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None
    decision: str
    risk_level: str
    quality_score: float
    evidence_coverage: float
    confidence: str
    engine_version: str
    policy_version: str
    content_hash: str
    artifact_version: int
    is_stale: bool
    status: str
    human_override_decision: Optional[str] = None
    human_override_reason: Optional[str] = None
    human_override_by_id: Optional[uuid.UUID] = None
    human_override_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    findings: List[RiskFindingSchema] = []
    quality_checks: List[QualityCheckSchema] = []

    class Config:
        from_attributes = True
