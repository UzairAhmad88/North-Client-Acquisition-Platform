"""Celery background worker task for async Estimation Agent effort and commercial calculation."""

import asyncio
import logging
import uuid
from app.db.session import SessionLocal
from app.services.estimate import EstimateService

logger = logging.getLogger(__name__)


def execute_estimation_task(estimate_id_str: str) -> None:
    """Background task evaluating project effort ranges, costs, and commercial range recommendations."""
    logger.info(f"Starting background project estimation task for estimate {estimate_id_str}")
    db = SessionLocal()
    try:
        estimate_id = uuid.UUID(estimate_id_str)
        est_obj = asyncio.run(EstimateService.calculate_estimate(db, estimate_id))
        logger.info(
            f"Project estimation completed for estimate {estimate_id_str}: Status={est_obj.status}, Hours={est_obj.estimated_hours}, RecommendedRange=${est_obj.recommended_min}-${est_obj.recommended_max}"
        )
    except Exception as exc:
        logger.error(f"Failed background project estimation task for estimate {estimate_id_str}: {exc}")
    finally:
        db.close()
