"""
API Router for Phase 66 — Autonomous Cybersecurity, Zero-Trust Security Operations & AI Defense Platform.
Mounted at /cybersecurity-zero-trust.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from backend.app.core.database import get_db
except ImportError:
    from app.core.database import get_db
from backend.app.services.security.service import AutonomousCybersecurityZeroTrustService
from backend.app.schemas.autonomous_cybersecurity_zero_trust import (
    AssetCreate,
    AssetResponse,
    ZeroTrustAccessRequest,
    ZeroTrustAccessDecision,
    PrivilegedAccessRequestCreate,
    PrivilegedAccessResponse,
    SecretCreate,
    SecretResponse,
    SecurityEventIngest,
    DetectionRuleCreate,
    SecurityAlertResponse,
    ThreatIndicatorCreate,
    VulnerabilityResponse,
    SbomScanRequest,
    IncidentCreate,
    IncidentResponse,
    AiPromptSecurityCheck,
    AiPromptSecurityResponse,
    AgentToolValidationRequest,
    AgentToolValidationResponse,
    SecurityGraphQuery,
    DefenseLoopRequest,
    DefenseLoopResponse,
)

router = APIRouter(prefix="/cybersecurity-zero-trust", tags=["Phase 66 — Autonomous Cybersecurity & Zero-Trust"])


def get_security_service(db: Session = Depends(get_db)) -> AutonomousCybersecurityZeroTrustService:
    return AutonomousCybersecurityZeroTrustService(db)


# 1. Health & Command Center Telemetry
@router.get("/health", response_model=Dict[str, Any])
def get_security_health(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    summary = service.get_command_center_summary(tenant_id)
    return {
        "status": "HEALTHY",
        "platform": "Autonomous Cybersecurity, Zero-Trust Security Operations & AI Defense",
        "telemetry": summary,
    }


# 2. Continuous Zero-Trust Evaluation
@router.post("/zero-trust/evaluate", response_model=Dict[str, Any])
def evaluate_zero_trust_access(
    req: ZeroTrustAccessRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    device_compliant = req.context_data.get("device_compliant", True)
    risk_score = float(req.context_data.get("risk_score", 0.1))
    decision = service.zero_trust.evaluate_access(
        subject_id=req.subject_id,
        subject_type=req.subject_type,
        resource=req.resource,
        action=req.action,
        device_compliant=device_compliant,
        risk_score=risk_score,
        tenant_id=tenant_id
    )
    # Log audit
    service.audit.log_event(
        actor_id=req.subject_id,
        action=f"ZERO_TRUST_{req.action}",
        resource=req.resource,
        decision=decision["decision"],
        tenant_id=tenant_id
    )
    return decision


# 3. Privileged Access Management (JIT)
@router.post("/privileged-access/request", response_model=Dict[str, Any])
def request_privileged_access(
    req: PrivilegedAccessRequestCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.privileged_access.request_access(
        requester_id=req.requester_id,
        target_role=req.target_role,
        justification=req.justification,
        duration_minutes=req.duration_minutes,
        tenant_id=tenant_id
    )


@router.get("/privileged-access/requests", response_model=List[Dict[str, Any]])
def list_privileged_access_requests(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.privileged_access.list_requests(tenant_id)


# 4. Assets
@router.post("/assets", response_model=Dict[str, Any])
def register_asset(
    asset: AssetCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.assets.register_asset(asset.model_dump(), tenant_id=tenant_id)


@router.get("/assets", response_model=List[Dict[str, Any]])
def list_assets(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.assets.list_assets(tenant_id=tenant_id)


# 5. Secrets Governance
@router.post("/secrets", response_model=Dict[str, Any])
def register_secret(
    secret: SecretCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.secrets.register_secret(
        secret_name=secret.secret_name,
        vault_reference_key=secret.vault_reference_key,
        owner=secret.owner,
        secret_type=secret.secret_type,
        tenant_id=tenant_id
    )


@router.post("/secrets/{secret_id}/rotate", response_model=Dict[str, Any])
def rotate_secret(
    secret_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    res = service.secrets.rotate_secret(secret_id, tenant_id=tenant_id)
    if not res:
        raise HTTPException(status_code=404, detail="Secret not found")
    return res


# 6. SIEM Events & Detections
@router.post("/events/ingest", response_model=Dict[str, Any])
def ingest_security_event(
    evt: SecurityEventIngest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.events.ingest_event(
        source=evt.source,
        actor_id=evt.actor_id,
        action=evt.action,
        target_resource=evt.target_resource,
        status=evt.status,
        severity=evt.severity,
        ip=evt.ip_address,
        payload=evt.payload,
        tenant_id=tenant_id
    )


@router.get("/events", response_model=List[Dict[str, Any]])
def list_security_events(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.events.list_events(tenant_id)


@router.get("/alerts", response_model=List[Dict[str, Any]])
def list_security_alerts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.alerts.list_alerts(tenant_id)


# 7. Threat Intelligence & Vulnerabilities
@router.post("/threats/indicators", response_model=Dict[str, Any])
def add_threat_indicator(
    ioc: ThreatIndicatorCreate,
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.threat_intelligence.add_indicator(
        indicator_type=ioc.indicator_type,
        value=ioc.value,
        threat_actor=ioc.threat_actor,
        severity=ioc.severity
    )


@router.get("/vulnerabilities", response_model=List[Dict[str, Any]])
def list_vulnerabilities(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.vulnerabilities.list_vulnerabilities(tenant_id)


@router.post("/sbom/scan", response_model=Dict[str, Any])
def scan_sbom(
    req: SbomScanRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.sbom.scan_sbom(req.application_name, req.packages, tenant_id=tenant_id)


# 8. Incident Management
@router.post("/incidents", response_model=Dict[str, Any])
def create_incident(
    req: IncidentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.incidents.create_incident(
        title=req.title,
        severity=req.severity,
        affected_assets=req.affected_assets,
        tenant_id=tenant_id
    )


@router.get("/incidents", response_model=List[Dict[str, Any]])
def list_incidents(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.incidents.list_incidents(tenant_id)


# 9. AI Security Guardrails
@router.post("/ai-security/scan-prompt", response_model=Dict[str, Any])
def scan_ai_prompt(
    req: AiPromptSecurityCheck,
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.ai_security.scan_prompt(req.prompt_text)


@router.post("/ai-security/validate-tool", response_model=Dict[str, Any])
def validate_agent_tool(
    req: AgentToolValidationRequest,
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.ai_security.validate_tool_execution(
        agent_id=req.agent_id,
        tool_name=req.tool_name,
        args=req.tool_arguments
    )


# 10. Security Graph
@router.post("/graph/query", response_model=Dict[str, Any])
def query_security_graph(
    req: SecurityGraphQuery,
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.graph.query_blast_radius(req.entity_id)


# 11. Closed-Loop Autonomous Defense Cycle
@router.post("/defense-loop/run", response_model=Dict[str, Any])
def run_defense_loop(
    req: DefenseLoopRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCybersecurityZeroTrustService = Depends(get_security_service)
):
    return service.run_continuous_defense_loop(tenant_id=tenant_id, target_asset_id=req.asset_id)
