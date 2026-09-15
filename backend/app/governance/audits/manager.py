"""
Audit Management & Formal Attestation Engine (Section 38-42).
Enforces structured audit lifecycles, evidence packages, and dual-approved attestations.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.governance.base import (
    AttestationStatus,
    AuditRequestStatus,
    AuditStatus,
    GovernanceAttestation,
)


class AuditCampaign(BaseModel):
    audit_code: str
    title: str
    framework_code: str
    lead_auditor: str
    audit_type: str = "INTERNAL"
    status: AuditStatus = AuditStatus.PLANNING
    scope_controls: List[str] = Field(default_factory=list)
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: Optional[datetime] = None


class AuditRequest(BaseModel):
    request_code: str
    audit_code: str
    control_code: str
    description: str
    assigned_to: str
    due_date: datetime
    status: AuditRequestStatus = AuditRequestStatus.OPEN
    evidence_ids: List[str] = Field(default_factory=list)


class AuditManager:
    """Oversees internal/external compliance audits, request fulfillment, and formal attestations."""

    def __init__(self):
        self._audits: Dict[str, AuditCampaign] = {}
        self._requests: Dict[str, AuditRequest] = {}
        self._attestations: Dict[str, GovernanceAttestation] = {}

    def create_audit(
        self,
        audit_code: str,
        title: str,
        framework_code: str,
        lead_auditor: str,
        scope_controls: List[str],
        audit_type: str = "INTERNAL"
    ) -> AuditCampaign:
        """Initializes a new audit campaign."""
        if not lead_auditor:
            raise ValueError("Audit campaign requires an appointed lead auditor.")

        audit = AuditCampaign(
            audit_code=audit_code,
            title=title,
            framework_code=framework_code,
            lead_auditor=lead_auditor,
            scope_controls=scope_controls,
            audit_type=audit_type,
            status=AuditStatus.PLANNING
        )
        self._audits[audit_code] = audit
        return audit

    def create_audit_request(
        self,
        request_code: str,
        audit_code: str,
        control_code: str,
        description: str,
        assigned_to: str,
        due_date: datetime
    ) -> AuditRequest:
        """Creates an evidence request assigned to an operator during an audit."""
        req = AuditRequest(
            request_code=request_code,
            audit_code=audit_code,
            control_code=control_code,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            status=AuditRequestStatus.OPEN
        )
        self._requests[request_code] = req
        return req

    def submit_request_evidence(self, request_code: str, evidence_ids: List[str]) -> AuditRequest:
        req = self._requests.get(request_code)
        if not req:
            raise KeyError(f"Audit request '{request_code}' not found.")
        req.evidence_ids.extend(evidence_ids)
        req.status = AuditRequestStatus.SUBMITTED
        return req

    def prepare_attestation(
        self,
        attestation_code: str,
        scope: str,
        statement: str,
        framework_code: str,
        preparer_id: str,
        evidence_ids: List[str],
        is_ai_agent: bool = False
    ) -> GovernanceAttestation:
        """Drafts a formal compliance attestation. AI is prohibited from drafting or signing legally binding attestations."""
        if is_ai_agent:
            raise PermissionError("Safety violation: AI agents are strictly prohibited from generating formal attestations.")
        if not preparer_id:
            raise ValueError("Preparer ID is required.")

        att = GovernanceAttestation(
            attestation_code=attestation_code,
            scope=scope,
            statement=statement,
            framework_code=framework_code,
            preparer_id=preparer_id,
            evidence_ids=evidence_ids,
            status=AttestationStatus.DRAFT
        )
        self._attestations[attestation_code] = att
        return att

    def approve_attestation(
        self,
        attestation_code: str,
        approver_id: str,
        is_ai_agent: bool = False
    ) -> GovernanceAttestation:
        """Formally certifies an attestation. Enforces strict Separation of Duties (Preparer != Approver)."""
        if is_ai_agent:
            raise PermissionError("Safety violation: AI agents are strictly prohibited from certifying compliance attestations.")
        if not approver_id:
            raise ValueError("Approver ID is required.")

        att = self._attestations.get(attestation_code)
        if not att:
            raise KeyError(f"Attestation '{attestation_code}' not found.")

        # Separation of Duties: Preparer cannot self-approve attestation
        if att.preparer_id == approver_id:
            raise PermissionError("Separation of duties violation: Attestation preparer cannot be the approving certifier.")

        att.approver_id = approver_id
        att.attested_at = datetime.now(timezone.utc)
        att.status = AttestationStatus.ATTESTED
        return att

    def get_attestation(self, attestation_code: str) -> Optional[GovernanceAttestation]:
        return self._attestations.get(attestation_code)
