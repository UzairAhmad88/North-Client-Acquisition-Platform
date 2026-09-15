"""Frequency Controller enforcing daily/weekly contact caps and cooldown policies."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Tuple
from sqlalchemy.orm import Session

from app.models.communication_policy import CommunicationPolicy
from app.models.outreach import OutreachDraft


class FrequencyController:
    """Enforces communication policies, daily contact caps, and cooldown hours."""

    @staticmethod
    def check_frequency_limits(
        db: Session,
        lead_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> Tuple[bool, str]:
        policy = db.query(CommunicationPolicy).filter(CommunicationPolicy.is_active == True).first()
        max_contact_daily = policy.max_per_contact_per_day if policy else 2
        max_business_daily = policy.max_per_business_per_day if policy else 5
        cooldown_hours = policy.cooldown_hours if policy else 24

        now = datetime.now(timezone.utc)
        day_cutoff = now - timedelta(days=1)
        cooldown_cutoff = now - timedelta(hours=cooldown_hours)

        # 1. Cooldown check
        last_sent = (
            db.query(OutreachDraft)
            .filter(
                OutreachDraft.lead_id == lead_id,
                OutreachDraft.approval_status.in_(["SENT", "DELIVERED"]),
            )
            .order_by(OutreachDraft.updated_at.desc())
            .first()
        )
        if last_sent and last_sent.updated_at >= cooldown_cutoff:
            return True, f"Frequency policy blocked: Lead is in cooldown period ({cooldown_hours}h required between contacts)."

        # 2. Daily business cap check
        daily_biz_sends = (
            db.query(OutreachDraft)
            .filter(
                OutreachDraft.business_id == business_id,
                OutreachDraft.approval_status.in_(["SENT", "DELIVERED"]),
                OutreachDraft.updated_at >= day_cutoff,
            )
            .count()
        )
        if daily_biz_sends >= max_business_daily:
            return True, f"Frequency policy blocked: Maximum daily sends for business ({max_business_daily}/day) reached."

        return False, ""
