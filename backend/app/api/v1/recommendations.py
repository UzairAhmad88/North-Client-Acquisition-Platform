import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.schemas.recommendation import (
    RecommendationRejectRequest,
    ServiceRecommendationRead,
)
from app.services.recommendations import RecommendationService

router = APIRouter(tags=["Service Recommendations"])

rec_service = RecommendationService()


def _format_rec_read(rec) -> ServiceRecommendationRead:
    read_data = ServiceRecommendationRead.model_validate(rec)
    if hasattr(rec, "service") and rec.service:
        read_data.service_name = rec.service.name
        read_data.service_slug = rec.service.slug
    return read_data


@router.post("/leads/{lead_id}/recommendations/calculate", response_model=DataResponse[List[ServiceRecommendationRead]])
def calculate_lead_recommendations(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calculate and upsert service recommendations for a lead."""
    results = rec_service.calculate_lead_recommendations(db, lead_id)
    return DataResponse(data=[_format_rec_read(r) for r in results])


@router.get("/leads/{lead_id}/recommendations", response_model=PaginatedResponse[ServiceRecommendationRead])
def list_lead_recommendations(
    lead_id: uuid.UUID,
    status: Optional[str] = Query(default=None, description="Filter by status (SUGGESTED, ACCEPTED, REJECTED, STALE)"),
    min_score: Optional[float] = Query(default=None, ge=0.0, le=100.0, description="Minimum relevance score"),
    limit: int = Query(default=100, ge=1, le=100),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List service recommendations for a lead."""
    items, total = rec_service.list_recommendations(
        db, lead_id, status=status, min_score=min_score, limit=limit
    )

    formatted_items = [_format_rec_read(r) for r in items]
    return PaginatedResponse(
        data=formatted_items,
        pagination=PaginationMeta(
            total=total,
            page=page,
            page_size=limit,
            total_pages=(total + limit - 1) // limit if limit > 0 else 1,
        ),
    )


@router.get("/recommendations/{id}", response_model=DataResponse[ServiceRecommendationRead])
def get_recommendation(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get single service recommendation by ID."""
    rec = rec_service.get_recommendation(db, id)
    return DataResponse(data=_format_rec_read(rec))


@router.post("/recommendations/{id}/accept", response_model=DataResponse[ServiceRecommendationRead])
def accept_recommendation(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Accept a service recommendation."""
    rec = rec_service.accept_recommendation(db, id, current_user.id)
    return DataResponse(data=_format_rec_read(rec))


@router.post("/recommendations/{id}/reject", response_model=DataResponse[ServiceRecommendationRead])
def reject_recommendation(
    id: uuid.UUID,
    body: Optional[RecommendationRejectRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reject a service recommendation with an optional reason."""
    reason = body.reason if body else None
    rec = rec_service.reject_recommendation(db, id, current_user.id, reason=reason)
    return DataResponse(data=_format_rec_read(rec))
