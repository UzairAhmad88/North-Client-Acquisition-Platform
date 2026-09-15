import math
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.repositories.contact import ContactRepository
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.schemas.contact import ContactResponse
from app.schemas.lead import (
    LeadAssignInput,
    LeadCreate,
    LeadDuplicateCheckResponse,
    LeadResponse,
    LeadTransitionInput,
    LeadUpdate,
)
from app.services.lead import LeadService

router = APIRouter(prefix="/leads", tags=["Lead CRM"])


@router.post("", response_model=DataResponse[LeadResponse], status_code=201)
def create_lead(
    data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.create_lead(db, data, creator_user_id=current_user.id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.get("", response_model=PaginatedResponse[LeadResponse])
def list_leads(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    qualification_status: Optional[str] = Query(default=None),
    contactability_status: Optional[str] = Query(default=None),
    source: Optional[str] = Query(default=None),
    owner_user_id: Optional[uuid.UUID] = Query(default=None),
    business_id: Optional[uuid.UUID] = Query(default=None),
    sort: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = LeadService.list_leads(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        priority=priority,
        qualification_status=qualification_status,
        contactability_status=contactability_status,
        source=source,
        owner_user_id=owner_user_id,
        business_id=business_id,
        sort=sort,
        order=order,
    )

    lead_responses = []
    for item in items:
        resp = LeadResponse.model_validate(item)
        resp.data_quality = LeadService.calculate_data_quality(db, item)
        contacts = ContactRepository.list_by_lead(db, item.id)
        resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
        lead_responses.append(resp)

    total_pages = math.ceil(total / page_size) if page_size > 0 else 0

    return {
        "data": lead_responses,
        "pagination": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    }


@router.post("/check-duplicate", response_model=DataResponse[LeadDuplicateCheckResponse])
def check_duplicate_lead(
    business_id: uuid.UUID = Query(...),
    title: str = Query(..., min_length=1),
    exclude_id: Optional[uuid.UUID] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dup_result = LeadService.check_duplicates(
        db=db,
        business_id=business_id,
        title=title,
        exclude_id=exclude_id,
    )
    return {"data": dup_result}


@router.get("/{lead_id}", response_model=DataResponse[LeadResponse])
def get_lead(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.get_lead(db, lead_id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.patch("/{lead_id}", response_model=DataResponse[LeadResponse])
def update_lead(
    lead_id: uuid.UUID,
    data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.update_lead(db, lead_id, data)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.delete("/{lead_id}", response_model=DataResponse[LeadResponse])
def archive_lead_by_delete(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.archive_lead(db, lead_id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.post("/{lead_id}/archive", response_model=DataResponse[LeadResponse])
def archive_lead(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.archive_lead(db, lead_id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.post("/{lead_id}/restore", response_model=DataResponse[LeadResponse])
def restore_lead(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.restore_lead(db, lead_id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.post("/{lead_id}/transition", response_model=DataResponse[LeadResponse])
def transition_lead_status(
    lead_id: uuid.UUID,
    data: LeadTransitionInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.transition_lead_status(
        db=db,
        lead_id=lead_id,
        target_status=data.status,
        loss_reason=data.loss_reason,
        notes=data.notes,
    )
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}


@router.post("/{lead_id}/assign", response_model=DataResponse[LeadResponse])
def assign_lead(
    lead_id: uuid.UUID,
    data: LeadAssignInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = LeadService.assign_lead(db, lead_id, data.owner_user_id)
    quality = LeadService.calculate_data_quality(db, lead)
    contacts = ContactRepository.list_by_lead(db, lead.id)

    resp = LeadResponse.model_validate(lead)
    resp.data_quality = quality
    resp.contacts = [ContactResponse.model_validate(c) for c in contacts]
    return {"data": resp}
