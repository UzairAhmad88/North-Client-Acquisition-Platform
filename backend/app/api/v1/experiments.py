"""API router for Phase 31 Experiments & Continuous Improvement."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repositories.analytics import AnalyticsRepository
from app.services.analytics import AnalyticsService
from app.schemas.analytics import (
    ExperimentResponse,
    ExperimentCreateRequest,
    ExperimentResultCreateRequest,
)
from app.models.analytics import Experiment, ExperimentResult, ExperimentStatus

router = APIRouter(prefix="/experiments", tags=["experiments"])


def get_analytics_service(session: AsyncSession = Depends(get_db)) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(repo)


@router.get("", response_model=List[ExperimentResponse])
async def list_experiments(
    tenant_id: str = "default_tenant",
    status: Optional[str] = None,
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """List continuous improvement hypotheses and experiments."""
    return await service.repo.list_experiments(tenant_id, status=status)


@router.post("", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    req: ExperimentCreateRequest,
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Create a new formal experimental learning hypothesis."""
    exp = Experiment(
        tenant_id=tenant_id,
        title=req.title,
        hypothesis=req.hypothesis,
        target_workflow=req.target_workflow,
        target_metric=req.target_metric,
        baseline_value=req.baseline_value,
        target_value=req.target_value,
        sample_target=req.sample_target,
        status=ExperimentStatus.ACTIVE,
        created_by=req.created_by,
    )
    return await service.repo.create_experiment(exp)


@router.get("/{exp_id}", response_model=ExperimentResponse)
async def get_experiment(
    exp_id: str,
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get experiment details, targets, and recorded trial metrics."""
    exp = await service.repo.get_experiment(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail=f"Experiment '{exp_id}' not found.")
    return exp


@router.post("/{exp_id}/results")
async def record_trial_result(
    exp_id: str,
    req: ExperimentResultCreateRequest,
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Record an empirical trial outcome under an active experiment."""
    exp = await service.repo.get_experiment(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail=f"Experiment '{exp_id}' not found.")

    res = ExperimentResult(
        tenant_id=tenant_id,
        experiment_id=exp_id,
        entity_id=req.entity_id,
        observed_value=req.observed_value,
        notes=req.notes,
        metadata_json=req.metadata_json,
    )
    saved = await service.repo.record_experiment_result(res)
    return {"status": "SUCCESS", "result_id": saved.id, "current_sample_count": exp.current_sample_count}


@router.post("/{exp_id}/evaluate")
async def evaluate_experiment(
    exp_id: str,
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Statistically evaluate trial results against experimental baseline."""
    exp = await service.repo.get_experiment(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail=f"Experiment '{exp_id}' not found.")

    exp_meta = {
        "baseline_value": exp.baseline_value,
        "target_value": exp.target_value,
        "sample_target": exp.sample_target,
    }
    results = [{"observed_value": r.observed_value} for r in exp.results]
    evaluation = service.bi_agent.hypothesis_engine.evaluate_experiment_results(exp_meta, results)

    if evaluation.get("status") == "EVALUATED":
        await service.repo.update_experiment_status(
            exp_id=exp_id,
            status=ExperimentStatus.EVALUATED,
            conclusion=evaluation.get("conclusion"),
        )

    return evaluation
