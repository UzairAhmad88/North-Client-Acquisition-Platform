import math
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.business import (
    BusinessCreate,
    BusinessDuplicateCheckResponse,
    BusinessResponse,
    BusinessUpdate,
)
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.services.business import BusinessService

router = APIRouter(prefix="/businesses", tags=["Business CRM"])


@router.post("", response_model=DataResponse[BusinessResponse], status_code=201)
def create_business(
    data: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.create_business(db, data, user_id=current_user.id)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}


@router.get("", response_model=PaginatedResponse[BusinessResponse])
def list_businesses(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    industry: Optional[str] = Query(default=None),
    business_type: Optional[str] = Query(default=None),
    city: Optional[str] = Query(default=None),
    country: Optional[str] = Query(default=None),
    source: Optional[str] = Query(default=None),
    sort: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = BusinessService.list_businesses(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        industry=industry,
        business_type=business_type,
        city=city,
        country=country,
        source=source,
        sort=sort,
        order=order,
    )

    business_responses = []
    for item in items:
        resp = BusinessResponse.model_validate(item)
        resp.data_quality = BusinessService.calculate_data_quality(item)
        business_responses.append(resp)

    total_pages = math.ceil(total / page_size) if page_size > 0 else 0

    return {
        "data": business_responses,
        "pagination": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    }


@router.post("/check-duplicate", response_model=DataResponse[BusinessDuplicateCheckResponse])
def check_duplicate_business(
    name: str = Query(..., min_length=1),
    phone: Optional[str] = Query(default=None),
    email: Optional[str] = Query(default=None),
    website_url: Optional[str] = Query(default=None),
    city: Optional[str] = Query(default=None),
    source: Optional[str] = Query(default=None),
    external_id: Optional[str] = Query(default=None),
    exclude_id: Optional[uuid.UUID] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dup_result = BusinessService.check_duplicates(
        db=db,
        name=name,
        phone=phone,
        email=email,
        website_url=website_url,
        city=city,
        source=source,
        external_id=external_id,
        exclude_id=exclude_id,
    )
    return {"data": dup_result}


@router.get("/{business_id}", response_model=DataResponse[BusinessResponse])
def get_business(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.get_business(db, business_id)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}


@router.patch("/{business_id}", response_model=DataResponse[BusinessResponse])
def update_business(
    business_id: uuid.UUID,
    data: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.update_business(db, business_id, data)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}


@router.delete("/{business_id}", response_model=DataResponse[BusinessResponse])
def archive_business_by_delete(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.archive_business(db, business_id)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}


@router.post("/{business_id}/archive", response_model=DataResponse[BusinessResponse])
def archive_business(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.archive_business(db, business_id)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}


@router.post("/{business_id}/restore", response_model=DataResponse[BusinessResponse])
def restore_business(
    business_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = BusinessService.restore_business(db, business_id)
    quality = BusinessService.calculate_data_quality(business)
    resp = BusinessResponse.model_validate(business)
    resp.data_quality = quality
    return {"data": resp}
