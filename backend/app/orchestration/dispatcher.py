"""Task Dispatcher managing prioritized queue assignment and task dispatching."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orchestration import TaskPriority, TaskType, WorkflowTask, WorkflowTaskAttempt


class TaskDispatcher:
    """Dispatches workflow tasks to prioritized execution queues."""

    @staticmethod
    async def dispatch_task(
        db: AsyncSession,
        tenant_id: str,
        workflow_run_id: str,
        step_key: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.NORMAL,
        payload: Optional[Dict[str, Any]] = None,
        queue_name: str = "default",
    ) -> WorkflowTask:
        """Create and enqueue a new workflow task."""
        task = WorkflowTask(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            workflow_run_id=workflow_run_id,
            step_key=step_key,
            task_type=task_type,
            priority=priority,
            queue_name=queue_name,
            payload=payload or {},
            status="QUEUED",
            max_attempts=3,
            current_attempt=0,
            scheduled_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(task)
        await db.commit()
        return task

    @staticmethod
    async def fetch_next_task(
        db: AsyncSession,
        queue_name: str = "default",
    ) -> Optional[WorkflowTask]:
        """Fetch the highest priority queued task from the queue."""
        stmt = (
            select(WorkflowTask)
            .where(
                WorkflowTask.queue_name == queue_name,
                WorkflowTask.status == "QUEUED",
            )
            .order_by(
                WorkflowTask.priority.desc(),
                WorkflowTask.scheduled_at.asc(),
            )
            .limit(1)
        )
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        if task:
            task.status = "RUNNING"
            task.current_attempt += 1
            await db.commit()
        return task
