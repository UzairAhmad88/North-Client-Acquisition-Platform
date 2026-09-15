import asyncio
import uuid
from typing import Optional

from sqlalchemy.orm import Session

import agents.research  # Ensures ResearchAgent is registered
from agents.core.registry import global_registry
from app.services.agents import AgentRunRepository, AgentRuntimeService
from app.services.research import ResearchService


async def execute_research_task(
    db: Session,
    job_id: uuid.UUID,
    provider_type: str = "MOCK",
) -> None:
    """Asynchronous task worker function running Research Agent within Phase 14 runtime."""
    # 1. Fetch job to get business_id
    job = ResearchService.get_job(db, job_id)
    if not job:
        return

    # 2. Trigger Research Agent Run via AgentRuntimeService
    runtime_service = AgentRuntimeService()
    run = runtime_service.trigger_agent_run(
        db,
        agent_name="research_agent",
        business_id=job.business_id,
        workflow_id=f"wf-research-{job.id.hex[:8]}",
        input_data={"job_id": str(job.id), "requested_sections": job.requested_sections},
    )

    try:
        # Build least-privilege agent context
        context = runtime_service.build_context(
            db,
            workflow_id=run.workflow_id,
            task_id=run.task_id,
            agent_run_id=run.agent_run_id,
            business_id=job.business_id,
        )

        # Run Research Agent
        agent = global_registry.get("research_agent")
        result = await agent.run(context)

        # Also run Phase 10 provider persistence for backwards compatibility
        await ResearchService.run_job(db, job_id, provider_type=provider_type)

        # Update Agent Run completion status
        AgentRunRepository.update_run_status(
            db,
            run.id,
            status=result.status,
            output_summary=result.result,
            confidence=result.confidence,
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_COMPLETED", f"Research Agent finished with status {result.status}."
        )

    except Exception as e:
        AgentRunRepository.update_run_status(
            db, run.id, status="FAILED", error_message=str(e)
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_FAILED", f"Research Agent failed: {str(e)}"
        )
        raise e


def run_research_job_task_sync(
    db: Session,
    job_id: uuid.UUID,
    provider_type: str = "MOCK",
) -> None:
    """Synchronous wrapper for thread/process execution."""
    asyncio.run(execute_research_task(db, job_id, provider_type=provider_type))
