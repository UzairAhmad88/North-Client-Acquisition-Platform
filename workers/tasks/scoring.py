import asyncio
import uuid

from app.services.scoring import ScoringService
from sqlalchemy.orm import Session


async def execute_scoring_task(
    db: Session,
    lead_id: uuid.UUID,
    user_id: uuid.UUID | None = None,
) -> None:
    """
    Asynchronous task worker function to run lead scoring calculation in background.
    """
    ScoringService.calculate_lead_score(db, lead_id, user_id=user_id)


def run_scoring_job_task_sync(
    db: Session,
    lead_id: uuid.UUID,
    user_id: uuid.UUID | None = None,
) -> None:
    """
    Synchronous wrapper for thread/process execution.
    """
    asyncio.run(execute_scoring_task(db, lead_id, user_id=user_id))
