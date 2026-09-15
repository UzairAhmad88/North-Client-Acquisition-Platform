"""Central Workflow Engine managing execution, transitions, and wait states."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orchestration import (
    HumanTask,
    HumanTaskStatus,
    TaskPriority,
    TaskType,
    WorkflowApproval,
    WorkflowCancellation,
    WorkflowRun,
    WorkflowRunStep,
    WorkflowStatus,
    WorkflowStepStatus,
    WorkflowWaitState,
)
from app.orchestration.dispatcher import TaskDispatcher
from app.orchestration.state_machine import WorkflowStateMachine
from app.orchestration.workflow_registry import global_workflow_registry


class WorkflowEngine:
    """Central engine orchestrating declarative workflows across business lifecycles."""

    @staticmethod
    async def start_workflow(
        db: AsyncSession,
        tenant_id: str,
        workflow_key: str,
        input_data: Optional[Dict[str, Any]] = None,
        trigger_type: str = "EVENT",
        trigger_reference: Optional[str] = None,
    ) -> WorkflowRun:
        """Instantiate and start a new workflow run from registered template."""
        template = global_workflow_registry.get(workflow_key)
        if not template:
            raise ValueError(f"Workflow template '{workflow_key}' not found in registry.")

        initial_step = template.steps[0] if template.steps else None
        correlation_id = f"corr_{uuid.uuid4().hex[:12]}"

        run = WorkflowRun(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            workflow_key=workflow_key,
            workflow_version=template.version,
            trigger_type=trigger_type,
            trigger_reference=trigger_reference,
            status=WorkflowStatus.RUNNING,
            current_step=initial_step.step_key if initial_step else None,
            correlation_id=correlation_id,
            input_data=input_data or {},
            output_data={},
            started_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(run)

        # Create first step record
        if initial_step:
            step_record = WorkflowRunStep(
                id=str(uuid.uuid4()),
                workflow_run_id=run.id,
                step_key=initial_step.step_key,
                step_type=initial_step.step_type,
                status=WorkflowStepStatus.RUNNING,
                attempt_count=1,
                input_data=input_data or {},
                started_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(step_record)

            # If the initial step is a human task, create human task queue entry
            if initial_step.step_type == TaskType.HUMAN_TASK:
                run.status = WorkflowStatus.WAITING
                human_task = HumanTask(
                    id=str(uuid.uuid4()),
                    tenant_id=tenant_id,
                    workflow_run_id=run.id,
                    step_key=initial_step.step_key,
                    title=f"Review: {initial_step.name}",
                    description=f"Action required for workflow {template.name}",
                    task_type=initial_step.config.get("task_type", "HUMAN_APPROVAL"),
                    priority=TaskPriority.HIGH,
                    status=HumanTaskStatus.PENDING,
                    input_data=input_data or {},
                    created_at=datetime.utcnow(),
                )
                db.add(human_task)

                wait_state = WorkflowWaitState(
                    id=str(uuid.uuid4()),
                    workflow_run_id=run.id,
                    step_key=initial_step.step_key,
                    wait_type="HUMAN_APPROVAL",
                    condition_data={"task_id": human_task.id},
                    status="WAITING",
                    created_at=datetime.utcnow(),
                )
                db.add(wait_state)

        await db.commit()
        return run

    @staticmethod
    async def advance_workflow(
        db: AsyncSession,
        workflow_run_id: str,
        step_key: str,
        step_output: Optional[Dict[str, Any]] = None,
    ) -> WorkflowRun:
        """Complete current step and transition to the next step or complete workflow."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError(f"WorkflowRun '{workflow_run_id}' not found.")

        template = global_workflow_registry.get(run.workflow_key)
        if not template:
            raise ValueError(f"Workflow template '{run.workflow_key}' not found.")

        # 1. Mark current step succeeded
        stmt_step = select(WorkflowRunStep).where(
            WorkflowRunStep.workflow_run_id == workflow_run_id,
            WorkflowRunStep.step_key == step_key,
        )
        res_step = await db.execute(stmt_step)
        current_step_record = res_step.scalar_one_or_none()
        if current_step_record:
            current_step_record.status = WorkflowStepStatus.SUCCEEDED
            current_step_record.output_data = step_output or {}
            current_step_record.completed_at = datetime.utcnow()
            if current_step_record.started_at:
                current_step_record.duration_ms = (
                    datetime.utcnow() - current_step_record.started_at
                ).total_seconds() * 1000.0

        # Merge step output into run output data
        if step_output:
            run.output_data[step_key] = step_output

        # 2. Determine next step
        next_step_keys = template.get_next_steps(step_key)
        if next_step_keys:
            next_key = next_step_keys[0]
            next_step_def = template.get_step(next_key)
            run.current_step = next_key
            run.status = WorkflowStatus.RUNNING

            next_step_record = WorkflowRunStep(
                id=str(uuid.uuid4()),
                workflow_run_id=run.id,
                step_key=next_key,
                step_type=next_step_def.step_type if next_step_def else TaskType.AGENT_TASK,
                status=WorkflowStepStatus.RUNNING,
                attempt_count=1,
                input_data=step_output or {},
                started_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(next_step_record)

            if next_step_def and next_step_def.step_type == TaskType.HUMAN_TASK:
                run.status = WorkflowStatus.WAITING
                human_task = HumanTask(
                    id=str(uuid.uuid4()),
                    tenant_id=run.tenant_id,
                    workflow_run_id=run.id,
                    step_key=next_key,
                    title=f"Review: {next_step_def.name}",
                    description=f"Action required for workflow {template.name}",
                    task_type=next_step_def.config.get("task_type", "HUMAN_APPROVAL"),
                    priority=TaskPriority.HIGH,
                    status=HumanTaskStatus.PENDING,
                    input_data=step_output or {},
                    created_at=datetime.utcnow(),
                )
                db.add(human_task)

                wait_state = WorkflowWaitState(
                    id=str(uuid.uuid4()),
                    workflow_run_id=run.id,
                    step_key=next_key,
                    wait_type="HUMAN_APPROVAL",
                    condition_data={"task_id": human_task.id},
                    status="WAITING",
                    created_at=datetime.utcnow(),
                )
                db.add(wait_state)
        else:
            # Workflow completed
            run.status = WorkflowStatus.COMPLETED
            run.current_step = None
            run.completed_at = datetime.utcnow()

        await db.commit()
        return run

    @staticmethod
    async def pause_workflow(
        db: AsyncSession,
        workflow_run_id: str,
        actor: str,
    ) -> WorkflowRun:
        """Pause a running or waiting workflow."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError(f"WorkflowRun '{workflow_run_id}' not found.")

        run.status = WorkflowStatus.PAUSED
        run.paused_at = datetime.utcnow()
        await db.commit()
        return run

    @staticmethod
    async def resume_workflow(
        db: AsyncSession,
        workflow_run_id: str,
        actor: str,
    ) -> WorkflowRun:
        """Resume a paused workflow."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError(f"WorkflowRun '{workflow_run_id}' not found.")

        run.status = WorkflowStatus.RUNNING
        run.paused_at = None
        await db.commit()
        return run

    @staticmethod
    async def cancel_workflow(
        db: AsyncSession,
        workflow_run_id: str,
        cancelled_by: str,
        reason: str,
    ) -> WorkflowRun:
        """Cancel a workflow and record audit cancellation."""
        stmt = select(WorkflowRun).where(WorkflowRun.id == workflow_run_id)
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError(f"WorkflowRun '{workflow_run_id}' not found.")

        run.status = WorkflowStatus.CANCELLED
        run.cancelled_at = datetime.utcnow()

        cancellation = WorkflowCancellation(
            id=str(uuid.uuid4()),
            tenant_id=run.tenant_id,
            workflow_run_id=run.id,
            cancelled_by=cancelled_by,
            reason=reason,
            created_at=datetime.utcnow(),
        )
        db.add(cancellation)
        await db.commit()
        return run

    @staticmethod
    async def handle_human_decision(
        db: AsyncSession,
        human_task_id: str,
        decision: str,  # APPROVED, REJECTED, REVISION_REQUIRED
        decision_reason: str,
        actor: str,
        content_hash: Optional[str] = None,
    ) -> HumanTask:
        """Process a human review decision and resume the workflow if approved."""
        stmt = select(HumanTask).where(HumanTask.id == human_task_id)
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"HumanTask '{human_task_id}' not found.")

        task.status = (
            HumanTaskStatus.APPROVED if decision == "APPROVED"
            else HumanTaskStatus.REJECTED if decision == "REJECTED"
            else HumanTaskStatus.REVISION_REQUIRED
        )
        task.decision = decision
        task.decision_reason = decision_reason
        task.assigned_to = actor
        task.completed_at = datetime.utcnow()

        if decision == "APPROVED":
            approval = WorkflowApproval(
                id=str(uuid.uuid4()),
                tenant_id=task.tenant_id,
                workflow_run_id=task.workflow_run_id,
                step_key=task.step_key,
                approved_by=actor,
                content_hash=content_hash or "APPROVED_NO_HASH",
                notes=decision_reason,
                created_at=datetime.utcnow(),
            )
            db.add(approval)
            await db.commit()

            # Advance workflow
            await WorkflowEngine.advance_workflow(
                db,
                workflow_run_id=task.workflow_run_id,
                step_key=task.step_key,
                step_output={"human_decision": "APPROVED", "approved_by": actor},
            )
        elif decision == "REJECTED":
            await db.commit()
            # Cancel or fail the workflow run
            await WorkflowEngine.cancel_workflow(
                db,
                workflow_run_id=task.workflow_run_id,
                cancelled_by=actor,
                reason=f"Human reviewer rejected task '{task.step_key}': {decision_reason}",
            )
        else:
            await db.commit()

        return task
