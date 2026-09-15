"""
REST API endpoints for Phase 46 Security Operations, Threat Intelligence, and Automated Defense.
"""

from typing import List, Dict, Any, Optional
import uuid

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

try:
    from app.api.deps import get_db, get_security_context, require_permission
    from app.schemas.common import DataResponse
    from app.schemas.security_ops import (
        IngestSecurityEventRequest,
        SecurityAlertResponse,
        UpdateAlertStatusRequest,
        CreateIncidentRequest,
        UpdateIncidentStatusRequest,
        SecurityIncidentResponse,
        RemediationExecuteRequest,
        EmergencyControlToggleRequest,
        ThreatIndicatorCreateRequest,
        SecurityCopilotQueryRequest,
    )
    from app.security.base import (
        SecurityIncident,
        SecurityEvent,
        AlertStatus,
        IncidentStatus,
        SecuritySeverity,
        ThreatIndicator,
        ThreatIndicatorType,
    )
    from app.security.service import SecurityOperationsService
except ImportError:
    from backend.app.api.deps import get_db, get_security_context, require_permission
    from backend.app.schemas.common import DataResponse
    from backend.app.schemas.security_ops import (
        IngestSecurityEventRequest,
        SecurityAlertResponse,
        UpdateAlertStatusRequest,
        CreateIncidentRequest,
        UpdateIncidentStatusRequest,
        SecurityIncidentResponse,
        RemediationExecuteRequest,
        EmergencyControlToggleRequest,
        ThreatIndicatorCreateRequest,
        SecurityCopilotQueryRequest,
    )
    from backend.app.security.base import (
        SecurityIncident,
        SecurityEvent,
        AlertStatus,
        IncidentStatus,
        SecuritySeverity,
        ThreatIndicator,
        ThreatIndicatorType,
    )
    from backend.app.security.service import SecurityOperationsService

router = APIRouter(prefix="/security", tags=["Security Operations & Intelligence"])

# Shared singleton service instance for memory-resident streaming buffer & rules engine
soc_service = SecurityOperationsService()


# 1. Overview & Posture
@router.get("/overview", response_model=DataResponse[Dict[str, Any]])
def get_security_overview():
    """Returns real-time security posture, grade, risk scores, and open critical incidents."""
    data = soc_service.get_executive_overview()
    return DataResponse(data=data)


@router.get("/posture", response_model=DataResponse[Dict[str, Any]])
def get_security_posture():
    """Returns SOC performance metrics, MTTR, MTTD, and detection coverage."""
    assessment = soc_service.get_risk_assessment()
    incidents = soc_service.list_incidents()
    alerts = soc_service.list_alerts()
    metrics = soc_service.posture_engine.compute_soc_metrics(incidents, alerts)
    grade = soc_service.posture_engine.calculate_posture_grade(assessment.composite_risk_score)
    return DataResponse(data={
        "posture_grade": grade.value,
        "risk_score": assessment.composite_risk_score,
        "metrics": metrics
    })


@router.get("/risk", response_model=DataResponse[Dict[str, Any]])
def get_risk_assessment():
    """Returns 6-dimension risk evaluation and risk heatmap."""
    assessment = soc_service.get_risk_assessment()
    heatmap = soc_service.get_risk_heatmap()
    return DataResponse(data={
        "assessment": assessment.model_dump(),
        "heatmap": heatmap
    })


# 2. Telemetry & Events
@router.get("/events", response_model=DataResponse[List[Dict[str, Any]]])
def list_security_events(limit: int = Query(50, ge=1, le=200)):
    """Streams recent normalized canonical security events."""
    events = soc_service.list_events(limit=limit)
    return DataResponse(data=[e.model_dump() for e in events])


@router.post("/events", response_model=DataResponse[Dict[str, Any]], status_code=status.HTTP_201_CREATED)
def ingest_security_event(req: IngestSecurityEventRequest):
    """Ingests, normalizes, sanitizes secrets, and runs detection rules against a telemetry event."""
    event = soc_service.ingest_event(req.model_dump())
    return DataResponse(data=event.model_dump())


# 3. Detections & Rules
@router.get("/detections", response_model=DataResponse[List[Dict[str, Any]]])
def list_detections(limit: int = Query(50, ge=1, le=200)):
    """Lists recent automated detections mapped to MITRE ATT&CK."""
    dets = soc_service.list_detections(limit=limit)
    return DataResponse(data=[d.model_dump() for d in dets])


# 4. Alerts
@router.get("/alerts", response_model=DataResponse[List[Dict[str, Any]]])
def list_alerts(limit: int = Query(50, ge=1, le=200)):
    """Lists actionable security alerts."""
    alerts = soc_service.list_alerts(limit=limit)
    return DataResponse(data=[a.model_dump() for a in alerts])


@router.get("/alerts/{alert_id}", response_model=DataResponse[Dict[str, Any]])
def get_alert(alert_id: str):
    """Fetches details and evidence for a specific security alert."""
    alert = soc_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return DataResponse(data=alert.model_dump())


@router.post("/alerts/{alert_id}/status", response_model=DataResponse[Dict[str, Any]])
def update_alert_status(alert_id: str, req: UpdateAlertStatusRequest):
    """Advances or triages alert lifecycle."""
    alert = soc_service.update_alert_status(alert_id, req.status)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return DataResponse(data=alert.model_dump())


# 5. Incidents
@router.get("/incidents", response_model=DataResponse[List[Dict[str, Any]]])
def list_incidents():
    """Lists all confirmed security incidents."""
    incidents = soc_service.list_incidents()
    return DataResponse(data=[i.model_dump() for i in incidents])


