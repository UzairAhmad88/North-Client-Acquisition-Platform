"""Central Communication Service orchestrating send validation, provider dispatch, and conversation tracking."""

import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.outreach import OutreachDraft
from app.models.outreach_event import OutreachEvent
from app.services.outreach.communication_guard import CommunicationGuard
from app.services.outreach.idempotency import IdempotencyManager
from integrations.email import EmailMessagePayload, EmailProviderService


class CommunicationService:
    """Central orchestrator executing guarded communications."""

    @staticmethod
    async def send_outreach(
        db: Session,
        draft_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> OutreachDraft:
        # 1. Fetch Draft
        draft = db.query(OutreachDraft).filter(OutreachDraft.id == draft_id).first()
        if not draft:
            raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found.", status_code=404)

        if draft.approval_status in ("SENT", "DELIVERED"):
            raise AppError(code="OUTREACH_ALREADY_SENT", message="This outreach message has already been sent.", status_code=400)

        # 2. Execute CommunicationGuard Validation Chain
        is_valid, err_code, recipient_or_msg = CommunicationGuard.validate_send(db, draft, user_id)
        if not is_valid:
            raise AppError(code=err_code, message=recipient_or_msg, status_code=400)

        recipient_email = recipient_or_msg
        idempotency_key = IdempotencyManager.get_idempotency_key(draft.id, draft.version)

        try:
            # 3. Record SEND_STARTED Event
            evt_start = OutreachEvent(
                outreach_id=draft.id,
                lead_id=draft.lead_id,
                business_id=draft.business_id,
                user_id=user_id,
                event_type="SEND_STARTED",
                details={"recipient": recipient_email, "version": draft.version},
            )
            db.add(evt_start)
            db.commit()

            # 4. Dispatch Payload via EmailProviderService
            provider_service = EmailProviderService()
            payload = EmailMessagePayload(
                recipient_email=recipient_email,
                subject=draft.subject or "Message from North's",
                body=draft.body,
                metadata={"outreach_id": str(draft.id), "lead_id": str(draft.lead_id)},
            )
            send_resp = await provider_service.send_email(payload)

            # 5. Handle Provider Response & Update Draft Status
            now_utc = datetime.now(timezone.utc)
            draft.approval_status = send_resp.status

            evt_resp = OutreachEvent(
                outreach_id=draft.id,
                lead_id=draft.lead_id,
                business_id=draft.business_id,
                user_id=user_id,
                event_type=f"PROVIDER_{send_resp.status}",
                details={
                    "provider_message_id": send_resp.provider_message_id,
                    "provider_name": send_resp.provider_name,
                    "error_message": send_resp.error_message,
                },
            )
            db.add(evt_resp)

            # 6. Create Conversation & Message if ACCEPTED or DELIVERED
            if send_resp.status in ("ACCEPTED", "DELIVERED"):
                conv = (
                    db.query(Conversation)
                    .filter(Conversation.lead_id == draft.lead_id)
                    .first()
                )
                if not conv:
                    conv = Conversation(
                        lead_id=draft.lead_id,
                        business_id=draft.business_id,
                        status="ACTIVE",
                        channel=draft.channel,
                    )
                    db.add(conv)
                    db.flush()

                msg = Message(
                    conversation_id=conv.id,
                    outreach_id=draft.id,
                    direction="OUTBOUND",
                    channel=draft.channel,
                    subject=draft.subject,
                    body=draft.body,
                    status=send_resp.status,
                    provider_message_id=send_resp.provider_message_id,
                    sent_at=now_utc,
                )
                db.add(msg)

            db.commit()
            db.refresh(draft)
            return draft

        finally:
            IdempotencyManager.release_lock(idempotency_key)
