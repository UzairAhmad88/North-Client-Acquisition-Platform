"""REST API endpoints for Client Requirements & Discovery Intelligence System."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.requirements import (
    AnswerQuestionSchema,
    DiscoveryQuestionResponseSchema,
    DiscoverySessionCreateSchema,
    DiscoverySessionDetailSchema,
    DiscoverySessionResponseSchema,
    RequirementCreateSchema,
    RequirementResponseSchema,
    RequirementUpdateSchema,
    ScopeItemResponseSchema,
)
from app.services.requirements import RequirementsService

router = APIRouter(prefix="/discovery-sessions", tags=["Discovery Requirements"])


@router.post("", response_model=DiscoverySessionResponseSchema, status_code=status.HTTP_201_CREATED)
def create_discovery_session(
    payload: DiscoverySessionCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new discovery session for a business/lead."""
    session_obj = RequirementsService.create_discovery_session(
        db,
        business_id=payload.business_id,
        lead_id=payload.lead_id,
        conversation_id=payload.conversation_id,
        user_id=current_user.id,
        notes=payload.notes,
    )
    return session_obj


@router.get("", response_model=List[DiscoverySessionResponseSchema])
def list_discovery_sessions(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List discovery sessions with optional status filter."""
    return RequirementsService.list_discovery_sessions(db, status=status_filter, limit=limit, offset=offset)


@router.get("/{id}", response_model=DiscoverySessionDetailSchema)
def get_discovery_session_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve discovery session detail workspace with requirements, questions, and scope items."""
    session_obj = RequirementsService.get_discovery_session(db, id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Discovery session not found")
    return session_obj


@router.post("/{id}/analyze", response_model=DiscoverySessionDetailSchema)
async def analyze_discovery_session(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger AI requirements analysis and extraction for a discovery session."""
    try:
        session_obj = await RequirementsService.analyze_discovery_session(db, id)
        return session_obj
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/requirements/{req_id}/confirm", response_model=RequirementResponseSchema)
def confirm_requirement(
    id: uuid.UUID,
    req_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Explicitly confirm a requirement (Human Review)."""
    try:
        return RequirementsService.confirm_requirement(db, req_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/questions/{q_id}/answer", response_model=DiscoveryQuestionResponseSchema)
def answer_discovery_question(
    id: uuid.UUID,
    q_id: uuid.UUID,
    payload: AnswerQuestionSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit an answer to a discovery question."""
    try:
        return RequirementsService.answer_question(db, q_id, payload.answer_text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
