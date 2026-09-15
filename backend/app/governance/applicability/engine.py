"""
Applicability Assessment Engine (Section 8).
Evaluates and documents regulatory applicability with immutable justification and reviewer accountability.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from backend.app.governance.base import ApplicabilityDecision


class ApplicabilityRecord(BaseModel):
    requirement_code: str
    decision: ApplicabilityDecision
    justification: str
    reviewer_id: str
    policy_version: str = "1.0"
    reviewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    evidence_references: List[str] = Field(default_factory=list)


class ApplicabilityEngine:
    """Manages applicability determinations for compliance requirements."""

    def __init__(self):
        self._assessments: Dict[str, ApplicabilityRecord] = {}

    def record_decision(
        self,
        requirement_code: str,
        decision: ApplicabilityDecision,
        justification: str,
        reviewer_id: str,
        evidence_references: Optional[List[str]] = None,
        policy_version: str = "1.0"
    ) -> ApplicabilityRecord:
        """Records a formal, binding applicability determination by an authorized human reviewer."""
        if not reviewer_id:
            raise ValueError("Applicability assessment requires an accountable human reviewer ID.")
        if not justification or len(justification.strip()) < 10:
            raise ValueError("Detailed justification (>10 characters) is required for compliance auditability.")

        record = ApplicabilityRecord(
            requirement_code=requirement_code,
            decision=decision,
            justification=justification,
            reviewer_id=reviewer_id,
            policy_version=policy_version,
            reviewed_at=datetime.now(timezone.utc),
            evidence_references=evidence_references or []
        )
        self._assessments[requirement_code] = record
        return record

    def get_decision(self, requirement_code: str) -> Optional[ApplicabilityRecord]:
        return self._assessments.get(requirement_code)

    def is_applicable(self, requirement_code: str) -> bool:
        rec = self.get_decision(requirement_code)
        if not rec:
            return True  # Default conservative stance: assumed applicable until documented otherwise
        return rec.decision in (ApplicabilityDecision.APPLICABLE, ApplicabilityDecision.CONDITIONALLY_APPLICABLE)
