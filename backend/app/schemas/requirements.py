"""Pydantic schemas for discovery sessions and requirements REST API."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class RequirementCreateSchema(BaseModel):
    category: str
    title: str
    description: str
    source_type: str = "CLIENT_MESSAGE"
    source_reference: Optional[str] = None
    explicit: bool = True
    confidence: str = "HIGH"
    priority: str = "MEDIUM"
    evidence_text: Optional[str] = None


class RequirementUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    confidence: Optional[str] = None


class RequirementResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    discovery_session_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    category: str
    title: str
    description: str
    source_type: str
    source_reference: Optional[str] = None
    explicit: bool
    confidence: str
    status: str
    priority: str
    version: int
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class DiscoveryQuestionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    discovery_session_id: uuid.UUID
    question: str
    category: str
    priority: str
    reason: Optional[str] = None
    status: str
    answer_text: Optional[str] = None
    answered_at: Optional[datetime] = None
    created_at: datetime


class AnswerQuestionSchema(BaseModel):
    answer_text: str


class ScopeItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    discovery_session_id: uuid.UUID
    requirement_id: Optional[uuid.UUID] = None
    scope_status: str
    description: str
    priority: str
    confirmed: bool
    version: int


class DiscoverySessionCreateSchema(BaseModel):
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    conversation_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None


class DiscoverySessionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    conversation_id: Optional[uuid.UUID] = None
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    readiness_stage: str
    readiness_score: float
    completeness_score: float
    scope_complexity: str
    version: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DiscoverySessionDetailSchema(DiscoverySessionResponseSchema):
    requirements: List[RequirementResponseSchema] = Field(default_factory=list)
    questions: List[DiscoveryQuestionResponseSchema] = Field(default_factory=list)
    scope_items: List[ScopeItemResponseSchema] = Field(default_factory=list)
