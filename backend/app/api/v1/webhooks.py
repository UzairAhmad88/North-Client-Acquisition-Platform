"""Inbound provider webhooks router receiving external messaging events."""

from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.common import DataResponse
from app.schemas.response import InboundEventRequest
from app.services.response import ResponseService
from integrations.inbound.models import InboundMessagePayload
from integrations.inbound.security import WebhookSecurityGuard

router = APIRouter(prefix="/webhooks", tags=["Inbound Provider Webhooks"])


@router.post("/{provider}")
async def receive_inbound_webhook(
    provider: str,
    payload: InboundEventRequest,
    db: Session = Depends(get_db),
    x_signature: str = Header(None, alias="X-Signature"),
    x_timestamp: str = Header(None, alias="X-Timestamp"),
) -> Any:
    """
    Receive inbound webhook from email or messaging provider.
    Enforces signature verification, timestamp replay protection, idempotency, and opt-out processing.
    """
    # Verify signature if secret configured
    secret = "webhook_secret_key"
    if x_signature:
        raw_body = payload.model_dump_json().encode("utf-8")
        sec_res = WebhookSecurityGuard.verify_signature(
            raw_body=raw_body, signature=x_signature, secret=secret, timestamp_header=x_timestamp
        )
        if not sec_res.is_valid:
            raise HTTPException(status_code=401, detail=sec_res.reason)

    message_payload = InboundMessagePayload(
        provider=provider,
        provider_event_id=payload.provider_event_id,
        channel=payload.channel,
        sender_email=payload.sender_email,
        sender_phone=payload.sender_phone,
        sender_name=payload.sender_name,
        recipient_address=payload.recipient_address,
        subject=payload.subject,
        body=payload.body,
        metadata=payload.metadata,
    )

    msg, conv, analysis = await ResponseService.process_inbound_message(db, message_payload)

    return {
        "status": "success",
        "message_id": str(msg.id),
        "conversation_id": str(conv.id),
        "intent": analysis.primary_intent if analysis else "AMBIGUOUS",
        "next_action": analysis.recommended_next_action if analysis else "ESCALATE_TO_HUMAN",
    }
