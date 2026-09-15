import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.business import Business


class BusinessRepository:
    ALLOWED_SORT_FIELDS = {
        "name": Business.name,
        "created_at": Business.created_at,
        "updated_at": Business.updated_at,
        "status": Business.status,
        "city": Business.city,
        "industry": Business.industry,
        "business_type": Business.business_type,
    }

    @staticmethod
    def get_by_id(db: Session, business_id: uuid.UUID) -> Optional[Business]:
        return db.query(Business).filter(Business.id == business_id).first()

    @staticmethod
    def create(db: Session, business_data: Dict[str, Any]) -> Business:
        business = Business(**business_data)
        db.add(business)
        db.commit()
        db.refresh(business)
        return business

    @staticmethod
    def list_businesses(
        db: Session,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        status: Optional[str] = None,
        industry: Optional[str] = None,
        business_type: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        source: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Business], int]:
        query = db.query(Business)

        # Filters
        if status:
            query = query.filter(Business.status == status)
        if industry:
            query = query.filter(Business.industry == industry)
        if business_type:
            query = query.filter(Business.business_type == business_type)
        if city:
            query = query.filter(Business.city.ilike(f"%{city}%"))
        if country:
            query = query.filter(Business.country.ilike(f"%{country}%"))
        if source:
            query = query.filter(Business.source == source)

        # Search across name, email, phone, website, city
        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Business.name.ilike(search_pattern),
                    Business.email.ilike(search_pattern),
                    Business.phone.ilike(search_pattern),
                    Business.website_url.ilike(search_pattern),
                    Business.city.ilike(search_pattern),
                )
            )

        total = query.count()

        # Sorting validation
        sort_column = BusinessRepository.ALLOWED_SORT_FIELDS.get(sort, Business.created_at)
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    @staticmethod
    def update(db: Session, business: Business, update_data: Dict[str, Any]) -> Business:
        for key, value in update_data.items():
            setattr(business, key, value)
        business.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(business)
        return business

    @staticmethod
    def archive(db: Session, business: Business) -> Business:
        business.status = "ARCHIVED"
        business.archived_at = datetime.now(timezone.utc)
        business.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(business)
        return business

    @staticmethod
    def restore(db: Session, business: Business) -> Business:
        business.status = "ACTIVE"
        business.archived_at = None
        business.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(business)
        return business

    @staticmethod
    def find_candidate_duplicates(
        db: Session,
        normalized_name: Optional[str] = None,
        normalized_phone: Optional[str] = None,
        normalized_email: Optional[str] = None,
        normalized_website: Optional[str] = None,
        city: Optional[str] = None,
        source: Optional[str] = None,
        external_id: Optional[str] = None,
        exclude_id: Optional[uuid.UUID] = None,
    ) -> List[Business]:
        conditions = []

        if normalized_website:
            conditions.append(Business.normalized_website == normalized_website)
        if normalized_phone:
            conditions.append(Business.normalized_phone == normalized_phone)
        if normalized_email:
            conditions.append(Business.normalized_email == normalized_email)
        if source and external_id:
            conditions.append((Business.source == source) & (Business.external_id == external_id))
        if normalized_name and city:
            conditions.append(
                (Business.normalized_name == normalized_name) & (Business.city.ilike(f"%{city}%"))
            )

        if not conditions:
            return []

        query = db.query(Business).filter(or_(*conditions))
        if exclude_id:
            query = query.filter(Business.id != exclude_id)

        return query.all()
