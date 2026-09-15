"""Service layer for Project Initiation, Delivery Planning & Execution Management."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract, ContractBaseline
from app.models.project import (
    ClientDependency,
    EffortEntry,
    Project,
    ProjectAssumption,
    ProjectBlocker,
    ProjectDeliverable,
    ProjectHealthSnapshot,
    ProjectMember,
    ProjectMilestone,
    ProjectRisk,
    ProjectScopeSignal,
    ProjectTask,
    TaskDependency,
)
from app.repositories.project import ProjectRepository
from agents.core.risk.evaluator import SemanticRiskEvaluator


class ProjectService:
    """Service layer enforcing execution boundaries, health rules, and lifecycle transitions."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProjectRepository(db)
        self.risk_evaluator = SemanticRiskEvaluator()

    async def initialize_project_from_contract(
        self,
        contract: Contract,
        baseline: ContractBaseline,
        owner_id: Optional[uuid.UUID] = None,
    ) -> Project:
        """Initialize a new delivery project from a signed contract and locked baseline."""
        project_number = f"PRJ-{uuid.uuid4().hex[:8].upper()}"

        project = Project(
            project_number=project_number,
            name=f"Delivery: {contract.title}",
            description=contract.summary,
            business_id=contract.business_id,
            client_id=contract.lead_id,
            contract_id=contract.id,
            baseline_id=baseline.id,
            owner_id=owner_id,
            status="INITIATED",
            health="HEALTHY",
            priority="MEDIUM",
            progress_percent=0.0,
            total_estimated_hours=0.0,
            total_actual_hours=0.0,
        )

        project = await self.repo.create_project(project)

        # Automatically assign owner as member
        if owner_id:
            member = ProjectMember(
                project_id=project.id,
                user_id=owner_id,
                role="PROJECT_MANAGER",
                is_active=True,
            )
            self.db.add(member)
            await self.db.flush()

        return project

    async def transition_project_status(self, project_id: uuid.UUID, new_status: str) -> Project:
        """Enforce valid project lifecycle state machine transitions."""
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found.")

        valid_transitions = {
            "INITIATED": ["PLANNING", "CANCELLED"],
            "PLANNING": ["READY", "CANCELLED"],
            "READY": ["IN_PROGRESS", "ON_HOLD", "CANCELLED"],
            "IN_PROGRESS": ["ON_HOLD", "COMPLETED", "CANCELLED"],
            "ON_HOLD": ["IN_PROGRESS", "CANCELLED"],
            "COMPLETED": ["ARCHIVED"],
            "CANCELLED": ["ARCHIVED"],
            "ARCHIVED": [],
        }

        allowed = valid_transitions.get(project.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Invalid project status transition from '{project.status}' to '{new_status}'. Allowed: {allowed}"
            )

        project.status = new_status
        if new_status == "IN_PROGRESS" and not project.actual_start:
            project.actual_start = datetime.now(timezone.utc)
        elif new_status == "COMPLETED":
            project.actual_end = datetime.now(timezone.utc)
            project.health = "COMPLETED"
            project.progress_percent = 100.0

        project.version += 1
        await self.db.flush()
        return project

    async def add_task(
        self,
        project_id: uuid.UUID,
        name: str,
        description: str,
        priority: str = "MEDIUM",
        estimated_hours: float = 0.0,
        parent_task_id: Optional[uuid.UUID] = None,
        deliverable_id: Optional[uuid.UUID] = None,
        milestone_id: Optional[uuid.UUID] = None,
        assignee_id: Optional[uuid.UUID] = None,
        created_by_id: Optional[uuid.UUID] = None,
    ) -> ProjectTask:
        """Create a new WBS task or subtask."""
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found.")

        task_count = len(project.tasks) + 1
        task_number = f"TSK-{task_count:03d}"

        task = ProjectTask(
            project_id=project_id,
            parent_task_id=parent_task_id,
            deliverable_id=deliverable_id,
            milestone_id=milestone_id,
            task_number=task_number,
            name=name,
            description=description,
            status="TODO",
            priority=priority,
            assignee_id=assignee_id,
            created_by_id=created_by_id,
            estimated_hours=estimated_hours,
            actual_hours=0.0,
            progress_percent=0.0,
        )

        task = await self.repo.create_task(task)
        await self._recalculate_project_metrics(project_id)
        return task

    async def update_task_status(
        self, task_id: uuid.UUID, new_status: str, progress_percent: Optional[float] = None, blocked_reason: Optional[str] = None
    ) -> ProjectTask:
        """Update task status and trigger progress rollup."""
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found.")

        valid_statuses = {"TODO", "READY", "IN_PROGRESS", "BLOCKED", "IN_REVIEW", "COMPLETED", "CANCELLED"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid task status '{new_status}'.")

        task.status = new_status
        if new_status == "COMPLETED":
            task.progress_percent = 100.0
            task.actual_end = datetime.now(timezone.utc)
        elif new_status == "TODO":
            task.progress_percent = 0.0
        elif progress_percent is not None:
            task.progress_percent = max(0.0, min(100.0, progress_percent))

        if new_status == "BLOCKED":
            task.blocked_reason = blocked_reason or "Blocked by dependency or constraint"
        else:
            task.blocked_reason = None

        task.version += 1
        await self.db.flush()

        # Recalculate parent task progress if subtask
        if task.parent_task_id:
            await self._recalculate_parent_task(task.parent_task_id)

        await self._recalculate_project_metrics(task.project_id)
        await self.evaluate_project_health(task.project_id)
        return task

    async def add_task_dependency(
        self, project_id: uuid.UUID, predecessor_id: uuid.UUID, successor_id: uuid.UUID
    ) -> TaskDependency:
        """Add task dependency with circular graph check."""
        is_circular = await self.repo.check_circular_dependency(project_id, predecessor_id, successor_id)
        if is_circular:
            raise ValueError("Circular dependency graph detected. Cannot link task dependency.")

        dep = TaskDependency(
            project_id=project_id,
            predecessor_task_id=predecessor_id,
            successor_task_id=successor_id,
            dependency_type="FINISH_TO_START",
        )
        dep = await self.repo.create_task_dependency(dep)

        # Update successor dependency status if predecessor is not completed
        pred_task = await self.repo.get_task_by_id(predecessor_id)
        succ_task = await self.repo.get_task_by_id(successor_id)
        if pred_task and succ_task and pred_task.status != "COMPLETED":
            succ_task.dependency_status = "BLOCKED_BY_PREDECESSOR"
            await self.db.flush()

        return dep

    async def log_effort(
        self,
        project_id: uuid.UUID,
        task_id: uuid.UUID,
        user_id: uuid.UUID,
        hours: float,
        description: str,
    ) -> EffortEntry:
        """Log manual effort hours against task."""
        if hours <= 0:
            raise ValueError("Effort hours must be greater than zero.")

        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found.")

        entry = EffortEntry(
            project_id=project_id,
            task_id=task_id,
            user_id=user_id,
            log_date=datetime.now(timezone.utc),
            hours=hours,
            description=description,
            source="MANUAL",
        )

        entry = await self.repo.create_effort_entry(entry)
        task.actual_hours += hours
        await self.db.flush()

        await self._recalculate_project_metrics(project_id)
        await self.evaluate_project_health(project_id)
        return entry

    async def evaluate_project_health(self, project_id: uuid.UUID) -> ProjectHealthSnapshot:
        """Evaluate deterministic health rules engine."""
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found.")

        reasons: List[str] = []
        health = "HEALTHY"

        tasks = project.tasks
        milestones = project.milestones
        blockers = [b for b in project.blockers if b.get("status") in ("OPEN", "IN_PROGRESS")]
        client_deps = [c for c in project.client_dependencies if c.get("status") == "OVERDUE"]

        overdue_tasks = [t for t in tasks if t.status in ("TODO", "IN_PROGRESS") and t.planned_end and t.planned_end < datetime.now(timezone.utc)]
        blocked_tasks = [t for t in tasks if t.status == "BLOCKED"]
        missed_milestones = [m for m in milestones if m.status == "MISSED"]

        effort_variance = project.total_actual_hours - project.total_estimated_hours

        if len(blocked_tasks) >= 3 or len(missed_milestones) >= 1 or len(client_deps) >= 2:
            health = "CRITICAL"
            if len(blocked_tasks) >= 3:
                reasons.append(f"Severe execution block: {len(blocked_tasks)} tasks are blocked.")
            if missed_milestones:
                reasons.append(f"Missed {len(missed_milestones)} target delivery milestones.")
            if client_deps:
                reasons.append(f"{len(client_deps)} critical client dependencies are overdue.")

        elif len(overdue_tasks) >= 2 or len(blocked_tasks) >= 1 or effort_variance > 20.0:
            health = "AT_RISK"
            if overdue_tasks:
                reasons.append(f"{len(overdue_tasks)} tasks are overdue.")
            if blocked_tasks:
                reasons.append(f"{len(blocked_tasks)} task is blocked.")
            if effort_variance > 20.0:
                reasons.append(f"Effort variance exceeds estimate (+{effort_variance:.1f}h).")

        if project.status == "ON_HOLD":
            health = "BLOCKED"
            reasons.append("Project is explicitly on hold.")
        elif project.status == "COMPLETED":
            health = "COMPLETED"
            reasons.append("All project deliverables and tasks are completed.")

        if not reasons:
            reasons.append("All delivery milestones, tasks, and client dependencies are on schedule.")

        project.health = health
        await self.db.flush()

        snapshot = ProjectHealthSnapshot(
            project_id=project.id,
            health=health,
            reasons=reasons,
            schedule_variance_days=0,
            effort_variance_hours=effort_variance,
            overdue_task_count=len(overdue_tasks),
            blocked_task_count=len(blocked_tasks),
            unresolved_blocker_count=len(blockers),
        )

        return await self.repo.create_health_snapshot(snapshot)

    async def _recalculate_parent_task(self, parent_id: uuid.UUID) -> None:
        """Recalculate parent task progress based on subtasks."""
        parent = await self.repo.get_task_by_id(parent_id)
        if not parent or not parent.subtasks:
            return

        total_subtasks = len(parent.subtasks)
        subtask_progress_sum = sum(st.progress_percent for st in parent.subtasks)
        parent.progress_percent = round(subtask_progress_sum / total_subtasks, 2)
        if parent.progress_percent >= 100.0:
            parent.status = "COMPLETED"
        await self.db.flush()

    async def _recalculate_project_metrics(self, project_id: uuid.UUID) -> None:
        """Recalculate overall project progress, total estimated hours, and total actual hours."""
        project = await self.repo.get_project_by_id(project_id)
        if not project or not project.tasks:
            return

        tasks = project.tasks
        total_est = sum(t.estimated_hours for t in tasks)
        total_act = sum(t.actual_hours for t in tasks)

        if total_est > 0:
            weighted_sum = sum((t.progress_percent / 100.0) * t.estimated_hours for t in tasks)
            overall_pct = (weighted_sum / total_est) * 100.0
        else:
            completed = sum(1 for t in tasks if t.status == "COMPLETED")
            overall_pct = (completed / len(tasks)) * 100.0

        project.total_estimated_hours = total_est
        project.total_actual_hours = total_act
        project.progress_percent = round(overall_pct, 2)
        await self.db.flush()
