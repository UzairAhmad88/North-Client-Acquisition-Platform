"""Celery background worker task for async Solution Agent analysis."""

import asyncio
import logging
import uuid
from app.db.session import SessionLocal
from app.services.solution import SolutionService

logger = logging.getLogger(__name__)


def execute_solution_design_task(solution_id_str: str) -> None:
    """Background task evaluating solution design feature mapping and architecture specs."""
    logger.info(f"Starting background solution design task for solution {solution_id_str}")
    db = SessionLocal()
    try:
        solution_id = uuid.UUID(solution_id_str)
        sol_obj = asyncio.run(SolutionService.analyze_solution_design(db, solution_id))
        logger.info(
            f"Solution design analysis completed for solution {solution_id_str}: Status={sol_obj.status}, Complexity={sol_obj.complexity_tier}"
        )
    except Exception as exc:
        logger.error(f"Failed background solution design task for solution {solution_id_str}: {exc}")
    finally:
        db.close()
