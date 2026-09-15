"""Celery background worker task for async Requirements Agent analysis."""

import asyncio
import logging
import uuid
from app.db.session import SessionLocal
from app.services.requirements import RequirementsService

logger = logging.getLogger(__name__)


def execute_requirements_analysis_task(session_id_str: str) -> None:
    """Background task evaluating discovery session requirements intelligence."""
    logger.info(f"Starting background requirements analysis task for discovery session {session_id_str}")
    db = SessionLocal()
    try:
        session_id = uuid.UUID(session_id_str)
        session_obj = asyncio.run(RequirementsService.analyze_discovery_session(db, session_id))
        logger.info(
            f"Requirements analysis completed for discovery session {session_id_str}: Readiness={session_obj.readiness_stage}, ReadinessScore={session_obj.readiness_score}"
        )
    except Exception as exc:
        logger.error(f"Failed background requirements analysis task for session {session_id_str}: {exc}")
    finally:
        db.close()
