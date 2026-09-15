"""
Core enums, data contracts, and safety constants for Phase 47 GRC Platform.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


# --- Enums ---

class FrameworkCategory(str, Enum):
    INFORMATION_SECURITY = "INFORMATION_SECURITY"
    PRIVACY = "PRIVACY"
    AI_GOVERNANCE = "AI_GOVERNANCE"
    FINANCIAL_CONTROL = "FINANCIAL_CONTROL"
    RELIABILITY = "RELIABILITY"
    DATA_GOVERNANCE = "DATA_GOVERNANCE"
    VENDOR_RISK = "VENDOR_RISK"


class RequirementStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    NON_COMPLIANT = "NON_COMPLIANT"
    SUPERSEDED = "SUPERSEDED"


class ApplicabilityDecision(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CONDITIONALLY_APPLICABLE = "CONDITIONALLY_APPLICABLE"
    UNKNOWN = "UNKNOWN"


class ControlDomain(str, Enum):
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    DATA = "DATA"
    AI = "AI"
    IDENTITY = "IDENTITY"
    ACCESS = "ACCESS"
    FINANCE = "FINANCE"
    COMMUNICATION = "COMMUNICATION"
    OPERATIONS = "OPERATIONS"
    RELIABILITY = "RELIABILITY"
    VENDOR = "VENDOR"
    GOVERNANCE = "GOVERNANCE"


class ControlType(str, Enum):
    PREVENTIVE = "PREVENTIVE"
    DETECTIVE = "DETECTIVE"
    CORRECTIVE = "CORRECTIVE"
    COMPENSATING = "COMPENSATING"
    DIRECTIVE = "DIRECTIVE"


class ControlFrequency(str, Enum):
    CONTINUOUS = "CONTINUOUS"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUAL = "ANNUAL"


class AutomationLevel(str, Enum):
    MANUAL = "MANUAL"
    SEMI_AUTOMATED = "SEMI_AUTOMATED"
    AUTOMATED = "AUTOMATED"
    CONTINUOUSLY_MONITORED = "CONTINUOUSLY_MONITORED"


class ControlHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class EvidenceType(str, Enum):
    CONFIGURATION = "CONFIGURATION"
    AUDIT_LOG = "AUDIT_LOG"
    SECURITY_EVENT = "SECURITY_EVENT"
    POLICY = "POLICY"
    APPROVAL = "APPROVAL"
    TEST_RESULT = "TEST_RESULT"
    AI_TRACE = "AI_TRACE"
    BACKUP_VERIFICATION = "BACKUP_VERIFICATION"
    ATTESTATION = "ATTESTATION"


class EvidenceFreshness(str, Enum):
    FRESH = "FRESH"
    AGING = "AGING"
    STALE = "STALE"
    MISSING = "MISSING"


class TestResult(str, Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"
    NOT_TESTABLE = "NOT_TESTABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


TestResult.__test__ = False


class TestType(str, Enum):
    DESIGN_EFFECTIVENESS = "DESIGN_EFFECTIVENESS"
    OPERATING_EFFECTIVENESS = "OPERATING_EFFECTIVENESS"


TestType.__test__ = False



class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskTreatmentType(str, Enum):
    MITIGATE = "MITIGATE"
    TRANSFER = "TRANSFER"
    AVOID = "AVOID"
    ACCEPT = "ACCEPT"
    MONITOR = "MONITOR"


class ExceptionStatus(str, Enum):
    REQUESTED = "REQUESTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class FindingSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_REMEDIATION = "IN_REMEDIATION"
    READY_FOR_VERIFICATION = "READY_FOR_VERIFICATION"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    ACCEPTED_RISK = "ACCEPTED_RISK"


class RemediationStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    VERIFIED = "VERIFIED"


class AuditStatus(str, Enum):
    PLANNING = "PLANNING"
    SCOPING = "SCOPING"
    IN_PROGRESS = "IN_PROGRESS"
    REPORTING = "REPORTING"
    CLOSED = "CLOSED"


class AuditRequestStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class AttestationStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    ATTESTED = "ATTESTED"
    REJECTED = "REJECTED"


class PrivacyRequestType(str, Enum):
    ACCESS = "ACCESS"
    CORRECTION = "CORRECTION"
    DELETION = "DELETION"
    EXPORT = "EXPORT"
    RESTRICTION = "RESTRICTION"
    OBJECTION = "OBJECTION"


class PrivacyRequestStatus(str, Enum):
    RECEIVED = "RECEIVED"
    SCOPING = "SCOPING"
    DATA_DISCOVERY = "DATA_DISCOVERY"
    RESPONSE_PREPARATION = "RESPONSE_PREPARATION"
    APPROVED = "APPROVED"
    FULFILLED = "FULFILLED"


class VendorCriticality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# --- Data Models ---

class GovernanceFramework(BaseModel):
    framework_code: str
    name: str
    version: str = "1.0"
    category: FrameworkCategory
    jurisdiction: str = "GLOBAL"
    description: str
    status: str = "ACTIVE"
    owner: str = "compliance_officer"
    source_url: Optional[str] = None
    effective_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GovernanceRequirement(BaseModel):
    requirement_code: str
    framework_code: str
    title: str
    description: str
    category: str
    priority: str = "HIGH"
    status: RequirementStatus = RequirementStatus.IMPLEMENTED
    interpretation_notes: Optional[str] = None
    version: str = "1.0"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GovernanceControl(BaseModel):
    control_code: str
    name: str
    objective: str
    domain: ControlDomain
    control_type: ControlType = ControlType.PREVENTIVE
    frequency: ControlFrequency = ControlFrequency.CONTINUOUS
    automation_level: AutomationLevel = AutomationLevel.AUTOMATED
    owner_id: str
    operator_id: str = "system_automated"
    health_status: ControlHealthStatus = ControlHealthStatus.HEALTHY
    test_method: str = "AUTOMATED_PROBE"
    version: str = "1.0"
    implementations: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GovernanceEvidence(BaseModel):
    evidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evidence_type: EvidenceType
    source_subsystem: str
    source_record_id: str
    sha256_hash: str
    provenance_uri: str
    summary: str
    data_payload: Dict[str, Any] = Field(default_factory=dict)
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None
    freshness_status: EvidenceFreshness = EvidenceFreshness.FRESH


class GovernanceRisk(BaseModel):
    risk_code: str
    title: str
    category: str
    threat: str
    vulnerability: str
    likelihood: float = 0.5
    impact: float = 0.5
    inherent_risk_score: float = 50.0
    residual_risk_score: float = 30.0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    treatment: RiskTreatmentType = RiskTreatmentType.MITIGATE
    owner_id: str
    status: str = "OPEN"
    mitigating_controls: List[str] = Field(default_factory=list)
    accepted_by: Optional[str] = None
    accepted_at: Optional[datetime] = None


class GovernanceException(BaseModel):
    exception_code: str
    title: str
    control_code: str
    reason: str
    risk_level: RiskLevel = RiskLevel.MEDIUM
    compensating_controls: List[str] = Field(default_factory=list)
    owner_id: str
    requester_id: str
    approver_id: Optional[str] = None
    status: ExceptionStatus = ExceptionStatus.REQUESTED
    expiration_date: datetime
    approved_at: Optional[datetime] = None


class GovernanceFinding(BaseModel):
    finding_code: str
    control_code: str
    title: str
    description: str
    severity: FindingSeverity = FindingSeverity.MEDIUM
    root_cause: Optional[str] = None
    owner_id: str
    status: FindingStatus = FindingStatus.OPEN
    due_date: datetime
    evidence_ids: List[str] = Field(default_factory=list)


class GovernanceAttestation(BaseModel):
    attestation_code: str
    scope: str
    statement: str
    framework_code: str
    preparer_id: str
    approver_id: Optional[str] = None
    status: AttestationStatus = AttestationStatus.DRAFT
    attested_at: Optional[datetime] = None
    evidence_ids: List[str] = Field(default_factory=list)
