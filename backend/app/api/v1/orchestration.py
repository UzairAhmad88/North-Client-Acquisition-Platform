"""FastAPI Router for Phase 34: Unified Workflow Orchestration, Event Bus & Automation."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.orchestration import (
    DLQStatus,
    HumanTaskStatus,
    ReplayMode,
    WorkflowStatus,
)
from app.models.user import User
from app.orchestration.workflow_registry import global_workflow_registry
from app.schemas.orchestration import (
    AutomationRuleResponse,
    CompleteHumanTaskRequest,
    CreateAutomationRuleRequest,
    DeadLetterResponse,
    EventReplayRequest,
    EventReplayResponse,
    EventResponse,
    HumanTaskResponse,
    StartWorkflowRequest,
    WorkflowRunResponse,
    WorkflowTemplateResponse,
)
from app.services.orchestration import OrchestrationService

router = APIRouter(tags=["Orchestration & Events"])


# ==============================================================================
# 1. Workflow Endpoints
# ==============================================================================

@router.get("/workflows/templates", response_model=List[WorkflowTemplateResponse])
async def list_workflow_templates(current_user: User = Depends(get_current_user)):
    """List all registered declarative workflow templates."""
    templates = global_workflow_registry.list_all()
    return [
        WorkflowTemplateResponse(
            workflow_key=t.workflow_key,
            name=t.name,
            description=t.description,
            category=t.category,
            version=t.version,
            steps=[s.to_dict() for s in t.steps],
            transitions=[tr.to_dict() for tr in t.transitions],
        )
        for t in templates
    ]


@router.get("/workflows", response_model=List[WorkflowRunResponse])
async def list_workflows(
    status: Optional[WorkflowStatus] = None,
    workflow_key: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List workflow execution runs for tenant."""
    service = OrchestrationService(db)
    runs = await service.repo.list_workflow_runs(
        tenant_id=str(current_user.id),
        status=status,
        workflow_key=workflow_key,
        limit=limit,
        offset=offset,
    )
    return [WorkflowRunResponse.model_validate(r) for r in runs]


