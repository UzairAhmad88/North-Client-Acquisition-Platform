"""Pydantic schemas for Client Collaboration API endpoints."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class InvitationCreateSchema(BaseModel):
    """Request schema to invite a new client user."""

    client_account_id: uuid.UUID
    email: str = Field(..., description="Client email address")
    role: str = Field("CLIENT_MEMBER", description="CLIENT_OWNER, CLIENT_ADMIN, CLIENT_MEMBER, CLIENT_REVIEWER, CLIENT_VIEWER")


class InvitationAcceptSchema(BaseModel):
    """Request schema to accept client portal invitation."""

    raw_token: str = Field(..., description="Invitation token string")


class ThreadCreateSchema(BaseModel):
    """Request schema to create a discussion thread."""

    title: str = Field(..., description="Thread title")
    thread_type: str = Field("GENERAL", description="GENERAL, DELIVERABLE, QUESTION, FEEDBACK, REQUEST, ANNOUNCEMENT")
    visibility: str = Field("CLIENT_VISIBLE", description="CLIENT_VISIBLE or INTERNAL_ONLY")
    deliverable_id: Optional[uuid.UUID] = None


class MessageCreateSchema(BaseModel):
    """Request schema to post a thread message."""

    content: str = Field(..., description="Message text content")
    visibility: str = Field("CLIENT_VISIBLE", description="CLIENT_VISIBLE or INTERNAL_ONLY")
    attachments: List[Dict[str, Any]] = Field(default_factory=list)


class DeliverableApprovalSchema(BaseModel):
    """Request schema for explicit deliverable approval."""

    version_number: int = Field(..., ge=1)
    approval_statement: str = Field(..., description="Assent text statement")
    content_payload: str = Field(..., description="Deliverable content payload to compute SHA-256 hash")


class ClientRequestCreateSchema(BaseModel):
    """Request schema for client request intake."""

    title: str
    description: str


class ClientFeedbackCreateSchema(BaseModel):
    """Request schema for submitting deliverable feedback."""

    category: str = Field("FUNCTIONALITY", description="DESIGN, FUNCTIONALITY, CONTENT, PERFORMANCE, BUG, USABILITY")
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5)


class ClientActionItemCreateSchema(BaseModel):
    """Request schema for creating a client action item."""

    title: str
    description: str
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None


class MessageResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thread_id: uuid.UUID
    sender_id: uuid.UUID
    sender_type: str
    content: str
    visibility: str
    created_at: datetime


class ThreadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    type: str
    title: str
    status: str
    visibility: str
    messages: List[MessageResponseSchema] = []
    created_at: datetime


class DeliverableApprovalResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deliverable_id: uuid.UUID
    version_number: int
    content_hash: str
    approval_statement: str
    signer_name: str
    signer_email: str
    approved_at: datetime


class ProjectFileResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    filename: str
    mime_type: str
    size_bytes: int
    visibility: str
    status: str
    created_at: datetime
