import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import pytest
import asyncio
from datetime import datetime, timedelta, timezone
import uuid

from app.governance.base import (
    FrameworkCategory,
    RequirementStatus,
    ApplicabilityDecision,
    ControlDomain,
    ControlType,
    ControlFrequency,
    AutomationLevel,
    ControlHealthStatus,
    EvidenceType,
    EvidenceFreshness,
    TestType,
    TestResult,
    RiskLevel,
    RiskTreatmentType,
    ExceptionStatus,
    FindingSeverity,
    FindingStatus,
    RemediationStatus,
    AuditStatus,
    AttestationStatus,
    PrivacyRequestType,
    PrivacyRequestStatus,
    VendorCriticality,
    GovernanceFramework,
    GovernanceRequirement,
    GovernanceControl,
    GovernanceEvidence,
    GovernanceRisk,
    GovernanceException,
    GovernanceFinding,
)
from app.governance.frameworks.registry import FrameworkRegistry
from app.governance.applicability.engine import ApplicabilityEngine
from app.governance.controls.catalog import ControlCatalog
from app.governance.evidence.integrity import EvidenceIntegrityManager
from app.governance.evidence.collector import EvidenceCollector
from app.governance.testing.engine import ControlTestingEngine
from app.governance.monitoring.continuous import ContinuousControlMonitor
from app.governance.risk.register import RiskRegister
from app.governance.exceptions.manager import ExceptionManager
from app.governance.findings.manager import FindingManager
from app.governance.remediation.engine import RemediationEngine
from app.governance.privacy.engine import PrivacyEngine
from app.governance.vendors.risk import VendorRiskManager
from app.governance.audits.manager import AuditManager
from app.governance.posture.engine import GovernancePostureEngine
from app.governance.service import GovernancePlatformService

from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS, validate_agent_permissions
from agents.core.errors import AgentPermissionDeniedError
from agents.governance.assessment_agent import GovernanceAssessmentAgent
from agents.governance.audit_assistant_agent import AuditAssistantAgent
from agents.governance.privacy_agent import PrivacyGovernanceAgent


# =========================================================================
# 1. Governance Framework Registry Tests
# =========================================================================

def test_framework_registry_seeded_frameworks():
    registry = FrameworkRegistry()
    frameworks = registry.list_frameworks()
    assert len(frameworks) >= 4

    codes = [f.framework_code for f in frameworks]
    assert "SOC2_TYPE_II" in codes
    assert "ISO_27001_2022" in codes
    assert "NIST_AI_RMF_1.0" in codes
    assert "GDPR" in codes

    soc2 = registry.get_framework("SOC2_TYPE_II")
    assert soc2 is not None
    assert soc2.category == FrameworkCategory.INFORMATION_SECURITY


def test_framework_registry_requirements():
    registry = FrameworkRegistry()
    reqs = registry.get_requirements("SOC2_TYPE_II")
    assert len(reqs) >= 4
    req_codes = [r.requirement_code for r in reqs]
    assert "SOC2_CC6.1" in req_codes
    assert "SOC2_CC6.3" in req_codes
    assert "SOC2_CC6.8" in req_codes
    assert "SOC2_A1.2" in req_codes


# =========================================================================
# 2. Applicability Assessment Engine Tests
# =========================================================================

def test_applicability_assessment_recording():
    engine = ApplicabilityEngine()
    assessment = engine.record_decision(
        requirement_code="SOC2_CC6.1",
        decision=ApplicabilityDecision.APPLICABLE,
        justification="Core platform handles multi-tenant customer authentication.",
        reviewer_id="compliance-officer-1",
    )
    assert assessment.requirement_code == "SOC2_CC6.1"
    assert assessment.decision == ApplicabilityDecision.APPLICABLE
    assert assessment.reviewer_id == "compliance-officer-1"

    retrieved = engine.get_decision("SOC2_CC6.1")
    assert retrieved is not None
    assert "multi-tenant" in retrieved.justification


