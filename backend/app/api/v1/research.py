import math
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import AppError
from app.models.user import User
from app.repositories.research import ResearchRepository
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.schemas.research import (
    BusinessResearchProfileResponse,
    ResearchJobCreate,
    ResearchJobResponse,
    ResearchRecordResponse,
)
from app.services.research import ResearchService

router = APIRouter(prefix="/research", tags=["Research System"])


@router.post("/jobs", response_model=DataResponse[ResearchJobResponse], status_code=201)
def create_research_job(
    data: ResearchJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new business research job for target information sections.
    """
    job = ResearchService.create_job(
        db,
        business_id=data.business_id,
        sections=data.sections,
        user_id=current_user.id,
    )
    return DataResponse(data=ResearchJobResponse.model_validate(job))


@router.get("/jobs", response_model=PaginatedResponse[ResearchJobResponse])
def list_research_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    business_id: Optional[uuid.UUID] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List research jobs with pagination and business/status filtering.
    """
    items, total = ResearchRepository.list_jobs(
        db,
        page=page,
        page_size=page_size,
        business_id=business_id,
        status=status,
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    job_responses = [ResearchJobResponse.model_validate(item) for item in items]

    return PaginatedResponse(
        data=job_responses,
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.get("/jobs/{job_id}", response_model=DataResponse[ResearchJobResponse])
def get_research_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get research job status details by ID.
    """
    job = ResearchRepository.get_job_by_id(db, job_id)
    if not job:
        raise AppError(code="RESEARCH_JOB_NOT_FOUND", message="Research job not found", status_code=404)
    return DataResponse(data=ResearchJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/run", response_model=DataResponse[ResearchJobResponse])
async def run_research_job(
    job_id: uuid.UUID,
    provider_type: str = Query(default="MOCK"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute a research job using specified research provider (MOCK or WEB).
    """
    job = await ResearchService.run_job(db, job_id, provider_type=provider_type)
    return DataResponse(data=ResearchJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/run-agent", response_model=DataResponse[ResearchJobResponse])
async def run_research_agent(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute research job via Research Agent within Phase 14 Agent Runtime.
    """
    from workers.tasks.research import execute_research_task
    await execute_research_task(db, job_id)
    job = ResearchService.get_job(db, job_id)
    if not job:
        raise AppError(code="RESEARCH_JOB_NOT_FOUND", message="Research job not found", status_code=404)
    return DataResponse(data=ResearchJobResponse.model_validate(job))


@router.post("/jobs/{job_id}/cancel", response_model=DataResponse[ResearchJobResponse])
def cancel_research_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel an active research job.
    """
    job = ResearchService.cancel_job(db, job_id)
    return DataResponse(data=ResearchJobResponse.model_validate(job))


@router.get("/businesses/{business_id}", response_model=DataResponse[BusinessResearchProfileResponse])
def get_business_research_profile(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get consolidated evidence-backed research profile for a business.
    """
    profile = ResearchService.get_business_research_profile(db, business_id)
    return DataResponse(data=profile)


@router.get("/businesses/{business_id}/records", response_model=DataResponse[List[ResearchRecordResponse]])
def list_business_research_records(
    business_id: uuid.UUID,
    research_type: Optional[str] = Query(default=None),
    confidence: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List research records for a business.
    """
    records = ResearchRepository.list_records_by_business(
        db, business_id, research_type=research_type, confidence=confidence, status=status
    )
    return DataResponse(data=[ResearchRecordResponse.model_validate(r) for r in records])


@router.get("/records/{record_id}", response_model=DataResponse[ResearchRecordResponse])
def get_research_record(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get specific research record evidence detail.
    """
    rec = ResearchRepository.get_record_by_id(db, record_id)
    if not rec:
        raise AppError(code="RESEARCH_RECORD_NOT_FOUND", message="Research record not found", status_code=404)
    return DataResponse(data=ResearchRecordResponse.model_validate(rec))
