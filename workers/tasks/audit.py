import asyncio
import uuid
from typing import Optional
from sqlalchemy.orm import Session

import agents.audit  # Ensures AuditAgent is registered
from agents.core.registry import global_registry
from app.repositories.audit import AuditRepository
from app.services.agents import AgentRunRepository, AgentRuntimeService
from app.services.audit import AuditService


async def execute_audit_task(
    db: Session,
    job_id: uuid.UUID,
    runner_type: str = "MOCK",
) -> None:
    """Asynchronous task worker function running Audit Agent within Phase 14 runtime."""
    # 1. Fetch job to get business_id and target_url
    job = AuditRepository.get_job_by_id(db, job_id)
    if not job:
        return

    # 2. Trigger Audit Agent Run via AgentRuntimeService
    runtime_service = AgentRuntimeService()
    run = runtime_service.trigger_agent_run(
        db,
        agent_name="audit_agent",
        business_id=job.business_id,
        workflow_id=f"wf-audit-{job.id.hex[:8]}",
        input_data={"job_id": str(job.id), "target_url": job.target_url},
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

        # Run Audit Agent
        agent = global_registry.get("audit_agent")
        result = await agent.run(context)

        # Also run Phase 11 audit runner for persistence compatibility
        await AuditService.run_job(db, job_id, runner_type=runner_type)

        # Update Agent Run completion status
        AgentRunRepository.update_run_status(
            db,
            run.id,
            status=result.status,
            output_summary=result.result,
            confidence=result.confidence,
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_COMPLETED", f"Audit Agent finished with status {result.status}."
        )

    except Exception as e:
        AgentRunRepository.update_run_status(
            db, run.id, status="FAILED", error_message=str(e)
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_FAILED", f"Audit Agent failed: {str(e)}"
        )
        raise e


def run_audit_job_task_sync(
    db: Session,
    job_id: uuid.UUID,
    runner_type: str = "MOCK",
) -> None:
    """Synchronous wrapper for thread/process execution."""
    asyncio.run(execute_audit_task(db, job_id, runner_type=runner_type))
