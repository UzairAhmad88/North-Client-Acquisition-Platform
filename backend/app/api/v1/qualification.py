import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import AppError
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.qualification import (
    QualificationHistoryResponse,
    QualificationOverrideRequest,
    QualificationResponse,
)
from app.services.qualification import QualificationService
from workers.tasks.qualification import execute_qualification_task

router = APIRouter(prefix="/leads", tags=["Lead Qualification"])


@router.post("/{lead_id}/qualification/run", response_model=DataResponse[QualificationResponse])
async def run_lead_qualification(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute qualification for target lead via Qualification Agent.
    """
    await execute_qualification_task(db, lead_id, user_id=current_user.id)
    latest = QualificationService.get_latest_qualification(db, lead_id)
    if not latest:
        raise AppError(
            code="QUALIFICATION_FAILED",
            message="Lead qualification failed to complete.",
            status_code=500,
        )
    return DataResponse(data=QualificationResponse.model_validate(latest))


@router.get("/{lead_id}/qualification", response_model=DataResponse[QualificationResponse])
def get_latest_qualification(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the latest qualification record for a lead.
    """
    latest = QualificationService.get_latest_qualification(db, lead_id)
    if not latest:
        raise AppError(
            code="QUALIFICATION_NOT_FOUND",
            message="No qualification record found for this lead.",
            status_code=404,
        )
    return DataResponse(data=QualificationResponse.model_validate(latest))


@router.get("/{lead_id}/qualification/history", response_model=DataResponse[QualificationHistoryResponse])
def get_qualification_history(
    lead_id: uuid.UUID,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get historical qualification records for a lead.
    """
    qualifications = QualificationService.get_qualification_history(db, lead_id, limit=limit)
    latest = qualifications[0] if qualifications else None
    qual_responses = [QualificationResponse.model_validate(q) for q in qualifications]

    return DataResponse(
        data=QualificationHistoryResponse(
            lead_id=lead_id,
            total_qualifications=len(qualifications),
            latest_qualification=QualificationResponse.model_validate(latest) if latest else None,
            qualifications=qual_responses,
        )
    )


@router.post("/{lead_id}/qualification/override", response_model=DataResponse[QualificationResponse])
def apply_qualification_override(
    lead_id: uuid.UUID,
    data: QualificationOverrideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Apply a human override decision to the latest qualification for a lead.
    """
    updated = QualificationService.apply_override(
        db,
        lead_id=lead_id,
        override_decision=data.decision,
        override_reason=data.reason,
        user_id=current_user.id,
    )
    return DataResponse(data=QualificationResponse.model_validate(updated))
