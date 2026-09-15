"""Service operations for Lead Qualification management and Agent orchestration."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.lead import Lead
from app.models.qualification import LeadQualification
from app.repositories.qualification import QualificationRepository


class QualificationService:
    @staticmethod
    def get_latest_qualification(db: Session, lead_id: uuid.UUID) -> Optional[LeadQualification]:
        return QualificationRepository.get_latest_by_lead(db, lead_id)

    @staticmethod
    def get_qualification_history(db: Session, lead_id: uuid.UUID, limit: int = 20) -> List[LeadQualification]:
        return QualificationRepository.list_history_by_lead(db, lead_id, limit=limit)

    @staticmethod
    def apply_override(
        db: Session,
        lead_id: uuid.UUID,
        override_decision: str,
        override_reason: str,
        user_id: Optional[uuid.UUID] = None,
    ) -> LeadQualification:
        latest = QualificationRepository.get_latest_by_lead(db, lead_id)
        if not latest:
            raise AppError(
                code="QUALIFICATION_NOT_FOUND",
                message="No qualification record exists for this lead to override.",
                status_code=404,
            )

        updated = QualificationRepository.apply_human_override(
            db,
            qual_id=latest.id,
            override_decision=override_decision,
            override_reason=override_reason,
            user_id=user_id,
        )

        # Update lead qualification_status field
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            lead.qualification_status = override_decision
            db.commit()

        return updated
