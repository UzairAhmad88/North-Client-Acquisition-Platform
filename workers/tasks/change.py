"""Celery background worker tasks for Change Management AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from agents.change_management.agent import ChangeAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.change.execute_change_agent_task")
def execute_change_agent_task(change_request_id: str, action: str = "CLASSIFY_CHANGE", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background Change Management classification, impact analysis, or PERT re-estimation."""
    logger.info(f"Starting Change AI agent task for request {change_request_id} with action {action}")

    async def _run():
        agent = ChangeAgent()
        params = payload or {}
        params["action"] = action
        params["change_request_id"] = change_request_id

        context = AgentContext(
            workflow_id="wf_change_worker",
            task_id=f"t_{change_request_id}",
            agent_run_id=None,
            metadata=params,
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
