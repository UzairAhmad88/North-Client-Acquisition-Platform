"""Service layer orchestrating recommendation context gathering, engine calculation, and status actions."""

import uuid
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.models.audit import AuditFinding, BusinessAudit
from app.models.business import Business
from app.models.lead import Lead
from app.models.recommendation import ServiceRecommendation
from app.models.research import ResearchRecord
from app.models.score import LeadScore
from app.models.service import LeadService, Service
from app.services.recommendations.components import RecommendationContext
from app.services.recommendations.engine import RecommendationEngine
from app.services.recommendations.repository import RecommendationRepository


class RecommendationService:
    """High-level service orchestrator for service recommendations."""

    def __init__(self) -> None:
        self.engine = RecommendationEngine()

    def build_context(self, db: Session, lead_id: uuid.UUID) -> RecommendationContext:
        """Gather full context for a Lead."""
        lead = db.scalar(select(Lead).where(Lead.id == lead_id))
        if not lead:
            raise NotFoundError(f"Lead with ID {lead_id} not found.")

        business = db.scalar(select(Business).where(Business.id == lead.business_id))
        if not business:
            raise NotFoundError(f"Business with ID {lead.business_id} not found for Lead {lead_id}.")

        # Research records
        research_records = list(
            db.scalars(
                select(ResearchRecord).where(ResearchRecord.business_id == business.id)
            ).all()
        )

        # Audit & findings
        audit = db.scalar(
            select(BusinessAudit)
            .where(BusinessAudit.business_id == business.id)
            .order_by(BusinessAudit.created_at.desc())
        )

        findings: List[AuditFinding] = []
        if audit:
            findings = list(
                db.scalars(
                    select(AuditFinding).where(AuditFinding.audit_id == audit.id)
                ).all()
            )

        # Lead score
        lead_score = db.scalar(
            select(LeadScore)
            .where(LeadScore.lead_id == lead_id)
            .order_by(LeadScore.calculated_at.desc())
        )

        # Existing lead services
        existing_lead_services = list(
            db.scalars(
                select(LeadService).where(LeadService.lead_id == lead_id)
            ).all()
        )

        # Active services from catalog
        available_services = list(
            db.scalars(
                select(Service).where(Service.is_active == True, Service.status == "ACTIVE")
            ).all()
        )

        return RecommendationContext(
            lead=lead,
            business=business,
            research_records=research_records,
            audit=audit,
            findings=findings,
            lead_score=lead_score,
            existing_lead_services=existing_lead_services,
            available_services=available_services,
        )

    def calculate_lead_recommendations(
        self, db: Session, lead_id: uuid.UUID
    ) -> List[ServiceRecommendation]:
        """Calculate and save recommendations for a lead."""
        context = self.build_context(db, lead_id)

        # Run engine
        candidates = self.engine.calculate_recommendations(context)

        # Save results preserving human decisions
        saved = RecommendationRepository.upsert_recommendations(
            db, lead_id, context.business.id, candidates
        )

        return saved

    def list_recommendations(
        self,
        db: Session,
        lead_id: uuid.UUID,
        status: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 100,
    ) -> Tuple[List[ServiceRecommendation], int]:
        """List recommendations for a lead."""
        # Ensure lead exists
        lead = db.scalar(select(Lead).where(Lead.id == lead_id))
        if not lead:
            raise NotFoundError(f"Lead with ID {lead_id} not found.")

        return RecommendationRepository.list_by_lead(
            db, lead_id, status=status, min_score=min_score, limit=limit
        )

    def get_recommendation(
        self, db: Session, recommendation_id: uuid.UUID
    ) -> ServiceRecommendation:
        """Get single recommendation by ID."""
        rec = RecommendationRepository.get_by_id(db, recommendation_id)
        if not rec:
            raise NotFoundError(f"Service recommendation with ID {recommendation_id} not found.")
        return rec

    def accept_recommendation(
        self, db: Session, recommendation_id: uuid.UUID, user_id: uuid.UUID
    ) -> ServiceRecommendation:
        """Accept a recommendation and create lead_service relationship."""
        rec = self.get_recommendation(db, recommendation_id)

        accepted_rec = RecommendationRepository.accept_recommendation(db, rec, user_id)

        # Sync with lead_services table if not already linked
        existing_ls = db.scalar(
            select(LeadService).where(
                LeadService.lead_id == rec.lead_id,
                LeadService.service_id == rec.service_id,
            )
        )
        if not existing_ls:
            new_ls = LeadService(
                id=uuid.uuid4(),
                lead_id=rec.lead_id,
                service_id=rec.service_id,
                relationship_type="RECOMMENDED",
                source="HUMAN_ACCEPTED_RECOMMENDATION",
                notes=f"Accepted recommendation {rec.id} (Relevance Score: {rec.relevance_score:.1f})",
            )
            db.add(new_ls)
            db.commit()

        return accepted_rec

    def reject_recommendation(
        self,
        db: Session,
        recommendation_id: uuid.UUID,
        user_id: uuid.UUID,
        reason: Optional[str] = None,
    ) -> ServiceRecommendation:
        """Reject a recommendation with optional reason."""
        rec = self.get_recommendation(db, recommendation_id)
        return RecommendationRepository.reject_recommendation(db, rec, user_id, reason=reason)
