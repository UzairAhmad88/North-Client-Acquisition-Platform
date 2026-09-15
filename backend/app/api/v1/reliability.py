"""FastAPI router for Reliability, SRE, Circuit Breakers, SLOs, and Incident Management."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_active_user
from app.models.user import User
from app.reliability.service import ReliabilityPlatformService
from app.schemas.reliability import (
    CircuitBreakerResetRequest,
    CircuitBreakerStatusSchema,
    DeepHealthResultSchema,
    ErrorBudgetSummarySchema,
    IncidentCreateSchema,
    IncidentMitigationStepAddSchema,
    IncidentResponseSchema,
    IncidentTimelineEventAddSchema,
    IncidentUpdateSchema,
    PostmortemCreateSchema,
    PostmortemResponseSchema,
    SLOCreateSchema,
    SLOMetricSnapshotSchema,
)

router = APIRouter(prefix="/reliability", tags=["Reliability & SRE Platform"])
_reliability_service = ReliabilityPlatformService()


# --- Deep Health Diagnostics ---

@router.get("/health", response_model=DeepHealthResultSchema, summary="Execute deep subsystem health checks")
def get_deep_health(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    return _reliability_service.run_deep_health()


# --- Circuit Breakers ---

@router.get("/circuits", response_model=List[CircuitBreakerStatusSchema], summary="List all circuit breaker states")
def list_circuit_breakers(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _reliability_service.get_circuit_states()


@router.post("/circuits/reset", summary="Manually reset a circuit breaker to CLOSED")
def reset_circuit_breaker(
    payload: CircuitBreakerResetRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _reliability_service.reset_circuit(payload.service_name)


# --- SLOs and Error Budgets ---

@router.get("/slos", response_model=ErrorBudgetSummarySchema, summary="Get current SLOs and error budget depletion")
def get_slo_dashboard(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    return _reliability_service.evaluate_slos()


@router.post("/slos", summary="Register or update an SLO definition")
def create_slo(
    payload: SLOCreateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _reliability_service.register_slo(
        slo_type=payload.slo_type,
        name=payload.name,
        target_percentage=payload.target_percentage,
        window_days=payload.window_days,
        service_tier=payload.service_tier,
    )


# --- Incident Management ---

@router.post("/incidents", response_model=IncidentResponseSchema, summary="Declare a reliability incident")
def declare_incident(
    payload: IncidentCreateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _reliability_service.declare_incident(
        title=payload.title,
        severity=payload.severity,
        affected_services=payload.affected_services,
        impact_summary=payload.impact_summary,
        lead_responder=payload.lead_responder or current_user.email,
        responders=payload.responders,
    )


@router.get("/incidents", response_model=List[IncidentResponseSchema], summary="List reliability incidents")
def list_incidents(
    status: Optional[str] = Query(None, description="Filter by status (e.g. TRIGGERED, MITIGATED, RESOLVED)"),
    current_user: User = Depends(get_current_active_user),
) -> List[Dict[str, Any]]:
    return _reliability_service.list_incidents(status=status)


@router.get("/incidents/{incident_id}", response_model=IncidentResponseSchema, summary="Get incident details")
def get_incident(
    incident_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    inc = _reliability_service.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.post("/incidents/{incident_id}/acknowledge", response_model=IncidentResponseSchema, summary="Acknowledge incident")
def acknowledge_incident(
    incident_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    inc = _reliability_service.acknowledge_incident(incident_id, responder=current_user.email)
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.post("/incidents/{incident_id}/mitigate", response_model=IncidentResponseSchema, summary="Mark incident as mitigated")
def mitigate_incident(
    incident_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    inc = _reliability_service.mitigate_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.post("/incidents/{incident_id}/resolve", response_model=IncidentResponseSchema, summary="Mark incident as resolved")
def resolve_incident(
    incident_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    inc = _reliability_service.resolve_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.post("/incidents/{incident_id}/timeline", response_model=IncidentResponseSchema, summary="Add timeline event")
def add_timeline_event(
    incident_id: str,
    payload: IncidentTimelineEventAddSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    inc = _reliability_service.add_timeline_event(
        incident_id=incident_id,
        description=payload.description,
        actor=payload.actor or current_user.email,
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


# --- Postmortems ---

@router.post("/postmortems", response_model=PostmortemResponseSchema, summary="Create blameless incident postmortem")
def create_postmortem(
    payload: PostmortemCreateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    pm = _reliability_service.create_postmortem(
        incident_id=payload.incident_id,
        summary=payload.summary,
        root_cause=payload.root_cause,
        five_whys=payload.five_whys,
        what_went_well=payload.what_went_well,
        what_could_improve=payload.what_could_improve,
        action_items=payload.action_items,
        owner=payload.owner or current_user.email,
    )
    if not pm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create postmortem; verify incident ID")
    return pm


@router.get("/postmortems/{incident_id}", response_model=PostmortemResponseSchema, summary="Get postmortem for incident")
def get_postmortem(
    incident_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    pm = _reliability_service.get_postmortem(incident_id)
    if not pm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Postmortem not found for incident")
    return pm


# --- Data Integrity Checks ---

@router.post("/integrity-check", summary="Run cross-system database and financial ledger data integrity checks")
def run_integrity_check(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    return _reliability_service.verify_data_integrity()
