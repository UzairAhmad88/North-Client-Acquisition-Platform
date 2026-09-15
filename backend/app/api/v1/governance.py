"""API Router for Phase 33: AI Agent Evaluation, Observability & Governance."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repositories.governance import GovernanceRepository
from app.services.governance import GovernanceService
from app.schemas.governance import (
    AIHealthSnapshotResponse,
    AIIncidentCreateRequest,
    AIIncidentResponse,
    EvaluationDatasetResponse,
    EvaluationRunRequest,
    EvaluationRunResponse,
    HumanEvaluationRequest,
    KillSwitchRequest,
    PromptCreateRequest,
    PromptItemResponse,
    TraceCreateRequest,
    TraceDetailResponse,
)

router = APIRouter(prefix="/ai", tags=["ai-governance"])


def get_governance_service(session: AsyncSession = Depends(get_db)) -> GovernanceService:
    repo = GovernanceRepository(session)
    return GovernanceService(repo)


# =============================================================================
# 1. Traces & Observability Endpoints
# =============================================================================

@router.get("/traces", response_model=List[TraceDetailResponse])
async def list_ai_traces(
    tenant_id: str = Query("default_tenant"),
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    service: GovernanceService = Depends(get_governance_service),
):
    traces = await service.list_traces(tenant_id, agent_id, status, limit)
    return traces


@router.get("/traces/{trace_id}", response_model=TraceDetailResponse)
async def get_ai_trace_detail(
    trace_id: str,
    service: GovernanceService = Depends(get_governance_service),
):
    trace = await service.get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI trace not found")
    return trace


@router.post("/traces", response_model=TraceDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_trace(
    payload: TraceCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    trace = await service.start_trace(
        workflow_id=payload.workflow_id,
        agent_id=payload.agent_id,
        agent_version=payload.agent_version,
        model_id=payload.model_id,
        model_version=payload.model_version,
        prompt_version=payload.prompt_version,
        project_id=payload.project_id,
        lead_id=payload.lead_id,
        tenant_id=tenant_id,
    )
    return trace


# =============================================================================
# 2. Prompt Registry Endpoints
# =============================================================================

@router.get("/prompts", response_model=List[PromptItemResponse])
async def list_registered_prompts(
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    return await service.list_prompts(tenant_id)


@router.post("/prompts", response_model=PromptItemResponse, status_code=status.HTTP_201_CREATED)
async def register_prompt_version(
    payload: PromptCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    try:
        return await service.register_prompt(
            prompt_key=payload.prompt_key,
            name=payload.name,
            agent_target=payload.agent_target,
            purpose=payload.purpose,
            content=payload.content,
            version=payload.version,
            tenant_id=tenant_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# =============================================================================
# 3. Evaluations & Regression Benchmarks
# =============================================================================

@router.get("/evaluations/datasets", response_model=List[EvaluationDatasetResponse])
async def list_evaluation_datasets(
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    return await service.list_evaluation_datasets(tenant_id)


@router.post("/evaluations/run", response_model=EvaluationRunResponse, status_code=status.HTTP_201_CREATED)
async def execute_evaluation_run(
    payload: EvaluationRunRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    try:
        return await service.run_evaluation_benchmark(
            dataset_id=payload.dataset_id,
            agent_key=payload.agent_key,
            agent_version=payload.agent_version,
            prompt_version=payload.prompt_version,
            model_version=payload.model_version,
            baseline_score=payload.baseline_score,
            tenant_id=tenant_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/evaluations/runs", response_model=List[EvaluationRunResponse])
async def list_evaluation_runs(
    agent_key: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    return await service.list_evaluation_runs(tenant_id, agent_key)


@router.post("/evaluations/human-review", status_code=status.HTTP_201_CREATED)
async def submit_human_evaluation(
    payload: HumanEvaluationRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    rec = await service.record_human_evaluation(
        trace_id=payload.trace_id,
        reviewer=payload.reviewer,
        correctness=payload.correctness_score,
        completeness=payload.completeness_score,
        evidence=payload.evidence_score,
        safety=payload.safety_score,
        usefulness=payload.usefulness_score,
        notes=payload.notes,
        tenant_id=tenant_id,
    )
    return {"status": "RECORDED", "id": rec.id}


# =============================================================================
# 4. Incidents & Emergency Kill Switch
# =============================================================================

@router.get("/incidents", response_model=List[AIIncidentResponse])
async def list_ai_incidents(
    status: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    return await service.list_incidents(tenant_id, status)


@router.post("/incidents", response_model=AIIncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_incident(
    payload: AIIncidentCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    return await service.create_incident(
        title=payload.title,
        affected_agent=payload.affected_agent,
        description=payload.description,
        severity=payload.severity,
        containment_action=payload.containment_action,
        tenant_id=tenant_id,
    )


@router.post("/kill-switch", status_code=status.HTTP_200_OK)
async def manage_kill_switch(
    payload: KillSwitchRequest,
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    event = await service.trigger_kill_switch(
        level=payload.level,
        target_key=payload.target_key,
        is_active=payload.is_active,
        activated_by=payload.activated_by,
        reason=payload.reason,
        tenant_id=tenant_id,
    )
    return {
        "status": "SUCCESS",
        "kill_switch_active": event.is_active,
        "level": event.level.value,
        "target_key": event.target_key,
        "reason": event.reason,
    }


@router.get("/kill-switch/active")
async def get_active_kill_switches(
    tenant_id: str = Query("default_tenant"),
    service: GovernanceService = Depends(get_governance_service),
):
    switches = await service.get_active_kill_switches(tenant_id)
    return switches
