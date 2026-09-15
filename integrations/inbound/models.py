"""Pydantic schemas and abstractions for inbound communication messages and webhook events."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class InboundMessagePayload(BaseModel):
    """Normalized inbound message payload across providers (Email, WhatsApp, SMS, LinkedIn)."""

    provider: str = Field(description="Provider name: Mock, SendGrid, Twilio, Meta, LinkedIn")
    provider_event_id: str = Field(description="Unique provider event ID for idempotency")
    channel: str = Field(default="EMAIL", description="Channel: EMAIL, WHATSAPP, SMS, LINKEDIN")
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None
    sender_name: Optional[str] = None
    recipient_address: str
    subject: Optional[str] = None
    body: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WebhookVerificationResult(BaseModel):
    """Result of webhook signature and replay security validation."""

    is_valid: bool
    error_code: Optional[str] = None
    reason: Optional[str] = None
