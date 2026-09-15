"""Signature Provider data models."""

from typing import Optional
from pydantic import BaseModel, Field


class SignatureRequest(BaseModel):
    contract_id: str
    signer_email: str
    signer_name: str
    document_title: str
    content_hash: str


class SignatureStatusResponse(BaseModel):
    provider_request_id: str
    status: str = Field("PENDING", description="PENDING, SIGNATURE_REQUIRED, SIGNED, REJECTED, EXPIRED")
    signed_at: Optional[str] = None
