"""Celery background worker task for async Risk & Quality Engine evaluation."""

import logging
import uuid
import asyncio
from app.db.session import SessionLocal
from app.services.risk import RiskService

logger = logging.getLogger(__name__)


def execute_risk_assessment_task(draft_id_str: str) -> None:
    """Background task evaluating risk assessment for outreach draft."""
    logger.info(f"Starting background risk assessment task for draft {draft_id_str}")
    db = SessionLocal()
    try:
        draft_id = uuid.UUID(draft_id_str)
        assessment = asyncio.run(RiskService.evaluate_outreach_draft(db, draft_id))
        logger.info(f"Risk assessment completed for draft {draft_id_str}: Decision={assessment.decision}, Level={assessment.risk_level}")
    except Exception as exc:
        logger.error(f"Failed background risk assessment task for draft {draft_id_str}: {exc}")
    finally:
        db.close()
