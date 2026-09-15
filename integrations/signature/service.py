"""Signature Service managing provider dispatch."""

from integrations.signature.models import SignatureRequest, SignatureStatusResponse
from integrations.signature.providers.mock import MockSignatureProvider


class SignatureService:
    """Service layer routing signature requests to configured signature provider."""

    _provider = MockSignatureProvider()

    @classmethod
    async def request_signature(cls, request: SignatureRequest) -> SignatureStatusResponse:
        return await cls._provider.create_signature_request(request)

    @classmethod
    async def complete_signature(cls, provider_request_id: str) -> SignatureStatusResponse:
        return await cls._provider.complete_signature(provider_request_id)