def test_applicability_assessment_missing_justification_error():
    engine = ApplicabilityEngine()
    with pytest.raises(ValueError, match="Detailed justification"):
        engine.record_decision(
            requirement_code="SOC2_CC6.1",
            decision=ApplicabilityDecision.NOT_APPLICABLE,
            justification="",  # Empty justification prohibited
            reviewer_id="compliance-officer-1",
        )


# =========================================================================
# 3. Control Catalog & Implementation Mappings Tests
# =========================================================================

def test_control_catalog_and_implementations():
    catalog = ControlCatalog()
    controls = catalog.list_controls()
    assert len(controls) >= 6

    ctrl_codes = [c.control_code for c in controls]
    assert "CTL_SEC_MFA" in ctrl_codes
    assert "CTL_SEC_TENANT_ISOLATION" in ctrl_codes
    assert "CTL_SEC_SECRET_SCRUBBING" in ctrl_codes
    assert "CTL_AI_HUMAN_APPROVAL" in ctrl_codes
    assert "CTL_OPS_CONFIG_IMMUTABILITY" in ctrl_codes
    assert "CTL_REL_BACKUP_INTEGRITY" in ctrl_codes

    mfa = catalog.get_control("CTL_SEC_MFA")
    assert mfa.domain == ControlDomain.IDENTITY
    assert mfa.control_type == ControlType.PREVENTIVE
    assert mfa.automation_level == AutomationLevel.CONTINUOUSLY_MONITORED
    assert len(mfa.implementations) >= 1
    assert "MFAService" in mfa.implementations[0]


# =========================================================================
# 4. Cryptographic Evidence Integrity & Freshness Tests
# =========================================================================

def test_evidence_integrity_hashing():
    raw_payload = {"user_id": "usr-123", "mfa_verified": True, "auth_timestamp": "2026-09-09T12:00:00Z"}
    evidence_hash = EvidenceIntegrityManager.calculate_evidence_hash(
        source_subsystem="Phase 35 Identity Platform",
        source_record_id="auth-log-9876",
        data_payload=raw_payload,
    )
    assert evidence_hash is not None
    assert len(evidence_hash) == 64

    # Verify authentic payload
    assert EvidenceIntegrityManager.verify_evidence_hash(
        evidence_hash, "Phase 35 Identity Platform", "auth-log-9876", raw_payload
    ) is True

    # Tampered payload must fail
    tampered = {"user_id": "usr-123", "mfa_verified": False, "auth_timestamp": "2026-09-09T12:00:00Z"}
    assert EvidenceIntegrityManager.verify_evidence_hash(
        evidence_hash, "Phase 35 Identity Platform", "auth-log-9876", tampered
    ) is False


def test_evidence_freshness_evaluation():
    collector = EvidenceCollector()
    ev = collector.ingest_evidence(
        evidence_type=EvidenceType.AUDIT_LOG,
        source_subsystem="Phase 35 Identity Platform",
        source_record_id="auth-log-01",
        provenance_uri="audit://identity/logs/auth-log-01",
        summary="MFA login success audit trace",
        data_payload={"user_id": "usr-1", "mfa": True},
        validity_days=90,
    )
    assert ev.freshness_status == EvidenceFreshness.FRESH
    assert ev.sha256_hash is not None

    audit_res = collector.audit_evidence_freshness()
    assert audit_res["total_evidence_items"] >= 1
    assert audit_res["fresh_count"] >= 1


# =========================================================================
# 5. Control Testing Engine Tests (Design vs Operating Effectiveness)
# =========================================================================

def test_control_testing_design_vs_operating():
    engine = ControlTestingEngine()

    design_run = engine.execute_test(
        control_code="CTL_SEC_MFA",
        test_type="DESIGN_EFFECTIVENESS",
        result=TestResult.PASS,
        details="MFA policy configuration inspected and verified per specification.",
        evidence_ids=["ev-design-01"],
        executed_by="auditor-jane",
    )
    assert design_run.test_type == "DESIGN_EFFECTIVENESS"
    assert design_run.result == TestResult.PASS

    operating_run = engine.execute_test(
        control_code="CTL_SEC_MFA",
        test_type="OPERATING_EFFECTIVENESS",
        result=TestResult.PASS,
        details="Sample of 500 authentication events showed zero unauthenticated bypasses.",
        evidence_ids=["ev-op-01"],
        executed_by="auditor-jane",
    )
    assert operating_run.test_type == "OPERATING_EFFECTIVENESS"
    assert operating_run.result == TestResult.PASS


