"""
Phase 73: Autonomous Legal, Compliance, Governance, Regulatory Intelligence,
Contract Intelligence & Enterprise Trust Operating System Models.
Prefix: trust_*
Classes: Trust*Model & Trust* aliases
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Index
)
from app.models.base import Base


class TrustLegalEntityModel(Base):
    __tablename__ = "trust_legal_entities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    entity_code = Column(String(50), nullable=False, unique=True, index=True)
    legal_name = Column(String(255), nullable=False)
    jurisdiction_code = Column(String(50), nullable=False)
    registration_number = Column(String(100), nullable=True)
    entity_type = Column(String(50), default="SUBSIDIARY")  # PARENT, SUBSIDIARY, JOINT_VENTURE, BRANCH
    status = Column(String(50), default="ACTIVE")
    parent_entity_id = Column(String(36), nullable=True)
    registered_address = Column(Text, nullable=True)
    directors = Column(JSON, default=list)
    officers = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrustJurisdictionModel(Base):
    __tablename__ = "trust_jurisdictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    jurisdiction_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    country_iso = Column(String(10), nullable=False)
    region_or_state = Column(String(100), nullable=True)
    primary_regulator = Column(String(100), nullable=True)
    applicable_privacy_law = Column(String(100), nullable=True)  # GDPR, CCPA, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustRegulationModel(Base):
    __tablename__ = "trust_regulations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    regulation_code = Column(String(50), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    issuing_authority = Column(String(150), nullable=False)
    jurisdiction_code = Column(String(50), nullable=False)
    category = Column(String(50), default="DATA_PRIVACY")  # PRIVACY, CYBERSECURITY, FINANCIAL, AI, COMMERCE
    effective_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="ACTIVE")
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustRegulatoryChangeModel(Base):
    __tablename__ = "trust_regulatory_changes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    change_reference = Column(String(50), nullable=False, unique=True)
    regulation_id = Column(String(36), nullable=False)
    change_type = Column(String(50), default="AMENDMENT")  # NEW_LAW, AMENDMENT, GUIDANCE, ENFORCEMENT
    impact_level = Column(String(20), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    summary = Column(Text, nullable=False)
    affected_departments = Column(JSON, default=list)
    affected_policies = Column(JSON, default=list)
    affected_controls = Column(JSON, default=list)
    required_action_items = Column(JSON, default=list)
    status = Column(String(50), default="UNDER_REVIEW")
    effective_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustRequirementModel(Base):
    __tablename__ = "trust_requirements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    requirement_code = Column(String(50), nullable=False, unique=True)
    framework_code = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    jurisdiction_code = Column(String(50), default="GLOBAL")
    compliance_status = Column(String(50), default="COMPLIANT")  # COMPLIANT, PARTIAL, NON_COMPLIANT, NEEDS_REVIEW
    owner_role = Column(String(100), default="Chief Compliance Officer")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustFrameworkModel(Base):
    __tablename__ = "trust_frameworks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    framework_code = Column(String(50), nullable=False, unique=True)  # ISO_27001, SOC_2, NIST_CSF, GDPR, HIPAA, EU_AI_ACT
    name = Column(String(150), nullable=False)
    version = Column(String(50), default="2026")
    applicability_status = Column(String(50), default="MANDATORY")
    readiness_percentage = Column(Float, default=95.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustControlModel(Base):
    __tablename__ = "trust_controls"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    control_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    control_type = Column(String(50), default="PREVENTIVE")  # PREVENTIVE, DETECTIVE, CORRECTIVE
    automation_level = Column(String(50), default="AUTOMATED")  # AUTOMATED, HYBRID, MANUAL
    enforcement_system = Column(String(100), default="Security Engine")
    testing_frequency = Column(String(50), default="CONTINUOUS")
    effectiveness_status = Column(String(50), default="EFFECTIVE")  # EFFECTIVE, DEFICIENT, FAILED
    mapped_requirements = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustControlTestModel(Base):
    __tablename__ = "trust_control_tests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    control_id = Column(String(36), nullable=False)
    test_type = Column(String(50), default="OPERATING_EFFECTIVENESS")  # DESIGN, OPERATING
    sample_size = Column(Integer, default=50)
    exceptions_count = Column(Integer, default=0)
    test_result = Column(String(50), default="PASS")  # PASS, FAIL, QUALIFIED
    evaluated_by = Column(String(100), default="Autonomous Audit Agent")
    tested_at = Column(DateTime, default=datetime.utcnow)


class TrustControlFailureModel(Base):
    __tablename__ = "trust_control_failures"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    control_id = Column(String(36), nullable=False)
    failure_code = Column(String(50), nullable=False, unique=True)
    severity = Column(String(20), default="HIGH")
    root_cause = Column(Text, nullable=True)
    remediation_plan = Column(Text, nullable=True)
    owner = Column(String(100), nullable=True)
    status = Column(String(50), default="OPEN")  # OPEN, REMEDIATING, VALIDATED, CLOSED
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustContractModel(Base):
    __tablename__ = "trust_contracts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    contract_number = Column(String(50), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    contract_type = Column(String(50), default="MSA")  # MSA, DPA, SLA, VENDOR_AGREEMENT, NDA
    counterparty_name = Column(String(255), nullable=False)
    total_value_usd = Column(Float, default=0.0)
    effective_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    renewal_type = Column(String(50), default="EXPLICIT")  # AUTO_RENEWAL, EXPLICIT, PERPETUAL
    notice_period_days = Column(Integer, default=30)
    governing_law_jurisdiction = Column(String(50), default="US_DELAWARE")
    lifecycle_status = Column(String(50), default="ACTIVE")  # DRAFT, NEGOTIATING, PENDING_SIGNATURE, ACTIVE, EXPIRED, TERMINATED
    risk_score = Column(Float, default=0.1)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustContractVersionModel(Base):
    __tablename__ = "trust_contract_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    contract_id = Column(String(36), nullable=False)
    version_number = Column(Integer, default=1)
    change_summary = Column(Text, nullable=True)
    redline_diff = Column(JSON, default=dict)
    author = Column(String(100), default="Legal Counsel")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustContractClauseModel(Base):
    __tablename__ = "trust_contract_clauses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    contract_id = Column(String(36), nullable=False)
    clause_category = Column(String(50), default="LIMITATION_OF_LIABILITY")  # INDEMNITY, IP, DATA_PROTECTION, TERMINATION
    clause_text = Column(Text, nullable=False)
    is_standard_template = Column(Boolean, default=True)
    risk_level = Column(String(20), default="LOW")  # CRITICAL, HIGH, MEDIUM, LOW
    ai_risk_findings = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustObligationModel(Base):
    __tablename__ = "trust_obligations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    obligation_code = Column(String(50), nullable=False, unique=True)
    source_type = Column(String(50), default="CONTRACT")  # CONTRACT, REGULATION, POLICY
    source_id = Column(String(36), nullable=True)
    title = Column(String(255), nullable=False)
    responsible_party = Column(String(100), default="Internal")
    due_date = Column(DateTime, nullable=True)
    frequency = Column(String(50), default="ANNUAL")  # ONE_TIME, MONTHLY, QUARTERLY, ANNUAL
    compliance_status = Column(String(50), default="FULFILLED")  # PENDING, FULFILLED, OVERDUE
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustDeadlineModel(Base):
    __tablename__ = "trust_deadlines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    deadline_code = Column(String(50), nullable=False, unique=True)
    category = Column(String(50), default="REGULATORY_FILING")  # COURT, CONTRACT_RENEWAL, AUDIT, CERTIFICATION
    title = Column(String(255), nullable=False)
    target_date = Column(DateTime, nullable=False)
    assigned_owner = Column(String(100), default="Legal Operations")
    is_critical = Column(Boolean, default=True)
    status = Column(String(50), default="SCHEDULED")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustLegalHoldModel(Base):
    __tablename__ = "trust_legal_holds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    hold_code = Column(String(50), nullable=False, unique=True)
    matter_name = Column(String(255), nullable=False)
    custodians = Column(JSON, default=list)
    affected_systems = Column(JSON, default=list)
    hold_status = Column(String(50), default="ACTIVE")  # ACTIVE, RELEASED
    issued_by = Column(String(100), default="General Counsel")
    effective_date = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)


class TrustPolicyModel(Base):
    __tablename__ = "trust_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    policy_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), default="SECURITY")  # PRIVACY, ETHICS, ACCEPTABLE_USE, AI_GOVERNANCE
    version = Column(String(20), default="1.0")
    lifecycle_status = Column(String(50), default="PUBLISHED")  # DRAFT, REVIEW, PUBLISHED, RETIRED
    acknowledgement_count = Column(Integer, default=0)
    owner = Column(String(100), default="Chief Compliance Officer")
    effective_date = Column(DateTime, default=datetime.utcnow)
    next_review_date = Column(DateTime, nullable=True)


class TrustPolicyExceptionModel(Base):
    __tablename__ = "trust_policy_exceptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    exception_code = Column(String(50), nullable=False, unique=True)
    policy_id = Column(String(36), nullable=False)
    justification = Column(Text, nullable=False)
    compensating_controls = Column(JSON, default=list)
    risk_level = Column(String(20), default="MEDIUM")
    approved_by = Column(String(100), nullable=True)
    expiration_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="APPROVED")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustDataAssetModel(Base):
    __tablename__ = "trust_data_assets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    asset_name = Column(String(255), nullable=False)
    classification = Column(String(50), default="CONFIDENTIAL")  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    data_categories = Column(JSON, default=list)  # PII, FINANCIAL, TELEMETRY, HEALTH
    storage_system = Column(String(100), default="PostgreSQL Production")
    retention_period_days = Column(Integer, default=365)
    legal_basis = Column(String(50), default="CONTRACTUAL_NECESSITY")  # CONSENT, LEGAL_OBLIGATION, LEGITIMATE_INTEREST
    is_subject_to_legal_hold = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustDataSubjectRequestModel(Base):
    __tablename__ = "trust_data_subject_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    request_code = Column(String(50), nullable=False, unique=True)
    subject_identifier = Column(String(100), nullable=False)
    request_type = Column(String(50), default="ACCESS")  # ACCESS, DELETION, CORRECTION, PORTABILITY
    jurisdiction = Column(String(50), default="GDPR")
    identity_verified = Column(Boolean, default=True)
    sla_deadline = Column(DateTime, nullable=False)
    status = Column(String(50), default="IN_PROGRESS")  # RECEIVED, VERIFIED, IN_PROGRESS, AWAITING_APPROVAL, COMPLETED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustAISystemModel(Base):
    __tablename__ = "trust_ai_systems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    system_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    model_provider = Column(String(100), default="Google DeepMind")
    purpose = Column(Text, nullable=False)
    risk_classification = Column(String(50), default="MEDIUM")  # UNACCEPTABLE, HIGH, MEDIUM, LOW (EU AI Act)
    human_in_the_loop_required = Column(Boolean, default=True)
    bias_audit_status = Column(String(50), default="PASSED")
    status = Column(String(50), default="APPROVED_FOR_PRODUCTION")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustAIEvaluationModel(Base):
    __tablename__ = "trust_ai_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    ai_system_id = Column(String(36), nullable=False)
    evaluation_type = Column(String(50), default="HALLUCINATION_AND_FACTUALITY")  # BIAS, SAFETY, ROBUSTNESS, FACTUALITY
    score = Column(Float, default=0.98)
    evaluation_notes = Column(Text, nullable=True)
    audited_by = Column(String(100), default="AI Governance Agent")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustAIIncidentModel(Base):
    __tablename__ = "trust_ai_incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    incident_code = Column(String(50), nullable=False, unique=True)
    ai_system_id = Column(String(36), nullable=False)
    incident_type = Column(String(50), default="HALLUCINATION")  # HALLUCINATION, DRIFT, DATA_LEAK, UNAUTHORIZED_PROMPT
    severity = Column(String(20), default="MEDIUM")
    resolution_status = Column(String(50), default="RESOLVED")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustThirdPartyModel(Base):
    __tablename__ = "trust_third_parties"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    party_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    party_type = Column(String(50), default="CRITICAL_VENDOR")  # VENDOR, PARTNER, PROCESSOR, SUPPLIER
    inherent_risk_rating = Column(String(20), default="MEDIUM")
    sanctions_screening_status = Column(String(50), default="CLEARED")
    soc2_verified = Column(Boolean, default=True)
    annual_spend_usd = Column(Float, default=0.0)
    lifecycle_status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustThirdPartyRiskModel(Base):
    __tablename__ = "trust_third_party_risks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    third_party_id = Column(String(36), nullable=False)
    risk_category = Column(String(50), default="CYBERSECURITY")
    risk_score = Column(Float, default=0.15)
    mitigation_controls = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustLegalMatterModel(Base):
    __tablename__ = "trust_legal_matters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    matter_code = Column(String(50), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    matter_type = Column(String(50), default="COMMERCIAL_CONTRACT")  # LITIGATION, IP_FILING, REGULATORY, ADVISORY
    lead_counsel = Column(String(100), default="Chief Legal Officer")
    estimated_exposure_usd = Column(Float, default=0.0)
    budget_usd = Column(Float, default=50000.0)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustLegalSpendModel(Base):
    __tablename__ = "trust_legal_spend"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    matter_id = Column(String(36), nullable=False)
    law_firm_name = Column(String(200), nullable=False)
    invoice_number = Column(String(100), nullable=False)
    amount_usd = Column(Float, default=0.0)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    approval_status = Column(String(50), default="APPROVED")


class TrustInvestigationModel(Base):
    __tablename__ = "trust_investigations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    case_number = Column(String(50), nullable=False, unique=True)
    allegation_category = Column(String(50), default="CONFLICT_OF_INTEREST")  # WHISTLEBLOWER, FRAUD, HARASSMENT, BRIBERY
    is_confidential = Column(Boolean, default=True)
    assigned_investigator = Column(String(100), default="Director of Ethics")
    status = Column(String(50), default="UNDER_INVESTIGATION")
    findings_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustChainOfCustodyModel(Base):
    __tablename__ = "trust_chain_of_custody"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    investigation_id = Column(String(36), nullable=False)
    evidence_name = Column(String(255), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    collected_by = Column(String(100), default="Digital Forensic Lead")
    storage_vault = Column(String(100), default="Encrypted Vault S3")
    custody_transfers = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustAuditModel(Base):
    __tablename__ = "trust_audits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    audit_code = Column(String(50), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    framework_code = Column(String(50), default="SOC_2_TYPE_II")
    auditor_firm = Column(String(150), default="External Big 4 Auditor")
    status = Column(String(50), default="IN_PROGRESS")  # PLANNING, FIELDWORK, REPORTING, CLOSED
    start_date = Column(DateTime, default=datetime.utcnow)
    target_completion_date = Column(DateTime, nullable=True)


class TrustFindingModel(Base):
    __tablename__ = "trust_findings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    audit_id = Column(String(36), nullable=False)
    finding_code = Column(String(50), nullable=False, unique=True)
    severity = Column(String(20), default="LOW")  # CRITICAL, HIGH, MEDIUM, LOW
    title = Column(String(255), nullable=False)
    remediation_owner = Column(String(100), default="VP Security")
    target_remediation_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="REMEDIATED")  # OPEN, IN_PROGRESS, REMEDIATED, VALIDATED
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustLicenseModel(Base):
    __tablename__ = "trust_licenses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    license_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    issuing_authority = Column(String(150), nullable=False)
    renewal_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustInsuranceModel(Base):
    __tablename__ = "trust_insurance"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    policy_number = Column(String(100), nullable=False, unique=True)
    insurance_type = Column(String(50), default="CYBER_LIABILITY")  # D_AND_O, GENERAL_COMMERCIAL, CYBER, E_AND_O
    coverage_limit_usd = Column(Float, default=10000000.0)
    carrier_name = Column(String(150), default="Lloyds of London")
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustDecisionModel(Base):
    __tablename__ = "trust_decisions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    decision_code = Column(String(50), nullable=False, unique=True)
    body_name = Column(String(100), default="Audit & AI Ethics Committee")
    resolution_text = Column(Text, nullable=False)
    votes_in_favor = Column(Integer, default=5)
    votes_against = Column(Integer, default=0)
    decision_date = Column(DateTime, default=datetime.utcnow)


class TrustConflictModel(Base):
    __tablename__ = "trust_conflicts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    person_name = Column(String(150), nullable=False)
    entity_name = Column(String(200), nullable=False)
    nature_of_interest = Column(Text, nullable=False)
    disposition = Column(String(50), default="RECUSED_FROM_VOTES")
    reported_date = Column(DateTime, default=datetime.utcnow)


class TrustAgentRunModel(Base):
    __tablename__ = "trust_agent_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    agent_id = Column(String(50), nullable=False)
    action_type = Column(String(100), nullable=False)
    evidence_hash = Column(String(64), nullable=True)
    status = Column(String(50), default="COMPLETED")
    metadata_payload = Column(JSON, default=dict)
    executed_at = Column(DateTime, default=datetime.utcnow)


# Aliases for clean importing
TrustLegalEntity = TrustLegalEntityModel
TrustJurisdiction = TrustJurisdictionModel
TrustRegulation = TrustRegulationModel
TrustRegulatoryChange = TrustRegulatoryChangeModel
TrustRequirement = TrustRequirementModel
TrustFramework = TrustFrameworkModel
TrustControl = TrustControlModel
TrustControlTest = TrustControlTestModel
TrustControlFailure = TrustControlFailureModel
TrustContract = TrustContractModel
TrustContractVersion = TrustContractVersionModel
TrustContractClause = TrustContractClauseModel
TrustObligation = TrustObligationModel
TrustDeadline = TrustDeadlineModel
TrustLegalHold = TrustLegalHoldModel
TrustPolicy = TrustPolicyModel
TrustPolicyException = TrustPolicyExceptionModel
TrustDataAsset = TrustDataAssetModel
TrustDataSubjectRequest = TrustDataSubjectRequestModel
TrustAISystem = TrustAISystemModel
TrustAIEvaluation = TrustAIEvaluationModel
TrustAIIncident = TrustAIIncidentModel
TrustThirdParty = TrustThirdPartyModel
TrustThirdPartyRisk = TrustThirdPartyRiskModel
TrustLegalMatter = TrustLegalMatterModel
TrustLegalSpend = TrustLegalSpendModel
TrustInvestigation = TrustInvestigationModel
TrustChainOfCustody = TrustChainOfCustodyModel
TrustAudit = TrustAuditModel
TrustFinding = TrustFindingModel
TrustLicense = TrustLicenseModel
TrustInsurance = TrustInsuranceModel
TrustDecision = TrustDecisionModel
TrustConflict = TrustConflictModel
TrustAgentRun = TrustAgentRunModel
