"""REST API endpoints for Commercial & Technical Proposal Generation."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.proposal import (
    ProposalCreateSchema,
    ProposalDetailSchema,
    ProposalResponseSchema,
)
from app.services.proposal import ProposalService

router = APIRouter(prefix="/proposals", tags=["Proposals"])


@router.post("", response_model=ProposalResponseSchema, status_code=status.HTTP_201_CREATED)
def create_proposal(
    payload: ProposalCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new proposal draft for a solution design."""
    try:
        return ProposalService.create_proposal(
            db,
            solution_id=payload.solution_id,
            proposal_type=payload.proposal_type,
            user_id=current_user.id,
            title=payload.title,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ProposalResponseSchema])
def list_proposals(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List proposals with optional status filter."""
    return ProposalService.list_proposals(db, status=status_filter, limit=limit, offset=offset)


@router.get("/{id}", response_model=ProposalDetailSchema)
def get_proposal_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve proposal detail workspace with items and version history."""
    prop_obj = ProposalService.get_proposal(db, id)
    if not prop_obj:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return prop_obj


@router.post("/{id}/generate", response_model=ProposalDetailSchema)
async def generate_proposal(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger ProposalAgent composition, claim evidence validation, and Risk Engine evaluation."""
    try:
        return await ProposalService.generate_proposal(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/approve", response_model=ProposalResponseSchema)
def approve_proposal(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve a proposal draft (Human Operator Action)."""
    try:
        return ProposalService.approve_proposal(db, id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