# =========================================================================
# 6. Continuous Control Monitoring Tests
# =========================================================================

def test_continuous_control_monitoring():
    catalog = ControlCatalog()
    monitor = ContinuousControlMonitor(catalog)
    health_results = monitor.run_continuous_health_check()
    assert health_results["total_monitored"] >= 6
    assert health_results["healthy"] >= 6

    health_map = health_results["control_health_map"]
    assert health_map["CTL_SEC_MFA"] == "HEALTHY"
    assert health_map["CTL_SEC_TENANT_ISOLATION"] == "HEALTHY"


# =========================================================================
# 7. Risk Register & Non-Negotiable Human Acceptance Guard Tests
# =========================================================================

def test_risk_scoring_and_human_acceptance_guard():
    register = RiskRegister()
    new_risk = GovernanceRisk(
        risk_code="RSK_INFRA_UNENCRYPTED_BACKUP",
        title="Unencrypted S3 Backup Export Exposure",
        category="INFRASTRUCTURE",
        threat="Unauthorized access to unencrypted cloud backups",
        vulnerability="Public bucket exposure without KMS key enforcement",
        likelihood=0.7,
        impact=0.9,
        inherent_risk_score=63.0,
        residual_risk_score=20.0,
        risk_level=RiskLevel.HIGH,
        treatment=RiskTreatmentType.MITIGATE,
        owner_id="ciso-officer",
        mitigating_controls=["CTL_REL_BACKUP_INTEGRITY"],
    )
    register.register_risk(new_risk)

    # Missing approver ID must raise ValueError
    with pytest.raises(ValueError, match="Risk acceptance requires an authorized human approver ID"):
        register.accept_risk(new_risk.risk_code, approver_id="", justification="Compensating KMS encryption active.")

    # Short justification must raise ValueError
    with pytest.raises(ValueError, match="Detailed business justification"):
        register.accept_risk(new_risk.risk_code, approver_id="ciso-officer", justification="looks ok")

    # AI is strictly prohibited from accepting risk (Rule 5)
    with pytest.raises(PermissionError, match="AI agents are strictly prohibited from accepting organizational risk"):
        register.accept_risk(
            new_risk.risk_code,
            approver_id="ai_copilot_bot",
            justification="Compensating KMS envelope encryption applied.",
            is_ai_agent=True,
        )

    # Valid human acceptance
    accepted = register.accept_risk(
        new_risk.risk_code,
        approver_id="ciso-officer",
        justification="Compensating KMS envelope encryption is active with dedicated audit logging.",
        is_ai_agent=False,
    )
    assert accepted.treatment == RiskTreatmentType.ACCEPT
    assert accepted.status == "ACCEPTED"


# =========================================================================
# 8. Time-Bound Exceptions & Separation of Duties Tests
# =========================================================================

def test_exception_mandatory_expiry_and_dual_approval():
    mgr = ExceptionManager()

    # Missing compensating controls must fail
    with pytest.raises(ValueError, match="must specify at least one verified compensating control"):
        mgr.request_exception(
            exception_code="EXC-001",
            title="Legacy ERP Connection without MFA",
            control_code="CTL_SEC_MFA",
            reason="Legacy protocol limitation",
            compensating_controls=[],  # Missing compensating controls
            owner_id="erp-eng-1",
            requester_id="erp-eng-1",
            expiration_date=datetime.now(timezone.utc) + timedelta(days=60),
        )

    # Valid request
    exc = mgr.request_exception(
        exception_code="EXC-001",
        title="Legacy ERP Connection without MFA",
        control_code="CTL_SEC_MFA",
        reason="Legacy protocol limitation",
        compensating_controls=["IP Whitelisting", "Dedicated VPN Gateway", "15-minute Session TTL"],
        owner_id="erp-eng-1",
        requester_id="erp-eng-1",
        expiration_date=datetime.now(timezone.utc) + timedelta(days=60),
    )
    assert exc.status == ExceptionStatus.REQUESTED

    # AI cannot approve exceptions
    with pytest.raises(PermissionError, match="AI agents cannot approve compliance or security exceptions"):
        mgr.approve_exception("EXC-001", approver_id="ai_bot", is_ai_agent=True)

    # Separation of duties: Requester cannot approve own exception
    with pytest.raises(PermissionError, match="Separation of duties violation"):
        mgr.approve_exception("EXC-001", approver_id="erp-eng-1")

    # Authorized independent approver
    approved = mgr.approve_exception("EXC-001", approver_id="security-director-9")
    assert approved.status == ExceptionStatus.ACTIVE
    assert approved.approver_id == "security-director-9"


