"""FastAPI router for Disaster Recovery, Backup Verification, Isolated Restores, and DR Drills."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_active_user
from app.disaster_recovery.service import DisasterRecoveryService
from app.models.user import User
from app.schemas.reliability import (
    BackupRecordSchema,
    BackupTriggerSchema,
    DRDrillResponseSchema,
    DRDrillTriggerSchema,
    DRPlanSchema,
    RestoreVerificationResponseSchema,
    RestoreVerificationTriggerSchema,
)

router = APIRouter(prefix="/disaster-recovery", tags=["Disaster Recovery & Business Continuity"])
_dr_service = DisasterRecoveryService()


# --- Backups ---

@router.post("/backups", response_model=BackupRecordSchema, summary="Trigger an automated or on-demand backup")
def trigger_backup(
    payload: BackupTriggerSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _dr_service.trigger_backup(
        backup_type=payload.backup_type,
        storage_location=payload.storage_location,
        retention_days=payload.retention_days,
    )


@router.get("/backups", response_model=List[BackupRecordSchema], summary="List system backup records")
def list_backups(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _dr_service.list_backups()


# --- Restore Verification Tests ---

@router.post("/restore-tests", response_model=RestoreVerificationResponseSchema, summary="Run isolated sandbox restore test")
def run_restore_test(
    payload: RestoreVerificationTriggerSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _dr_service.run_restore_test(
        backup_id=payload.backup_id,
        environment=payload.environment,
    )


@router.get("/restore-tests", response_model=List[RestoreVerificationResponseSchema], summary="List restore verification test runs")
def list_restore_tests(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _dr_service.list_restore_tests()


# --- DR Plans ---

@router.get("/plans", response_model=List[DRPlanSchema], summary="List all Disaster Recovery recovery plans and sequence")
def list_dr_plans(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _dr_service.list_plans()


@router.get("/plans/{scenario}", response_model=DRPlanSchema, summary="Get DR plan for a specific scenario")
def get_dr_plan(
    scenario: str,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    plan = _dr_service.get_plan(scenario)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DR plan not found for scenario")
    return plan


# --- DR Drills ---

@router.post("/drills", response_model=DRDrillResponseSchema, summary="Execute a simulated or live DR drill")
def run_dr_drill(
    payload: DRDrillTriggerSchema,
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    return _dr_service.execute_drill(
        scenario=payload.scenario,
        initiated_by=payload.initiated_by or current_user.email,
        plan_name=payload.plan_name,
    )


@router.get("/drills", response_model=List[DRDrillResponseSchema], summary="List executed DR drill reports and scorecards")
def list_dr_drills(current_user: User = Depends(get_current_active_user)) -> List[Dict[str, Any]]:
    return _dr_service.list_drills()
