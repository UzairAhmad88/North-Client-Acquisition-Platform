"""Base Abstract Interface for Signature Providers."""

from abc import ABC, abstractmethod
from integrations.signature.models import SignatureRequest, SignatureStatusResponse


class BaseSignatureProvider(ABC):
    """Abstract signature provider interface for document execution."""

    @abstractmethod
    async def create_signature_request(self, request: SignatureRequest) -> SignatureStatusResponse:
        """Initiate a signature request for a contract document."""
        pass

    @abstractmethod
    async def get_signature_status(self, provider_request_id: str) -> SignatureStatusResponse:
        """Poll or query status of a signature request."""
        pass

    @abstractmethod
    async def complete_signature(self, provider_request_id: str) -> SignatureStatusResponse:
        """Simulate or complete signature execution."""
        pass
