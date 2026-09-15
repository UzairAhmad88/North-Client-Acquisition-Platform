"""Celery background worker tasks for Post-Delivery Support, Maintenance & Client Success AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from agents.support.agent import SupportAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.support.execute_support_agent_task")
def execute_support_agent_task(client_account_id: str, action: str = "CLASSIFY_TICKET", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background Support classification, troubleshooting, warranty evaluation, or opportunity detection."""
    logger.info(f"Starting Support AI agent task for client {client_account_id} with action {action}")

    async def _run():
        agent = SupportAgent()
        params = payload or {}
        params["action"] = action
        params["client_account_id"] = client_account_id

        context = AgentContext(
            workflow_id="wf_support_worker",
            task_id=f"t_{client_account_id}",
            agent_run_id=None,
            metadata=params,
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
