"""
REST API Router for Phase 47: Unified Compliance, Governance, Privacy, Risk & Regulatory Platform.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.governance.service import GovernancePlatformService
from app.governance.base import (
    ApplicabilityDecision,
    ControlDomain,
    EvidenceType,
    FindingSeverity,
    FindingStatus,
    PrivacyRequestStatus,
    PrivacyRequestType,
    RiskLevel,
    TestResult,
)
from app.schemas.grc import (
    ApplicabilityRequest,
    ApplicabilityResponse,
    AttestationApproveRequest,
    AttestationPrepareRequest,
    AttestationResponse,
    ControlResponse,
    ControlTestRequest,
    ControlTestResponse,
    EvidenceIngestRequest,
    EvidenceResponse,
    ExceptionApprovalRequest,
    ExceptionCreateRequest,
    ExceptionResponse,
    ExecutiveSummaryResponse,
    FindingCreateRequest,
    FindingResponse,
    FrameworkResponse,
    PostureSnapshotResponse,
    PrivacyRequestAdvance,
    PrivacyRequestCreate,
    PrivacyRequestResponse,
    RemediationPlanRequest,
    RemediationResponse,
    RemediationVerifyRequest,
    RequirementResponse,
    RiskAcceptanceRequest,
    RiskCreateRequest,
    RiskResponse,
    VendorResponse,
)

router = APIRouter(prefix="/governance", tags=["governance-grc"])

# Singleton service instance
_gov_service = GovernancePlatformService()


def get_governance_service() -> GovernancePlatformService:
    return _gov_service


# =============================================================================
# 1. Overview, Posture & Executive Intelligence
# =============================================================================

@router.get("/overview", response_model=ExecutiveSummaryResponse)
def get_governance_overview(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.get_executive_summary()


@router.get("/posture", response_model=PostureSnapshotResponse)
def get_posture_snapshot(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.get_posture_snapshot()


# =============================================================================
# 2. Frameworks & Requirements
# =============================================================================

@router.get("/frameworks", response_model=List[FrameworkResponse])
def list_frameworks(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.list_frameworks()


@router.get("/requirements", response_model=List[RequirementResponse])
def list_requirements(
    framework_code: str = Query("SOC2_TYPE_II"),
    service: GovernancePlatformService = Depends(get_governance_service)
):
    return service.list_requirements(framework_code)


@router.post("/applicability", response_model=ApplicabilityResponse)
def record_applicability(
    payload: ApplicabilityRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        decision = ApplicabilityDecision(payload.decision)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid decision '{payload.decision}'.")

    record = service.record_applicability(
        requirement_code=payload.requirement_code,
        decision=decision,
        justification=payload.justification,
        reviewer_id=payload.reviewer_id,
        evidence_references=payload.evidence_references
    )
    return record


# =============================================================================
# 3. Control Catalog & Testing
# =============================================================================

@router.get("/controls", response_model=List[ControlResponse])
def list_controls(
    domain: Optional[str] = None,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    cd = None
    if domain:
        try:
            cd = ControlDomain(domain)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid domain '{domain}'.")
    return service.list_controls(cd)


@router.post("/controls/{control_code}/test", response_model=ControlTestResponse)
def test_control(
    control_code: str,
    payload: ControlTestRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        res = TestResult(payload.result)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid result '{payload.result}'.")

    try:
        run = service.execute_control_test(
            control_code=control_code,
            test_type=payload.test_type,
            result=res,
            details=payload.details,
            executed_by=payload.executed_by,
            evidence_ids=payload.evidence_ids
        )
        return run
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/monitoring/continuous")
def run_continuous_monitoring(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.run_continuous_monitoring()


# =============================================================================
# 4. Evidence
# =============================================================================

@router.post("/evidence/ingest", response_model=EvidenceResponse)
def ingest_evidence(
    payload: EvidenceIngestRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        etype = EvidenceType(payload.evidence_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid evidence_type '{payload.evidence_type}'.")

    evidence = service.ingest_evidence(
        evidence_type=etype,
        source_subsystem=payload.source_subsystem,
        source_record_id=payload.source_record_id,
        provenance_uri=payload.provenance_uri,
        summary=payload.summary,
        data_payload=payload.data_payload,
        control_codes=payload.control_codes
    )
    return evidence


@router.get("/evidence/control/{control_code}", response_model=List[EvidenceResponse])
def get_control_evidence(
    control_code: str,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    return service.get_evidence_for_control(control_code)


@router.get("/evidence/audit-freshness")
def audit_freshness(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.audit_evidence_freshness()


# =============================================================================
# 5. Risk & Exceptions
# =============================================================================

@router.get("/risks", response_model=List[RiskResponse])
def list_risks(
    category: Optional[str] = None,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    return service.list_risks(category)


@router.post("/risks/{risk_code}/accept", response_model=RiskResponse)
def accept_risk(
    risk_code: str,
    payload: RiskAcceptanceRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.accept_risk(risk_code, payload.approver_id, payload.justification, is_ai=False)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except (KeyError, ValueError) as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/exceptions", response_model=List[ExceptionResponse])
def list_exceptions(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.exception_manager.list_exceptions()


@router.post("/exceptions", response_model=ExceptionResponse)
def request_exception(
    payload: ExceptionCreateRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        rlevel = RiskLevel(payload.risk_level)
    except ValueError:
        rlevel = RiskLevel.MEDIUM

    try:
        return service.request_exception(
            exception_code=payload.exception_code,
            title=payload.title,
            control_code=payload.control_code,
            reason=payload.reason,
            compensating_controls=payload.compensating_controls,
            owner_id=payload.owner_id,
            requester_id=payload.requester_id,
            expiration_date=payload.expiration_date,
            risk_level=rlevel
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.post("/exceptions/{exception_code}/approve", response_model=ExceptionResponse)
def approve_exception(
    exception_code: str,
    payload: ExceptionApprovalRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.approve_exception(exception_code, payload.approver_id, is_ai=False)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except (KeyError, ValueError) as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


# =============================================================================
# 6. Findings & Remediation
# =============================================================================

@router.get("/findings", response_model=List[FindingResponse])
def list_findings(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.list_findings()


@router.post("/findings", response_model=FindingResponse)
def raise_finding(
    payload: FindingCreateRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        sev = FindingSeverity(payload.severity)
    except ValueError:
        sev = FindingSeverity.MEDIUM

    return service.raise_finding(
        finding_code=payload.finding_code,
        control_code=payload.control_code,
        title=payload.title,
        description=payload.description,
        severity=sev,
        owner_id=payload.owner_id,
        due_date=payload.due_date,
        root_cause=payload.root_cause
    )


@router.post("/findings/{finding_code}/remediation", response_model=RemediationResponse)
def create_remediation_plan(
    finding_code: str,
    payload: RemediationPlanRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.create_remediation_plan(finding_code, payload.plan_title, payload.actions, payload.owner_id)
    except KeyError as ke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ke))


@router.post("/findings/{finding_code}/verify", response_model=RemediationResponse)
def verify_remediation(
    finding_code: str,
    payload: RemediationVerifyRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.verify_and_close_finding(
            finding_code,
            payload.verifier_id,
            payload.verification_evidence_id,
            payload.retest_passed
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except KeyError as ke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ke))


# =============================================================================
# 7. Privacy & DSAR Requests
# =============================================================================

@router.get("/privacy/requests", response_model=List[PrivacyRequestResponse])
def list_privacy_requests(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.list_privacy_requests()


@router.post("/privacy/requests", response_model=PrivacyRequestResponse)
def create_privacy_request(
    payload: PrivacyRequestCreate,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        rtype = PrivacyRequestType(payload.request_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request_type '{payload.request_type}'.")

    return service.create_privacy_request(payload.request_code, payload.subject_id, rtype)


@router.post("/privacy/requests/{request_code}/advance", response_model=PrivacyRequestResponse)
def advance_privacy_request(
    request_code: str,
    payload: PrivacyRequestAdvance,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        nstatus = PrivacyRequestStatus(payload.next_status)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status '{payload.next_status}'.")

    try:
        return service.advance_privacy_request(
            request_code,
            nstatus,
            payload.note,
            has_legal_hold=payload.has_legal_hold
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except KeyError as ke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ke))


# =============================================================================
# 8. Vendors & Third Parties
# =============================================================================

@router.get("/vendors", response_model=List[VendorResponse])
def list_vendors(service: GovernancePlatformService = Depends(get_governance_service)):
    return service.list_vendors()


@router.get("/vendors/{vendor_code}/blast-radius")
def get_vendor_blast_radius(
    vendor_code: str,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    return {"vendor_code": vendor_code, "dependent_services": service.get_vendor_blast_radius(vendor_code)}


# =============================================================================
# 9. Attestations
# =============================================================================

@router.post("/attestations/prepare", response_model=AttestationResponse)
def prepare_attestation(
    payload: AttestationPrepareRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.prepare_attestation(
            attestation_code=payload.attestation_code,
            scope=payload.scope,
            statement=payload.statement,
            framework_code=payload.framework_code,
            preparer_id=payload.preparer_id,
            evidence_ids=payload.evidence_ids,
            is_ai=False
        )
    except (ValueError, PermissionError) as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post("/attestations/{attestation_code}/approve", response_model=AttestationResponse)
def approve_attestation(
    attestation_code: str,
    payload: AttestationApproveRequest,
    service: GovernancePlatformService = Depends(get_governance_service)
):
    try:
        return service.approve_attestation(attestation_code, payload.approver_id, is_ai=False)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except (KeyError, ValueError) as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


# =============================================================================
# 10. AI Copilot Endpoint
# =============================================================================

@router.post("/copilot/query")
def copilot_query(
    query: str = Query(..., min_length=2),
    service: GovernancePlatformService = Depends(get_governance_service)
):
    """
    GRC AI Copilot: strictly advisory assistance with evidence citations.
    Discloses that conclusions are informational and not legal determinations.
    """
    snapshot = service.get_posture_snapshot()
    q_lower = query.lower()

    if "finding" in q_lower or "deficiency" in q_lower:
        findings = service.list_findings(status=FindingStatus.OPEN)
        response_text = f"Found {len(findings)} open compliance findings. Critical findings count: {snapshot.critical_findings_count}."
        citations = [f.finding_code for f in findings[:5]]
    elif "mfa" in q_lower or "access" in q_lower:
        mfa_ctl = service.get_control("CTL_SEC_MFA")
        response_text = f"Control CTL_SEC_MFA is currently '{mfa_ctl.health_status.value}' with automated continuous monitoring." if mfa_ctl else "MFA control not found."
        citations = ["CTL_SEC_MFA"]
    else:
        response_text = f"Overall compliance score is {snapshot.composite_compliance_score}% ({snapshot.overall_health}) across {snapshot.total_requirements} requirements and {snapshot.total_controls} controls."
        citations = ["SOC2_TYPE_II", "ISO_27001_2022", "GDPR"]

    return {
        "query": query,
        "answer": response_text,
        "evidence_citations": citations,
        "disclaimer": "Informational GRC decision-support only. Does not constitute binding legal advice or compliance attestation.",
        "uncertainty_score": 0.05,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
