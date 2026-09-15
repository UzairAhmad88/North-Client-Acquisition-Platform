import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.score import LeadScore
from app.repositories.audit import AuditRepository
from app.repositories.business import BusinessRepository
from app.repositories.lead import LeadRepository
from app.repositories.research import ResearchRepository
from app.repositories.scoring import ScoringRepository
from app.repositories.service import ServiceRepository
from app.services.scoring.engine import ScoringEngine
from app.services.scoring.models import ScoringContext


class ScoringService:
    @staticmethod
    def calculate_lead_score(
        db: Session, lead_id: uuid.UUID, user_id: Optional[uuid.UUID] = None
    ) -> LeadScore:
        lead = LeadRepository.get_by_id(db, lead_id)
        if not lead:
            raise AppError(
                code="LEAD_NOT_FOUND", message="Lead opportunity not found", status_code=404
            )

        business = BusinessRepository.get_by_id(db, lead.business_id)
        if not business:
            raise AppError(
                code="BUSINESS_NOT_FOUND", message="Associated business not found", status_code=404
            )

        audit = AuditRepository.get_latest_audit_by_business(db, business.id)
        research_records = ResearchRepository.list_records_by_business(db, business.id)
        services, _ = ServiceRepository.list_services(db, page_size=100, is_active=True)

        ctx = ScoringContext(
            business=business,
            lead=lead,
            audit=audit,
            research_records=research_records,
            available_services=services,
        )

        result = ScoringEngine.calculate_opportunity_score(ctx)
        now = datetime.now(timezone.utc)

        # Mark previous active scores stale
        ScoringRepository.mark_scores_stale_for_business(db, business.id)

        c = result.component_scores
        score_data = {
            "lead_id": lead.id,
            "business_id": business.id,
            "audit_id": audit.id if audit else None,
            "score_version": result.score_version,
            "total_score": result.total_score,
            "band": result.band,
            "website_need_score": c["website_need"].score,
            "online_presence_score": c["online_presence"].score,
            "lead_capture_score": c["lead_capture"].score,
            "automation_potential_score": c["automation_potential"].score,
            "business_activity_score": c["business_activity"].score,
            "contactability_score": c["contactability"].score,
            "service_fit_score": c["service_fit"].score,
            "explanation": result.explanation,
            "evidence": result.evidence,
            "breakdown": result.to_dict()["component_scores"],
            "confidence": result.confidence,
            "is_stale": False,
            "calculated_at": now,
            "calculated_by": user_id,
        }

        score_rec = ScoringRepository.create_score(db, score_data)
        return score_rec

    @staticmethod
    def calculate_business_score(
        db: Session, business_id: uuid.UUID, user_id: Optional[uuid.UUID] = None
    ) -> LeadScore:
        business = BusinessRepository.get_by_id(db, business_id)
        if not business:
            raise AppError(
                code="BUSINESS_NOT_FOUND", message="Business not found", status_code=404
            )

        audit = AuditRepository.get_latest_audit_by_business(db, business.id)
        research_records = ResearchRepository.list_records_by_business(db, business.id)
        services, _ = ServiceRepository.list_services(db, page_size=100, is_active=True)

        ctx = ScoringContext(
            business=business,
            lead=None,
            audit=audit,
            research_records=research_records,
            available_services=services,
        )

        result = ScoringEngine.calculate_opportunity_score(ctx)
        now = datetime.now(timezone.utc)

        ScoringRepository.mark_scores_stale_for_business(db, business.id)

        c = result.component_scores
        score_data = {
            "lead_id": None,
            "business_id": business.id,
            "audit_id": audit.id if audit else None,
            "score_version": result.score_version,
            "total_score": result.total_score,
            "band": result.band,
            "website_need_score": c["website_need"].score,
            "online_presence_score": c["online_presence"].score,
            "lead_capture_score": c["lead_capture"].score,
            "automation_potential_score": c["automation_potential"].score,
            "business_activity_score": c["business_activity"].score,
            "contactability_score": c["contactability"].score,
            "service_fit_score": c["service_fit"].score,
            "explanation": result.explanation,
            "evidence": result.evidence,
            "breakdown": result.to_dict()["component_scores"],
            "confidence": result.confidence,
            "is_stale": False,
            "calculated_at": now,
            "calculated_by": user_id,
        }

        score_rec = ScoringRepository.create_score(db, score_data)
        return score_rec

    @staticmethod
    def get_lead_score(db: Session, lead_id: uuid.UUID) -> LeadScore:
        score = ScoringRepository.get_latest_score_by_lead(db, lead_id)
        if not score:
            # Auto calculate initial score if missing
            return ScoringService.calculate_lead_score(db, lead_id)
        return score

    @staticmethod
    def get_lead_score_history(
        db: Session, lead_id: uuid.UUID, limit: int = 20
    ) -> List[LeadScore]:
        return ScoringRepository.list_scores_by_lead(db, lead_id, limit=limit)

    @staticmethod
    def get_business_score(db: Session, business_id: uuid.UUID) -> LeadScore:
        score = ScoringRepository.get_latest_score_by_business(db, business_id)
        if not score:
            return ScoringService.calculate_business_score(db, business_id)
        return score
