"""
Pydantic V2 schemas for Phase 47 GRC Platform API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FrameworkResponse(BaseModel):
    framework_code: str
    name: str
    version: str
    category: str
    jurisdiction: str
    description: str
    status: str
    owner: str


class RequirementResponse(BaseModel):
    requirement_code: str
    framework_code: str
    title: str
    description: str
    category: str
    priority: str
    status: str


class ApplicabilityRequest(BaseModel):
    requirement_code: str
    decision: str
    justification: str
    reviewer_id: str
    evidence_references: List[str] = Field(default_factory=list)


class ApplicabilityResponse(BaseModel):
    requirement_code: str
    decision: str
    justification: str
    reviewer_id: str
    reviewed_at: datetime


class ControlResponse(BaseModel):
    control_code: str
    name: str
    objective: str
    domain: str
    control_type: str
    frequency: str
    automation_level: str
    owner_id: str
    operator_id: str
    health_status: str
    implementations: List[str] = Field(default_factory=list)


class EvidenceIngestRequest(BaseModel):
    evidence_type: str
    source_subsystem: str
    source_record_id: str
    provenance_uri: str
    summary: str
    data_payload: Dict[str, Any] = Field(default_factory=dict)
    control_codes: List[str] = Field(default_factory=list)


class EvidenceResponse(BaseModel):
    evidence_id: str
    evidence_type: str
    source_subsystem: str
    source_record_id: str
    sha256_hash: str
    provenance_uri: str
    summary: str
    collected_at: datetime
    freshness_status: str


class ControlTestRequest(BaseModel):
    test_type: str
    result: str
    details: str
    executed_by: str
    evidence_ids: List[str] = Field(default_factory=list)


class ControlTestResponse(BaseModel):
    test_run_id: str
    control_code: str
    test_type: str
    result: str
    details: str
    executed_by: str
    executed_at: datetime


class RiskCreateRequest(BaseModel):
    risk_code: str
    title: str
    category: str
    threat: str
    vulnerability: str
    likelihood: float
    impact: float
    owner_id: str
    mitigating_controls: List[str] = Field(default_factory=list)


class RiskAcceptanceRequest(BaseModel):
    approver_id: str
    justification: str


class RiskResponse(BaseModel):
    risk_code: str
    title: str
    category: str
    likelihood: float
    impact: float
    inherent_risk_score: float
    residual_risk_score: float
    risk_level: str
    treatment: str
    owner_id: str
    status: str
    mitigating_controls: List[str]


class ExceptionCreateRequest(BaseModel):
    exception_code: str
    title: str
    control_code: str
    reason: str
    compensating_controls: List[str]
    owner_id: str
    requester_id: str
    expiration_date: datetime
    risk_level: str = "MEDIUM"


class ExceptionApprovalRequest(BaseModel):
    approver_id: str


class ExceptionResponse(BaseModel):
    exception_code: str
    title: str
    control_code: str
    reason: str
    compensating_controls: List[str]
    owner_id: str
    requester_id: str
    approver_id: Optional[str] = None
    status: str
    expiration_date: datetime


class FindingCreateRequest(BaseModel):
    finding_code: str
    control_code: str
    title: str
    description: str
    severity: str
    owner_id: str
    due_date: datetime
    root_cause: Optional[str] = None


class FindingResponse(BaseModel):
    finding_code: str
    control_code: str
    title: str
    description: str
    severity: str
    root_cause: Optional[str] = None
    owner_id: str
    status: str
    due_date: datetime


class RemediationPlanRequest(BaseModel):
    plan_title: str
    actions: List[Dict[str, Any]]
    owner_id: str


class RemediationVerifyRequest(BaseModel):
    verifier_id: str
    verification_evidence_id: str
    retest_passed: bool


class RemediationResponse(BaseModel):
    finding_code: str
    plan_title: str
    status: str
    owner_id: str
    verified_by: Optional[str] = None


class PrivacyRequestCreate(BaseModel):
    request_code: str
    subject_id: str
    request_type: str


class PrivacyRequestAdvance(BaseModel):
    next_status: str
    note: str
    has_legal_hold: bool = False


class PrivacyRequestResponse(BaseModel):
    request_code: str
    subject_id: str
    request_type: str
    status: str
    requested_at: datetime
    due_date: datetime
    assigned_to: str


class VendorResponse(BaseModel):
    vendor_code: str
    name: str
    service_provided: str
    criticality: str
    data_access_level: str
    security_risk: str
    privacy_risk: str
    owner_id: str
    status: str
    dependent_services: List[str]


class AttestationPrepareRequest(BaseModel):
    attestation_code: str
    scope: str
    statement: str
    framework_code: str
    preparer_id: str
    evidence_ids: List[str] = Field(default_factory=list)


class AttestationApproveRequest(BaseModel):
    approver_id: str


class AttestationResponse(BaseModel):
    attestation_code: str
    scope: str
    statement: str
    framework_code: str
    preparer_id: str
    approver_id: Optional[str] = None
    status: str
    attested_at: Optional[datetime] = None


class PostureSnapshotResponse(BaseModel):
    composite_compliance_score: float
    overall_health: str
    total_requirements: int
    implemented_requirements: int
    total_controls: int
    healthy_controls: int
    failing_controls: int
    open_findings_count: int
    critical_findings_count: int
    active_exceptions_count: int
    stale_evidence_count: int
    domain_scores: Dict[str, float]
    technical_debt_score: float
    captured_at: datetime


class ExecutiveSummaryResponse(BaseModel):
    governance_health: str
    composite_compliance_score: float
    critical_blockers: int
    governance_debt_score: float
    active_exceptions: int
    advisory_recommendation: str
    generated_at: str
