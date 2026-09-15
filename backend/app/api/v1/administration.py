"""FastAPI router for Platform Administration, Configuration, Policy & Control Center."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.administration.base import (
    AdminHealthReport,
    ConfigItem,
    ConfigScope,
    EnvironmentType,
    FeatureFlagItem,
    FlagStatus,
    KillSwitchItem,
    MaintenanceMode,
    PolicyDomain,
    PolicyItem,
    RolloutType,
)
from app.administration.service import PlatformAdministrationService
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.administration import (
    AdminOverviewResponse,
    ConfigChangeProposalRequest,
    ConfigCreateRequest,
    ConfigRollbackRequest,
    EnvironmentPromotionCreateRequest,
    FeatureFlagCreateRequest,
    FeatureFlagRolloutUpdateRequest,
    FeatureFlagStatusUpdateRequest,
    KillSwitchActionRequest,
    MaintenanceStartRequest,
    PolicyCreateRequest,
    PolicyEvaluateRequest,
)

router = APIRouter(prefix="/administration", tags=["Platform Administration & Control Center"])
_admin_service = PlatformAdministrationService()


# --- Overview & Health ---

@router.get("/overview", summary="Get administrative platform overview and metrics")
def get_overview(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    return _admin_service.get_overview()


@router.get("/health", summary="Get administrative health score and governance status")
def get_admin_health(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    return _admin_service.health_engine.compute_health_report().model_dump()


# --- Configuration Management ---

@router.get("/configs", summary="List platform configurations")
def list_configs(
    category: Optional[str] = Query(None, description="Filter by configuration category"),
    current_user: User = Depends(get_current_active_user),
) -> List[Dict[str, Any]]:
    return [c.model_dump() for c in _admin_service.config_manager.list_configs(category=category)]


@router.post("/configs", summary="Register a new platform configuration definition")
def register_config(
    payload: ConfigCreateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    item = ConfigItem(**payload.model_dump())
    registered = _admin_service.config_manager.register_config(item)
    return registered.model_dump()


@router.post("/configs/change-request", summary="Submit a configuration change request")
def submit_change_request(
    payload: ConfigChangeProposalRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    change = _admin_service.config_manager.create_change_request(
        key=payload.key,
        new_value=payload.new_value,
        reason=payload.reason,
        requested_by=current_user.email if hasattr(current_user, "email") else "admin",
        risk_level=payload.risk_level,
    )
    return change.model_dump()


@router.post("/configs/approve/{change_id}", summary="Approve and apply a pending configuration change")
def approve_change(
    change_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    approved_by = current_user.email if hasattr(current_user, "email") else "admin"
    cfg = _admin_service.config_manager.approve_and_apply_change(change_id, approved_by=approved_by)
    return cfg.model_dump()


@router.post("/configs/rollback", summary="Rollback configuration to a historical version")
def rollback_config(
    payload: ConfigRollbackRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    rolled_by = current_user.email if hasattr(current_user, "email") else "admin"
    cfg = _admin_service.config_manager.rollback_to_version(
        key=payload.key,
        target_version=payload.target_version,
        rolled_back_by=rolled_by,
        reason=payload.reason,
    )
    return cfg.model_dump()


@router.get("/configs/diff", summary="Compute visual diff between configuration versions")
def get_config_diff(
    key: str = Query(..., description="Configuration key"),
    v_from: int = Query(..., description="Source version"),
    v_to: int = Query(..., description="Target version"),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _admin_service.config_manager.compute_diff(key, v_from, v_to)


# --- Policy Management ---

@router.get("/policies", summary="List platform governance policies")
def list_policies(
    domain: Optional[PolicyDomain] = Query(None, description="Filter by policy domain"),
    current_user: User = Depends(get_current_active_user),
) -> List[Dict[str, Any]]:
    return [p.model_dump() for p in _admin_service.policy_engine.list_policies(domain=domain)]


@router.post("/policies", summary="Register or update a governance policy")
def register_policy(
    payload: PolicyCreateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    policy = PolicyItem(**payload.model_dump())
    registered = _admin_service.policy_engine.register_policy(policy)
    return registered.model_dump()


@router.post("/policies/evaluate", summary="Evaluate an action against policy rules")
def evaluate_policy_action(
    payload: PolicyEvaluateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    res, reason = _admin_service.policy_engine.evaluate_action(
        domain=payload.domain,
        action=payload.action,
        actor_type=payload.actor_type,
        context=payload.context,
        amount=payload.amount,
    )
    return {"action_result": res.value, "reason": reason}


# --- Feature Flags ---

@router.get("/feature-flags", summary="List feature flags")
def list_feature_flags(
    environment: Optional[EnvironmentType] = Query(None, description="Filter by environment"),
    current_user: User = Depends(get_current_active_user),
) -> List[Dict[str, Any]]:
    return [f.model_dump() for f in _admin_service.feature_flag_manager.list_flags(environment=environment)]


@router.post("/feature-flags", summary="Register a feature flag")
def register_feature_flag(
    payload: FeatureFlagCreateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    flag = FeatureFlagItem(**payload.model_dump())
    registered = _admin_service.feature_flag_manager.register_flag(flag)
    return registered.model_dump()


@router.post("/feature-flags/{key}/status", summary="Update feature flag status")
def update_feature_flag_status(
    key: str,
    payload: FeatureFlagStatusUpdateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    updated_by = current_user.email if hasattr(current_user, "email") else "admin"
    flag = _admin_service.feature_flag_manager.set_flag_status(key, payload.status, updated_by=updated_by)
    return flag.model_dump()


@router.post("/feature-flags/{key}/rollout", summary="Update feature flag rollout parameters")
def update_feature_flag_rollout(
    key: str,
    payload: FeatureFlagRolloutUpdateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    flag = _admin_service.feature_flag_manager.update_rollout(
        key=key,
        rollout_type=payload.rollout_type,
        percentage=payload.rollout_percentage,
        allowed_tiers=payload.allowed_tiers,
    )
    return flag.model_dump()


# --- Environments ---

@router.get("/environments", summary="List registered environments")
def list_environments(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return [e.model_dump() for e in _admin_service.environment_manager.list_environments()]


@router.post("/environments/promote", summary="Create configuration promotion request between environments")
def create_environment_promotion(
    payload: EnvironmentPromotionCreateRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    requested_by = current_user.email if hasattr(current_user, "email") else "admin"
    promo = _admin_service.environment_manager.create_promotion_request(
        source_env=payload.source_env,
        target_env=payload.target_env,
        keys=payload.keys,
        requested_by=requested_by,
    )
    return promo.model_dump()


# --- Integrations ---

@router.get("/integrations", summary="List provider integrations and health status")
def list_integrations(
    category: Optional[str] = Query(None, description="Filter by provider category"),
    current_user: User = Depends(get_current_active_user),
) -> List[Dict[str, Any]]:
    return [p.model_dump() for p in _admin_service.integration_manager.list_providers(category=category)]


# --- System Controls & Emergency Kill Switches ---

@router.get("/system-controls", summary="List system-wide emergency kill switches")
def list_system_controls(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return [s.model_dump() for s in _admin_service.system_controls.list_switches()]


@router.post("/system-controls/{switch_id}/activate", summary="Activate an emergency kill switch")
def activate_kill_switch(
    switch_id: str,
    payload: KillSwitchActionRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    activated_by = current_user.email if hasattr(current_user, "email") else "admin"
    s = _admin_service.system_controls.activate_kill_switch(switch_id, activated_by=activated_by, reason=payload.reason)
    return s.model_dump()


@router.post("/system-controls/{switch_id}/release", summary="Release/disarm an emergency kill switch")
def release_kill_switch(
    switch_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    released_by = current_user.email if hasattr(current_user, "email") else "admin"
    s = _admin_service.system_controls.release_kill_switch(switch_id, released_by=released_by)
    return s.model_dump()


# --- Maintenance Mode ---

@router.get("/maintenance", summary="Get active maintenance window and platform operational mode")
def get_maintenance_state(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    window = _admin_service.maintenance_manager.get_active_window()
    return {
        "current_mode": _admin_service.maintenance_manager.get_current_mode().value,
        "is_mutation_allowed": _admin_service.maintenance_manager.is_mutation_allowed(),
        "active_window": window.model_dump() if window else None,
    }


@router.post("/maintenance/start", summary="Enter maintenance mode with broadcast banners")
def start_maintenance_mode(
    payload: MaintenanceStartRequest,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    initiated_by = current_user.email if hasattr(current_user, "email") else "admin"
    window = _admin_service.maintenance_manager.start_maintenance(
        mode=payload.mode,
        title=payload.title,
        description=payload.description,
        initiated_by=initiated_by,
        internal_banner=payload.internal_banner,
        client_banner=payload.client_banner,
        affected_services=payload.affected_services,
    )
    return window.model_dump()


@router.post("/maintenance/end", summary="End maintenance mode and restore normal operations")
def end_maintenance_mode(current_user: User = Depends(get_current_active_user)) -> Dict[str, Any]:
    ended_by = current_user.email if hasattr(current_user, "email") else "admin"
    mode = _admin_service.maintenance_manager.end_maintenance(ended_by=ended_by)
    return {"status": "SUCCESS", "current_mode": mode.value}


# --- Drift Detection ---

@router.get("/drift", summary="List unresolved configuration drifts")
def list_drifts(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return [d.model_dump() for d in _admin_service.drift_detector.list_unresolved_drifts()]


@router.post("/drift/{drift_id}/resolve", summary="Reconcile and resolve configuration drift")
def resolve_drift(
    drift_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    resolved_by = current_user.email if hasattr(current_user, "email") else "admin"
    item = _admin_service.drift_detector.resolve_drift(drift_id, resolved_by=resolved_by)
    return item.model_dump()
