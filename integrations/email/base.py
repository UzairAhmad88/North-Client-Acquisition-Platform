"""Abstract base class for email providers."""

from abc import ABC, abstractmethod
from typing import Tuple
from integrations.email.models import EmailMessagePayload, EmailSendResponse


class BaseEmailProvider(ABC):
    """Abstract interface enforcing provider contracts."""

    @abstractmethod
    async def send(self, payload: EmailMessagePayload) -> EmailSendResponse:
        """Send an email message through the provider."""
        pass

    @abstractmethod
    def validate(self, payload: EmailMessagePayload) -> Tuple[bool, str]:
        """Validate payload formatting prior to send."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check provider connectivity status."""
        pass
