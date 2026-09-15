"""Celery background worker tasks for Decision Intelligence & Predictive Operations AI Agent."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from agents.decision_intelligence.agent import DecisionIntelligenceAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.decision_intelligence.execute_decision_intelligence_task")
def execute_decision_intelligence_task(tenant_id: str, action: str = "GENERATE_PREDICTION", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Celery task executing background predictive inference, leakage verification, or decision support synthesis."""
    logger.info(f"Starting Decision Intelligence task for tenant {tenant_id} with action {action}")

    async def _run():
        agent = DecisionIntelligenceAgent()
        params = payload or {}
        params["action"] = action
        params["tenant_id"] = tenant_id

        context = AgentContext(
            workflow_id="wf_decision_intelligence",
            task_id=f"t_{tenant_id}",
            agent_run_id=f"run_di_{tenant_id}",
            metadata={"parameters": params},
        )

        res = await agent.execute(context)
        return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
