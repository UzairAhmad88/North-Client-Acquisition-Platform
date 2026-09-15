"""Repository operations for LeadQualification entity."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.qualification import LeadQualification


class QualificationRepository:
    @staticmethod
    def create_qualification(db: Session, qual_data: Dict[str, Any]) -> LeadQualification:
        qual = LeadQualification(**qual_data)
        db.add(qual)
        db.commit()
        db.refresh(qual)
        return qual

    @staticmethod
    def get_latest_by_lead(db: Session, lead_id: uuid.UUID) -> Optional[LeadQualification]:
        return (
            db.query(LeadQualification)
            .filter(LeadQualification.lead_id == lead_id)
            .order_by(LeadQualification.created_at.desc())
            .first()
        )

    @staticmethod
    def list_history_by_lead(db: Session, lead_id: uuid.UUID, limit: int = 20) -> List[LeadQualification]:
        return (
            db.query(LeadQualification)
            .filter(LeadQualification.lead_id == lead_id)
            .order_by(LeadQualification.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def apply_human_override(
        db: Session,
        qual_id: uuid.UUID,
        override_decision: str,
        override_reason: str,
        user_id: Optional[uuid.UUID] = None,
    ) -> Optional[LeadQualification]:
        qual = db.query(LeadQualification).filter(LeadQualification.id == qual_id).first()
        if not qual:
            return None

        qual.human_override_decision = override_decision
        qual.human_override_reason = override_reason
        qual.overridden_by_user_id = user_id
        qual.overridden_at = datetime.now(timezone.utc)
        qual.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(qual)
        return qual