@router.post("/incidents", response_model=DataResponse[Dict[str, Any]], status_code=status.HTTP_201_CREATED)
def create_incident(req: CreateIncidentRequest):
    """Declares a new security incident."""
    new_inc = SecurityIncident(
        incident_id=f"inc_{uuid.uuid4().hex[:8]}",
        title=req.title,
        description=req.description,
        severity=req.severity,
        status=IncidentStatus.DETECTED,
        affected_tenants=req.affected_tenants,
        affected_users=req.affected_users,
        affected_services=req.affected_services,
        affected_resources=req.affected_resources,
        owner=req.owner or "unassigned"
    )
    saved = soc_service.create_incident(new_inc)
    return DataResponse(data=saved.model_dump())


@router.get("/incidents/{incident_id}", response_model=DataResponse[Dict[str, Any]])
def get_incident(incident_id: str):
    """Fetches full security incident detail."""
    inc = soc_service.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return DataResponse(data=inc.model_dump())


@router.post("/incidents/{incident_id}/status", response_model=DataResponse[Dict[str, Any]])
def update_incident_status(incident_id: str, req: UpdateIncidentStatusRequest):
    """Updates status or closes an incident with resolution postmortem."""
    inc = soc_service.update_incident_status(incident_id, req.status, resolution=req.resolution)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return DataResponse(data=inc.model_dump())


# 6. Investigation Workspace, Timeline & Evidence Graph
@router.get("/investigations/{incident_id}", response_model=DataResponse[Dict[str, Any]])
def get_investigation_workspace(incident_id: str):
    """Loads complete investigation workspace with timeline, evidence graph, and root-cause hypotheses."""
    workspace = soc_service.get_investigation_workspace(incident_id)
    if "error" in workspace:
        raise HTTPException(status_code=404, detail=workspace["error"])
    return DataResponse(data=workspace)


@router.get("/attack-chains", response_model=DataResponse[List[Dict[str, Any]]])
def list_attack_chains():
    """Lists correlated multi-stage attack chains."""
    chains = soc_service.get_attack_chains()
    return DataResponse(data=[c.model_dump() for c in chains])


@router.get("/blast-radius/{incident_id}", response_model=DataResponse[Dict[str, Any]])
def get_blast_radius(incident_id: str):
    """Evaluates blast radius across users, clients, tenants, docs, finance, agents, and workflows."""
    radius = soc_service.calculate_blast_radius(incident_id)
    return DataResponse(data=radius.model_dump())


# 7. Runbooks & Controlled Remediation
@router.get("/runbooks", response_model=DataResponse[List[Dict[str, Any]]])
def list_runbooks():
    """Lists standard operating playbooks available for incident response."""
    pbs = soc_service.remediation_engine.playbook_registry.list_playbooks()
    return DataResponse(data=pbs)


@router.post("/remediation/execute", response_model=DataResponse[Dict[str, Any]])
def execute_remediation(req: RemediationExecuteRequest):
    """Executes a remediation action with dual approval and idempotency guarantees."""
    res = soc_service.execute_remediation(
        alert_id=req.alert_id,
        action_name=req.action_name,
        requested_by=req.requested_by,
        approved_by=req.approved_by,
        parameters=req.parameters,
        idempotency_key=req.idempotency_key
    )
    return DataResponse(data=res)


# 8. Emergency Controls & Kill Switches
@router.get("/emergency-controls", response_model=DataResponse[Dict[str, bool]])
def get_emergency_controls():
    """Lists status of global emergency security kill switches."""
    state = soc_service.get_emergency_controls()
    return DataResponse(data=state)


@router.post("/emergency-controls/toggle", response_model=DataResponse[Dict[str, Any]])
def toggle_emergency_control(req: EmergencyControlToggleRequest):
    """Engages or disengages global emergency security kill switches."""
    res = soc_service.toggle_emergency_kill_switch(
        control_name=req.control,
        enable=req.enable,
        operator_id=req.operator_id,
        reason=req.reason
    )
    return DataResponse(data=res)


# 9. Threat Intelligence
@router.get("/indicators", response_model=DataResponse[List[Dict[str, Any]]])
def list_threat_indicators():
    """Lists active indicators of compromise (IOCs)."""
    inds = soc_service.list_threat_indicators()
    return DataResponse(data=[i.model_dump() for i in inds])


@router.post("/indicators", response_model=DataResponse[Dict[str, Any]], status_code=status.HTTP_201_CREATED)
def create_threat_indicator(req: ThreatIndicatorCreateRequest):
    """Registers a new threat indicator."""
    ind = ThreatIndicator(
        indicator_id=f"ioc_{uuid.uuid4().hex[:8]}",
        indicator_type=ThreatIndicatorType(req.indicator_type),
        indicator_value=req.indicator_value,
        threat_category=req.threat_category,
        severity=req.severity,
        confidence=req.confidence,
        source=req.source,
        reputation=req.reputation
    )
    soc_service.add_threat_indicator(ind)
    return DataResponse(data=ind.model_dump())


# 10. Security AI Copilot
@router.post("/copilot", response_model=DataResponse[Dict[str, Any]])
def query_security_copilot(req: SecurityCopilotQueryRequest):
    """Answers SOC queries with evidence citations and enforced non-execution safeguards."""
    resp = soc_service.query_security_copilot(req.query, context_id=req.context_id)
    return DataResponse(data=resp)
