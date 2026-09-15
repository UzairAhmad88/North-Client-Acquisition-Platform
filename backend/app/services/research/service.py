import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.research import ResearchJob, ResearchRecord
from app.repositories.business import BusinessRepository
from app.repositories.research import ResearchRepository
from app.schemas.research import (
    BusinessResearchProfileResponse,
    ResearchConflictResponse,
    ResearchRecordResponse,
)
from app.services.research.mock_provider import MockResearchProvider
from app.services.research.provider import ResearchEvidence, ResearchProvider
from app.services.research.web_provider import WebScraperResearchProvider


class ResearchService:
    @staticmethod
    def get_job(db: Session, job_id: uuid.UUID) -> Optional[ResearchJob]:
        return ResearchRepository.get_job_by_id(db, job_id)

    @staticmethod
    def get_provider(provider_type: str = "MOCK") -> ResearchProvider:
        if provider_type.upper() == "WEB":
            return WebScraperResearchProvider()
        return MockResearchProvider()

    @staticmethod
    def create_job(
        db: Session,
        business_id: uuid.UUID,
        sections: List[str],
        user_id: Optional[uuid.UUID] = None,
    ) -> ResearchJob:
        business = BusinessRepository.get_by_id(db, business_id)
        if not business:
            raise AppError(code="RESEARCH_BUSINESS_NOT_FOUND", message="Business not found", status_code=404)

        return ResearchRepository.create_job(db, business_id, sections, user_id=user_id)

    @staticmethod
    async def run_job(
        db: Session,
        job_id: uuid.UUID,
        provider_type: str = "MOCK",
    ) -> ResearchJob:
        job = ResearchRepository.get_job_by_id(db, job_id)
        if not job:
            raise AppError(code="RESEARCH_JOB_NOT_FOUND", message="Research job not found", status_code=404)

        business = BusinessRepository.get_by_id(db, job.business_id)
        if not business:
            raise AppError(code="RESEARCH_BUSINESS_NOT_FOUND", message="Business not found", status_code=404)

        now = datetime.now(timezone.utc)
        ResearchRepository.update_job(db, job, {"status": "RUNNING", "started_at": now})

        try:
            provider = ResearchService.get_provider(provider_type)
            requested_sections: List[str] = job.requested_sections if isinstance(job.requested_sections, list) else []
            evidence_list: List[ResearchEvidence] = await provider.research(business, requested_sections)

            records_found = len(evidence_list)
            records_validated = 0
            records_rejected = 0

            # Existing records for conflict checking
            existing_records = ResearchRepository.list_records_by_business(db, business.id)
            existing_field_map: Dict[str, List[ResearchRecord]] = {}
            for rec in existing_records:
                existing_field_map.setdefault(rec.field_name, []).append(rec)

            for ev in evidence_list:
                # 1. Freshness expiration rule (30 days for contact/website, 90 days for general)
                days_valid = 30 if ev.research_type in ("CONTACT", "WEBSITE") else 90
                expires_at = (ev.observed_at or now) + timedelta(days=days_valid)

                # 2. Conflict detection
                existing_for_field = existing_field_map.get(ev.field_name, [])
                has_conflict = False
                competing_list = []

                for prev in existing_for_field:
                    if prev.normalized_value.lower() != ev.normalized_value.lower():
                        has_conflict = True
                        competing_list.append({
                            "value": prev.normalized_value,
                            "source_url": prev.source_url,
                            "confidence": prev.confidence,
                            "observed_at": prev.observed_at.isoformat() if prev.observed_at else None,
                        })

                if has_conflict:
                    competing_list.append({
                        "value": ev.normalized_value,
                        "source_url": ev.source_url,
                        "confidence": ev.confidence,
                        "observed_at": (ev.observed_at or now).isoformat(),
                    })
                    ResearchRepository.create_or_update_conflict(
                        db, business.id, ev.field_name, competing_list
                    )

                # 3. Create ResearchRecord
                record_status = "CONFLICT" if has_conflict else "VALIDATED"
                rec_data = {
                    "business_id": business.id,
                    "research_job_id": job.id,
                    "source_url": ev.source_url,
                    "source_trust": ev.source_trust,
                    "research_type": ev.research_type,
                    "field_name": ev.field_name,
                    "raw_value": ev.raw_value,
                    "normalized_value": ev.normalized_value,
                    "confidence": ev.confidence,
                    "evidence_text": ev.evidence_text,
                    "observed_at": ev.observed_at or now,
                    "expires_at": expires_at,
                    "status": record_status,
                    "meta_info": ev.meta_info,
                }
                ResearchRepository.create_record(db, rec_data)
                records_validated += 1

                # 4. Safe Business Profile Enrichment
                if ev.confidence == "HIGH":
                    if ev.field_name == "phone" and not business.phone:
                        BusinessRepository.update(db, business, {"phone": ev.normalized_value, "normalized_phone": ev.normalized_value})
                    elif ev.field_name == "email" and not business.email:
                        BusinessRepository.update(db, business, {"email": ev.normalized_value, "normalized_email": ev.normalized_value})
                    elif ev.field_name == "description" and not business.description:
                        BusinessRepository.update(db, business, {"description": ev.normalized_value})

            status = "COMPLETED" if records_rejected == 0 else "PARTIAL"
            return ResearchRepository.update_job(
                db,
                job,
                {
                    "status": status,
                    "source_count": 1,
                    "records_found": records_found,
                    "records_validated": records_validated,
                    "records_rejected": records_rejected,
                    "completed_at": datetime.now(timezone.utc),
                },
            )

        except Exception as e:
            return ResearchRepository.update_job(
                db,
                job,
                {
                    "status": "FAILED",
                    "error_message": str(e),
                    "completed_at": datetime.now(timezone.utc),
                },
            )

    @staticmethod
    def cancel_job(db: Session, job_id: uuid.UUID) -> ResearchJob:
        job = ResearchRepository.get_job_by_id(db, job_id)
        if not job:
            raise AppError(code="RESEARCH_JOB_NOT_FOUND", message="Research job not found", status_code=404)

        if job.status in ("COMPLETED", "FAILED", "CANCELLED"):
            raise AppError(code="RESEARCH_JOB_FINISHED", message="Cannot cancel finished job", status_code=400)

        return ResearchRepository.update_job(
            db,
            job,
            {"status": "CANCELLED", "completed_at": datetime.now(timezone.utc)},
        )

    @staticmethod
    def get_business_research_profile(
        db: Session, business_id: uuid.UUID
    ) -> BusinessResearchProfileResponse:
        business = BusinessRepository.get_by_id(db, business_id)
        if not business:
            raise AppError(code="RESEARCH_BUSINESS_NOT_FOUND", message="Business not found", status_code=404)

        records = ResearchRepository.list_records_by_business(db, business_id)
        conflicts = ResearchRepository.get_conflicts_by_business(db, business_id)
        jobs, total_jobs = ResearchRepository.list_jobs(db, page=1, page_size=100, business_id=business_id)

        last_job = jobs[0] if jobs else None
        last_researched_at = last_job.completed_at if last_job else None

        if records:
            high_conf_count = sum(1 for r in records if r.confidence == "HIGH")
            confidence_score = int((high_conf_count / len(records)) * 100)
        else:
            confidence_score = 0

        record_responses = [ResearchRecordResponse.model_validate(r) for r in records]
        conflict_responses = [ResearchConflictResponse.model_validate(c) for c in conflicts]

        return BusinessResearchProfileResponse(
            business_id=business.id,
            business_name=business.name,
            total_jobs=total_jobs,
            total_records=len(records),
            active_conflicts_count=len(conflicts),
            last_researched_at=last_researched_at,
            confidence_score=confidence_score,
            records=record_responses,
            conflicts=conflict_responses,
        )
