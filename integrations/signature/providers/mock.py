"""Mock Signature Provider implementation for development and testing."""

import uuid
from datetime import datetime
from integrations.signature.base import BaseSignatureProvider
from integrations.signature.models import SignatureRequest, SignatureStatusResponse


class MockSignatureProvider(BaseSignatureProvider):
    """Mock implementation simulating signature creation and execution (REAL_SIGNATURE=false)."""

    def __init__(self):
        self._requests = {}

    async def create_signature_request(self, request: SignatureRequest) -> SignatureStatusResponse:
        req_id = f"sig-req-{str(uuid.uuid4())[:8]}"
        response = SignatureStatusResponse(
            provider_request_id=req_id,
            status="PENDING",
            signed_at=None,
        )
        self._requests[req_id] = response
        return response

    async def get_signature_status(self, provider_request_id: str) -> SignatureStatusResponse:
        return self._requests.get(
            provider_request_id,
            SignatureStatusResponse(provider_request_id=provider_request_id, status="PENDING"),
        )

    async def complete_signature(self, provider_request_id: str) -> SignatureStatusResponse:
        now_str = datetime.utcnow().isoformat()
        response = SignatureStatusResponse(
            provider_request_id=provider_request_id,
            status="SIGNED",
            signed_at=now_str,
        )
        self._requests[provider_request_id] = response
        return response
