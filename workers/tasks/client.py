"""Celery background worker tasks for Client Collaboration AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from agents.client_collaboration.agent import ClientCollaborationAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.client.execute_client_collaboration_agent_task")
def execute_client_collaboration_agent_task(project_id: str, action: str = "CLASSIFY_REQUEST", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background client request classification or feedback summarization."""
    logger.info(f"Starting Client Collaboration AI agent task for project {project_id} with action {action}")

    async def _run():
        agent = ClientCollaborationAgent()
        params = payload or {}
        params["action"] = action
        params["project_id"] = project_id

        context = AgentContext(
            workflow_id="wf_client_worker",
            task_id=f"t_{project_id}",
            agent_run_id=None,
            metadata=params,
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
