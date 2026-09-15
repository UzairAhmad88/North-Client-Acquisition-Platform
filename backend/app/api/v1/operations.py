"""FastAPI router for Operations: Deployments, Automated Rollbacks, and Tenant Feature Flags."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_active_user
from app.models.user import User
from app.operations.service import OperationsService
from app.schemas.reliability import (
    DeploymentRecordCreateSchema,
    DeploymentRecordSchema,
    FeatureFlagCreateUpdateSchema,
    FeatureFlagEvaluationRequest,
    RollbackTriggerSchema,
)

router = APIRouter(prefix="/operations", tags=["Operations & Deployments Platform"])
_ops_service = OperationsService()


# --- Deployments ---

@router.post("/deployments", response_model=DeploymentRecordSchema, summary="Record a deployment release")
def record_deployment(
    payload: DeploymentRecordCreateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _ops_service.record_deployment(
        version=payload.version,
        deployed_by=payload.deployed_by or current_user.email,
        environment=payload.environment,
        git_commit_sha=payload.git_commit_sha,
        release_notes=payload.release_notes,
    )


@router.get("/deployments", response_model=List[DeploymentRecordSchema], summary="List deployment history")
def list_deployments(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _ops_service.list_deployments()


# --- Rollbacks ---

@router.post("/rollbacks", summary="Evaluate and execute deployment rollback")
def evaluate_and_rollback(
    payload: RollbackTriggerSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _ops_service.evaluate_and_rollback(
        current_version=payload.current_version,
        target_version=payload.target_version,
        error_rate_pct=payload.error_rate_pct,
        p99_latency_ms=payload.p99_latency_ms,
        smoke_tests_passed=payload.smoke_tests_passed,
        initiated_by=payload.initiated_by or current_user.email,
        reason=payload.reason,
    )


@router.get("/rollbacks", summary="List executed rollbacks")
def list_rollbacks(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _ops_service.list_rollbacks()


# --- Feature Flags ---

@router.get("/feature-flags", summary="List all feature flags")
def list_feature_flags(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _ops_service.list_flags()


@router.post("/feature-flags", summary="Create or update feature flag")
def set_feature_flag(
    payload: FeatureFlagCreateUpdateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _ops_service.set_flag(
        flag_name=payload.name,
        enabled=payload.enabled,
        percentage_rollout=payload.percentage_rollout,
        allowed_tiers=payload.allowed_tiers,
        tenant_whitelist=payload.tenant_whitelist,
        tenant_blacklist=payload.tenant_blacklist,
        description=payload.description,
    )


@router.post("/feature-flags/evaluate", summary="Evaluate feature flag for a specific tenant context")
def evaluate_feature_flag(
    payload: FeatureFlagEvaluationRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    is_enabled = _ops_service.evaluate_flag(
        flag_name=payload.flag_name,
        tenant_id=payload.tenant_id or getattr(current_user, "tenant_id", None),
        tenant_tier=payload.tenant_tier,
    )
    return {
        "flag_name": payload.flag_name,
        "is_enabled": is_enabled,
        "tenant_id": payload.tenant_id,
        "tenant_tier": payload.tenant_tier,
    }
