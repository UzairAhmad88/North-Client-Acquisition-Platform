import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.service import LeadService, Service


class ServiceRepository:
    ALLOWED_SORT_FIELDS = {
        "name": Service.name,
        "category": Service.category,
        "created_at": Service.created_at,
        "updated_at": Service.updated_at,
        "status": Service.status,
        "base_price": Service.base_price,
        "estimated_duration_days": Service.estimated_duration_days,
    }

    @staticmethod
    def get_by_id(db: Session, service_id: uuid.UUID) -> Optional[Service]:
        return db.query(Service).filter(Service.id == service_id).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Service]:
        return db.query(Service).filter(Service.slug == slug).first()

    @staticmethod
    def create(db: Session, service_data: Dict[str, Any]) -> Service:
        service = Service(**service_data)
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def list_services(
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
        query = db.query(Service)

        if category:
            query = query.filter(Service.category == category)
        if status:
            query = query.filter(Service.status == status)
        if delivery_model:
            query = query.filter(Service.delivery_model == delivery_model)
        if pricing_model:
            query = query.filter(Service.pricing_model == pricing_model)
        if is_featured is not None:
            query = query.filter(Service.is_featured == is_featured)
        if is_active is not None:
            query = query.filter(Service.is_active == is_active)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Service.name.ilike(search_pattern),
                    Service.slug.ilike(search_pattern),
                    Service.short_description.ilike(search_pattern),
                    Service.description.ilike(search_pattern),
                )
            )

        total = query.count()

        sort_column = ServiceRepository.ALLOWED_SORT_FIELDS.get(sort, Service.created_at)
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    @staticmethod
    def update(db: Session, service: Service, update_data: Dict[str, Any]) -> Service:
        for key, value in update_data.items():
            setattr(service, key, value)
        service.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def archive(db: Session, service: Service) -> Service:
        service.status = "ARCHIVED"
        service.is_active = False
        service.archived_at = datetime.now(timezone.utc)
        service.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def restore(db: Session, service: Service) -> Service:
        service.status = "ACTIVE"
        service.is_active = True
        service.archived_at = None
        service.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(service)
        return service


class LeadServiceRepository:
    @staticmethod
    def get_by_lead_and_service(
        db: Session, lead_id: uuid.UUID, service_id: uuid.UUID
    ) -> Optional[LeadService]:
        return (
            db.query(LeadService)
            .filter(LeadService.lead_id == lead_id, LeadService.service_id == service_id)
            .first()
        )

    @staticmethod
    def add_service_to_lead(
        db: Session,
        lead_id: uuid.UUID,
        service_id: uuid.UUID,
        relationship_type: str = "CONSIDERED",
        source: str = "HUMAN",
        notes: Optional[str] = None,
    ) -> LeadService:
        existing = LeadServiceRepository.get_by_lead_and_service(db, lead_id, service_id)
        if existing:
            existing.relationship_type = relationship_type
            existing.source = source
            if notes:
                existing.notes = notes
            existing.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(existing)
            return existing

        lead_service = LeadService(
            lead_id=lead_id,
            service_id=service_id,
            relationship_type=relationship_type,
            source=source,
            notes=notes,
        )
        db.add(lead_service)
        db.commit()
        db.refresh(lead_service)
        return lead_service

    @staticmethod
    def remove_service_from_lead(db: Session, lead_id: uuid.UUID, service_id: uuid.UUID) -> bool:
        record = LeadServiceRepository.get_by_lead_and_service(db, lead_id, service_id)
        if record:
            db.delete(record)
            db.commit()
            return True
        return False

    @staticmethod
    def list_by_lead(db: Session, lead_id: uuid.UUID) -> List[LeadService]:
        return db.query(LeadService).filter(LeadService.lead_id == lead_id).all()
