"""API Endpoints for Organizational Risk Register and Mitigation Workflows."""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.business_os.base import RiskCategory, RiskLifecycleStatus, RiskSeverity
from app.business_os.service import BusinessOSPlatformService
from app.schemas.business_os import RiskCreate, RiskResponse

router = APIRouter(prefix="/risks", tags=["organizational-risks"])

_service_instance = BusinessOSPlatformService()


def get_business_os_service() -> BusinessOSPlatformService:
    return _service_instance


@router.get("", response_model=List[RiskResponse])
async def list_risks(
    category: Optional[RiskCategory] = Query(None),
    min_severity: Optional[RiskSeverity] = Query(None),
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """List organizational risks ordered by risk score severity."""
    recs = service.list_risks(category=category, min_severity=min_severity)
    return [
        RiskResponse(
            risk_id=r.risk_id,
            title=r.title,
            description=r.description,
            category=r.category,
            probability=r.probability,
            impact=r.impact,
            risk_score=r.risk_score,
            severity=r.severity,
            owner=r.owner,
            status=r.status,
            identified_at=r.identified_at,
            due_date=r.due_date,
            evidence_signals=r.evidence_signals,
            mitigation_strategy=r.mitigation_strategy,
            contingency_plan=r.contingency_plan,
            last_reviewed_at=r.last_reviewed_at,
        )
        for r in recs
    ]


@router.post("", response_model=RiskResponse, status_code=status.HTTP_201_CREATED)
async def register_risk(
    payload: RiskCreate,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Register a new organizational risk."""
    rec = service.create_risk(
        title=payload.title,
        description=payload.description,
        category=payload.category,
        probability=payload.probability,
        impact=payload.impact,
        owner=payload.owner,
        evidence_signals=payload.evidence_signals,
        mitigation_strategy=payload.mitigation_strategy,
        contingency_plan=payload.contingency_plan,
    )
    return RiskResponse(
        risk_id=rec.risk_id,
        title=rec.title,
        description=rec.description,
        category=rec.category,
        probability=rec.probability,
        impact=rec.impact,
        risk_score=rec.risk_score,
        severity=rec.severity,
        owner=rec.owner,
        status=rec.status,
        identified_at=rec.identified_at,
        due_date=rec.due_date,
        evidence_signals=rec.evidence_signals,
        mitigation_strategy=rec.mitigation_strategy,
        contingency_plan=rec.contingency_plan,
        last_reviewed_at=rec.last_reviewed_at,
    )


@router.patch("/{risk_id}/status", response_model=RiskResponse)
async def update_risk_status(
    risk_id: str,
    status: RiskLifecycleStatus = Query(...),
    notes: Optional[str] = Query(None),
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Update risk status (e.g. MITIGATION_PLANNED, MONITORED, MITIGATED, CLOSED)."""
    rec = service.risk_register.update_risk_status(risk_id=risk_id, new_status=status, mitigation_notes=notes)
    if not rec:
        raise HTTPException(status_code=404, detail="Risk not found.")
    return RiskResponse(
        risk_id=rec.risk_id,
        title=rec.title,
        description=rec.description,
        category=rec.category,
        probability=rec.probability,
        impact=rec.impact,
        risk_score=rec.risk_score,
        severity=rec.severity,
        owner=rec.owner,
        status=rec.status,
        identified_at=rec.identified_at,
        due_date=rec.due_date,
        evidence_signals=rec.evidence_signals,
        mitigation_strategy=rec.mitigation_strategy,
        contingency_plan=rec.contingency_plan,
        last_reviewed_at=rec.last_reviewed_at,
    )
