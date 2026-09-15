"""
Unified Governance, Risk, Compliance & Privacy Platform Service Facade (Section 61).
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from backend.app.governance.applicability.engine import ApplicabilityEngine, ApplicabilityRecord
from backend.app.governance.audits.manager import AuditCampaign, AuditManager, AuditRequest
from backend.app.governance.base import (
    ApplicabilityDecision,
    ControlDomain,
    ControlHealthStatus,
    EvidenceFreshness,
    EvidenceType,
    ExceptionStatus,
    FindingSeverity,
    FindingStatus,
    GovernanceAttestation,
    GovernanceControl,
    GovernanceEvidence,
    GovernanceException,
    GovernanceFinding,
    GovernanceFramework,
    GovernanceRequirement,
    GovernanceRisk,
    PrivacyRequestStatus,
    PrivacyRequestType,
    RiskLevel,
    TestResult,
    VendorCriticality,
)
from backend.app.governance.controls.catalog import ControlCatalog
from backend.app.governance.evidence.collector import EvidenceCollector
from backend.app.governance.exceptions.manager import ExceptionManager
from backend.app.governance.findings.manager import FindingManager
from backend.app.governance.frameworks.registry import FrameworkRegistry
from backend.app.governance.monitoring.continuous import ContinuousControlMonitor
from backend.app.governance.posture.engine import GovernancePostureEngine, GovernancePostureSnapshot
from backend.app.governance.privacy.engine import PrivacyConsent, PrivacyEngine, PrivacyRequest, ProcessingActivity
from backend.app.governance.remediation.engine import RemediationEngine, RemediationPlan
from backend.app.governance.risk.register import RiskRegister
from backend.app.governance.testing.engine import ControlTestingEngine, ControlTestRun
from backend.app.governance.vendors.risk import VendorProfile, VendorRiskAssessment, VendorRiskManager


class GovernancePlatformService:
    """Unified service facade for Phase 47 GRC, Privacy, Risk & Regulatory Platform."""

    def __init__(self):
        self.framework_registry = FrameworkRegistry()
        self.applicability_engine = ApplicabilityEngine()
        self.control_catalog = ControlCatalog()
        self.evidence_collector = EvidenceCollector()
        self.testing_engine = ControlTestingEngine()
        self.continuous_monitor = ContinuousControlMonitor(self.control_catalog)
        self.risk_register = RiskRegister()
        self.exception_manager = ExceptionManager()
        self.finding_manager = FindingManager()
        self.remediation_engine = RemediationEngine(self.finding_manager)
        self.privacy_engine = PrivacyEngine()
        self.vendor_manager = VendorRiskManager()
        self.audit_manager = AuditManager()
        self.posture_engine = GovernancePostureEngine(
            self.framework_registry,
            self.control_catalog,
            self.evidence_collector,
            self.risk_register,
            self.finding_manager,
            self.exception_manager
        )

    # --- Frameworks & Requirements ---
    def list_frameworks(self) -> List[GovernanceFramework]:
        return self.framework_registry.list_frameworks()

    def get_framework(self, framework_code: str) -> Optional[GovernanceFramework]:
        return self.framework_registry.get_framework(framework_code)

    def list_requirements(self, framework_code: str) -> List[GovernanceRequirement]:
        return self.framework_registry.get_requirements(framework_code)

    def record_applicability(
        self,
        requirement_code: str,
        decision: ApplicabilityDecision,
        justification: str,
        reviewer_id: str,
        evidence_references: Optional[List[str]] = None
    ) -> ApplicabilityRecord:
        return self.applicability_engine.record_decision(
            requirement_code=requirement_code,
            decision=decision,
            justification=justification,
            reviewer_id=reviewer_id,
            evidence_references=evidence_references
        )

    # --- Controls & Monitoring ---
    def list_controls(self, domain: Optional[ControlDomain] = None) -> List[GovernanceControl]:
        return self.control_catalog.list_controls(domain)

    def get_control(self, control_code: str) -> Optional[GovernanceControl]:
        return self.control_catalog.get_control(control_code)

    def run_continuous_monitoring(self) -> Dict[str, Any]:
        return self.continuous_monitor.run_continuous_health_check()

    # --- Evidence ---
    def ingest_evidence(
        self,
        evidence_type: EvidenceType,
        source_subsystem: str,
        source_record_id: str,
        provenance_uri: str,
        summary: str,
        data_payload: Dict[str, Any],
        control_codes: Optional[List[str]] = None
    ) -> GovernanceEvidence:
        return self.evidence_collector.ingest_evidence(
            evidence_type=evidence_type,
            source_subsystem=source_subsystem,
            source_record_id=source_record_id,
            provenance_uri=provenance_uri,
            summary=summary,
            data_payload=data_payload,
            control_codes=control_codes
        )

    def get_evidence_for_control(self, control_code: str) -> List[GovernanceEvidence]:
        return self.evidence_collector.get_evidence_for_control(control_code)

    def audit_evidence_freshness(self) -> Dict[str, Any]:
        return self.evidence_collector.audit_evidence_freshness()

    # --- Testing ---
    def execute_control_test(
        self,
        control_code: str,
        test_type: str,
        result: TestResult,
        details: str,
        executed_by: str,
        evidence_ids: Optional[List[str]] = None
    ) -> ControlTestRun:
        control = self.control_catalog.get_control(control_code)
        if not control:
            raise KeyError(f"Control '{control_code}' not found.")
        return self.testing_engine.execute_test(
            control=control,
            test_type=test_type,
            result=result,
            details=details,
            executed_by=executed_by,
            evidence_ids=evidence_ids
        )

    def get_test_history(self, control_code: Optional[str] = None) -> List[ControlTestRun]:
        return self.testing_engine.get_test_history(control_code)

    # --- Risk ---
    def list_risks(self, category: Optional[str] = None) -> List[GovernanceRisk]:
        return self.risk_register.list_risks(category)

    def get_risk(self, risk_code: str) -> Optional[GovernanceRisk]:
        return self.risk_register.get_risk(risk_code)

    def accept_risk(self, risk_code: str, approver_id: str, justification: str, is_ai: bool = False) -> GovernanceRisk:
        return self.risk_register.accept_risk(risk_code, approver_id, justification, is_ai_agent=is_ai)

    # --- Exceptions ---
    def request_exception(
        self,
        exception_code: str,
        title: str,
        control_code: str,
        reason: str,
        compensating_controls: List[str],
        owner_id: str,
        requester_id: str,
        expiration_date: datetime,
        risk_level: RiskLevel = RiskLevel.MEDIUM
    ) -> GovernanceException:
        return self.exception_manager.request_exception(
            exception_code=exception_code,
            title=title,
            control_code=control_code,
            reason=reason,
            compensating_controls=compensating_controls,
            owner_id=owner_id,
            requester_id=requester_id,
            expiration_date=expiration_date,
            risk_level=risk_level
        )

    def approve_exception(self, exception_code: str, approver_id: str, is_ai: bool = False) -> GovernanceException:
        return self.exception_manager.approve_exception(exception_code, approver_id, is_ai_agent=is_ai)

    def sweep_expired_exceptions(self) -> int:
        return self.exception_manager.sweep_expired_exceptions()

    # --- Findings & Remediation ---
    def raise_finding(
        self,
        finding_code: str,
        control_code: str,
        title: str,
        description: str,
        severity: FindingSeverity,
        owner_id: str,
        due_date: datetime,
        root_cause: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None
    ) -> GovernanceFinding:
        return self.finding_manager.raise_finding(
            finding_code=finding_code,
            control_code=control_code,
            title=title,
            description=description,
            severity=severity,
            owner_id=owner_id,
            due_date=due_date,
            root_cause=root_cause,
            evidence_ids=evidence_ids
        )

    def list_findings(self, severity: Optional[FindingSeverity] = None, status: Optional[FindingStatus] = None) -> List[GovernanceFinding]:
        return self.finding_manager.list_findings(severity=severity, status=status)

    def create_remediation_plan(self, finding_code: str, plan_title: str, actions: List[Dict[str, Any]], owner_id: str) -> RemediationPlan:
        return self.remediation_engine.create_remediation_plan(finding_code, plan_title, actions, owner_id)

    def verify_and_close_finding(self, finding_code: str, verifier_id: str, verification_evidence_id: str, retest_passed: bool) -> RemediationPlan:
        return self.remediation_engine.verify_and_close_finding(finding_code, verifier_id, verification_evidence_id, retest_passed)

    # --- Privacy ---
    def list_processing_activities(self) -> List[ProcessingActivity]:
        return self.privacy_engine.list_processing_activities()

    def record_consent(self, subject_id: str, purpose: str, channel: str = "EMAIL") -> PrivacyConsent:
        return self.privacy_engine.record_consent(subject_id, purpose, channel)

    def create_privacy_request(self, request_code: str, subject_id: str, request_type: PrivacyRequestType) -> PrivacyRequest:
        return self.privacy_engine.create_privacy_request(request_code, subject_id, request_type)

    def advance_privacy_request(self, request_code: str, next_status: PrivacyRequestStatus, note: str, has_legal_hold: bool = False) -> PrivacyRequest:
        return self.privacy_engine.advance_request_status(request_code, next_status, note, has_legal_hold=has_legal_hold)

    def list_privacy_requests(self) -> List[PrivacyRequest]:
        return self.privacy_engine.list_requests()

    # --- Vendors ---
    def list_vendors(self, criticality: Optional[VendorCriticality] = None) -> List[VendorProfile]:
        return self.vendor_manager.list_vendors(criticality)

    def get_vendor_blast_radius(self, vendor_code: str) -> List[str]:
        return self.vendor_manager.get_dependent_blast_radius(vendor_code)

    def record_vendor_assessment(self, assessment_id: str, vendor_code: str, assessor_id: str, score: float, findings: List[str]) -> VendorRiskAssessment:
        return self.vendor_manager.record_assessment(assessment_id, vendor_code, assessor_id, score, findings)

    # --- Audits & Attestation ---
    def create_audit(self, audit_code: str, title: str, framework_code: str, lead_auditor: str, scope_controls: List[str]) -> AuditCampaign:
        return self.audit_manager.create_audit(audit_code, title, framework_code, lead_auditor, scope_controls)

    def create_audit_request(self, request_code: str, audit_code: str, control_code: str, description: str, assigned_to: str, due_date: datetime) -> AuditRequest:
        return self.audit_manager.create_audit_request(request_code, audit_code, control_code, description, assigned_to, due_date)

    def prepare_attestation(self, attestation_code: str, scope: str, statement: str, framework_code: str, preparer_id: str, evidence_ids: List[str], is_ai: bool = False) -> GovernanceAttestation:
        return self.audit_manager.prepare_attestation(attestation_code, scope, statement, framework_code, preparer_id, evidence_ids, is_ai_agent=is_ai)

    def approve_attestation(self, attestation_code: str, approver_id: str, is_ai: bool = False) -> GovernanceAttestation:
        return self.audit_manager.approve_attestation(attestation_code, approver_id, is_ai_agent=is_ai)

    # --- Posture & Executive Intelligence ---
    def get_posture_snapshot(self) -> GovernancePostureSnapshot:
        return self.posture_engine.calculate_posture_snapshot()

    def get_executive_summary(self) -> Dict[str, Any]:
        return self.posture_engine.get_executive_summary()