# =========================================================================
# 9. Deficiencies, Findings & Non-Negotiable Rule 20 Retest Enforcement
# =========================================================================

def test_findings_and_rule_20_verification_enforcement():
    finding_mgr = FindingManager()
    finding = finding_mgr.raise_finding(
        finding_code="FND-TENANT-001",
        control_code="CTL_SEC_TENANT_ISOLATION",
        title="Tenant Isolation Bypass on Experimental Endpoint",
        description="Filter param optional on experimental search route.",
        severity=FindingSeverity.CRITICAL,
        root_cause="Missing default tenant constraint in search query builder.",
        owner_id="backend-team-lead",
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
    )
    assert finding.severity == FindingSeverity.CRITICAL
    assert finding.status == FindingStatus.OPEN

    remediation_engine = RemediationEngine(finding_mgr)
    plan = remediation_engine.create_remediation_plan(
        finding_code="FND-TENANT-001",
        plan_title="Patch Tenant Filter & Add Regression Tests",
        actions=[
            {"action_title": "Enforce mandatory tenant_id in search query", "assigned_to": "eng-1"},
            {"action_title": "Add cross-tenant penetration test cases", "assigned_to": "qa-1"},
        ],
        owner_id="backend-team-lead",
    )
    assert plan.status == RemediationStatus.PLANNED
    assert finding_mgr.get_finding("FND-TENANT-001").status == FindingStatus.IN_REMEDIATION

    # Rule 20: Retest verification MUST pass before closure
    with pytest.raises(ValueError, match="Verification retest failed"):
        remediation_engine.verify_and_close_finding(
            finding_code="FND-TENANT-001",
            verifier_id="qa-lead",
            verification_evidence_id="ev-fail-1",
            retest_passed=False,  # Retest failed! Cannot close
        )

    # When retest passes, finding and remediation close
    verified_plan = remediation_engine.verify_and_close_finding(
        finding_code="FND-TENANT-001",
        verifier_id="qa-lead",
        verification_evidence_id="ev-pass-1",
        retest_passed=True,
    )
    assert verified_plan.status == RemediationStatus.VERIFIED
    closed_finding = finding_mgr.get_finding("FND-TENANT-001")
    assert closed_finding.status == FindingStatus.CLOSED


# =========================================================================
# 10. Privacy Governance, Consent & DSAR Lifecycle Tests
# =========================================================================

def test_privacy_ropa_and_dsar_legal_hold():
    privacy = PrivacyEngine()

    # Consent Recording & Positive Verification
    consent = privacy.record_consent(
        subject_id="customer-john-doe",
        purpose="Product Updates Newsletter",
        channel="EMAIL",
    )
    assert consent.status == "GRANTED"
    assert privacy.has_active_consent("customer-john-doe", "Product Updates Newsletter") is True

    # Consent Withdrawal
    privacy.withdraw_consent("customer-john-doe", "Product Updates Newsletter")
    assert privacy.has_active_consent("customer-john-doe", "Product Updates Newsletter") is False

    # DSAR Deletion Request with Active Legal Hold
    req = privacy.create_privacy_request(
        request_code="DSAR-REQ-001",
        subject_id="litigant-bob",
        request_type=PrivacyRequestType.DELETION,
    )
    assert req.status == PrivacyRequestStatus.RECEIVED

    # Processing under active legal hold -> must raise PermissionError
    with pytest.raises(PermissionError, match="Legal hold active"):
        privacy.advance_request_status(
            request_code="DSAR-REQ-001",
            next_status=PrivacyRequestStatus.FULFILLED,
            note="Attempting autonomous deletion",
            has_legal_hold=True,
        )

    # Lawful fulfillment without legal hold succeeds
    fulfilled = privacy.advance_request_status(
        request_code="DSAR-REQ-001",
        next_status=PrivacyRequestStatus.FULFILLED,
        note="Personal data scrubbed per GDPR Art. 17",
        has_legal_hold=False,
    )
    assert fulfilled.status == PrivacyRequestStatus.FULFILLED
    assert fulfilled.fulfilled_at is not None


