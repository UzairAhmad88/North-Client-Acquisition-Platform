import re
import uuid
from enum import Enum
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.service import LeadService, Service
from app.repositories.lead import LeadRepository
from app.repositories.service import LeadServiceRepository, ServiceRepository
from app.schemas.service import LeadServiceCreate, ServiceCreate, ServiceUpdate


class ServiceCatalogService:
    @staticmethod
    def slugify(name: str) -> str:
        if not name:
            return ""
        cleaned = re.sub(r"[^\w\s-]", "", name.lower())
        slug = re.sub(r"[\s_]+", "-", cleaned).strip("-")
        return slug

    @classmethod
    def validate_pricing(
        cls,
        base_price: Optional[float] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
    ) -> None:
        if base_price is not None and base_price < 0:
            raise AppError(
                code="INVALID_PRICING", message="Base price cannot be negative.", status_code=400
            )
        if price_min is not None and price_min < 0:
            raise AppError(
                code="INVALID_PRICING", message="Minimum price cannot be negative.", status_code=400
            )
        if price_max is not None and price_max < 0:
            raise AppError(
                code="INVALID_PRICING", message="Maximum price cannot be negative.", status_code=400
            )
        if price_min is not None and price_max is not None and price_min > price_max:
            raise AppError(
                code="INVALID_PRICING",
                message="Minimum price cannot exceed maximum price.",
                status_code=400,
            )

    @classmethod
    def create_service(cls, db: Session, service_in: ServiceCreate) -> Service:
        cls.validate_pricing(service_in.base_price, service_in.price_min, service_in.price_max)

        slug = service_in.slug if service_in.slug else cls.slugify(service_in.name)
        existing = ServiceRepository.get_by_slug(db, slug)
        if existing:
            raise AppError(
                code="DUPLICATE_SERVICE_SLUG",
                message=f"Service with slug '{slug}' already exists.",
                status_code=400,
            )

        service_data = service_in.model_dump()
        service_data["slug"] = slug

        for enum_field in ["category", "status", "delivery_model", "pricing_model"]:
            if enum_field in service_data and isinstance(service_data[enum_field], Enum):
                service_data[enum_field] = service_data[enum_field].value

        return ServiceRepository.create(db, service_data)

    @classmethod
    def get_service_by_id(cls, db: Session, service_id: uuid.UUID) -> Service:
        service = ServiceRepository.get_by_id(db, service_id)
        if not service:
            raise AppError(
                code="SERVICE_NOT_FOUND", message="Service record not found.", status_code=404
            )
        return service

    @classmethod
    def get_service_by_slug(cls, db: Session, slug: str) -> Service:
        service = ServiceRepository.get_by_slug(db, slug)
        if not service:
            raise AppError(
                code="SERVICE_NOT_FOUND", message=f"Service '{slug}' not found.", status_code=404
            )
        return service

    @classmethod
    def list_services(
        cls,
        db: Session,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        delivery_model: Optional[str] = None,
        pricing_model: Optional[str] = None,
        is_featured: Optional[bool] = None,
        is_active: Optional[bool] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Service], int]:
        return ServiceRepository.list_services(
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

    @classmethod
    def update_service(
        cls, db: Session, service_id: uuid.UUID, service_in: ServiceUpdate
    ) -> Service:
        service = cls.get_service_by_id(db, service_id)
        update_dict = service_in.model_dump(exclude_unset=True)

        base_p = update_dict.get("base_price", service.base_price)
        min_p = update_dict.get("price_min", service.price_min)
        max_p = update_dict.get("price_max", service.price_max)
        cls.validate_pricing(base_p, min_p, max_p)

        if "slug" in update_dict and update_dict["slug"] and update_dict["slug"] != service.slug:
            new_slug = update_dict["slug"]
            existing = ServiceRepository.get_by_slug(db, new_slug)
            if existing and existing.id != service.id:
                raise AppError(
                    code="DUPLICATE_SERVICE_SLUG",
                    message=f"Service with slug '{new_slug}' already exists.",
                    status_code=400,
                )

        for enum_field in ["category", "status", "delivery_model", "pricing_model"]:
            if enum_field in update_dict and hasattr(update_dict[enum_field], "value"):
                update_dict[enum_field] = update_dict[enum_field].value

        return ServiceRepository.update(db, service, update_dict)

    @classmethod
    def archive_service(cls, db: Session, service_id: uuid.UUID) -> Service:
        service = cls.get_service_by_id(db, service_id)
        if service.status == "ARCHIVED":
            return service
        return ServiceRepository.archive(db, service)

    @classmethod
    def restore_service(cls, db: Session, service_id: uuid.UUID) -> Service:
        service = cls.get_service_by_id(db, service_id)
        if service.status == "ACTIVE":
            return service
        return ServiceRepository.restore(db, service)

    @classmethod
    def add_service_to_lead(
        cls, db: Session, lead_id: uuid.UUID, data: LeadServiceCreate
    ) -> LeadService:
        lead = LeadRepository.get_by_id(db, lead_id)
        if not lead:
            raise AppError(code="LEAD_NOT_FOUND", message="Lead record not found.", status_code=404)

        service = cls.get_service_by_id(db, data.service_id)
        rel_type = (
            data.relationship_type.value
            if hasattr(data.relationship_type, "value")
            else str(data.relationship_type)
        )
        src_val = data.source.value if hasattr(data.source, "value") else str(data.source)

        return LeadServiceRepository.add_service_to_lead(
            db=db,
            lead_id=lead.id,
            service_id=service.id,
            relationship_type=rel_type,
            source=src_val,
            notes=data.notes,
        )

    @classmethod
    def remove_service_from_lead(
        cls, db: Session, lead_id: uuid.UUID, service_id: uuid.UUID
    ) -> bool:
        lead = LeadRepository.get_by_id(db, lead_id)
        if not lead:
            raise AppError(code="LEAD_NOT_FOUND", message="Lead record not found.", status_code=404)
        return LeadServiceRepository.remove_service_from_lead(db, lead_id, service_id)

    @classmethod
    def list_lead_services(cls, db: Session, lead_id: uuid.UUID) -> List[LeadService]:
        lead = LeadRepository.get_by_id(db, lead_id)
        if not lead:
            raise AppError(code="LEAD_NOT_FOUND", message="Lead record not found.", status_code=404)
        return LeadServiceRepository.list_by_lead(db, lead_id)