@router.post("/workflows/start", response_model=WorkflowRunResponse, status_code=status.HTTP_201_CREATED)
async def start_workflow(
    request: StartWorkflowRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Instantiate and start a new workflow run."""
    service = OrchestrationService(db)
    try:
        run = await service.start_workflow(
            tenant_id=str(current_user.id),
            workflow_key=request.workflow_key,
            input_data=request.input_data,
            trigger_type=request.trigger_type,
            trigger_reference=request.trigger_reference,
        )
        return WorkflowRunResponse.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/workflows/{run_id}", response_model=WorkflowRunResponse)
async def get_workflow(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get workflow run details by ID."""
    service = OrchestrationService(db)
    run = await service.repo.get_workflow_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    return WorkflowRunResponse.model_validate(run)


@router.post("/workflows/{run_id}/pause", response_model=WorkflowRunResponse)
async def pause_workflow(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Pause an active workflow."""
    service = OrchestrationService(db)
    try:
        run = await service.pause_workflow(run_id, actor=current_user.email)
        return WorkflowRunResponse.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workflows/{run_id}/resume", response_model=WorkflowRunResponse)
async def resume_workflow(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Resume a paused workflow."""
    service = OrchestrationService(db)
    try:
        run = await service.resume_workflow(run_id, actor=current_user.email)
        return WorkflowRunResponse.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workflows/{run_id}/cancel", response_model=WorkflowRunResponse)
async def cancel_workflow(
    run_id: str,
    reason: str = Query("Operator cancellation", min_length=3),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancel a workflow."""
    service = OrchestrationService(db)
    try:
        run = await service.cancel_workflow(run_id, cancelled_by=current_user.email, reason=reason)
        return WorkflowRunResponse.model_validate(run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==============================================================================
# 2. Event Endpoints
# ==============================================================================

@router.get("/events", response_model=List[EventResponse])
async def list_events(
    event_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List historical domain events for tenant."""
    service = OrchestrationService(db)
    events = await service.repo.list_events(tenant_id=str(current_user.id), event_type=event_type, limit=limit)
    return [EventResponse.model_validate(e) for e in events]


@router.post("/events/replay", response_model=EventReplayResponse)
async def replay_events(
    request: EventReplayRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger controlled event replay."""
    service = OrchestrationService(db)
    mode = ReplayMode(request.replay_mode)
    replay = await service.replay_events(
        tenant_id=str(current_user.id),
        event_type=request.event_type,
        replay_mode=mode,
        triggered_by=current_user.email,
    )
    return EventReplayResponse.model_validate(replay)


# ==============================================================================
# 3. Human Task Endpoints
# ==============================================================================

@router.get("/tasks", response_model=List[HumanTaskResponse])
async def list_human_tasks(
    status: Optional[HumanTaskStatus] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List human review tasks in the queue."""
    service = OrchestrationService(db)
    tasks = await service.repo.list_human_tasks(tenant_id=str(current_user.id), status=status, limit=limit)
    return [HumanTaskResponse.model_validate(t) for t in tasks]


@router.post("/tasks/{task_id}/complete", response_model=HumanTaskResponse)
async def complete_human_task(
    task_id: str,
    request: CompleteHumanTaskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit human review decision (Approve, Reject, Revision)."""
    service = OrchestrationService(db)
    try:
        task = await service.complete_human_task(
            task_id=task_id,
            decision=request.decision,
            decision_reason=request.decision_reason,
            actor=current_user.email,
            content_hash=request.content_hash,
        )
        return HumanTaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==============================================================================
# 4. Automation Rule Endpoints
# ==============================================================================

@router.get("/automations", response_model=List[AutomationRuleResponse])
async def list_automations(
    enabled_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List automation rules for tenant."""
    service = OrchestrationService(db)
    rules = await service.repo.list_automation_rules(tenant_id=str(current_user.id), enabled_only=enabled_only)
    return [AutomationRuleResponse.model_validate(r) for r in rules]


@router.post("/automations", response_model=AutomationRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_automation(
    request: CreateAutomationRuleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new automation rule."""
    service = OrchestrationService(db)
    rule = await service.create_automation_rule(
        tenant_id=str(current_user.id),
        name=request.name,
        description=request.description,
        trigger_type=request.trigger_type,
        trigger_config=request.trigger_config,
        condition_config=request.condition_config,
        action_config=request.action_config,
        created_by=current_user.email,
        requires_human_approval=request.requires_human_approval,
    )
    return AutomationRuleResponse.model_validate(rule)


@router.post("/automations/{rule_id}/toggle", response_model=AutomationRuleResponse)
async def toggle_automation(
    rule_id: str,
    enabled: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enable or disable an automation rule."""
    service = OrchestrationService(db)
    rule = await service.toggle_automation_rule(rule_id, enabled=enabled)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found.")
    return AutomationRuleResponse.model_validate(rule)


# ==============================================================================
# 5. Dead Letter Queue Endpoints
# ==============================================================================

@router.get("/dead-letter", response_model=List[DeadLetterResponse])
async def list_dead_letters(
    status: Optional[DLQStatus] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List messages in the Dead Letter Queue."""
    service = OrchestrationService(db)
    messages = await service.repo.list_dead_letters(status=status, limit=limit)
    return [DeadLetterResponse.model_validate(m) for m in messages]


@router.post("/dead-letter/{dlq_id}/retry", response_model=DeadLetterResponse)
async def retry_dead_letter(
    dlq_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Schedule retry for a DLQ message."""
    service = OrchestrationService(db)
    msg = await service.retry_dlq_message(dlq_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Dead letter message not found.")
    return DeadLetterResponse.model_validate(msg)
