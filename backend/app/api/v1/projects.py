"""REST API Endpoints for Project Initiation, Delivery Planning & Execution Management."""

import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.repositories.contract import ContractRepository
from app.schemas.project import (
    BlockerCreateSchema,
    ClientDependencyCreateSchema,
    EffortEntryCreateSchema,
    MilestoneCreateSchema,
    MilestoneResponseSchema,
    ProjectCreateSchema,
    ProjectDetailResponseSchema,
    ProjectResponseSchema,
    ProjectStatusUpdateSchema,
    RiskCreateSchema,
    TaskCreateSchema,
    TaskDependencyCreateSchema,
    TaskResponseSchema,
    TaskStatusUpdateSchema,
)
from app.services.project import ProjectService
from agents.core.context import AgentContext
from agents.project.agent import ProjectAgent

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Initialize a new delivery project from contract baseline."""
    contract_repo = ContractRepository(db)
    contract = await contract_repo.get_contract_by_id(payload.contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")

    baselines = await contract_repo.list_contract_baselines(payload.contract_id)
    if not baselines:
        raise HTTPException(status_code=400, detail="Contract has no locked baseline. Sign contract first.")

    service = ProjectService(db)
    project = await service.initialize_project_from_contract(
        contract=contract,
        baseline=baselines[0],
        owner_id=payload.owner_id or current_user.id,
    )
    return project


@router.get("", response_model=Dict[str, Any])
async def list_projects(
    status_filter: Optional[str] = Query(None, alias="status"),
    health_filter: Optional[str] = Query(None, alias="health"),
    business_id: Optional[uuid.UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List delivery projects with filtering and pagination."""
    service = ProjectService(db)
    items, total = await service.repo.list_projects(
        status=status_filter, health=health_filter, business_id=business_id, skip=skip, limit=limit
    )
    return {
        "items": [ProjectResponseSchema.model_validate(p) for p in items],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{project_id}", response_model=ProjectDetailResponseSchema)
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed project workspace."""
    service = ProjectService(db)
    project = await service.repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.patch("/{project_id}/status", response_model=ProjectResponseSchema)
async def update_project_status(
    project_id: uuid.UUID,
    payload: ProjectStatusUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Transition project lifecycle state."""
    service = ProjectService(db)
    try:
        project = await service.transition_project_status(project_id, payload.status)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{project_id}/tasks", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: uuid.UUID,
    payload: TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a new task or subtask to project WBS."""
    service = ProjectService(db)
    try:
        task = await service.add_task(
            project_id=project_id,
            name=payload.name,
            description=payload.description,
            priority=payload.priority,
            estimated_hours=payload.estimated_hours,
            parent_task_id=payload.parent_task_id,
            deliverable_id=payload.deliverable_id,
            milestone_id=payload.milestone_id,
            assignee_id=payload.assignee_id,
            created_by_id=current_user.id,
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task_status(
    task_id: uuid.UUID,
    payload: TaskStatusUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update task execution status and progress."""
    service = ProjectService(db)
    try:
        task = await service.update_task_status(
            task_id=task_id,
            new_status=payload.status,
            progress_percent=payload.progress_percent,
            blocked_reason=payload.blocked_reason,
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{project_id}/tasks/dependencies", status_code=status.HTTP_201_CREATED)
async def add_task_dependency(
    project_id: uuid.UUID,
    payload: TaskDependencyCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add task predecessor-successor dependency link."""
    service = ProjectService(db)
    try:
        dep = await service.add_task_dependency(
            project_id=project_id,
            predecessor_id=payload.predecessor_id,
            successor_id=payload.successor_id,
        )
        return {"status": "SUCCESS", "dependency_id": dep.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{project_id}/milestones", response_model=MilestoneResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_milestone(
    project_id: uuid.UUID,
    payload: MilestoneCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add delivery milestone target."""
    service = ProjectService(db)
    from app.models.project import ProjectMilestone

    milestone = ProjectMilestone(
        project_id=project_id,
        name=payload.name,
        description=payload.description,
        target_date=payload.target_date,
        owner_id=payload.owner_id or current_user.id,
        status="UPCOMING",
        progress_percent=0.0,
    )
    milestone = await service.repo.create_milestone(milestone)
    return milestone


@router.post("/{project_id}/effort", status_code=status.HTTP_201_CREATED)
async def log_effort(
    project_id: uuid.UUID,
    payload: EffortEntryCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Log actual effort hours against a task."""
    service = ProjectService(db)
    try:
        entry = await service.log_effort(
            project_id=project_id,
            task_id=payload.task_id,
            user_id=current_user.id,
            hours=payload.hours,
            description=payload.description,
        )
        return {"status": "SUCCESS", "effort_id": entry.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}/health")
async def get_project_health(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Evaluate and fetch deterministic project health."""
    service = ProjectService(db)
    try:
        snapshot = await service.evaluate_project_health(project_id)
        return {
            "health": snapshot.health,
            "reasons": snapshot.reasons,
            "schedule_variance_days": snapshot.schedule_variance_days,
            "effort_variance_hours": snapshot.effort_variance_hours,
            "overdue_task_count": snapshot.overdue_task_count,
            "blocked_task_count": snapshot.blocked_task_count,
            "unresolved_blocker_count": snapshot.unresolved_blocker_count,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{project_id}/run-agent")
async def run_project_agent(
    project_id: uuid.UUID,
    action: str = Query("SUMMARIZE", description="Action: PLAN_WBS, SUMMARIZE, ANALYZE_RISKS_AND_SCOPE"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger Project AI Assistant analysis or WBS plan suggestion."""
    service = ProjectService(db)
    project = await service.repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    agent = ProjectAgent()
    context = AgentContext(
        workflow_id="wf_project_execution",
        task_id="t_project_execution",
        agent_run_id=str(uuid.uuid4()),
        metadata={
            "action": action,
            "project_name": project.name,
            "project_data": {
                "id": str(project.id),
                "name": project.name,
                "status": project.status,
                "health": project.health,
                "progress_percent": project.progress_percent,
            },
            "tasks": [{"name": t.name, "status": t.status, "estimated_hours": t.estimated_hours, "actual_hours": t.actual_hours} for t in project.tasks],
            "milestones": [{"name": m.name, "status": m.status} for m in project.milestones],
            "blockers": [{"title": b.title, "status": b.status, "severity": b.severity} for b in project.blockers],
            "risks": [{"title": r.title, "status": r.status} for r in project.risks],
            "client_dependencies": [{"title": c.title, "status": c.status} for c in project.client_dependencies],
        },
    )


    res = await agent.execute(context)
    return res
