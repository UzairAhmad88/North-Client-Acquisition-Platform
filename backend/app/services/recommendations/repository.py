"""Repository handling database operations for Service Recommendations."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.recommendation import ServiceRecommendation
from app.services.recommendations.components import CandidateRecommendation


class RecommendationRepository:
    """DB operations for service recommendations."""

    @staticmethod
    def get_by_id(db: Session, rec_id: uuid.UUID) -> Optional[ServiceRecommendation]:
        """Fetch single recommendation by ID."""
        return db.scalar(select(ServiceRecommendation).where(ServiceRecommendation.id == rec_id))

    @staticmethod
    def get_by_lead_and_service(
        db: Session, lead_id: uuid.UUID, service_id: uuid.UUID
    ) -> Optional[ServiceRecommendation]:
        """Fetch recommendation for a lead and service pair."""
        return db.scalar(
            select(ServiceRecommendation).where(
                ServiceRecommendation.lead_id == lead_id,
                ServiceRecommendation.service_id == service_id,
            )
        )

    @staticmethod
    def list_by_lead(
        db: Session,
        lead_id: uuid.UUID,
        status: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 100,
    ) -> Tuple[List[ServiceRecommendation], int]:
        """List recommendations for a lead with filtering."""
        query = select(ServiceRecommendation).where(ServiceRecommendation.lead_id == lead_id)

        if status:
            query = query.where(ServiceRecommendation.status == status)
        if min_score is not None:
            query = query.where(ServiceRecommendation.relevance_score >= min_score)

        # Count total matching
        total_query = select(ServiceRecommendation.id).where(ServiceRecommendation.lead_id == lead_id)
        if status:
            total_query = total_query.where(ServiceRecommendation.status == status)
        if min_score is not None:
            total_query = total_query.where(ServiceRecommendation.relevance_score >= min_score)
        
        total_count = len(db.scalars(total_query).all())

        query = query.order_by(ServiceRecommendation.relevance_score.desc()).limit(limit)
        results = db.scalars(query).all()
        return list(results), total_count

    @staticmethod
    def mark_lead_recommendations_stale(db: Session, lead_id: uuid.UUID) -> int:
        """Mark active SUGGESTED recommendations for a lead as STALE."""
        stmt = (
            update(ServiceRecommendation)
            .where(
                ServiceRecommendation.lead_id == lead_id,
                ServiceRecommendation.status == "SUGGESTED",
            )
            .values(status="STALE", updated_at=datetime.now(timezone.utc))
        )
        result = db.execute(stmt)
        db.commit()
        return int(getattr(result, "rowcount", 0))

    @staticmethod
    def upsert_recommendations(
        db: Session,
        lead_id: uuid.UUID,
        business_id: uuid.UUID,
        candidates: List[CandidateRecommendation],
    ) -> List[ServiceRecommendation]:
        """Upsert calculated candidate recommendations.

        Preserves human ACCEPTED and REJECTED statuses.
        """
        now = datetime.now(timezone.utc)
        saved_records: List[ServiceRecommendation] = []

        for candidate in candidates:
            existing = RecommendationRepository.get_by_lead_and_service(
                db, lead_id, candidate.service_id
            )

            if existing:
                # If human decision exists (ACCEPTED or REJECTED), preserve status & score
                if existing.status in ("ACCEPTED", "REJECTED"):
                    saved_records.append(existing)
                    continue

                # Update existing record
                existing.recommendation_version = candidate.recommendation_version
                existing.relevance_score = candidate.relevance_score
                existing.band = candidate.band
                existing.priority = candidate.priority
                existing.confidence = candidate.confidence
                existing.status = "SUGGESTED"
                existing.reasons = candidate.reasons
                existing.evidence = candidate.evidence
                existing.limitations = candidate.limitations
                existing.updated_at = now
                saved_records.append(existing)
            else:
                # Create new record
                rec = ServiceRecommendation(
                    id=uuid.uuid4(),
                    lead_id=lead_id,
                    business_id=business_id,
                    service_id=candidate.service_id,
                    recommendation_version=candidate.recommendation_version,
                    relevance_score=candidate.relevance_score,
                    band=candidate.band,
                    priority=candidate.priority,
                    confidence=candidate.confidence,
                    status="SUGGESTED",
                    reasons=candidate.reasons,
                    evidence=candidate.evidence,
                    limitations=candidate.limitations,
                    created_at=now,
                    updated_at=now,
                )
                db.add(rec)
                saved_records.append(rec)

        db.commit()
        return saved_records

    @staticmethod
    def accept_recommendation(
        db: Session, rec: ServiceRecommendation, user_id: uuid.UUID
    ) -> ServiceRecommendation:
        """Mark recommendation as ACCEPTED by user."""
        now = datetime.now(timezone.utc)
        rec.status = "ACCEPTED"
        rec.accepted_by = user_id
        rec.accepted_at = now
        rec.updated_at = now
        db.commit()
        db.refresh(rec)
        return rec

    @staticmethod
    def reject_recommendation(
        db: Session, rec: ServiceRecommendation, user_id: uuid.UUID, reason: Optional[str] = None
    ) -> ServiceRecommendation:
        """Mark recommendation as REJECTED by user."""
        now = datetime.now(timezone.utc)
        rec.status = "REJECTED"
        rec.rejected_by = user_id
        rec.rejected_at = now
        rec.rejection_reason = reason
        rec.updated_at = now
        db.commit()
        db.refresh(rec)
        return rec
