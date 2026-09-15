import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.research import ResearchConflict, ResearchJob, ResearchRecord


class ResearchRepository:
    # --- Job Operations ---
    @staticmethod
    def create_job(
        db: Session,
        business_id: uuid.UUID,
        sections: List[str],
        user_id: Optional[uuid.UUID] = None,
    ) -> ResearchJob:
        job = ResearchJob(
            business_id=business_id,
            user_id=user_id,
            requested_sections=sections,
            status="PENDING",
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def get_job_by_id(db: Session, job_id: uuid.UUID) -> Optional[ResearchJob]:
        return db.query(ResearchJob).filter(ResearchJob.id == job_id).first()

    @staticmethod
    def list_jobs(
        db: Session,
        page: int = 1,
        page_size: int = 25,
        business_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
    ) -> Tuple[List[ResearchJob], int]:
        query = db.query(ResearchJob)
        if business_id:
            query = query.filter(ResearchJob.business_id == business_id)
        if status:
            query = query.filter(ResearchJob.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(ResearchJob.created_at.desc()).offset(offset).limit(page_size).all()
        return items, total

    @staticmethod
    def update_job(db: Session, job: ResearchJob, update_data: Dict[str, Any]) -> ResearchJob:
        for key, value in update_data.items():
            setattr(job, key, value)
        job.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(job)
        return job

    # --- Record Operations ---
    @staticmethod
    def create_record(db: Session, record_data: Dict[str, Any]) -> ResearchRecord:
        record = ResearchRecord(**record_data)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list_records_by_business(
        db: Session,
        business_id: uuid.UUID,
        research_type: Optional[str] = None,
        confidence: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ResearchRecord]:
        query = db.query(ResearchRecord).filter(ResearchRecord.business_id == business_id)
        if research_type:
            query = query.filter(ResearchRecord.research_type == research_type)
        if confidence:
            query = query.filter(ResearchRecord.confidence == confidence)
        if status:
            query = query.filter(ResearchRecord.status == status)

        return query.order_by(ResearchRecord.observed_at.desc()).all()

    @staticmethod
    def get_record_by_id(db: Session, record_id: uuid.UUID) -> Optional[ResearchRecord]:
        return db.query(ResearchRecord).filter(ResearchRecord.id == record_id).first()

    # --- Conflict Operations ---
    @staticmethod
    def get_conflicts_by_business(db: Session, business_id: uuid.UUID) -> List[ResearchConflict]:
        return (
            db.query(ResearchConflict)
            .filter(ResearchConflict.business_id == business_id)
            .order_by(ResearchConflict.created_at.desc())
            .all()
        )

    @staticmethod
    def create_or_update_conflict(
        db: Session,
        business_id: uuid.UUID,
        field_name: str,
        competing_values: List[Dict[str, Any]],
    ) -> ResearchConflict:
        conflict = (
            db.query(ResearchConflict)
            .filter(
                ResearchConflict.business_id == business_id,
                ResearchConflict.field_name == field_name,
            )
            .first()
        )
        if conflict:
            conflict.competing_values = competing_values
            conflict.status = "CONFLICT"
            conflict.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(conflict)
            return conflict

        conflict = ResearchConflict(
            business_id=business_id,
            field_name=field_name,
            competing_values=competing_values,
            status="CONFLICT",
        )
        db.add(conflict)
        db.commit()
        db.refresh(conflict)
        return conflict
