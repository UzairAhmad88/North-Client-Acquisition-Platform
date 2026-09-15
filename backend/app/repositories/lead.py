import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.lead import Lead


class LeadRepository:
    ALLOWED_SORT_FIELDS = {
        "title": Lead.title,
        "created_at": Lead.created_at,
        "updated_at": Lead.updated_at,
        "status": Lead.status,
        "priority": Lead.priority,
        "qualification_status": Lead.qualification_status,
        "contactability_status": Lead.contactability_status,
        "estimated_value": Lead.estimated_value,
        "next_action_at": Lead.next_action_at,
    }

    @staticmethod
    def get_by_id(db: Session, lead_id: uuid.UUID) -> Optional[Lead]:
        return db.query(Lead).filter(Lead.id == lead_id).first()

    @staticmethod
    def create(db: Session, lead_data: Dict[str, Any]) -> Lead:
        lead = Lead(**lead_data)
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def list_leads(
        db: Session,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        qualification_status: Optional[str] = None,
        contactability_status: Optional[str] = None,
        source: Optional[str] = None,
        owner_user_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Lead], int]:
        query = db.query(Lead).join(Business, Lead.business_id == Business.id)

        if status:
            query = query.filter(Lead.status == status)
        if priority:
            query = query.filter(Lead.priority == priority)
        if qualification_status:
            query = query.filter(Lead.qualification_status == qualification_status)
        if contactability_status:
            query = query.filter(Lead.contactability_status == contactability_status)
        if source:
            query = query.filter(Lead.source == source)
        if owner_user_id:
            query = query.filter(Lead.owner_user_id == owner_user_id)
        if business_id:
            query = query.filter(Lead.business_id == business_id)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Lead.title.ilike(search_pattern),
                    Lead.description.ilike(search_pattern),
                    Business.name.ilike(search_pattern),
                )
            )

        total = query.count()

        sort_column = LeadRepository.ALLOWED_SORT_FIELDS.get(sort, Lead.created_at)
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    @staticmethod
    def update(db: Session, lead: Lead, update_data: Dict[str, Any]) -> Lead:
        for key, value in update_data.items():
            setattr(lead, key, value)
        lead.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def archive(db: Session, lead: Lead) -> Lead:
        lead.status = "ARCHIVED"
        lead.archived_at = datetime.now(timezone.utc)
        lead.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def restore(db: Session, lead: Lead) -> Lead:
        lead.status = "NEW"
        lead.archived_at = None
        lead.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def find_candidate_duplicates(
        db: Session,
        business_id: uuid.UUID,
        title: str,
        exclude_id: Optional[uuid.UUID] = None,
    ) -> List[Lead]:
        query = db.query(Lead).filter(
            Lead.business_id == business_id,
            Lead.status != "ARCHIVED",
        )
        if exclude_id:
            query = query.filter(Lead.id != exclude_id)
        return query.all()
