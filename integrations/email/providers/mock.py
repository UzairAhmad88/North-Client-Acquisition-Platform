"""Mock email provider simulating network responses safely without external sending."""

import uuid
from datetime import datetime
from typing import Tuple
from integrations.email.base import BaseEmailProvider
from integrations.email.models import EmailMessagePayload, EmailSendResponse


class MockEmailProvider(BaseEmailProvider):
    """Mock Email Provider simulating email delivery events for development and testing."""

    def __init__(self, mode: str = "success"):
        self.mode = mode

    def validate(self, payload: EmailMessagePayload) -> Tuple[bool, str]:
        if not payload.recipient_email or "@" not in payload.recipient_email:
            return False, "Invalid recipient email address format."
        if not payload.body:
            return False, "Email message body cannot be empty."
        return True, ""

    async def send(self, payload: EmailMessagePayload) -> EmailSendResponse:
        is_valid, err = self.validate(payload)
        if not is_valid:
            return EmailSendResponse(
                status="FAILED",
                provider_name="mock",
                provider_message_id=f"mock-err-{uuid.uuid4().hex[:8]}",
                timestamp=datetime.utcnow(),
                error_message=err,
            )

        msg_id = f"mock-msg-{uuid.uuid4().hex[:12]}"

        if self.mode == "bounce":
            return EmailSendResponse(
                status="BOUNCED",
                provider_name="mock",
                provider_message_id=msg_id,
                timestamp=datetime.utcnow(),
                error_message="Simulated permanent bounce: Address non-existent.",
            )
        elif self.mode == "failure":
            return EmailSendResponse(
                status="FAILED",
                provider_name="mock",
                provider_message_id=msg_id,
                timestamp=datetime.utcnow(),
                error_message="Simulated provider connection failure.",
            )

        # Default success mode
        return EmailSendResponse(
            status="ACCEPTED",
            provider_name="mock",
            provider_message_id=msg_id,
            timestamp=datetime.utcnow(),
            raw_response={"mock_send": True, "recipient": payload.recipient_email},
        )

    def health_check(self) -> bool:
        return True
