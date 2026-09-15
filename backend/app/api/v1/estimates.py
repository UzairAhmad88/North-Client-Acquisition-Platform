"""REST API endpoints for Project Estimation, Effort & Commercial Intelligence Engine."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.estimate import (
    ProjectEstimateCreateSchema,
    ProjectEstimateDetailSchema,
    ProjectEstimateResponseSchema,
)
from app.services.estimate import EstimateService

router = APIRouter(prefix="/estimates", tags=["Project Estimates"])


@router.post("", response_model=ProjectEstimateResponseSchema, status_code=status.HTTP_201_CREATED)
def create_estimate(
    payload: ProjectEstimateCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project estimate draft for a solution design."""
    try:
        return EstimateService.create_estimate(
            db, solution_id=payload.solution_id, user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ProjectEstimateResponseSchema])
def list_estimates(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List project estimates with optional status filter."""
    return EstimateService.list_estimates(db, status=status_filter, limit=limit, offset=offset)


@router.get("/{id}", response_model=ProjectEstimateDetailSchema)
def get_estimate_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve detailed project estimate workspace with WBS work items, costs, and scenarios."""
    est_obj = EstimateService.get_estimate(db, id)
    if not est_obj:
        raise HTTPException(status_code=404, detail="Project estimate not found")
    return est_obj


@router.post("/{id}/calculate", response_model=ProjectEstimateDetailSchema)
async def calculate_estimate(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger EstimationAgent effort calculation, PERT ranges, and commercial range recommendation."""
    try:
        return await EstimateService.calculate_estimate(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/approve", response_model=ProjectEstimateResponseSchema)
def approve_estimate(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve a commercial project estimate recommendation (Human Operator Action)."""
    try:
        return EstimateService.approve_estimate(db, id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
