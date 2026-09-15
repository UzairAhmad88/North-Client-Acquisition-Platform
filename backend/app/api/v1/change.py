"""REST API router for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.change import (
    ChangeApprovalSubmitSchema,
    ChangeRequestCreateSchema,
    ChangeRequestResponseSchema,
)
from app.services.change import ChangeService

router = APIRouter()


@router.get("/projects/{project_id}/changes", response_model=List[ChangeRequestResponseSchema])
async def list_project_change_requests(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    """List all change requests for a project."""
    service = ChangeService(db)
    items = await service.repo.list_by_project(project_id)
    return [ChangeRequestResponseSchema.model_validate(i) for i in items]


@router.post("/projects/{project_id}/changes", response_model=ChangeRequestResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_change_request(
    project_id: str,
    payload: ChangeRequestCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create a new formal change request."""
    service = ChangeService(db)
    try:
        req = await service.create_change_request(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            requested_by=payload.requested_by,
            category=payload.category,
            source=payload.source,
            reason=payload.reason,
        )
        loaded = await service.repo.get_by_id(req.id)
        return ChangeRequestResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/changes/{change_id}", response_model=ChangeRequestResponseSchema)
async def get_change_request_detail(
    change_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed change request record."""
    service = ChangeService(db)
    req = await service.repo.get_by_id(change_id)
    if not req:
        raise HTTPException(status_code=404, detail="Change request not found.")
    return ChangeRequestResponseSchema.model_validate(req)


@router.post("/changes/{change_id}/triage", response_model=ChangeRequestResponseSchema)
async def triage_change_request(
    change_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Triage & classify a change request into scope buckets."""
    service = ChangeService(db)
    try:
        req = await service.triage_and_classify(change_id)
        loaded = await service.repo.get_by_id(req.id)
        return ChangeRequestResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/changes/{change_id}/analyze")
async def run_impact_analysis(
    change_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Execute AI multi-dimensional impact analysis & PERT re-estimation."""
    service = ChangeService(db)
    try:
        res = await service.run_impact_analysis(change_id)
        return {
            "change_request_id": change_id,
            "overall_impact_level": res["impact_analysis"].overall_impact_level,
            "expected_hours": res["effort_estimate"].expected_hours,
            "change_value": res["commercial_analysis"].change_value,
            "summary": res["summary"].executive_summary,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/changes/{change_id}/approve", response_model=ChangeRequestResponseSchema)
async def approve_internal(
    change_id: str,
    approver_id: str = Query(default="North Operator"),
    db: AsyncSession = Depends(get_db),
):
    """Submit internal engineering and commercial approval."""
    service = ChangeService(db)
    try:
        req = await service.approve_internal(change_id, approver_id=approver_id)
        loaded = await service.repo.get_by_id(req.id)
        return ChangeRequestResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/changes/{change_id}/client-approve", response_model=ChangeRequestResponseSchema)
async def approve_client(
    change_id: str,
    payload: ChangeApprovalSubmitSchema,
    db: AsyncSession = Depends(get_db),
):
    """Submit explicit client approval with SHA-256 hash verification."""
    service = ChangeService(db)
    try:
        req = await service.approve_client(change_id, client_signer_id=payload.signer_id, approval_statement=payload.approval_statement)
        loaded = await service.repo.get_by_id(req.id)
        return ChangeRequestResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/changes/{change_id}/baseline")
async def update_baseline(
    change_id: str,
    actor_id: str = Query(default="North Operator"),
    db: AsyncSession = Depends(get_db),
):
    """Update contract baseline version to lock approved change scope."""
    service = ChangeService(db)
    try:
        baseline = await service.update_baseline_revision(change_id, actor_id=actor_id)
        return {"baseline_id": baseline.id, "version": baseline.version, "scope_hash": baseline.scope_hash}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/changes/{change_id}/implement")
async def implement_change(
    change_id: str,
    actor_id: str = Query(default="North Operator"),
    db: AsyncSession = Depends(get_db),
):
    """Convert approved change into active execution tasks."""
    service = ChangeService(db)
    try:
        tasks = await service.implement_change_tasks(change_id, actor_id=actor_id)
        return {"task_count": len(tasks), "task_ids": [t.id for t in tasks]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
