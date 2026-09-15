"""REST API endpoints for Solution Design Intelligence System."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.solution import (
    SolutionDesignCreateSchema,
    SolutionDesignDetailSchema,
    SolutionDesignResponseSchema,
)
from app.services.solution import SolutionService

router = APIRouter(prefix="/solutions", tags=["Solution Designs"])


@router.post("", response_model=SolutionDesignResponseSchema, status_code=status.HTTP_201_CREATED)
def create_solution_design(
    payload: SolutionDesignCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new solution design for a discovery session."""
    try:
        return SolutionService.create_solution_design(
            db,
            discovery_session_id=payload.discovery_session_id,
            user_id=current_user.id,
            overview=payload.overview,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[SolutionDesignResponseSchema])
def list_solution_designs(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List solution designs with optional status filter."""
    return SolutionService.list_solutions(db, status=status_filter, limit=limit, offset=offset)


@router.get("/{id}", response_model=SolutionDesignDetailSchema)
def get_solution_design_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve solution design workspace detail with features, deliverables, and architecture."""
    sol_obj = SolutionService.get_solution(db, id)
    if not sol_obj:
        raise HTTPException(status_code=404, detail="Solution design not found")
    return sol_obj


@router.post("/{id}/analyze", response_model=SolutionDesignDetailSchema)
async def analyze_solution_design(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger SolutionAgent analysis and feature mapping for a solution design."""
    try:
        return await SolutionService.analyze_solution_design(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/approve", response_model=SolutionDesignResponseSchema)
def approve_solution_design(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve a solution design workspace (Human Operator Action)."""
    try:
        return SolutionService.approve_solution_design(db, id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
