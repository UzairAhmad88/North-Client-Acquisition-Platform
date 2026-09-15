import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.audit import AuditFinding, AuditJob, AuditPage, BusinessAudit


class AuditRepository:
    # --- Audit Job Operations ---
    @staticmethod
    def create_job(
        db: Session,
        business_id: uuid.UUID,
        target_url: Optional[str] = None,
        requested_categories: Optional[List[str]] = None,
        pages_requested: int = 10,
        user_id: Optional[uuid.UUID] = None,
    ) -> AuditJob:
        job = AuditJob(
            business_id=business_id,
            user_id=user_id,
            target_url=target_url,
            requested_categories=requested_categories or ["ALL"],
            pages_requested=pages_requested,
            status="PENDING",
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def get_job_by_id(db: Session, job_id: uuid.UUID) -> Optional[AuditJob]:
        return db.query(AuditJob).filter(AuditJob.id == job_id).first()

    @staticmethod
    def list_jobs(
        db: Session,
        page: int = 1,
        page_size: int = 25,
        business_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
    ) -> Tuple[List[AuditJob], int]:
        query = db.query(AuditJob)
        if business_id:
            query = query.filter(AuditJob.business_id == business_id)
        if status:
            query = query.filter(AuditJob.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(AuditJob.created_at.desc()).offset(offset).limit(page_size).all()
        return items, total

    @staticmethod
    def update_job(db: Session, job: AuditJob, update_data: Dict[str, Any]) -> AuditJob:
        for key, value in update_data.items():
            setattr(job, key, value)
        job.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(job)
        return job

    # --- Business Audit Operations ---
    @staticmethod
    def create_audit(db: Session, audit_data: Dict[str, Any]) -> BusinessAudit:
        audit = BusinessAudit(**audit_data)
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit

    @staticmethod
    def get_audit_by_id(db: Session, audit_id: uuid.UUID) -> Optional[BusinessAudit]:
        return db.query(BusinessAudit).filter(BusinessAudit.id == audit_id).first()

    @staticmethod
    def get_latest_audit_by_business(
        db: Session, business_id: uuid.UUID
    ) -> Optional[BusinessAudit]:
        return (
            db.query(BusinessAudit)
            .filter(BusinessAudit.business_id == business_id)
            .order_by(BusinessAudit.created_at.desc())
            .first()
        )

    @staticmethod
    def list_audits_by_business(
        db: Session, business_id: uuid.UUID, limit: int = 20
    ) -> List[BusinessAudit]:
        return (
            db.query(BusinessAudit)
            .filter(BusinessAudit.business_id == business_id)
            .order_by(BusinessAudit.created_at.desc())
            .limit(limit)
            .all()
        )

    # --- Findings Operations ---
    @staticmethod
    def create_finding(db: Session, finding_data: Dict[str, Any]) -> AuditFinding:
        finding = AuditFinding(**finding_data)
        db.add(finding)
        db.commit()
        db.refresh(finding)
        return finding

    @staticmethod
    def list_findings_by_audit(
        db: Session,
        audit_id: uuid.UUID,
        category: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[AuditFinding]:
        query = db.query(AuditFinding).filter(AuditFinding.audit_id == audit_id)
        if category:
            query = query.filter(AuditFinding.category == category)
        if severity:
            query = query.filter(AuditFinding.severity == severity)
        return query.order_by(AuditFinding.severity.desc(), AuditFinding.created_at.desc()).all()

    # --- Audit Pages Operations ---
    @staticmethod
    def create_page(db: Session, page_data: Dict[str, Any]) -> AuditPage:
        page = AuditPage(**page_data)
        db.add(page)
        db.commit()
        db.refresh(page)
        return page

    @staticmethod
    def list_pages_by_audit(db: Session, audit_id: uuid.UUID) -> List[AuditPage]:
        return (
            db.query(AuditPage)
            .filter(AuditPage.audit_id == audit_id)
            .order_by(AuditPage.is_homepage.desc(), AuditPage.created_at.asc())
            .all()
        )
