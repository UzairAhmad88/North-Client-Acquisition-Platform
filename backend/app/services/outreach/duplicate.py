"""Duplicate outreach detection preventing accidental double-sending."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Tuple
from sqlalchemy.orm import Session

from app.models.outreach import OutreachDraft


class DuplicateDetector:
    """Detects duplicate communications sent to the same lead within a lookback window."""

    @staticmethod
    def check_duplicate(
        db: Session,
        lead_id: uuid.UUID,
        current_outreach_id: uuid.UUID,
        window_days: int = 7,
    ) -> Tuple[bool, str]:
        """Check if an outreach message was already sent to this lead within window_days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)

        recent_sent = (
            db.query(OutreachDraft)
            .filter(
                OutreachDraft.lead_id == lead_id,
                OutreachDraft.id != current_outreach_id,
                OutreachDraft.approval_status.in_(["SENT", "DELIVERED"]),
                OutreachDraft.updated_at >= cutoff,
            )
            .first()
        )

        if recent_sent:
            return True, f"Duplicate send blocked: Communication was already sent to this lead within the last {window_days} days."

        return False, ""
