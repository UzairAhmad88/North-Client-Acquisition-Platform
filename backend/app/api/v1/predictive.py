"""API router for Phase 32: Advanced AI/ML Decision Intelligence & Predictive Operations."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repositories.predictive import PredictiveRepository
from app.services.predictive import PredictiveService
from app.schemas.predictive import (
    DecisionReviewRequest,
    DecisionSupportResponse,
    ForecastResponse,
    ModelApproveRequest,
    ModelDriftEventResponse,
    ModelGovernanceResponse,
    OutcomeRecordRequest,
    PredictionCreateRequest,
    PredictionResponse,
)

router = APIRouter(prefix="/predictive", tags=["predictive"])


def get_predictive_service(session: AsyncSession = Depends(get_db)) -> PredictiveService:
    repo = PredictiveRepository(session)
    return PredictiveService(repo)


# =============================================================================
# 1. Predictions Endpoints
# =============================================================================

@router.get("/predictions", response_model=List[PredictionResponse])
async def list_predictions(
    tenant_id: str = "default_tenant",
    prediction_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    risk_band: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """List historical point-in-time predictions with explanations and outcomes."""
    return await service.repo.list_predictions(
        tenant_id=tenant_id,
        prediction_type=prediction_type,
        entity_id=entity_id,
        risk_band=risk_band,
        limit=limit,
        offset=offset,
    )


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: str,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Get full details of a prediction including explanation and outcome."""
    pred = await service.repo.get_prediction(prediction_id)
    if not pred:
        raise HTTPException(status_code=404, detail=f"Prediction '{prediction_id}' not found.")
    return pred


@router.post("/predictions", status_code=status.HTTP_201_CREATED)
async def generate_prediction(
    req: PredictionCreateRequest,
    tenant_id: str = "default_tenant",
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Generate a calibrated prediction and create a linked human decision support record."""
    res = await service.generate_prediction(
        tenant_id=tenant_id,
        prediction_type=req.prediction_type,
        entity_id=req.entity_id,
        features=req.features,
    )
    if res.get("status") == "FAILED_LEAKAGE_CHECK":
        raise HTTPException(
            status_code=400,
            detail={"message": "Prediction blocked due to feature data leakage.", "reasons": res.get("reasons")},
        )
    return res


@router.post("/predictions/{prediction_id}/outcome")
async def record_prediction_outcome(
    prediction_id: str,
    req: OutcomeRecordRequest,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Record authoritative real-world outcome against a past prediction for calibration tracking."""
    outcome = await service.repo.record_prediction_outcome(
        prediction_id=prediction_id,
        actual_numeric_outcome=req.actual_numeric_outcome,
        outcome_label=req.outcome_label,
        recorded_by=req.recorded_by,
    )
    if not outcome:
        raise HTTPException(status_code=404, detail=f"Prediction '{prediction_id}' not found.")
    return {"status": "SUCCESS", "outcome_id": outcome.id, "error_magnitude": outcome.error_magnitude}


# =============================================================================
# 2. Decision Support & Human Review Endpoints
# =============================================================================

@router.get("/decision-support", response_model=List[DecisionSupportResponse])
async def list_decision_support_records(
    tenant_id: str = "default_tenant",
    state: Optional[str] = None,
    limit: int = 50,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """List human decision queue items ('AI Recommends -> You Decide')."""
    return await service.repo.list_decision_support_records(tenant_id=tenant_id, state=state, limit=limit)


@router.get("/decision-support/{record_id}", response_model=DecisionSupportResponse)
async def get_decision_support_record(
    record_id: str,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Get single decision support record with override logs."""
    rec = await service.repo.get_decision_support_record(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Decision support record '{record_id}' not found.")
    return rec


@router.post("/decision-support/{record_id}/review", response_model=DecisionSupportResponse)
async def review_decision_support(
    record_id: str,
    req: DecisionReviewRequest,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Record human operator decision (ACCEPT, OVERRIDE, REJECT). Never alters production policies automatically."""
    updated = await service.repo.review_decision_support(
        record_id=record_id,
        reviewer=req.reviewer,
        action=req.action,
        notes=req.notes,
        override_reason=req.override_reason,
        chosen_action=req.chosen_action,
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Decision support record '{record_id}' not found.")
    return updated


# =============================================================================
# 3. Model Governance & Drift Monitoring Endpoints
# =============================================================================

@router.get("/models", response_model=List[ModelGovernanceResponse])
async def list_models(
    tenant_id: str = "default_tenant",
    prediction_type: Optional[str] = None,
    status: Optional[str] = None,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """List predictive models in the model registry."""
    await service.ensure_default_models_seeded(tenant_id)
    return await service.repo.list_models(tenant_id=tenant_id, prediction_type=prediction_type, status=status)


@router.post("/models/{model_id}/approve", response_model=ModelGovernanceResponse)
async def approve_model_for_production(
    model_id: str,
    req: ModelApproveRequest,
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Human approval gate promoting candidate model to APPROVED status."""
    model = await service.repo.approve_model(model_id, req.approved_by)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return model


@router.get("/forecasts")
async def get_forecast(
    tenant_id: str = "default_tenant",
    forecast_type: str = "WORKLOAD_DEMAND",
    time_horizon: str = "30d",
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Generate multi-horizon forecast with explicit prediction intervals."""
    return await service.generate_workload_forecast(tenant_id, forecast_type, time_horizon)


@router.get("/model-monitoring/drift")
async def evaluate_drift_monitoring(
    tenant_id: str = "default_tenant",
    service: PredictiveService = Depends(get_predictive_service),
) -> Any:
    """Check for statistical feature and prediction drift across production models."""
    return await service.evaluate_drift_monitoring(tenant_id)
