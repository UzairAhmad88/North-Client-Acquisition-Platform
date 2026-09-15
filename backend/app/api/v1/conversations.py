"""REST API endpoints for Conversations and Response Intelligence."""

import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse
from app.schemas.response import (
    ConversationAnalysisResponse,
    ConversationDetailResponse,
    HumanCorrectionRequest,
)
from app.services.response import ResponseService

router = APIRouter(prefix="/conversations", tags=["Conversation & Response Intelligence"])


@router.get("", response_model=PaginatedResponse[ConversationDetailResponse])
def list_conversations(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List active conversations with optional status filtering."""
    items = ResponseService.list_conversations(db, limit=limit, offset=offset, status_filter=status)
    res_items = []
    for item in items:
        latest_analysis = ResponseService.get_latest_analysis(db, item.id)
        c_res = ConversationDetailResponse.model_validate(item)
        if latest_analysis:
            c_res.latest_analysis = ConversationAnalysisResponse.model_validate(latest_analysis)
        res_items.append(c_res)

    return PaginatedResponse(items=res_items, total=len(res_items), limit=limit, offset=offset)


@router.get("/{id}", response_model=DataResponse[ConversationDetailResponse])
def get_conversation(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Fetch conversation details, message timeline, and latest intelligence analysis."""
    conv = ResponseService.get_conversation_detail(db, id)
    latest_analysis = ResponseService.get_latest_analysis(db, id)
    c_res = ConversationDetailResponse.model_validate(conv)
    if latest_analysis:
        c_res.latest_analysis = ConversationAnalysisResponse.model_validate(latest_analysis)

    return DataResponse(data=c_res)


@router.post("/{id}/analyze", response_model=DataResponse[ConversationAnalysisResponse])
async def analyze_conversation(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Trigger Response Agent analysis for a conversation."""
    analysis = await ResponseService.analyze_conversation(db, id)
    return DataResponse(data=ConversationAnalysisResponse.model_validate(analysis))


@router.get("/{id}/analysis", response_model=DataResponse[ConversationAnalysisResponse])
def get_conversation_analysis(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Fetch latest analysis for a conversation."""
    analysis = ResponseService.get_latest_analysis(db, id)
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for conversation")
    return DataResponse(data=ConversationAnalysisResponse.model_validate(analysis))


@router.post("/{id}/correction", response_model=DataResponse[ConversationAnalysisResponse])
def record_correction(
    id: uuid.UUID,
    payload: HumanCorrectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Record human correction for AI intent or next action recommendation."""
    correction_data = {
        "corrected_intent": payload.corrected_intent,
        "corrected_next_action": payload.corrected_next_action,
        "reason": payload.reason,
    }
    updated = ResponseService.record_human_correction(db, id, current_user.id, correction_data)
    return DataResponse(data=ConversationAnalysisResponse.model_validate(updated))
