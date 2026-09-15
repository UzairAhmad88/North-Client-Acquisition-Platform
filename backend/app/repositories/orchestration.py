"""Repository layer for Phase 34: Unified Workflow Orchestration, Event Bus & Automation."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.orchestration import (
    AutomationRule,
    AutomationRuleRun,
    DeadLetterMessage,
    DLQStatus,
    EventInbox,
    EventOutbox,
    EventRegistryItem,
    EventReplay,
    HumanTask,
    HumanTaskStatus,
    WorkflowApproval,
    WorkflowCancellation,
    WorkflowDefinition,
    WorkflowRun,
    WorkflowRunEvent,
    WorkflowRunStep,
    WorkflowSchedule,
    WorkflowStatus,
    WorkflowTask,
)


class OrchestrationRepository:
    """Database repository for workflows, events, tasks, automations, and DLQ."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # 1. Workflows
    async def list_workflow_runs(
        self,
        tenant_id: str,
        status: Optional[WorkflowStatus] = None,
        workflow_key: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[WorkflowRun]:
        stmt = (
            select(WorkflowRun)
            .where(WorkflowRun.tenant_id == tenant_id)
            .order_by(desc(WorkflowRun.started_at))
        )
        if status:
            stmt = stmt.where(WorkflowRun.status == status)
        if workflow_key:
            stmt = stmt.where(WorkflowRun.workflow_key == workflow_key)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_workflow_run(self, run_id: str) -> Optional[WorkflowRun]:
        stmt = (
            select(WorkflowRun)
            .options(
                selectinload(WorkflowRun.run_steps),
                selectinload(WorkflowRun.run_events),
            )
            .where(WorkflowRun.id == run_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 2. Events & Outbox
    async def list_events(
        self,
        tenant_id: str,
        event_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[EventOutbox]:
        stmt = (
            select(EventOutbox)
            .where(EventOutbox.tenant_id == tenant_id)
            .order_by(desc(EventOutbox.created_at))
        )
        if event_type:
            stmt = stmt.where(EventOutbox.event_type == event_type)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_event(self, event_id: str) -> Optional[EventOutbox]:
        stmt = select(EventOutbox).where(EventOutbox.event_id == event_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 3. Human Tasks
    async def list_human_tasks(
        self,
        tenant_id: str,
        status: Optional[HumanTaskStatus] = None,
        limit: int = 50,
    ) -> List[HumanTask]:
        stmt = (
            select(HumanTask)
            .where(HumanTask.tenant_id == tenant_id)
            .order_by(desc(HumanTask.created_at))
        )
        if status:
            stmt = stmt.where(HumanTask.status == status)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_human_task(self, task_id: str) -> Optional[HumanTask]:
        stmt = select(HumanTask).where(HumanTask.id == task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 4. Automations
    async def list_automation_rules(
        self,
        tenant_id: str,
        enabled_only: bool = False,
    ) -> List[AutomationRule]:
        stmt = (
            select(AutomationRule)
            .where(AutomationRule.tenant_id == tenant_id)
            .order_by(desc(AutomationRule.created_at))
        )
        if enabled_only:
            stmt = stmt.where(AutomationRule.enabled == True)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_automation_rule(self, rule_id: str) -> Optional[AutomationRule]:
        stmt = select(AutomationRule).where(AutomationRule.id == rule_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 5. Dead Letter Queue
    async def list_dead_letters(
        self,
        status: Optional[DLQStatus] = None,
        limit: int = 50,
    ) -> List[DeadLetterMessage]:
        stmt = select(DeadLetterMessage).order_by(desc(DeadLetterMessage.created_at))
        if status:
            stmt = stmt.where(DeadLetterMessage.status == status)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_dead_letter(self, dlq_id: str) -> Optional[DeadLetterMessage]:
        stmt = select(DeadLetterMessage).where(DeadLetterMessage.id == dlq_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
