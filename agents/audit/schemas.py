"""Pydantic schemas for Phase 16 Audit Agent requests, findings, metrics, and results."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AuditTargetPolicy(BaseModel):
    prefer_official_website: bool = True
    max_pages: int = 10
    max_age_days: int = 7


class AuditAgentRequest(BaseModel):
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    target_url: Optional[str] = None
    sections: List[str] = Field(
        default_factory=lambda: [
            "website_health",
            "seo",
            "mobile",
            "lead_capture",
            "content_information",
            "digital_presence",
        ]
    )
    target_policy: AuditTargetPolicy = Field(default_factory=AuditTargetPolicy)


class AuditEvidenceItem(BaseModel):
    source_url: Optional[str] = None
    source_type: str = "WEBSITE"
    observed_at: str
    confidence: str = "HIGH"
    details: Optional[str] = None


class AuditFindingItem(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"find-{uuid.uuid4().hex[:8]}")
    category: str  # website_health, seo, mobile, lead_capture, business_consistency, security
    title: str
    description: str
    severity: str = "INFO"  # INFO, LOW, MEDIUM, HIGH
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW
    evidence: List[AuditEvidenceItem] = Field(default_factory=list)
    affected_area: Optional[str] = None
    limitations: List[str] = Field(default_factory=list)


class AuditMetricItem(BaseModel):
    name: str
    value: Any
    unit: Optional[str] = None
    observed_at: str


class AuditAgentResult(BaseModel):
    audit_status: str  # COMPLETED, PARTIAL, FAILED, NO_WEBSITE
    target_url: Optional[str] = None
    overall_health: str = "LIMITED_DATA"  # HEALTHY, FAIR, NEEDS_ATTENTION, LIMITED_DATA
    findings: List[AuditFindingItem] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    evidence: List[AuditEvidenceItem] = Field(default_factory=list)
    conflicts: List[Dict[str, Any]] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
