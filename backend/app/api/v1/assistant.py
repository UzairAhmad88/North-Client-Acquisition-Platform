"""FastAPI endpoints for Platform Assistant and Grounded Question Answering."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.assistant.service import PlatformAssistantService
from app.models.user import User
from app.schemas.search import (
    AssistantQueryRequest,
    AssistantQueryResponseSchema,
)

router = APIRouter(prefix="/assistant", tags=["Platform Assistant"])
_assistant_service = PlatformAssistantService()


@router.post("/query", response_model=AssistantQueryResponseSchema, summary="Ask Platform Assistant")
def ask_assistant(
    request: AssistantQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ask natural-language question and receive grounded answer with source citations."""
    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    role = getattr(current_user, "role", "USER")

    return _assistant_service.ask(
        question=request.question,
        tenant_id=str(current_user.tenant_id),
        user_id=str(current_user.id),
        session_id=request.session_id,
        is_client=is_client,
        role=role,
    )


@router.get("/sessions/{session_id}/history", summary="Get Conversation History")
def get_session_history(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve message history for assistant conversation session."""
    return _assistant_service.get_session_history(session_id)
