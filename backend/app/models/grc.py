"""
ORM models for Phase 47: Unified Compliance, Governance, Privacy, Risk & Regulatory Control Platform.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class GovernanceFrameworkModel(BaseModel):
    """Governance standards and regulatory frameworks (e.g. SOC2, ISO27001, NIST AI RMF, GDPR)."""

    __tablename__ = "governance_frameworks"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    framework_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # INFORMATION_SECURITY, PRIVACY, AI_GOVERNANCE, FINANCIAL_CONTROL, RELIABILITY
    jurisdiction: Mapped[str] = mapped_column(String(100), default="GLOBAL", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)  # DRAFT, ACTIVE, SUPERSEDED, RETIRED
    owner: Mapped[str] = mapped_column(String(100), default="compliance_officer", nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    effective_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class GovernanceRequirementModel(BaseModel):
    """Granular regulatory or framework requirement clause."""

    __tablename__ = "governance_requirements"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    framework_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    requirement_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IMPLEMENTED", nullable=False)  # IDENTIFIED, UNDER_REVIEW, APPLICABLE, NOT_APPLICABLE, IMPLEMENTED, PARTIALLY_IMPLEMENTED, NON_COMPLIANT
    interpretation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class GovernanceApplicabilityModel(BaseModel):
    """Documented applicability assessment for a specific requirement."""

    __tablename__ = "governance_applicability_assessments"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    requirement_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    decision: Mapped[str] = mapped_column(String(50), nullable=False)  # APPLICABLE, NOT_APPLICABLE, CONDITIONALLY_APPLICABLE, UNKNOWN
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    policy_version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    evidence_references: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class GovernanceControlModel(BaseModel):
    """Operational GRC control designed to satisfy requirements."""

    __tablename__ = "governance_controls"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # SECURITY, PRIVACY, DATA, AI, IDENTITY, FINANCE, RELIABILITY, OPERATIONS
    control_type: Mapped[str] = mapped_column(String(50), default="PREVENTIVE", nullable=False)  # PREVENTIVE, DETECTIVE, CORRECTIVE, COMPENSATING, DIRECTIVE
    frequency: Mapped[str] = mapped_column(String(50), default="CONTINUOUS", nullable=False)  # CONTINUOUS, DAILY, WEEKLY, MONTHLY, QUARTERLY, ANNUAL
    automation_level: Mapped[str] = mapped_column(String(50), default="AUTOMATED", nullable=False)  # MANUAL, SEMI_AUTOMATED, AUTOMATED, CONTINUOUSLY_MONITORED
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(100), default="system_automated", nullable=False)
    health_status: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, DEGRADED, FAILED, UNKNOWN
    test_method: Mapped[str] = mapped_column(String(100), default="AUTOMATED_PROBE", nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class GovernanceControlImplementationModel(BaseModel):
    """Explicit mapping from a control to actual codebase/platform subsystem components."""

    __tablename__ = "governance_control_implementations"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    component_type: Mapped[str] = mapped_column(String(100), nullable=False)  # API, SERVICE, POLICY, CONFIGURATION, FEATURE_FLAG, WORKFLOW, DATABASE_CONTROL, SECURITY_CONTROL, AI_GUARD
    component_reference: Mapped[str] = mapped_column(String(300), nullable=False)  # e.g., "backend/app/security/base.py", "AuthorizationEngine"
    verification_rule: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


class GovernanceEvidenceModel(BaseModel):
    """Cryptographically anchored evidence proving control implementation and operation."""

    __tablename__ = "governance_evidence"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # AUDIT_LOG, SECURITY_EVENT, CONFIGURATION, TEST_RESULT, ATTESTATION, AI_TRACE, BACKUP_VERIFICATION
    source_subsystem: Mapped[str] = mapped_column(String(100), nullable=False)  # Phase 35, Phase 46, Phase 44, Phase 43, Phase 33
    source_record_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    provenance_uri: Mapped[str] = mapped_column(String(300), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    data_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    freshness_status: Mapped[str] = mapped_column(String(50), default="FRESH", nullable=False)  # FRESH, AGING, STALE, MISSING


class GovernanceEvidenceLinkModel(BaseModel):
    """Association linking an evidence record to a control or requirement."""

    __tablename__ = "governance_evidence_links"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # CONTROL, REQUIREMENT, AUDIT_REQUEST, RISK
    target_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)


class GovernanceControlTestModel(BaseModel):
    """Defines automated or manual testing specifications for a control."""

    __tablename__ = "governance_control_tests"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    test_name: Mapped[str] = mapped_column(String(200), nullable=False)
    test_type: Mapped[str] = mapped_column(String(50), default="OPERATING_EFFECTIVENESS", nullable=False)  # DESIGN_EFFECTIVENESS, OPERATING_EFFECTIVENESS
    execution_frequency: Mapped[str] = mapped_column(String(50), default="DAILY", nullable=False)
    test_script_ref: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    is_automated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class GovernanceControlTestRunModel(BaseModel):
    """Execution run and result of a control test."""

    __tablename__ = "governance_control_test_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    test_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(50), nullable=False)  # PASS, PARTIAL, FAIL, NOT_TESTABLE, NOT_APPLICABLE
    details: Mapped[Text] = mapped_column(Text, nullable=False)
    executed_by: Mapped[str] = mapped_column(String(100), default="system_automated", nullable=False)
    evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )


class GovernanceRiskModel(BaseModel):
    """Enterprise GRC Risk Register entry."""

    __tablename__ = "governance_risks"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    risk_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # SECURITY, PRIVACY, AI, FINANCE, RELIABILITY, VENDOR, COMPLIANCE
    threat: Mapped[str] = mapped_column(Text, nullable=False)
    vulnerability: Mapped[str] = mapped_column(Text, nullable=False)
    likelihood: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)  # 0.0 - 1.0
    impact: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)  # 0.0 - 1.0
    inherent_risk_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    residual_risk_score: Mapped[float] = mapped_column(Float, default=30.0, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    treatment: Mapped[str] = mapped_column(String(50), default="MITIGATE", nullable=False)  # MITIGATE, TRANSFER, AVOID, ACCEPT, MONITOR
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)
    mitigating_controls: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    accepted_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class GovernanceExceptionModel(BaseModel):
    """Time-bound policy exception with compensating controls and approval audit trail."""

    __tablename__ = "governance_exceptions"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    exception_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    reason: Mapped[Text] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    compensating_controls: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    requester_id: Mapped[str] = mapped_column(String(100), nullable=False)
    approver_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="REQUESTED", nullable=False)  # REQUESTED, APPROVED, REJECTED, ACTIVE, EXPIRED
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class GovernanceFindingModel(BaseModel):
    """Audit or continuous monitoring deficiency finding."""

    __tablename__ = "governance_findings"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    finding_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)  # OPEN, ACKNOWLEDGED, IN_REMEDIATION, READY_FOR_VERIFICATION, VERIFIED, CLOSED, ACCEPTED_RISK
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class GovernanceRemediationPlanModel(BaseModel):
    """Structured remediation plan required to resolve a finding."""

    __tablename__ = "governance_remediation_plans"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    finding_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    plan_title: Mapped[str] = mapped_column(String(250), nullable=False)
    actions: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PLANNED", nullable=False)  # PLANNED, IN_PROGRESS, COMPLETED, VERIFIED
    verified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class GovernanceAuditModel(BaseModel):
    """Internal or external compliance audit campaign."""

    __tablename__ = "governance_audits"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    audit_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    framework_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    lead_auditor: Mapped[str] = mapped_column(String(100), nullable=False)
    audit_type: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)  # INTERNAL, EXTERNAL, REGULATORY
    status: Mapped[str] = mapped_column(String(50), default="PLANNING", nullable=False)  # PLANNING, SCOPING, IN_PROGRESS, REPORTING, CLOSED
    scope_controls: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class GovernanceAuditRequestModel(BaseModel):
    """Granular evidence or inquiry request within an audit."""

    __tablename__ = "governance_audit_requests"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    audit_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    request_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    control_code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    assigned_to: Mapped[str] = mapped_column(String(100), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)  # OPEN, SUBMITTED, ACCEPTED, REJECTED
    evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class GovernanceAttestationModel(BaseModel):
    """Formal compliance attestation statement with dual approval enforcement."""

    __tablename__ = "governance_attestations"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    attestation_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(250), nullable=False)
    statement: Mapped[Text] = mapped_column(Text, nullable=False)
    framework_code: Mapped[str] = mapped_column(String(100), nullable=False)
    preparer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    approver_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)  # DRAFT, REVIEW, APPROVED, ATTESTED, REJECTED
    attested_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class PrivacyProcessingActivityModel(BaseModel):
    """Record of Processing Activities (ROPA) under GDPR/privacy governance."""

    __tablename__ = "privacy_processing_activities"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    activity_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    purpose: Mapped[Text] = mapped_column(Text, nullable=False)
    data_categories: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    data_subject_categories: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    systems: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    retention_period_days: Mapped[int] = mapped_column(Integer, default=365, nullable=False)
    security_controls: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class PrivacyConsentModel(BaseModel):
    """Explicit subject consent record."""

    __tablename__ = "privacy_consent_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    subject_id: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    purpose: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="EMAIL", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="GRANTED", nullable=False)  # GRANTED, WITHDRAWN, EXPIRED
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class PrivacyRequestModel(BaseModel):
    """Data Subject Access Request (DSAR) lifecycle."""

    __tablename__ = "privacy_requests"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    request_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    subject_id: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    request_type: Mapped[str] = mapped_column(String(50), nullable=False)  # ACCESS, CORRECTION, DELETION, EXPORT, RESTRICTION, OBJECTION
    status: Mapped[str] = mapped_column(String(50), default="RECEIVED", nullable=False)  # RECEIVED, SCOPING, DATA_DISCOVERY, RESPONSE_PREPARATION, APPROVED, FULFILLED
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fulfilled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    assigned_to: Mapped[str] = mapped_column(String(100), default="dpo_lead", nullable=False)


class VendorProfileModel(BaseModel):
    """Third-party provider risk profile and dependency mapping."""

    __tablename__ = "vendor_profiles"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    vendor_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    service_provided: Mapped[str] = mapped_column(String(200), nullable=False)
    criticality: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    data_access_level: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)  # NONE, PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    security_risk: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    privacy_risk: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    dependent_services: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class VendorRiskAssessmentModel(BaseModel):
    """Periodic vendor compliance and security review."""

    __tablename__ = "vendor_risk_assessments"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    vendor_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    assessor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    findings: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(50), default="APPROVE", nullable=False)  # APPROVE, CONDITIONALLY_APPROVE, REJECT
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    next_review_due: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class GovernancePostureSnapshotModel(BaseModel):
    """Periodic snapshot of organizational GRC posture and compliance metrics."""

    __tablename__ = "governance_posture_snapshots"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    composite_compliance_score: Mapped[float] = mapped_column(Float, default=90.0, nullable=False)
    overall_health: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, AT_RISK, CRITICAL
    total_requirements: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    implemented_requirements: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_controls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    healthy_controls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failing_controls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    open_findings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    critical_findings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_exceptions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stale_evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    domain_scores: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    technical_debt_score: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
