"""Durable Crash Recovery & Timeout Detection Engine for Phase 34."""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orchestration import (
    WorkflowRun,
    WorkflowRunStep,
    WorkflowStatus,
    WorkflowStepStatus,
    WorkflowTask,
)


class WorkflowRecoveryEngine:
    """Detects stalled or timed-out workflows and tasks, restoring them to healthy states."""

    @staticmethod
    async def recover_stale_tasks(
        db: AsyncSession,
        timeout_minutes: int = 15,
    ) -> int:
        """Find tasks stuck in 'RUNNING' status past timeout window and requeue or fail them."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        stmt = select(WorkflowTask).where(
            WorkflowTask.status == "RUNNING",
            WorkflowTask.scheduled_at < cutoff_time,
        )
        result = await db.execute(stmt)
        stale_tasks = result.scalars().all()

        recovered_count = 0
        for task in stale_tasks:
            if task.current_attempt < task.max_attempts:
                task.status = "QUEUED"
                task.scheduled_at = datetime.utcnow()
                recovered_count += 1
            else:
                task.status = "FAILED"
                recovered_count += 1

        if stale_tasks:
            await db.commit()
        return recovered_count

    @staticmethod
    async def detect_workflow_timeouts(
        db: AsyncSession,
        max_runtime_hours: int = 24,
    ) -> int:
        """Find workflow runs executing beyond maximum allowed runtime and transition them to EXPIRED."""
        cutoff = datetime.utcnow() - timedelta(hours=max_runtime_hours)
        stmt = select(WorkflowRun).where(
            WorkflowRun.status.in_([WorkflowStatus.RUNNING, WorkflowStatus.WAITING]),
            WorkflowRun.started_at < cutoff,
        )
        result = await db.execute(stmt)
        expired_runs = result.scalars().all()

        for run in expired_runs:
            run.status = WorkflowStatus.EXPIRED
            run.error_code = "WORKFLOW_TIMEOUT"
            run.error_summary = f"Workflow exceeded maximum allowed runtime of {max_runtime_hours} hours."
            run.completed_at = datetime.utcnow()

        if expired_runs:
            await db.commit()
        return len(expired_runs)
