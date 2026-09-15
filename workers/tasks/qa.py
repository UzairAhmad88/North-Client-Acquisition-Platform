"""Celery background worker tasks for Quality Assurance, UAT & Handover AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from agents.qa.agent import QAAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.qa.execute_qa_agent_task")
def execute_qa_agent_task(project_id: str, action: str = "GENERATE_TEST_CASES", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background QA test generation, defect triage, or release gate evaluation."""
    logger.info(f"Starting QA AI agent task for project {project_id} with action {action}")

    async def _run():
        agent = QAAgent()
        params = payload or {}
        params["action"] = action
        params["project_id"] = project_id

        context = AgentContext(
            workflow_id="wf_qa_worker",
            task_id=f"t_{project_id}",
            agent_run_id=None,
            metadata=params,
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
