"""Celery background worker task for async Response Agent analysis."""

import logging
import uuid
import asyncio
from app.db.session import SessionLocal
from app.services.response import ResponseService

logger = logging.getLogger(__name__)


def execute_response_analysis_task(conversation_id_str: str) -> None:
    """Background task evaluating conversation response intelligence analysis."""
    logger.info(f"Starting background response analysis task for conversation {conversation_id_str}")
    db = SessionLocal()
    try:
        conv_id = uuid.UUID(conversation_id_str)
        analysis = asyncio.run(ResponseService.analyze_conversation(db, conv_id))
        logger.info(f"Response analysis completed for conversation {conversation_id_str}: Intent={analysis.primary_intent}, NextAction={analysis.recommended_next_action}")
    except Exception as exc:
        logger.error(f"Failed background response analysis task for conversation {conversation_id_str}: {exc}")
    finally:
        db.close()
