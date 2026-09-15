"""
Phase 73: Autonomous Legal, Compliance, Governance, Regulatory Intelligence,
Contract Intelligence & Enterprise Trust Operating System Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Executive Trust Command Center Summary & 11-Stage Loop
class TrustControlCenterSummaryResponse(BaseModel):
    trust_score_composite: float
    legal_health_pct: float
    compliance_posture_pct: float
    privacy_health_pct: float
    ai_governance_score_pct: float
    contract_risk_index_pct: float
    third_party_risk_pct: float
    audit_readiness_pct: float
    active_legal_entities_count: int
    monitored_regulations_count: int
    open_regulatory_changes_count: int
    active_contracts_count: int
    open_high_risk_clauses_count: int
    pending_obligations_count: int
    active_legal_holds_count: int
    pending_dsar_requests_count: int
    active_ai_systems_count: int
    open_investigations_count: int
    active_trust_agents_count: int


class TrustOperatingCycleExecutionResponse(BaseModel):
    cycle_run_id: str
    stage_progress: Dict[str, str]
    overall_status: str
    regulations_analyzed: int
    contracts_reviewed: int
    controls_tested: int
    actions_requiring_human_approval: int
    evidence_hashes_recorded: int


# 2. Multi-Dimensional Trust Score
class TrustScoreResponse(BaseModel):
    overall_score: float
    legal_health: float
    compliance_health: float
    privacy_health: float
    security_governance: float
    ai_governance: float
    contract_health: float
    third_party_risk: float
    audit_readiness: float
    control_health: float
    status: str
    calculated_at: datetime


# 3. Legal Entities & Jurisdictions
class TrustLegalEntityCreate(BaseModel):
    entity_code: str
    legal_name: str
    jurisdiction_code: str
    entity_type: str = "SUBSIDIARY"
    registration_number: Optional[str] = None
    parent_entity_id: Optional[str] = None


class TrustLegalEntityResponse(BaseModel):
    id: str
    entity_code: str
    legal_name: str
    jurisdiction_code: str
    entity_type: str
    status: str
    registration_number: Optional[str] = None
    created_at: datetime


# 4. Regulatory Intelligence & Changes
class TrustRegulationResponse(BaseModel):
    id: str
    regulation_code: str
    title: str
    issuing_authority: str
    jurisdiction_code: str
    category: str
    effective_date: Optional[datetime] = None
    status: str


class TrustRegulatoryChangeResponse(BaseModel):
    id: str
    change_reference: str
    regulation_id: str
    change_type: str
    impact_level: str
    summary: str
    affected_departments: List[str]
    affected_policies: List[str]
    affected_controls: List[str]
    status: str


# 5. Compliance Frameworks, Requirements & Controls
class TrustRequirementResponse(BaseModel):
    id: str
    requirement_code: str
    framework_code: str
    title: str
    description: str
    jurisdiction_code: str
    compliance_status: str
    owner_role: str


class TrustControlResponse(BaseModel):
    id: str
    control_code: str
    name: str
    control_type: str
    automation_level: str
    enforcement_system: str
    effectiveness_status: str
    mapped_requirements: List[str]


class TrustControlTestResponse(BaseModel):
    id: str
    control_id: str
    test_type: str
    sample_size: int
    exceptions_count: int
    test_result: str
    evaluated_by: str
    tested_at: datetime


# 6. Contract Lifecycle Management & Clause Intelligence
class TrustContractCreate(BaseModel):
    contract_number: str
    title: str
    contract_type: str = "MSA"
    counterparty_name: str
    total_value_usd: float = 0.0
    governing_law_jurisdiction: str = "US_DELAWARE"
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class TrustContractResponse(BaseModel):
    id: str
    contract_number: str
    title: str
    contract_type: str
    counterparty_name: str
    total_value_usd: float
    governing_law_jurisdiction: str
    lifecycle_status: str
    risk_score: float
    created_at: datetime


class TrustClauseRiskResponse(BaseModel):
    contract_id: str
    clause_category: str
    risk_level: str
    is_standard_template: bool
    ai_risk_findings: List[str]
    recommendations: List[str]
    requires_human_approval: bool


# 7. Obligations, Deadlines & Legal Holds
class TrustObligationResponse(BaseModel):
    id: str
    obligation_code: str
    source_type: str
    title: str
    responsible_party: str
    due_date: Optional[datetime] = None
    frequency: str
    compliance_status: str


class TrustDeadlineResponse(BaseModel):
    id: str
    deadline_code: str
    category: str
    title: str
    target_date: datetime
    assigned_owner: str
    is_critical: bool
    status: str


class TrustLegalHoldResponse(BaseModel):
    id: str
    hold_code: str
    matter_name: str
    custodians: List[str]
    affected_systems: List[str]
    hold_status: str
    issued_by: str
    effective_date: datetime


# 8. Policy Management & Exceptions
class TrustPolicyResponse(BaseModel):
    id: str
    policy_code: str
    name: str
    category: str
    version: str
    lifecycle_status: str
    owner: str
    effective_date: datetime


class TrustPolicyExceptionCreate(BaseModel):
    policy_id: str
    justification: str
    compensating_controls: List[str]
    risk_level: str = "MEDIUM"
    expiration_date: datetime


class TrustPolicyExceptionResponse(BaseModel):
    id: str
    exception_code: str
    policy_id: str
    justification: str
    risk_level: str
    approved_by: Optional[str] = None
    status: str
    expiration_date: datetime


# 9. Privacy OS, Data Inventory & DSAR
class TrustDataAssetResponse(BaseModel):
    id: str
    asset_name: str
    classification: str
    data_categories: List[str]
    storage_system: str
    retention_period_days: int
    legal_basis: str
    is_subject_to_legal_hold: bool


class TrustDsarCreate(BaseModel):
    subject_identifier: str
    request_type: str = "ACCESS"
    jurisdiction: str = "GDPR"
    sla_deadline: datetime


class TrustDsarResponse(BaseModel):
    id: str
    request_code: str
    subject_identifier: str
    request_type: str
    jurisdiction: str
    identity_verified: bool
    sla_deadline: datetime
    status: str


# 10. AI Governance & Incident Management
class TrustAISystemResponse(BaseModel):
    id: str
    system_code: str
    name: str
    model_provider: str
    risk_classification: str
    human_in_the_loop_required: bool
    bias_audit_status: str
    status: str


class TrustAIEvaluationResponse(BaseModel):
    id: str
    ai_system_id: str
    evaluation_type: str
    score: float
    audited_by: str
    created_at: datetime


class TrustAIIncidentResponse(BaseModel):
    id: str
    incident_code: str
    ai_system_id: str
    incident_type: str
    severity: str
    resolution_status: str


# 11. Third-Party Risk Management (TPRM)
class TrustThirdPartyResponse(BaseModel):
    id: str
    party_code: str
    name: str
    party_type: str
    inherent_risk_rating: str
    sanctions_screening_status: str
    soc2_verified: bool
    annual_spend_usd: float
    lifecycle_status: str


class TrustDueDiligenceResponse(BaseModel):
    third_party_id: str
    risk_score: float
    screening_passed: bool
    findings: List[str]
    recommended_approval: bool


# 12. Legal Matters, Litigation & Legal Spend
class TrustLegalMatterResponse(BaseModel):
    id: str
    matter_code: str
    title: str
    matter_type: str
    lead_counsel: str
    estimated_exposure_usd: float
    budget_usd: float
    status: str


class TrustLegalSpendResponse(BaseModel):
    id: str
    matter_id: str
    law_firm_name: str
    invoice_number: str
    amount_usd: float
    approval_status: str


# 13. Investigations, Evidence & Audits
class TrustInvestigationResponse(BaseModel):
    id: str
    case_number: str
    allegation_category: str
    is_confidential: bool
    assigned_investigator: str
    status: str


class TrustEvidenceChainResponse(BaseModel):
    id: str
    investigation_id: str
    evidence_name: str
    sha256_hash: str
    storage_vault: str
    is_tamper_evident: bool


class TrustAuditResponse(BaseModel):
    id: str
    audit_code: str
    title: str
    framework_code: str
    auditor_firm: str
    status: str


class TrustFindingResponse(BaseModel):
    id: str
    audit_id: str
    finding_code: str
    severity: str
    title: str
    remediation_owner: str
    status: str


# 14. Licenses, Insurance & Governance Bodies
class TrustLicenseResponse(BaseModel):
    id: str
    license_code: str
    name: str
    issuing_authority: str
    renewal_date: datetime
    status: str


class TrustInsuranceResponse(BaseModel):
    id: str
    policy_number: str
    insurance_type: str
    coverage_limit_usd: float
    carrier_name: str
    expiry_date: datetime


class TrustDecisionResponse(BaseModel):
    id: str
    decision_code: str
    body_name: str
    resolution_text: str
    votes_in_favor: int
    decision_date: datetime