# =========================================================================
# 11. Vendor Risk Management (TPRM) & Blast Radius Tests
# =========================================================================

def test_vendor_risk_and_blast_radius():
    tprm = VendorRiskManager()
    vendors = tprm.list_vendors()
    assert len(vendors) >= 3

    stripe = tprm.get_vendor("VND_STRIPE")
    assert stripe is not None
    assert stripe.criticality == VendorCriticality.CRITICAL
    assert "BillingService" in stripe.dependent_services

    blast_radius = tprm.get_dependent_blast_radius("VND_STRIPE")
    assert len(blast_radius) >= 2
    assert "BillingService" in blast_radius


# =========================================================================
# 12. Audit Management & Dual-Approval Attestation Tests
# =========================================================================

def test_audit_and_attestation_dual_approval():
    audit_mgr = AuditManager()
    audit = audit_mgr.create_audit(
        audit_code="AUD-SOC2-2026",
        title="2026 Annual SOC 2 Type II Examination",
        framework_code="SOC2_TYPE_II",
        lead_auditor="external-auditor-ey",
        scope_controls=["CTL_SEC_MFA", "CTL_SEC_TENANT_ISOLATION"],
    )
    assert audit.status == AuditStatus.PLANNING

    # Draft attestation
    attestation = audit_mgr.prepare_attestation(
        attestation_code="ATT-2026-Q3",
        scope="Production Cloud SaaS Infrastructure",
        statement="All security, identity, and tenant isolation controls operated effectively.",
        framework_code="SOC2_TYPE_II",
        preparer_id="grc-manager-alice",
        evidence_ids=["ev-01", "ev-02"],
    )
    assert attestation.status == AttestationStatus.DRAFT

    # Rule: AI cannot draft formal attestations
    with pytest.raises(PermissionError, match="AI agents are strictly prohibited"):
        audit_mgr.prepare_attestation(
            attestation_code="ATT-BOT",
            scope="AI Scope",
            statement="All good",
            framework_code="SOC2_TYPE_II",
            preparer_id="ai_agent",
            evidence_ids=[],
            is_ai_agent=True,
        )

    # Rule: Preparer cannot approve own attestation (Separation of Duties)
    with pytest.raises(PermissionError, match="Separation of duties violation"):
        audit_mgr.approve_attestation("ATT-2026-Q3", approver_id="grc-manager-alice")

    # Independent Officer approval
    approved_att = audit_mgr.approve_attestation("ATT-2026-Q3", approver_id="ciso-director-dan")
    assert approved_att.status == AttestationStatus.ATTESTED
    assert approved_att.approver_id == "ciso-director-dan"


# =========================================================================
# 13. Governance Posture Engine & Rule 18 Critical Failure Visibility
# =========================================================================

