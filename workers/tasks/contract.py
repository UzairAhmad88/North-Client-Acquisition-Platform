"""Celery background worker task for async Contract Agent section generation and discrepancy detection."""

import asyncio
import logging
import uuid
from app.db.session import SessionLocal
from app.services.contract import ContractService

logger = logging.getLogger(__name__)


def execute_contract_task(contract_id_str: str) -> None:
    """Background task generating contract sections, evaluating completeness, and detecting discrepancies."""
    logger.info(f"Starting background contract task for contract {contract_id_str}")
    db = SessionLocal()
    try:
        contract_id = uuid.UUID(contract_id_str)
        contract_obj = asyncio.run(ContractService.generate_contract(db, contract_id))
        logger.info(
            f"Contract generation completed for contract {contract_id_str}: Status={contract_obj.status}, Version={contract_obj.version}"
        )
    except Exception as exc:
        logger.error(f"Failed background contract task for contract {contract_id_str}: {exc}")
    finally:
        db.close()
