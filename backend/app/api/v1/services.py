import math
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.schemas.service import (
    LeadServiceCreate,
    LeadServiceResponse,
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from app.services.service import ServiceCatalogService

router = APIRouter(tags=["Service Catalog"])


@router.post("/services", response_model=DataResponse[ServiceResponse], status_code=201)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ServiceCatalogService.create_service(db, data)
    return {"data": ServiceResponse.model_validate(service)}


@router.get("/services", response_model=PaginatedResponse[ServiceResponse])
def list_services(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    delivery_model: Optional[str] = Query(default=None),
    pricing_model: Optional[str] = Query(default=None),
    is_featured: Optional[bool] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    sort: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    db: Session = Depends(get_db),
):
    items, total = ServiceCatalogService.list_services(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        category=category,
        status=status,
        delivery_model=delivery_model,
        pricing_model=pricing_model,
        is_featured=is_featured,
        is_active=is_active,
        sort=sort,
        order=order,
    )

    responses = [ServiceResponse.model_validate(s) for s in items]
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0

    return {
        "data": responses,
        "pagination": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    }


@router.get("/services/slug/{slug}", response_model=DataResponse[ServiceResponse])
def get_service_by_slug(slug: str, db: Session = Depends(get_db)):
    service = ServiceCatalogService.get_service_by_slug(db, slug)
    return {"data": ServiceResponse.model_validate(service)}


@router.get("/services/{service_id}", response_model=DataResponse[ServiceResponse])
def get_service(service_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ServiceCatalogService.get_service_by_id(db, service_id)
    return {"data": ServiceResponse.model_validate(service)}


@router.patch("/services/{service_id}", response_model=DataResponse[ServiceResponse])
def update_service(
    service_id: uuid.UUID,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ServiceCatalogService.update_service(db, service_id, data)
    return {"data": ServiceResponse.model_validate(service)}


@router.delete("/services/{service_id}", response_model=DataResponse[ServiceResponse])
def archive_service_by_delete(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ServiceCatalogService.archive_service(db, service_id)
    return {"data": ServiceResponse.model_validate(service)}


@router.post("/services/{service_id}/archive", response_model=DataResponse[ServiceResponse])
def archive_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ServiceCatalogService.archive_service(db, service_id)
    return {"data": ServiceResponse.model_validate(service)}


@router.post("/services/{service_id}/restore", response_model=DataResponse[ServiceResponse])
def restore_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ServiceCatalogService.restore_service(db, service_id)
    return {"data": ServiceResponse.model_validate(service)}


# Lead-Service Associations
@router.get("/leads/{lead_id}/services", response_model=DataResponse[List[LeadServiceResponse]])
def list_lead_services(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = ServiceCatalogService.list_lead_services(db, lead_id)
    return {"data": [LeadServiceResponse.model_validate(r) for r in records]}


@router.post(
    "/leads/{lead_id}/services", response_model=DataResponse[LeadServiceResponse], status_code=201
)
def add_service_to_lead(
    lead_id: uuid.UUID,
    data: LeadServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = ServiceCatalogService.add_service_to_lead(db, lead_id, data)
    return {"data": LeadServiceResponse.model_validate(record)}


@router.delete("/leads/{lead_id}/services/{service_id}")
def remove_service_from_lead(
    lead_id: uuid.UUID,
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = ServiceCatalogService.remove_service_from_lead(db, lead_id, service_id)
    return {"data": {"success": success, "message": "Service association removed."}}
