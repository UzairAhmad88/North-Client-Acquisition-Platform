"""Email Provider Router Service enforcing REAL_SEND=false mock provider defaults."""

import os
from typing import Optional
from integrations.email.base import BaseEmailProvider
from integrations.email.models import EmailMessagePayload, EmailSendResponse
from integrations.email.providers.mock import MockEmailProvider


class EmailProviderService:
    """Service routing email delivery to MockEmailProvider or configured active provider."""

    def __init__(self, provider: Optional[BaseEmailProvider] = None):
        self.real_send = os.getenv("REAL_SEND", "false").lower() == "true"
        if provider:
            self.provider = provider
        else:
            # Enforce MockEmailProvider by default when REAL_SEND=false
            self.provider = MockEmailProvider(mode=os.getenv("MOCK_EMAIL_PROVIDER_MODE", "success"))

    async def send_email(self, payload: EmailMessagePayload) -> EmailSendResponse:
        return await self.provider.send(payload)
