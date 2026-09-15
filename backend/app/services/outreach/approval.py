"""Approval Engine handling content hash binding and human approval state management."""

import hashlib
import uuid
from typing import Any, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.outreach import OutreachDraft
from app.models.outreach_event import OutreachEvent


class ApprovalEngine:
    """Manages human approval states, content hash validation, and approval invalidation."""

    @staticmethod
    def compute_content_hash(subject: Optional[str], body: str, recipient: str) -> str:
        """Compute SHA-256 hash over subject, body, and recipient for approval binding."""
        raw = f"sub:{subject or ''}|body:{body}|recip:{recipient.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def approve_draft(
        db: Session,
        draft: OutreachDraft,
        user_id: Optional[uuid.UUID],
        recipient_email: str,
    ) -> OutreachDraft:
        """Approve a draft, bind its content hash, and record event."""
        content_hash = ApprovalEngine.compute_content_hash(draft.subject, draft.body, recipient_email)
        draft.approval_status = "APPROVED"
        draft.content_hash = content_hash
        draft.user_id = user_id or draft.user_id

        evt = OutreachEvent(
            outreach_id=draft.id,
            lead_id=draft.lead_id,
            business_id=draft.business_id,
            user_id=user_id,
            event_type="APPROVED",
            details={"version": draft.version, "content_hash": content_hash},
        )
        db.add(evt)
        db.commit()
        db.refresh(draft)
        return draft

    @staticmethod
    def reject_draft(
        db: Session,
        draft: OutreachDraft,
        user_id: Optional[uuid.UUID],
        reason: str,
    ) -> OutreachDraft:
        """Reject a draft with explicit reason."""
        draft.approval_status = "REJECTED"
        draft.rejection_reason = reason

        evt = OutreachEvent(
            outreach_id=draft.id,
            lead_id=draft.lead_id,
            business_id=draft.business_id,
            user_id=user_id,
            event_type="REJECTED",
            details={"reason": reason},
        )
        db.add(evt)
        db.commit()
        db.refresh(draft)
        return draft

    @staticmethod
    def verify_approval(draft: OutreachDraft, recipient_email: str) -> Tuple[bool, str]:
        """Verify that draft has APPROVED status and that current content hash matches approved hash."""
        if draft.approval_status != "APPROVED":
            return False, f"Outreach draft approval status is '{draft.approval_status}', not 'APPROVED'."

        current_hash = ApprovalEngine.compute_content_hash(draft.subject, draft.body, recipient_email)
        if draft.content_hash and draft.content_hash != current_hash:
            return False, "Content hash mismatch: Draft content was modified after human approval."

        return True, ""
