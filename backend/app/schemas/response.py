"""Pydantic schemas for Response & Conversation Intelligence REST endpoints."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InboundEventRequest(BaseModel):
    provider: str = "Mock"
    provider_event_id: str
    channel: str = "EMAIL"
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None
    sender_name: Optional[str] = None
    recipient_address: str
    subject: Optional[str] = None
    body: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HumanCorrectionRequest(BaseModel):
    corrected_intent: Optional[str] = None
    corrected_next_action: Optional[str] = None
    reason: str = Field(min_length=3)


class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    direction: str
    channel: str
    subject: Optional[str] = None
    body: str
    status: str
    provider_message_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationAnalysisResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    latest_message_id: Optional[uuid.UUID] = None
    primary_intent: str
    all_intents: List[str] = []
    intent_confidence: str
    buying_signal_level: str
    objection_type: Optional[str] = None
    extracted_requirements: List[Dict[str, Any]] = []
    missing_information: List[str] = []
    conversation_stage: str
    recommended_next_action: str
    recommended_next_action_reason: Optional[str] = None
    next_action_confidence: str
    sentiment_signal: str
    priority: str
    human_correction: Optional[Dict[str, Any]] = None
    human_correction_by_id: Optional[uuid.UUID] = None
    human_correction_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    business_id: uuid.UUID
    contact_id: Optional[uuid.UUID] = None
    status: str
    channel: str
    current_intent: Optional[str] = None
    conversation_stage: str
    next_action: Optional[str] = None
    priority: str
    last_inbound_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    latest_analysis: Optional[ConversationAnalysisResponse] = None

    class Config:
        from_attributes = True
