"""Celery background worker tasks for Business Intelligence & Organizational Learning AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from agents.learning.agent import BusinessIntelligenceAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.analytics.execute_analytics_agent_task")
def execute_analytics_agent_task(tenant_id: str, action: str = "GENERATE_INSIGHTS", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background BI analysis, learning cycle, or hypothesis evaluation."""
    logger.info(f"Starting BI & Learning AI agent task for tenant {tenant_id} with action {action}")

    async def _run():
        agent = BusinessIntelligenceAgent()
        params = payload or {}
        params["action"] = action
        params["tenant_id"] = tenant_id

        context = AgentContext(
            workflow_id="wf_analytics_learning",
            task_id=f"t_{tenant_id}",
            agent_run_id=None,
            metadata=params,
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
