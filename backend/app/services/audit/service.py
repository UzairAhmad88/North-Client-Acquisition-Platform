import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.audit import AuditJob
from app.repositories.audit import AuditRepository
from app.repositories.business import BusinessRepository
from app.services.audit.runner import BaseAuditRunner, MockAuditRunner, RealAuditRunner


class AuditService:
    @staticmethod
    def get_runner(runner_type: str = "MOCK") -> BaseAuditRunner:
        if runner_type.upper() == "WEB" or runner_type.upper() == "REAL":
            return RealAuditRunner()
        return MockAuditRunner()

    @staticmethod
    def create_job(
        db: Session,
        business_id: uuid.UUID,
        target_url: Optional[str] = None,
        requested_categories: Optional[List[str]] = None,
        pages_requested: int = 10,
        user_id: Optional[uuid.UUID] = None,
    ) -> AuditJob:
        business = BusinessRepository.get_by_id(db, business_id)
        if not business:
            raise AppError(
                code="AUDIT_BUSINESS_NOT_FOUND",
                message="Business not found",
                status_code=404,
            )

        url = target_url or business.website_url or (
            f"https://{business.normalized_website}" if business.normalized_website else None
        )

        return AuditRepository.create_job(
            db,
            business_id=business_id,
            target_url=url,
            requested_categories=requested_categories,
            pages_requested=pages_requested,
            user_id=user_id,
        )

    @staticmethod
    async def run_job(
        db: Session, job_id: uuid.UUID, runner_type: str = "MOCK"
    ) -> AuditJob:
        job = AuditRepository.get_job_by_id(db, job_id)
        if not job:
            raise AppError(
                code="AUDIT_JOB_NOT_FOUND",
                message="Audit job not found",
                status_code=404,
            )

        business = BusinessRepository.get_by_id(db, job.business_id)
        if not business:
            raise AppError(
                code="AUDIT_BUSINESS_NOT_FOUND",
                message="Business not found",
                status_code=404,
            )

        now = datetime.now(timezone.utc)
        AuditRepository.update_job(db, job, {"status": "RUNNING", "started_at": now})

        try:
            runner = AuditService.get_runner(runner_type)
            result = await runner.run_audit(
                business, target_url=job.target_url, max_pages=job.pages_requested
            )

            # Create BusinessAudit record
            findings_dicts = [f.to_dict() for f in result.findings]
            audit_data = {
                "business_id": business.id,
                "audit_job_id": job.id,
                "target_url": result.target_url,
                "audit_version": "1.0",
                "status": result.status,
                "overall_health": result.overall_health,
                "summary": result.summary,
                "categories": result.categories,
                "findings": findings_dicts,
                "metrics": result.metrics,
                "warnings": result.warnings,
                "errors": result.errors,
                "started_at": result.started_at,
                "completed_at": result.completed_at,
            }
            audit = AuditRepository.create_audit(db, audit_data)

            # Persist individual findings
            for f in result.findings:
                finding_data = {
                    "audit_id": audit.id,
                    "code": f.code,
                    "category": f.category,
                    "severity": f.severity,
                    "confidence": f.confidence,
                    "title": f.title,
                    "description": f.description,
                    "evidence": f.evidence,
                    "affected_page": f.affected_page,
                }
                AuditRepository.create_finding(db, finding_data)

            # Persist crawled pages
            for p in result.pages:
                page_data = {
                    "audit_id": audit.id,
                    "url": p.url,
                    "status_code": 200,
                    "response_time_ms": result.metrics.get("homepage_response_time_ms", 0),
                    "title": p.title,
                    "content_type": "text/html",
                    "meta_description": p.meta_description,
                    "is_homepage": p.url == result.target_url,
                    "has_contact_form": p.contact_forms_count > 0,
                }
                AuditRepository.create_page(db, page_data)

            warnings_count = len(result.warnings)
            errors_count = len(result.errors)
            job_status = "COMPLETED" if errors_count == 0 else "PARTIAL"

            return AuditRepository.update_job(
                db,
                job,
                {
                    "status": job_status,
                    "pages_analyzed": len(result.pages),
                    "findings_count": len(result.findings),
                    "warnings_count": warnings_count,
                    "errors_count": errors_count,
                    "completed_at": datetime.now(timezone.utc),
                },
            )

        except Exception as e:
            return AuditRepository.update_job(
                db,
                job,
                {
                    "status": "FAILED",
                    "error_message": str(e),
                    "completed_at": datetime.now(timezone.utc),
                },
            )

    @staticmethod
    def cancel_job(db: Session, job_id: uuid.UUID) -> AuditJob:
        job = AuditRepository.get_job_by_id(db, job_id)
        if not job:
            raise AppError(
                code="AUDIT_JOB_NOT_FOUND",
                message="Audit job not found",
                status_code=404,
            )

        if job.status in ("COMPLETED", "FAILED", "CANCELLED"):
            raise AppError(
                code="AUDIT_JOB_FINISHED",
                message="Cannot cancel finished job",
                status_code=400,
            )

        return AuditRepository.update_job(
            db,
            job,
            {"status": "CANCELLED", "completed_at": datetime.now(timezone.utc)},
        )
