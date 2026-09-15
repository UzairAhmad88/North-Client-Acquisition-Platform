"""Service orchestration layer for Phase 34."""

import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent
from app.events.bus import global_event_bus
from app.events.dlq import DLQManager
from app.events.outbox import OutboxPublisher
from app.events.replay import EventReplayEngine
from app.models.orchestration import (
    AutomationRule,
    AutomationRuleRun,
    DLQStatus,
    EventOutbox,
    EventReplay,
    HumanTask,
    ReplayMode,
    WorkflowRun,
    WorkflowStatus,
)
from app.orchestration.engine import WorkflowEngine
from app.orchestration.workflow_registry import global_workflow_registry
from app.repositories.orchestration import OrchestrationRepository


class OrchestrationService:
    """Unified application service coordinating workflows, events, tasks, and automations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = OrchestrationRepository(db)
        self.outbox_pub = OutboxPublisher(global_event_bus)

    # 1. Workflows
    async def start_workflow(
        self,
        tenant_id: str,
        workflow_key: str,
        input_data: Optional[Dict[str, Any]] = None,
        trigger_type: str = "MANUAL",
        trigger_reference: Optional[str] = None,
    ) -> WorkflowRun:
        run = await WorkflowEngine.start_workflow(
            self.db,
            tenant_id=tenant_id,
            workflow_key=workflow_key,
            input_data=input_data,
            trigger_type=trigger_type,
            trigger_reference=trigger_reference,
        )

        # Emit domain event for workflow start
        event = DomainEvent(
            event_type="workflow.started",
            tenant_id=tenant_id,
            aggregate_type="workflow_run",
            aggregate_id=run.id,
            producer="workflow_engine",
            correlation_id=run.correlation_id,
            payload={"workflow_key": workflow_key, "run_id": run.id},
        )
        await self.outbox_pub.record_outbox_event(self.db, event)
        await self.db.commit()
        return run

    async def pause_workflow(self, run_id: str, actor: str) -> WorkflowRun:
        return await WorkflowEngine.pause_workflow(self.db, run_id, actor)

    async def resume_workflow(self, run_id: str, actor: str) -> WorkflowRun:
        return await WorkflowEngine.resume_workflow(self.db, run_id, actor)

    async def cancel_workflow(self, run_id: str, actor: str, reason: str) -> WorkflowRun:
        return await WorkflowEngine.cancel_workflow(self.db, run_id, actor, reason)

    async def advance_step(self, run_id: str, step_key: str, output: Optional[Dict[str, Any]] = None) -> WorkflowRun:
        return await WorkflowEngine.advance_workflow(self.db, run_id, step_key, output)

    # 2. Human Tasks
    async def complete_human_task(
        self,
        task_id: str,
        decision: str,
        decision_reason: str,
        actor: str,
        content_hash: Optional[str] = None,
    ) -> HumanTask:
        return await WorkflowEngine.handle_human_decision(
            self.db,
            human_task_id=task_id,
            decision=decision,
            decision_reason=decision_reason,
            actor=actor,
            content_hash=content_hash,
        )

    # 3. Automations
    async def create_automation_rule(
        self,
        tenant_id: str,
        name: str,
        description: str,
        trigger_type: str,
        trigger_config: Dict[str, Any],
        condition_config: Dict[str, Any],
        action_config: Dict[str, Any],
        created_by: str,
        requires_human_approval: bool = True,
    ) -> AutomationRule:
        rule = AutomationRule(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            name=name,
            description=description,
            version="v1.0",
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            condition_config=condition_config,
            action_config=action_config,
            enabled=True,
            requires_human_approval=requires_human_approval,
            created_by=created_by,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(rule)
        await self.db.commit()
        return rule

    async def toggle_automation_rule(self, rule_id: str, enabled: bool) -> Optional[AutomationRule]:
        rule = await self.repo.get_automation_rule(rule_id)
        if rule:
            rule.enabled = enabled
            rule.updated_at = datetime.utcnow()
            await self.db.commit()
        return rule

    # 4. Replay & DLQ
    async def replay_events(
        self,
        tenant_id: str,
        event_type: str,
        replay_mode: ReplayMode,
        triggered_by: str,
    ) -> EventReplay:
        return await EventReplayEngine.execute_replay(
            self.db,
            tenant_id=tenant_id,
            event_type=event_type,
            replay_mode=replay_mode,
            triggered_by=triggered_by,
        )

    async def retry_dlq_message(self, dlq_id: str) -> Optional[Any]:
        dlq_entry = await self.repo.get_dead_letter(dlq_id)
        if not dlq_entry:
            return None
        dlq_entry.status = DLQStatus.RETRY_SCHEDULED
        await self.db.commit()
        return dlq_entry
