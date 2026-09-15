"""Email integrations package."""

from integrations.email.base import BaseEmailProvider
from integrations.email.models import EmailMessagePayload, EmailSendResponse
from integrations.email.providers.mock import MockEmailProvider
from integrations.email.service import EmailProviderService

__all__ = [
    "BaseEmailProvider",
    "EmailMessagePayload",
    "EmailSendResponse",
    "MockEmailProvider",
    "EmailProviderService",
]
