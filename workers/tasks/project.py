"""Celery background worker tasks for Project AI Agent execution."""

import asyncio
import logging
from typing import Any, Dict
from workers.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from agents.project.agent import ProjectAgent
from agents.core.context import AgentContext

logger = logging.getLogger(__name__)


@celery_app.task(name="workers.tasks.project.execute_project_agent_task")
def execute_project_agent_task(project_id: str, action: str = "SUMMARIZE") -> Dict[str, Any]:
    """Celery task executing background project AI planning or health analysis."""
    logger.info(f"Starting Project AI agent background task for project {project_id} with action {action}")

    async def _run():
        async with AsyncSessionLocal() as db:
            from app.services.project import ProjectService
            service = ProjectService(db)
            project = await service.repo.get_project_by_id(project_id)
            if not project:
                return {"status": "FAILED", "error": f"Project {project_id} not found."}

            agent = ProjectAgent()
            context = AgentContext(
                workflow_id="wf_project_worker",
                task_id=f"t_{project_id}",
                agent_run_id=str(uuid.uuid4()),
                metadata={
                    "action": action,
                    "project_name": project.name,
                    "project_data": {
                        "id": str(project.id),
                        "name": project.name,
                        "status": project.status,
                        "health": project.health,
                        "progress_percent": project.progress_percent,
                    },
                    "tasks": [{"name": t.name, "status": t.status, "estimated_hours": t.estimated_hours, "actual_hours": t.actual_hours} for t in project.tasks],
                    "milestones": [{"name": m.name, "status": m.status} for m in project.milestones],
                    "blockers": [{"title": b.title, "status": b.status, "severity": b.severity} for b in project.blockers],
                    "risks": [{"title": r.title, "status": r.status} for r in project.risks],
                    "client_dependencies": [{"title": c.title, "status": c.status} for c in project.client_dependencies],
                },
            )


            res = await agent.execute(context)
            return {"status": "SUCCESS", "result": res}

    return asyncio.run(_run())
