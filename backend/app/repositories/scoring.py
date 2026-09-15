import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.score import LeadScore


class ScoringRepository:
    @staticmethod
    def create_score(db: Session, score_data: Dict[str, Any]) -> LeadScore:
        score = LeadScore(**score_data)
        db.add(score)
        db.commit()
        db.refresh(score)
        return score

    @staticmethod
    def get_latest_score_by_lead(db: Session, lead_id: uuid.UUID) -> Optional[LeadScore]:
        return (
            db.query(LeadScore)
            .filter(LeadScore.lead_id == lead_id)
            .order_by(LeadScore.calculated_at.desc())
            .first()
        )

    @staticmethod
    def get_latest_score_by_business(db: Session, business_id: uuid.UUID) -> Optional[LeadScore]:
        return (
            db.query(LeadScore)
            .filter(LeadScore.business_id == business_id)
            .order_by(LeadScore.calculated_at.desc())
            .first()
        )

    @staticmethod
    def list_scores_by_lead(db: Session, lead_id: uuid.UUID, limit: int = 20) -> List[LeadScore]:
        return (
            db.query(LeadScore)
            .filter(LeadScore.lead_id == lead_id)
            .order_by(LeadScore.calculated_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def list_scores_by_business(
        db: Session, business_id: uuid.UUID, limit: int = 20
    ) -> List[LeadScore]:
        return (
            db.query(LeadScore)
            .filter(LeadScore.business_id == business_id)
            .order_by(LeadScore.calculated_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def mark_scores_stale_for_business(db: Session, business_id: uuid.UUID) -> int:
        count = (
            db.query(LeadScore)
            .filter(LeadScore.business_id == business_id, LeadScore.is_stale == False)
            .update({"is_stale": True, "updated_at": datetime.now(timezone.utc)})
        )
        db.commit()
        return count
