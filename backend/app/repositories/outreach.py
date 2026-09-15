"""Repository operations for OutreachDraft entity."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.outreach import OutreachDraft


class OutreachDraftRepository:
    """Data access layer for outreach drafts."""

    @staticmethod
    def create_draft(db: Session, draft_data: Dict[str, Any]) -> OutreachDraft:
        draft = OutreachDraft(**draft_data)
        db.add(draft)
        db.commit()
        db.refresh(draft)
        return draft

    @staticmethod
    def get_by_id(db: Session, draft_id: uuid.UUID) -> Optional[OutreachDraft]:
        return db.query(OutreachDraft).filter(OutreachDraft.id == draft_id).first()

    @staticmethod
    def get_latest_by_lead(db: Session, lead_id: uuid.UUID) -> Optional[OutreachDraft]:
        return (
            db.query(OutreachDraft)
            .filter(OutreachDraft.lead_id == lead_id)
            .order_by(OutreachDraft.version.desc(), OutreachDraft.created_at.desc())
            .first()
        )

    @staticmethod
    def list_history_by_lead(db: Session, lead_id: uuid.UUID, limit: int = 20) -> List[OutreachDraft]:
        return (
            db.query(OutreachDraft)
            .filter(OutreachDraft.lead_id == lead_id)
            .order_by(OutreachDraft.version.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def list_all_drafts(
        db: Session, limit: int = 20, offset: int = 0, approval_status: Optional[str] = None
    ) -> List[OutreachDraft]:
        query = db.query(OutreachDraft)
        if approval_status:
            query = query.filter(OutreachDraft.approval_status == approval_status)
        return query.order_by(OutreachDraft.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def update_draft(db: Session, draft: OutreachDraft, updates: Dict[str, Any]) -> OutreachDraft:
        # If subject or body changed, increment version and reset approval to PENDING_APPROVAL
        content_changed = "body" in updates or "subject" in updates
        if content_changed:
            draft.version = (draft.version or 1) + 1
            draft.approval_status = "PENDING_APPROVAL"

        for key, val in updates.items():
            if hasattr(draft, key) and val is not None:
                setattr(draft, key, val)

        db.commit()
        db.refresh(draft)
        return draft
