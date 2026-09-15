"""REST API endpoints for Risk & Quality Engine."""

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.risk import RiskAssessmentResponse, RiskCheckRequest, RiskOverrideRequest
from app.services.risk import RiskService

router = APIRouter(prefix="", tags=["Risk & Quality Engine"])


@router.post("/risk/check", response_model=DataResponse[RiskAssessmentResponse])
async def check_risk(
    payload: RiskCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Evaluate an artifact for safety, evidence traceability, and quality."""
    try:
        draft_id = uuid.UUID(payload.artifact_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid artifact_id format")

    assessment = await RiskService.evaluate_outreach_draft(db, draft_id)
    return DataResponse(data=RiskAssessmentResponse.model_validate(assessment))


@router.get("/risk/assessments/{id}", response_model=DataResponse[RiskAssessmentResponse])
def get_assessment(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Fetch a specific risk assessment by ID."""
    assessment = RiskService.get_assessment_by_id(db, id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    return DataResponse(data=RiskAssessmentResponse.model_validate(assessment))


@router.get("/outreach/drafts/{id}/risk", response_model=DataResponse[RiskAssessmentResponse])
def get_outreach_draft_risk(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Fetch the latest risk assessment for an outreach draft."""
    assessment = RiskService.get_latest_assessment(db, str(id))
    if not assessment:
        raise HTTPException(status_code=404, detail="No risk assessment found for draft")
    return DataResponse(data=RiskAssessmentResponse.model_validate(assessment))


@router.post("/risk/assessments/{id}/override", response_model=DataResponse[RiskAssessmentResponse])
def override_assessment(
    id: uuid.UUID,
    payload: RiskOverrideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Record a human reviewer override for a risk finding or assessment decision."""
    assessment = RiskService.record_override(db, id, current_user.id, payload.decision, payload.reason)
    return DataResponse(data=RiskAssessmentResponse.model_validate(assessment))
