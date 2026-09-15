"""
FastAPI REST API Router for Phase 52:
Unified Autonomous Knowledge Worker & Multi-Agent Workforce Platform.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

try:
    from backend.app.schemas.workforce import (
        ConsensusRequest,
        ConsensusResponse,
        DepartmentResponse,
        HandoffCreateRequest,
        HandoffResponse,
        KillSwitchTriggerRequest,
        ReviewResolveRequest,
        TaskDecomposeRequest,
        TaskResponse,
        TeamResponse,
        WorkerRegisterRequest,
        WorkerResponse,
        WorkforceCopilotQueryRequest,
        WorkforceCopilotQueryResponse,
    )
    from backend.app.services.workforce.base import KillSwitchTarget, SupervisionLevel, TaskStatus, WorkerStatus
    from backend.app.services.workforce.service import WorkforcePlatformService
except ImportError:
    from app.schemas.workforce import (
        ConsensusRequest,
        ConsensusResponse,
        DepartmentResponse,
        HandoffCreateRequest,
        HandoffResponse,
        KillSwitchTriggerRequest,
        ReviewResolveRequest,
        TaskDecomposeRequest,
        TaskResponse,
        TeamResponse,
        WorkerRegisterRequest,
        WorkerResponse,
        WorkforceCopilotQueryRequest,
        WorkforceCopilotQueryResponse,
    )
    from app.services.workforce.base import KillSwitchTarget, SupervisionLevel, TaskStatus, WorkerStatus
    from app.services.workforce.service import WorkforcePlatformService

router = APIRouter(prefix="/workforce", tags=["Phase 52 - AI Workforce Platform"])

# Global Service Instance
_workforce_service = WorkforcePlatformService()


@router.get("/overview", response_model=Dict[str, Any])
def get_workforce_overview():
    """Returns organizational AI workforce overview, active departments, workers, and metrics."""
    workers = _workforce_service.list_workers()
    depts = _workforce_service.list_departments()
    tasks = _workforce_service.list_tasks()
    reviews = _workforce_service.list_pending_reviews()
    economics = _workforce_service.get_workforce_economics()

    return {
        "status": "OPERATIONAL",
        "total_active_workers": len([w for w in workers if w.status == WorkerStatus.ACTIVE]),
        "total_departments": len(depts),
        "total_tasks_processed": len(tasks),
        "pending_human_reviews": len(reviews),
        "economics": economics,
        "active_kill_switches": len(_workforce_service.list_active_kill_switches()),
    }


@router.get("/workers", response_model=List[Dict[str, Any]])
def list_workers(
    specialization: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """Lists registered AI workers with optional filtering."""
    st = WorkerStatus(status) if status else None
    workers = _workforce_service.list_workers(specialization=specialization, status=st)
    return [w.model_dump() if hasattr(w, "model_dump") else w.dict() for w in workers]


@router.post("/workers", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_worker(req: WorkerRegisterRequest):
    """Registers a new governed AI worker."""
    w = _workforce_service.register_worker(
        name=req.name,
        role=req.role,
        specialization=req.specialization,
        description=req.description,
        supervision_level=SupervisionLevel(req.supervision_level),
        capabilities=req.capabilities,
    )
    return w.model_dump() if hasattr(w, "model_dump") else w.dict()


@router.get("/departments", response_model=List[Dict[str, Any]])
def list_departments():
    """Lists all AI functional departments."""
    depts = _workforce_service.list_departments()
    return [d.model_dump() if hasattr(d, "model_dump") else d.dict() for d in depts]


@router.get("/teams", response_model=List[Dict[str, Any]])
def list_teams(department_code: Optional[str] = Query(None)):
    """Lists AI teams and collaborative squads."""
    teams = _workforce_service.list_teams(department_code=department_code)
    return [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in teams]


@router.post("/tasks/decompose", response_model=List[Dict[str, Any]])
def decompose_objective_into_tasks(req: TaskDecomposeRequest):
    """Decomposes a high-level business objective into a DAG task graph and assigns workers."""
    tasks = _workforce_service.plan_and_decompose_objective(req.objective, domain=req.domain)
    return [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in tasks]


@router.get("/tasks", response_model=List[Dict[str, Any]])
def list_tasks(
    worker_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """Lists scheduled and executed AI workforce tasks."""
    st = TaskStatus(status) if status else None
    tasks = _workforce_service.list_tasks(worker_code=worker_code, status=st)
    return [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in tasks]


@router.get("/reviews/pending", response_model=List[Dict[str, Any]])
def list_pending_human_reviews():
    """Retrieves tasks waiting for human executive sign-off."""
    return _workforce_service.list_pending_reviews()


@router.post("/reviews/{review_id}/resolve", response_model=Dict[str, Any])
def resolve_human_review(review_id: str, req: ReviewResolveRequest):
    """Resolves an item in the human review queue."""
    try:
        return _workforce_service.resolve_human_review(
            review_id=review_id,
            approved=req.approved,
            reviewer_id=req.reviewer_id,
            rationale=req.rationale,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/handoffs", response_model=Dict[str, Any])
def create_handoff(req: HandoffCreateRequest):
    """Records a structured context and artifact handoff between workers."""
    h = _workforce_service.execute_handoff(
        from_worker_code=req.from_worker_code,
        to_worker_code=req.to_worker_code,
        task_code=req.task_code,
        context_summary=req.context_summary,
        artifacts=req.artifacts,
        expected_next_action=req.expected_next_action,
    )
    return h.model_dump() if hasattr(h, "model_dump") else h.dict()


@router.post("/consensus", response_model=Dict[str, Any])
def evaluate_consensus(req: ConsensusRequest):
    """Aggregates multiple worker independent analyses into consensus ratings."""
    res = _workforce_service.evaluate_multi_worker_consensus(req.topic, req.worker_evaluations)
    return res.model_dump() if hasattr(res, "model_dump") else res.dict()


@router.get("/economics", response_model=Dict[str, Any])
def get_workforce_economics():
    """Returns total workforce costs, human hours saved, and ROI multiples."""
    return _workforce_service.get_workforce_economics()


@router.get("/workers/{worker_code}/scorecard", response_model=Dict[str, Any])
def get_worker_scorecard(worker_code: str):
    """Returns grounding, factuality, and policy compliance scorecard for a specific worker."""
    return _workforce_service.get_worker_scorecard(worker_code)


@router.post("/kill-switch", response_model=Dict[str, Any])
def trigger_kill_switch(req: KillSwitchTriggerRequest):
    """Activates an emergency kill switch halting target workforce execution."""
    target = KillSwitchTarget(req.target_type)
    return _workforce_service.activate_kill_switch(target, req.target_identifier, req.reason, req.operator_id)


@router.get("/kill-switches", response_model=List[Dict[str, Any]])
def list_kill_switches():
    """Lists active emergency workforce kill switches."""
    return _workforce_service.list_active_kill_switches()


@router.post("/copilot/query", response_model=WorkforceCopilotQueryResponse)
def query_workforce_copilot(req: WorkforceCopilotQueryRequest):
    """Natural language AI workforce intelligence copilot."""
    res = _workforce_service.query_workforce_copilot(req.query)
    return WorkforceCopilotQueryResponse(
        query=req.query,
        answer=res["answer"],
        evidence=res.get("evidence", []),
        suggested_actions=res.get("suggested_actions", []),
    )
