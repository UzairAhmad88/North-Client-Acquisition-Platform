"""
Privacy Governance, ROPA, Consent & Data Subject Requests Engine (Section 24-29).
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.governance.base import (
    PrivacyRequestStatus,
    PrivacyRequestType,
)


class ProcessingActivity(BaseModel):
    activity_code: str
    name: str
    purpose: str
    data_categories: List[str] = Field(default_factory=list)
    data_subject_categories: List[str] = Field(default_factory=list)
    systems: List[str] = Field(default_factory=list)
    retention_period_days: int = 365
    security_controls: List[str] = Field(default_factory=list)
    owner_id: str
    status: str = "ACTIVE"


class PrivacyConsent(BaseModel):
    subject_id: str
    purpose: str
    channel: str = "EMAIL"
    status: str = "GRANTED"  # GRANTED, WITHDRAWN, EXPIRED
    granted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    withdrawn_at: Optional[datetime] = None


class PrivacyRequest(BaseModel):
    request_code: str
    subject_id: str
    request_type: PrivacyRequestType
    status: PrivacyRequestStatus = PrivacyRequestStatus.RECEIVED
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: datetime
    assigned_to: str = "dpo_lead"
    fulfilled_at: Optional[datetime] = None
    audit_notes: List[str] = Field(default_factory=list)


class PrivacyEngine:
    """Manages privacy compliance, ROPA processing inventory, consent tracking, and DSAR lifecycle."""

    def __init__(self):
        self._activities: Dict[str, ProcessingActivity] = {}
        self._consents: Dict[str, PrivacyConsent] = {}  # key = f"{subject_id}:{purpose}"
        self._requests: Dict[str, PrivacyRequest] = {}
        self._seed_default_activities()

    def _seed_default_activities(self) -> None:
        """Seeds canonical platform data processing activities."""
        self.register_processing_activity(ProcessingActivity(
            activity_code="PA_LEAD_ACQUISITION",
            name="Lead Research & Business Intelligence Gathering",
            purpose="B2B sales prospecting, market research, and business opportunity analysis.",
            data_categories=["BUSINESS_CONTACT", "PUBLIC_PROFILE", "CORPORATE_DOMAIN"],
            data_subject_categories=["BUSINESS_PROSPECTS", "ENTERPRISE_CLIENTS"],
            systems=["CRM", "ResearchEngine", "EmailGateway"],
            retention_period_days=730,
            security_controls=["CTL_SEC_TENANT_ISOLATION", "CTL_SEC_SECRET_SCRUBBING"],
            owner_id="dpo_lead"
        ))

        self.register_processing_activity(ProcessingActivity(
            activity_code="PA_AI_ENGAGEMENT",
            name="AI-Assisted Personalization & Communication Drafting",
            purpose="Drafting tailored proposals and communication messages under human review.",
            data_categories=["PROJECT_REQUIREMENTS", "BUSINESS_CONTEXT"],
            data_subject_categories=["CLIENT_CONTACTS"],
            systems=["AIGovernanceRuntime", "PersonalizationEngine"],
            retention_period_days=365,
            security_controls=["CTL_AI_HUMAN_APPROVAL", "CTL_SEC_TENANT_ISOLATION"],
            owner_id="ai_governance_lead"
        ))

    def register_processing_activity(self, activity: ProcessingActivity) -> None:
        self._activities[activity.activity_code] = activity

    def get_processing_activity(self, activity_code: str) -> Optional[ProcessingActivity]:
        return self._activities.get(activity_code)

    def list_processing_activities(self) -> List[ProcessingActivity]:
        return list(self._activities.values())

    # --- Consent Management ---

    def record_consent(self, subject_id: str, purpose: str, channel: str = "EMAIL") -> PrivacyConsent:
        """Records explicit positive consent. Consent must never be inferred from silence."""
        consent = PrivacyConsent(
            subject_id=subject_id,
            purpose=purpose,
            channel=channel,
            status="GRANTED",
            granted_at=datetime.now(timezone.utc)
        )
        self._consents[f"{subject_id}:{purpose}"] = consent
        return consent

    def withdraw_consent(self, subject_id: str, purpose: str) -> Optional[PrivacyConsent]:
        key = f"{subject_id}:{purpose}"
        consent = self._consents.get(key)
        if consent:
            consent.status = "WITHDRAWN"
            consent.withdrawn_at = datetime.now(timezone.utc)
        return consent

    def has_active_consent(self, subject_id: str, purpose: str) -> bool:
        consent = self._consents.get(f"{subject_id}:{purpose}")
        return bool(consent and consent.status == "GRANTED")

    # --- Data Subject Requests (DSAR) ---

    def create_privacy_request(
        self,
        request_code: str,
        subject_id: str,
        request_type: PrivacyRequestType,
        assigned_to: str = "dpo_lead"
    ) -> PrivacyRequest:
        """Initiates a Data Subject Access Request with statutory 30-day fulfillment SLA."""
        now = datetime.now(timezone.utc)
        req = PrivacyRequest(
            request_code=request_code,
            subject_id=subject_id,
            request_type=request_type,
            status=PrivacyRequestStatus.RECEIVED,
            requested_at=now,
            due_date=now + timedelta(days=30),
            assigned_to=assigned_to
        )
        self._requests[request_code] = req
        return req

    def advance_request_status(
        self,
        request_code: str,
        next_status: PrivacyRequestStatus,
        note: str,
        has_legal_hold: bool = False
    ) -> PrivacyRequest:
        """Transitions request through fulfillment lifecycle."""
        req = self._requests.get(request_code)
        if not req:
            raise KeyError(f"Privacy request '{request_code}' not found.")

        # Section 27: Legal hold integration blocks deletion
        if req.request_type == PrivacyRequestType.DELETION and has_legal_hold:
            raise PermissionError("Legal hold active: Erasure of personal data is legally prohibited while under active hold.")

        req.status = next_status
        req.audit_notes.append(f"[{datetime.now(timezone.utc).isoformat()}] Status changed to {next_status.value}: {note}")
        if next_status == PrivacyRequestStatus.FULFILLED:
            req.fulfilled_at = datetime.now(timezone.utc)
        return req

    def get_request(self, request_code: str) -> Optional[PrivacyRequest]:
        return self._requests.get(request_code)

    def list_requests(self, status: Optional[PrivacyRequestStatus] = None) -> List[PrivacyRequest]:
        reqs = list(self._requests.values())
        if status:
            reqs = [r for r in reqs if r.status == status]
        return reqs
