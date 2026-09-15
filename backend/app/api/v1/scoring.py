import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.score import LeadScoreHistoryResponse, LeadScoreResponse
from app.services.scoring import ScoringService

router = APIRouter(prefix="/scoring", tags=["Lead Scoring System"])


@router.post("/leads/{lead_id}/calculate", response_model=DataResponse[LeadScoreResponse])
def calculate_lead_score(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate or recalculate opportunity score for a lead.
    """
    score = ScoringService.calculate_lead_score(db, lead_id, user_id=current_user.id)
    return DataResponse(data=LeadScoreResponse.model_validate(score))


@router.get("/leads/{lead_id}", response_model=DataResponse[LeadScoreResponse])
def get_lead_score(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current opportunity score for a lead.
    """
    score = ScoringService.get_lead_score(db, lead_id)
    return DataResponse(data=LeadScoreResponse.model_validate(score))


@router.get("/leads/{lead_id}/history", response_model=DataResponse[LeadScoreHistoryResponse])
def get_lead_score_history(
    lead_id: uuid.UUID,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get historical score snapshots for a lead.
    """
    scores = ScoringService.get_lead_score_history(db, lead_id, limit=limit)
    latest = scores[0] if scores else None

    resp = LeadScoreHistoryResponse(
        lead_id=lead_id,
        total_scores=len(scores),
        latest_score=LeadScoreResponse.model_validate(latest) if latest else None,
        history=[LeadScoreResponse.model_validate(s) for s in scores],
    )
    return DataResponse(data=resp)


@router.get("/businesses/{business_id}", response_model=DataResponse[LeadScoreResponse])
def get_business_score(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get latest opportunity score for a business.
    """
    score = ScoringService.get_business_score(db, business_id)
    return DataResponse(data=LeadScoreResponse.model_validate(score))
