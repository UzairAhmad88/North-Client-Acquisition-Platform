"""Communication Guard enforcing the 15-step safety validation pipeline."""

import uuid
from typing import Tuple
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.lead import Lead
from app.models.outreach import OutreachDraft
from app.models.outreach_event import OutreachEvent
from app.services.outreach.approval import ApprovalEngine
from app.services.outreach.dnc import DncService
from app.services.outreach.duplicate import DuplicateDetector
from app.services.outreach.frequency import FrequencyController
from app.services.outreach.idempotency import IdempotencyManager


class CommunicationGuard:
    """Central safety guard enforcing mandatory checks prior to provider invocation."""

    @staticmethod
    def validate_send(
        db: Session,
        draft: OutreachDraft,
        user_id: uuid.UUID,
    ) -> Tuple[bool, str, str]:
        """
        Execute comprehensive validation pipeline prior to sending.
        Returns (is_valid, error_code, error_message).
        """
        # 1. Validate Lead & Business Ownership
        lead = db.query(Lead).filter(Lead.id == draft.lead_id).first()
        if not lead:
            return False, "LEAD_NOT_FOUND", "Lead associated with outreach draft not found."

        business = db.query(Business).filter(Business.id == draft.business_id).first()
        if not business:
            return False, "BUSINESS_NOT_FOUND", "Business associated with outreach draft not found."

        # 2. Recipient Validation
        recipient_email = business.email or (lead.notes if "@" in str(lead.notes) else None)
        if not recipient_email or "@" not in recipient_email:
            return False, "RECIPIENT_INVALID", "No valid email recipient address found for lead."

        # 3. Channel Validation
        if draft.channel not in ("EMAIL", "WHATSAPP", "SMS", "LINKEDIN"):
            return False, "CHANNEL_UNSUPPORTED", f"Channel '{draft.channel}' is not supported."

        # 4. Human Approval Verification & Content Hash Binding Check
        is_approved, app_err = ApprovalEngine.verify_approval(draft, recipient_email)
        if not is_approved:
            return False, "APPROVAL_INVALID", app_err

        # 5. Do-Not-Contact (DNC) Registry Check
        is_dnc, dnc_reason = DncService.is_blocked(
            db, email=recipient_email, lead_id=lead.id, business_id=business.id
        )
        if is_dnc:
            # Record BLOCKED event
            CommunicationGuard._record_blocked(db, draft, user_id, "DNC_BLOCKED", dnc_reason)
            return False, "DNC_BLOCKED", dnc_reason

        # 6. Duplicate Send Check
        is_dup, dup_reason = DuplicateDetector.check_duplicate(db, lead.id, draft.id)
        if is_dup:
            CommunicationGuard._record_blocked(db, draft, user_id, "DUPLICATE_BLOCKED", dup_reason)
            return False, "DUPLICATE_BLOCKED", dup_reason

        # 7. Frequency & Cooldown Check
        is_freq, freq_reason = FrequencyController.check_frequency_limits(db, lead.id, business.id)
        if is_freq:
            CommunicationGuard._record_blocked(db, draft, user_id, "FREQUENCY_BLOCKED", freq_reason)
            return False, "FREQUENCY_BLOCKED", freq_reason

        # 8. Risk Level Check
        if draft.risk_level == "BLOCKED":
            reason = "Outreach draft has been assigned BLOCKED risk level due to policy violations."
            CommunicationGuard._record_blocked(db, draft, user_id, "RISK_BLOCKED", reason)
            return False, "RISK_BLOCKED", reason

        # 9. Idempotency & Concurrency Lock Check
        idempotency_key = IdempotencyManager.get_idempotency_key(draft.id, draft.version)
        acquired, lock_err = IdempotencyManager.acquire_lock(idempotency_key)
        if not acquired:
            return False, "IDEMPOTENCY_CONFLICT", lock_err

        return True, "", recipient_email

    @staticmethod
    def _record_blocked(
        db: Session,
        draft: OutreachDraft,
        user_id: uuid.UUID,
        event_type: str,
        reason: str,
    ) -> None:
        draft.outreach_readiness = "OUTREACH_BLOCKED"
        evt = OutreachEvent(
            outreach_id=draft.id,
            lead_id=draft.lead_id,
            business_id=draft.business_id,
            user_id=user_id,
            event_type=event_type,
            details={"reason": reason},
        )
        db.add(evt)
        db.commit()
