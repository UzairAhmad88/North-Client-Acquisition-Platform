from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.lead import Lead
from app.models.service import Service


class DashboardRepository:
    @staticmethod
    def get_business_metrics(db: Session) -> Dict[str, int]:
        active_count = (
            db.query(func.count(Business.id)).filter(Business.status == "ACTIVE").scalar() or 0
        )
        total_count = db.query(func.count(Business.id)).scalar() or 0
        incomplete_count = (
            db.query(func.count(Business.id))
            .filter(
                Business.status == "ACTIVE",
                or_(
                    Business.phone.is_(None),
                    Business.email.is_(None),
                    Business.website_url.is_(None),
                ),
            )
            .scalar()
            or 0
        )
        return {
            "active_count": active_count,
            "total_count": total_count,
            "incomplete_data_businesses_count": incomplete_count,
        }

    @staticmethod
    def get_lead_metrics(db: Session) -> Dict[str, Any]:
        open_count = (
            db.query(func.count(Lead.id))
            .filter(Lead.status.notin_(["LOST", "WON", "ARCHIVED"]))
            .scalar()
            or 0
        )
        qualified_count = (
            db.query(func.count(Lead.id))
            .filter(Lead.qualification_status == "QUALIFIED", Lead.status != "ARCHIVED")
            .scalar()
            or 0
        )
        high_priority_count = (
            db.query(func.count(Lead.id))
            .filter(
                Lead.status.notin_(["LOST", "WON", "ARCHIVED"]),
                Lead.priority.in_(["HIGH", "URGENT"]),
            )
            .scalar()
            or 0
        )
        total_count = db.query(func.count(Lead.id)).scalar() or 0

        # Pipeline breakdown by stage
        pipeline_results = db.query(Lead.status, func.count(Lead.id)).group_by(Lead.status).all()
        pipeline_counts: Dict[str, int] = {status: count for status, count in pipeline_results}

        return {
            "open_count": open_count,
            "qualified_count": qualified_count,
            "high_priority_count": high_priority_count,
            "total_count": total_count,
            "pipeline_counts": pipeline_counts,
        }

    @staticmethod
    def get_overdue_actions(db: Session, limit: int = 5) -> List[Tuple[Lead, Business]]:
        now = datetime.now(timezone.utc)
        results = (
            db.query(Lead, Business)
            .join(Business, Lead.business_id == Business.id)
            .filter(
                Lead.status.notin_(["LOST", "WON", "ARCHIVED"]),
                Lead.next_action_at.isnot(None),
                Lead.next_action_at < now,
            )
            .order_by(Lead.next_action_at.asc())
            .limit(limit)
            .all()
        )
        return [(row[0], row[1]) for row in results]

    @staticmethod
    def get_upcoming_actions(db: Session, limit: int = 5) -> List[Tuple[Lead, Business]]:
        now = datetime.now(timezone.utc)
        results = (
            db.query(Lead, Business)
            .join(Business, Lead.business_id == Business.id)
            .filter(
                Lead.status.notin_(["LOST", "WON", "ARCHIVED"]),
                Lead.next_action_at.isnot(None),
                Lead.next_action_at >= now,
            )
            .order_by(Lead.next_action_at.asc())
            .limit(limit)
            .all()
        )
        return [(row[0], row[1]) for row in results]

    @staticmethod
    def get_recent_leads(db: Session, limit: int = 5) -> List[Tuple[Lead, Business]]:
        results = (
            db.query(Lead, Business)
            .join(Business, Lead.business_id == Business.id)
            .order_by(Lead.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [(row[0], row[1]) for row in results]

    @staticmethod
    def get_recent_businesses(db: Session, limit: int = 5) -> List[Business]:
        return db.query(Business).order_by(Business.updated_at.desc()).limit(limit).all()

    @staticmethod
    def get_service_metrics(db: Session) -> Dict[str, Any]:
        active_count = (
            db.query(func.count(Service.id))
            .filter(Service.is_active.is_(True), Service.status == "ACTIVE")
            .scalar()
            or 0
        )
        featured_count = (
            db.query(func.count(Service.id))
            .filter(Service.is_featured.is_(True), Service.is_active.is_(True))
            .scalar()
            or 0
        )
        total_count = db.query(func.count(Service.id)).scalar() or 0

        cat_results = (
            db.query(Service.category, func.count(Service.id)).group_by(Service.category).all()
        )
        category_counts: Dict[str, int] = {cat: count for cat, count in cat_results}

        return {
            "active_services_count": active_count,
            "featured_services_count": featured_count,
            "total_services_count": total_count,
            "category_counts": category_counts,
        }
