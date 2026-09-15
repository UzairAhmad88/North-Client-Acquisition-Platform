"""Celery background tasks for Phase 34: Unified Workflow Orchestration, Event Bus & Automation."""

from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime

from workers.celery_app import celery_app
from app.database import async_session_factory
from app.events.outbox import OutboxPublisher
from app.events.bus import global_event_bus
from app.orchestration.dispatcher import TaskDispatcher
from app.orchestration.recovery import WorkflowRecoveryEngine
from app.services.orchestration import OrchestrationService


@celery_app.task(name="tasks.orchestration.process_outbox")
def process_outbox_events_task(batch_size: int = 50) -> Dict[str, Any]:
    """Process pending outbox events and publish to event bus."""
    async def _async_run():
        async with async_session_factory() as session:
            publisher = OutboxPublisher(global_event_bus)
            published = await publisher.process_pending_outbox_events(session, batch_size=batch_size)
            return {"status": "SUCCESS", "published_count": published}

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return asyncio.run(_async_run())
    return loop.run_until_complete(_async_run())


@celery_app.task(name="tasks.orchestration.recover_stale_tasks")
def recover_stale_tasks_task(timeout_minutes: int = 15) -> Dict[str, Any]:
    """Recover stalled or timed out workflow tasks."""
    async def _async_run():
        async with async_session_factory() as session:
            recovered = await WorkflowRecoveryEngine.recover_stale_tasks(session, timeout_minutes=timeout_minutes)
            timeouts = await WorkflowRecoveryEngine.detect_workflow_timeouts(session, max_runtime_hours=24)
            return {"status": "SUCCESS", "recovered_tasks": recovered, "expired_workflows": timeouts}

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return asyncio.run(_async_run())
    return loop.run_until_complete(_async_run())
