"""Domain models and Pydantic schemas for the Risk & Quality Engine."""

import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskArtifact(BaseModel):
    """Generic artifact abstraction passed into the Risk & Quality Engine for evaluation."""

    artifact_id: str
    artifact_type: str = Field(
        default="OUTREACH",
        description="Type of artifact: OUTREACH, RESPONSE, PROPOSAL, FOLLOW_UP, NOTE, AI_DRAFT, DOCUMENT",
    )
    tenant_id: str = "default"
    business_id: Optional[str] = None
    lead_id: Optional[str] = None
    recipient_id: Optional[str] = None
    channel: Optional[str] = Field(default="EMAIL", description="Channel: EMAIL, WHATSAPP, SMS, LINKEDIN")
    content: str
    subject: Optional[str] = None
    claims: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    content_hash: Optional[str] = None

    def get_content_hash(self) -> str:
        """Calculate SHA-256 content hash if not explicitly provided."""
        if self.content_hash:
            return self.content_hash
        raw = f"sub:{self.subject or ''}|body:{self.content}|recip:{self.metadata.get('recipient_email', '')}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class RiskFindingDetail(BaseModel):
    """Specific risk finding or issue detected during evaluation."""

    rule_id: str
    category: str = Field(
        description="Category: CLAIM_ACCURACY, EVIDENCE, PRIVACY, PII, RECIPIENT, CHANNEL, CONTENT, DECEPTION, SPAM, POLICY, DNC, DUPLICATE, FREQUENCY, APPROVAL, VERSION, HASH, PROMPT_INJECTION, DATA_QUALITY"
    )
    severity: str = Field(description="Severity: INFO, LOW, MEDIUM, HIGH, CRITICAL")
    message: str
    evidence_reference: Optional[str] = None
    remediation: Optional[str] = None


class QualityCheckDetail(BaseModel):
    """Quality check metric evaluation."""

    check_type: str
    status: str = Field(description="Status: PASS, WARNING, FAIL")
    score: float = Field(default=100.0, ge=0.0, le=100.0)
    details: Dict[str, Any] = Field(default_factory=dict)


class RiskAssessmentResult(BaseModel):
    """Structured result produced by RiskEngine.assess()."""

    assessment_id: Optional[str] = None
    artifact_id: str
    artifact_type: str
    decision: str = Field(description="Decision: PASS, REVIEW, BLOCK")
    risk_level: str = Field(description="Risk Level: LOW, MEDIUM, HIGH, BLOCKED")
    quality_score: float = Field(default=100.0, ge=0.0, le=100.0)
    confidence: str = Field(default="HIGH", description="Confidence: HIGH, MEDIUM, LOW")
    evidence_coverage: float = Field(default=1.0, ge=0.0, le=1.0)
    engine_version: str = "1.0.0"
    policy_version: str = "v1"
    content_hash: str
    artifact_version: int = 1
    findings: List[RiskFindingDetail] = Field(default_factory=list)
    quality_checks: List[QualityCheckDetail] = Field(default_factory=list)
    is_stale: bool = False
    status: str = "COMPLETED"
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