def test_governance_posture_and_rule_18():
    fw_reg = FrameworkRegistry()
    ctl_cat = ControlCatalog()
    ev_col = EvidenceCollector()
    rk_reg = RiskRegister()
    fnd_mgr = FindingManager()
    exc_mgr = ExceptionManager()

    # Raise a critical finding
    fnd_mgr.raise_finding(
        finding_code="FND-CRIT-TENANT",
        control_code="CTL_SEC_TENANT_ISOLATION",
        title="Critical Tenant Boundary Leak",
        description="Leaking data",
        severity=FindingSeverity.CRITICAL,
        owner_id="sec-lead",
        due_date=datetime.now(timezone.utc) + timedelta(days=3),
    )

    posture_engine = GovernancePostureEngine(
        framework_registry=fw_reg,
        control_catalog=ctl_cat,
        evidence_collector=ev_col,
        risk_register=rk_reg,
        finding_manager=fnd_mgr,
        exception_manager=exc_mgr,
    )

    snapshot = posture_engine.calculate_posture_snapshot()
    # Rule 18: Critical findings must mark overall health as CRITICAL and apply penalty
    assert snapshot.overall_health == "CRITICAL"
    assert snapshot.critical_findings_count >= 1
    assert snapshot.technical_debt_score > 0

    executive_summary = posture_engine.get_executive_summary()
    assert executive_summary["critical_blockers"] >= 1
    assert executive_summary["governance_health"] == "CRITICAL"


# =========================================================================
# 14. Unified Governance Platform Service Facade Tests
# =========================================================================

def test_governance_platform_service_facade():
    service = GovernancePlatformService()
    summary = service.get_executive_summary()
    assert "composite_compliance_score" in summary
    assert summary["governance_health"] in ["HEALTHY", "AT_RISK", "CRITICAL"]

    fw_list = service.list_frameworks()
    assert len(fw_list) >= 4

    ctrl_list = service.list_controls()
    assert len(ctrl_list) >= 6

    # Test continuous monitoring check
    mon_res = service.run_continuous_monitoring()
    assert mon_res["healthy"] >= 6


# =========================================================================
# 15. GRC AI Advisory Agents & Prohibited Permissions Blocking Tests
# =========================================================================

def test_governance_prohibited_permissions_blocking():
    expected_prohibited = [
        "APPROVE_COMPLIANCE",
        "ACCEPT_RISK",
        "CHANGE_POLICY",
        "CHANGE_CONTROL",
        "CLOSE_FINDING",
        "ATTEST",
        "DECLARE_COMPLIANCE",
        "MAKE_LEGAL_DETERMINATION",
        "MODIFY_RETENTION",
        "DELETE_EVIDENCE",
        "OVERRIDE_SECURITY",
    ]
    for perm in expected_prohibited:
        assert perm in PROHIBITED_PERMISSIONS

    # Autonomous agents cannot be granted prohibited permissions
    with pytest.raises(AgentPermissionDeniedError, match="is strictly prohibited"):
        validate_agent_permissions(["APPROVE_COMPLIANCE"])

    with pytest.raises(AgentPermissionDeniedError, match="is strictly prohibited"):
        validate_agent_permissions(["ACCEPT_RISK"])


def test_governance_assessment_agent():
    agent = GovernanceAssessmentAgent()
    required = agent.get_required_permissions()
    assert AgentPermission.READ_REQUIREMENTS in required
    assert "APPROVE_COMPLIANCE" not in [p.value if hasattr(p, "value") else str(p) for p in required]

    result = asyncio.run(agent.execute(AgentContext(workflow_id="wf-test-1", task_id="task-test-1", agent_run_id="run-test-1")))
    assert result["status"] == "SUCCESS"
    assert "composite_score" in result
    assert "advisory_notice" in result


def test_audit_assistant_agent():
    agent = AuditAssistantAgent()
    required = agent.get_required_permissions()
    assert AgentPermission.READ_AUDITS in required

    result = asyncio.run(agent.execute(AgentContext(workflow_id="wf-test-2", task_id="task-test-2", agent_run_id="run-test-2")))
    assert result["status"] == "SUCCESS"
    assert "evidence_coverage" in result
    assert "advisory_notice" in result


def test_privacy_governance_agent():
    agent = PrivacyGovernanceAgent()
    required = agent.get_required_permissions()
    assert AgentPermission.READ_PRIVACY_ACTIVITIES in required

    result = asyncio.run(agent.execute(AgentContext(workflow_id="wf-test-3", task_id="task-test-3", agent_run_id="run-test-3")))
    assert result["status"] == "SUCCESS"
    assert "active_processing_activities" in result
    assert "advisory_notice" in result
