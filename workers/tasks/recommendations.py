import asyncio
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.services.recommendations import RecommendationService


async def execute_recommendations_task(
    db: Session,
    lead_id: uuid.UUID,
) -> None:
    """Asynchronous task worker function to calculate service recommendations for a lead."""
    service = RecommendationService()
    service.calculate_lead_recommendations(db, lead_id)


def run_recommendations_job_task_sync(
    db: Session,
    lead_id: uuid.UUID,
) -> None:
    """Synchronous wrapper for thread/process execution."""
    asyncio.run(execute_recommendations_task(db, lead_id))
