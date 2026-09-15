"""
Remediation Governance Engine (Section 41 & Rule 20).
Enforces structured remediation plans and mandatory verification retests prior to closure.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.governance.base import (
    FindingStatus,
    RemediationStatus,
)
from backend.app.governance.findings.manager import FindingManager


class RemediationPlan(BaseModel):
    finding_code: str
    plan_title: str
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    owner_id: str
    status: RemediationStatus = RemediationStatus.PLANNED
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_evidence_id: Optional[str] = None


class RemediationEngine:
    """Oversees finding remediation workflows and validates verification criteria before finding closure."""

    def __init__(self, finding_manager: FindingManager):
        self.finding_manager = finding_manager
        self._plans: Dict[str, RemediationPlan] = {}

    def create_remediation_plan(
        self,
        finding_code: str,
        plan_title: str,
        actions: List[Dict[str, Any]],
        owner_id: str
    ) -> RemediationPlan:
        """Creates a structured corrective remediation plan for an open finding."""
        finding = self.finding_manager.get_finding(finding_code)
        if not finding:
            raise KeyError(f"Finding '{finding_code}' not found.")

        plan = RemediationPlan(
            finding_code=finding_code,
            plan_title=plan_title,
            actions=actions,
            owner_id=owner_id,
            status=RemediationStatus.PLANNED
        )
        self._plans[finding_code] = plan
        self.finding_manager.update_status(finding_code, FindingStatus.IN_REMEDIATION)
        return plan

    def mark_ready_for_verification(self, finding_code: str) -> RemediationPlan:
        plan = self._plans.get(finding_code)
        if not plan:
            raise KeyError(f"Remediation plan for finding '{finding_code}' not found.")
        plan.status = RemediationStatus.COMPLETED
        self.finding_manager.update_status(finding_code, FindingStatus.READY_FOR_VERIFICATION)
        return plan

    def verify_and_close_finding(
        self,
        finding_code: str,
        verifier_id: str,
        verification_evidence_id: str,
        retest_passed: bool
    ) -> RemediationPlan:
        """
        Rule 20: Remediation is not complete until verification succeeds.
        Requires independent verification retest before closing finding.
        """
        plan = self._plans.get(finding_code)
        if not plan:
            raise KeyError(f"Remediation plan for finding '{finding_code}' not found.")
        if not verifier_id:
            raise ValueError("Verification requires an accountable verifier ID.")
        if not verification_evidence_id:
            raise ValueError("Verification requires an authoritative verification evidence ID.")

        if not retest_passed:
            # Re-test failed: finding remains in remediation
            plan.status = RemediationStatus.IN_PROGRESS
            self.finding_manager.update_status(finding_code, FindingStatus.IN_REMEDIATION)
            raise ValueError("Verification retest failed: Finding cannot be closed until a passing retest is proven.")

        # Verification passed
        plan.status = RemediationStatus.VERIFIED
        plan.verified_by = verifier_id
        plan.verified_at = datetime.now(timezone.utc)
        plan.verification_evidence_id = verification_evidence_id

        self.finding_manager.update_status(finding_code, FindingStatus.VERIFIED)
        self.finding_manager.update_status(finding_code, FindingStatus.CLOSED)
        return plan

    def get_plan(self, finding_code: str) -> Optional[RemediationPlan]:
        return self._plans.get(finding_code)
