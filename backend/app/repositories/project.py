"""Repository layer for Project Initiation, Delivery Planning & Execution Management."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, update, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class ProjectRepository:
    """Repository handling project execution entities and relational dependency validation."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, project: Project) -> Project:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_project_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        stmt = (
            select(Project)
            .where(Project.id == project_id)
            .options(
                selectinload(Project.members),
                selectinload(Project.tasks),
                selectinload(Project.milestones),
                selectinload(Project.deliverables),
                selectinload(Project.risks),
                selectinload(Project.blockers),
                selectinload(Project.client_dependencies),
                selectinload(Project.assumptions),
                selectinload(Project.scope_signals),
                selectinload(Project.effort_entries),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_projects(
        self,
        status: Optional[str] = None,
        health: Optional[str] = None,
        business_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Project], int]:
        query = select(Project)
        if status:
            query = query.where(Project.status == status)
        if health:
            query = query.where(Project.health == health)
        if business_id:
            query = query.where(Project.business_id == business_id)

        count_stmt = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        query = query.order_by(Project.created_at.desc()).offset(skip).limit(limit)
        results = (await self.db.execute(query)).scalars().all()
        return list(results), total

    async def create_task(self, task: ProjectTask) -> ProjectTask:
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def get_task_by_id(self, task_id: uuid.UUID) -> Optional[ProjectTask]:
        stmt = select(ProjectTask).where(ProjectTask.id == task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_project_tasks(self, project_id: uuid.UUID) -> List[ProjectTask]:
        stmt = select(ProjectTask).where(ProjectTask.project_id == project_id).order_by(ProjectTask.created_at.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_task_dependency(self, dep: TaskDependency) -> TaskDependency:
        self.db.add(dep)
        await self.db.flush()
        await self.db.refresh(dep)
        return dep

    async def list_task_dependencies(self, project_id: uuid.UUID) -> List[TaskDependency]:
        stmt = select(TaskDependency).where(TaskDependency.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def check_circular_dependency(
        self, project_id: uuid.UUID, predecessor_id: uuid.UUID, successor_id: uuid.UUID
    ) -> bool:
        """Verify if adding predecessor -> successor creates a circular dependency graph."""
        if predecessor_id == successor_id:
            return True

        dependencies = await self.list_task_dependencies(project_id)
        adj: Dict[uuid.UUID, List[uuid.UUID]] = {}
        for d in dependencies:
            adj.setdefault(d.predecessor_task_id, []).append(d.successor_task_id)

        # Add proposed edge
        adj.setdefault(predecessor_id, []).append(successor_id)

        # BFS to detect if successor can reach predecessor
        visited = set()
        queue = [successor_id]
        while queue:
            curr = queue.pop(0)
            if curr == predecessor_id:
                return True
            if curr not in visited:
                visited.add(curr)
                queue.extend(adj.get(curr, []))

        return False

    async def create_milestone(self, milestone: ProjectMilestone) -> ProjectMilestone:
        self.db.add(milestone)
        await self.db.flush()
        await self.db.refresh(milestone)
        return milestone

    async def list_project_milestones(self, project_id: uuid.UUID) -> List[ProjectMilestone]:
        stmt = select(ProjectMilestone).where(ProjectMilestone.project_id == project_id).order_by(ProjectMilestone.target_date.asc().nulls_last())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_deliverable(self, deliverable: ProjectDeliverable) -> ProjectDeliverable:
        self.db.add(deliverable)
        await self.db.flush()
        await self.db.refresh(deliverable)
        return deliverable

    async def list_project_deliverables(self, project_id: uuid.UUID) -> List[ProjectDeliverable]:
        stmt = select(ProjectDeliverable).where(ProjectDeliverable.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_risk(self, risk: ProjectRisk) -> ProjectRisk:
        self.db.add(risk)
        await self.db.flush()
        await self.db.refresh(risk)
        return risk

    async def list_project_risks(self, project_id: uuid.UUID) -> List[ProjectRisk]:
        stmt = select(ProjectRisk).where(ProjectRisk.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_blocker(self, blocker: ProjectBlocker) -> ProjectBlocker:
        self.db.add(blocker)
        await self.db.flush()
        await self.db.refresh(blocker)
        return blocker

    async def list_project_blockers(self, project_id: uuid.UUID) -> List[ProjectBlocker]:
        stmt = select(ProjectBlocker).where(ProjectBlocker.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_client_dependency(self, dep: ClientDependency) -> ClientDependency:
        self.db.add(dep)
        await self.db.flush()
        await self.db.refresh(dep)
        return dep

    async def list_client_dependencies(self, project_id: uuid.UUID) -> List[ClientDependency]:
        stmt = select(ClientDependency).where(ClientDependency.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_effort_entry(self, entry: EffortEntry) -> EffortEntry:
        self.db.add(entry)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def list_effort_entries(self, project_id: uuid.UUID) -> List[EffortEntry]:
        stmt = select(EffortEntry).where(EffortEntry.project_id == project_id).order_by(EffortEntry.log_date.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_health_snapshot(self, snapshot: ProjectHealthSnapshot) -> ProjectHealthSnapshot:
        self.db.add(snapshot)
        await self.db.flush()
        await self.db.refresh(snapshot)
        return snapshot
