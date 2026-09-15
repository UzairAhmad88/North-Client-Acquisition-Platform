"""Pydantic API schemas for Outreach Drafts."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OutreachDraftResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    business_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    agent_run_id: Optional[uuid.UUID] = None
    channel: str
    tone: str
    language: str
    personalization_depth: str
    objective: str
    subject: Optional[str] = None
    body: str
    primary_angle: Dict[str, Any] = Field(default_factory=dict)
    personalization_profile: Dict[str, Any] = Field(default_factory=dict)
    claims: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    risk_level: str
    outreach_readiness: str
    approval_status: str
    rejection_reason: Optional[str] = None
    version: int
    content_hash: Optional[str] = None
    is_stale: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PersonalizationRunRequest(BaseModel):
    channel: str = "EMAIL"
    tone: str = "PROFESSIONAL"
    language: str = "en"
    personalization_depth: str = "STANDARD"
    objective: str = "INTRODUCE_SERVICE"


class OutreachDraftUpdateRequest(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    tone: Optional[str] = None
    channel: Optional[str] = None


class OutreachDraftRegenerateRequest(BaseModel):
    channel: Optional[str] = None
    tone: Optional[str] = None
    personalization_depth: Optional[str] = None


class OutreachRejectRequest(BaseModel):
    reason: str


class OutreachEventResponse(BaseModel):
    id: uuid.UUID
    outreach_id: uuid.UUID
    lead_id: uuid.UUID
    business_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    event_type: str
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = {"from_attributes": True}


class DncCreateRequest(BaseModel):
    scope: str = "EMAIL"  # EMAIL, PHONE, CONTACT, BUSINESS, GLOBAL
    target_value: str
    reason: Optional[str] = None


class DncResponse(BaseModel):
    id: uuid.UUID
    scope: str
    target_value: str
    reason: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
