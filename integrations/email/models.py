"""Pydantic models for email provider integration payloads and responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EmailMessagePayload(BaseModel):
    recipient_email: str
    recipient_name: Optional[str] = None
    subject: str
    body: str
    reply_to: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EmailSendResponse(BaseModel):
    status: str  # ACCEPTED, DELIVERED, BOUNCED, FAILED
    provider_name: str = "mock"
    provider_message_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_response: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
