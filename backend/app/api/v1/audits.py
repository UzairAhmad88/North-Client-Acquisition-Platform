import math
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import AppError
from app.models.user import User
from app.repositories.audit import AuditRepository
from app.schemas.audit import (
    AuditFindingResponse,
    AuditJobCreate,
    AuditJobResponse,
    BusinessAuditHistoryResponse,
    BusinessAuditResponse,
)
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.services.audit import AuditService

router = APIRouter(prefix="/audits", tags=["Website & Digital Presence Audit"])


@router.post("/jobs", response_model=DataResponse[AuditJobResponse], status_code=201)
def create_audit_job(
    data: AuditJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new website audit job for target business.
    """
    job = AuditService.create_job(
        db,
        business_id=data.business_id,
        target_url=data.target_url,
        requested_categories=data.requested_categories,
        pages_requested=data.pages_requested,
        user_id=current_user.id,
    )
    return DataResponse(data=AuditJobResponse.model_validate(job))


@router.get("/jobs", response_model=PaginatedResponse[AuditJobResponse])
def list_audit_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    business_id: Optional[uuid.UUID] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List audit jobs with pagination and filtering.
    """
    items, total = AuditRepository.list_jobs(
        db,
        page=page,
        page_size=page_size,
        business_id=business_id,
        status=status,
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    job_responses = [AuditJobResponse.model_validate(item) for item in items]

    return PaginatedResponse(
        data=job_responses,
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.get("/jobs/{job_id}", response_model=DataResponse[AuditJobResponse])
def get_audit_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get audit job status details by ID.
    """
    job = AuditRepository.get_job_by_id(db, job_id)
    if not job:
        raise AppError(code="AUDIT_JOB_NOT_FOUND", message="Audit job not found", status_code=404)
    return DataResponse(data=AuditJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/run", response_model=DataResponse[AuditJobResponse])
async def run_audit_job(
    job_id: uuid.UUID,
    runner_type: str = Query(default="MOCK"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute a website audit job using specified runner (MOCK or REAL).
    """
    job = await AuditService.run_job(db, job_id, runner_type=runner_type)
    return DataResponse(data=AuditJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/run-agent", response_model=DataResponse[AuditJobResponse])
async def run_audit_agent(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute audit job via Phase 16 Audit Agent.
    """
    from workers.tasks.audit import execute_audit_task

    await execute_audit_task(db, job_id)
    job = AuditRepository.get_job_by_id(db, job_id)
    if not job:
        raise AppError(code="AUDIT_JOB_NOT_FOUND", message="Audit job not found", status_code=404)
    return DataResponse(data=AuditJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/cancel", response_model=DataResponse[AuditJobResponse])
def cancel_audit_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel an active website audit job.
    """
    job = AuditService.cancel_job(db, job_id)
    return DataResponse(data=AuditJobResponse.model_validate(job))


@router.get("/businesses/{business_id}", response_model=DataResponse[BusinessAuditResponse])
def get_latest_business_audit(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the latest website audit for a business.
    """
    audit = AuditRepository.get_latest_audit_by_business(db, business_id)
    if not audit:
        raise AppError(
            code="AUDIT_NOT_FOUND",
            message="No audit record found for this business",
            status_code=404,
        )
    return DataResponse(data=BusinessAuditResponse.model_validate(audit))


@router.get("/businesses/{business_id}/findings", response_model=DataResponse[List[AuditFindingResponse]])
def list_business_audit_findings(
    business_id: uuid.UUID,
    category: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List structured audit findings for the latest business audit.
    """
    audit = AuditRepository.get_latest_audit_by_business(db, business_id)
    if not audit:
        raise AppError(
            code="AUDIT_NOT_FOUND",
            message="No audit record found for this business",
            status_code=404,
        )
    findings = AuditRepository.list_findings_by_audit(
        db, audit.id, category=category, severity=severity
    )
    return DataResponse(data=[AuditFindingResponse.model_validate(f) for f in findings])


@router.get("/businesses/{business_id}/history", response_model=DataResponse[BusinessAuditHistoryResponse])
def get_business_audit_history(
    business_id: uuid.UUID,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get historical timeline of all past website audits for a business.
    """
    audits = AuditRepository.list_audits_by_business(db, business_id, limit=limit)
    latest = audits[0] if audits else None
    audit_responses = [BusinessAuditResponse.model_validate(a) for a in audits]

    history_resp = BusinessAuditHistoryResponse(
        business_id=business_id,
        total_audits=len(audits),
        latest_audit=BusinessAuditResponse.model_validate(latest) if latest else None,
        audits=audit_responses,
    )
    return DataResponse(data=history_resp)


@router.get("/{audit_id}", response_model=DataResponse[BusinessAuditResponse])
def get_audit_by_id(
    audit_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get specific business audit detail by audit ID.
    """
    audit = AuditRepository.get_audit_by_id(db, audit_id)
    if not audit:
        raise AppError(code="AUDIT_NOT_FOUND", message="Audit not found", status_code=404)
    return DataResponse(data=BusinessAuditResponse.model_validate(audit))
