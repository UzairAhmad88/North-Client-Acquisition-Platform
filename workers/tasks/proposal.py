"""Celery background worker task for async Proposal Agent generation."""

import asyncio
import logging
import uuid
from app.db.session import SessionLocal
from app.services.proposal import ProposalService

logger = logging.getLogger(__name__)


def execute_proposal_generation_task(proposal_id_str: str) -> None:
    """Background task generating proposal sections, itemization, and Risk Engine evaluation."""
    logger.info(f"Starting background proposal generation task for proposal {proposal_id_str}")
    db = SessionLocal()
    try:
        proposal_id = uuid.UUID(proposal_id_str)
        prop_obj = asyncio.run(ProposalService.generate_proposal(db, proposal_id))
        logger.info(
            f"Proposal generation completed for proposal {proposal_id_str}: Status={prop_obj.status}, PricingStatus={prop_obj.pricing_status}"
        )
    except Exception as exc:
        logger.error(f"Failed background proposal generation task for proposal {proposal_id_str}: {exc}")
    finally:
        db.close()
