"""Pydantic request and response schemas for Phase 37 Unified Communication Infrastructure."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.communication.base import (
    CommunicationType,
    ConversationType,
    DeliveryChannel,
    DeliveryStatus,
    InboxState,
    MessageVisibility,
    NotificationPriority,
)


# =============================================================================
# 1. Unified Inbox Schemas
# =============================================================================

class InboxItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    recipient_id: UUID
    notification_id: Optional[UUID] = None
    conversation_message_id: Optional[UUID] = None
    item_type: str
    title: str
    summary: str
    priority: NotificationPriority
    state: InboxState
    is_read: bool
    is_starred: bool
    is_pinned: bool
    read_at: Optional[datetime] = None
    snoozed_until: Optional[datetime] = None
    action_url: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


class InboxUnreadCountResponse(BaseModel):
    unread_count: int
    tenant_id: UUID
    recipient_id: UUID


class InboxItemUpdateRequest(BaseModel):
    state: Optional[InboxState] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    is_pinned: Optional[bool] = None
    snoozed_until: Optional[datetime] = None


class InboxBulkUpdateRequest(BaseModel):
    item_ids: List[UUID]
    state: Optional[InboxState] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    is_pinned: Optional[bool] = None
    snoozed_until: Optional[datetime] = None


class BulkUpdateResponse(BaseModel):
    updated_count: int
    tenant_id: UUID
    recipient_id: UUID


# =============================================================================
# 2. Notifications & Preferences Schemas
# =============================================================================

class NotificationCreateRequest(BaseModel):
    notification_type: CommunicationType = CommunicationType.OPERATIONAL
    priority: NotificationPriority = NotificationPriority.NORMAL
    title: str
    body: str
    source_module: str
    source_event_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    action_url: Optional[str] = None
    recipients: Optional[List[str]] = None
    channels: Optional[List[DeliveryChannel]] = None
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    notification_type: CommunicationType
    priority: NotificationPriority
    title: str
    body: str
    source_module: str
    source_event_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    action_url: Optional[str] = None
    actor_id: Optional[UUID] = None
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class NotificationPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    user_id: UUID
    notification_type: CommunicationType
    in_app_enabled: bool
    email_enabled: bool
    sms_enabled: bool
    webhook_enabled: bool
    push_enabled: bool
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    timezone: str
    created_at: datetime
    updated_at: datetime


class NotificationPreferenceUpdateRequest(BaseModel):
    notification_type: CommunicationType
    in_app_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    webhook_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    timezone: Optional[str] = None


# =============================================================================
# 3. Conversations & Messages Schemas
# =============================================================================

class ConversationCreateRequest(BaseModel):
    title: str
    conversation_type: ConversationType = ConversationType.PROJECT
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    initial_members: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    title: str
    conversation_type: ConversationType
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    created_by: UUID
    is_closed: bool
    closed_at: Optional[datetime] = None
    closed_by: Optional[UUID] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class ConversationMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    user_id: UUID
    role: str
    joined_at: datetime
    last_read_at: Optional[datetime] = None


class ConversationAttachmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    message_id: UUID
    file_name: str
    file_type: str
    file_size_bytes: int
    file_url: str
    is_verified: bool
    created_at: datetime


class ConversationMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    sender_id: UUID
    body: str
    visibility: MessageVisibility
    parent_id: Optional[UUID] = None
    is_edited: bool
    edit_count: int
    created_at: datetime
    updated_at: datetime
    attachments: List[ConversationAttachmentResponse] = []


class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    members: List[ConversationMemberResponse] = []
    messages: List[ConversationMessageResponse] = []


class ConversationMessageCreateRequest(BaseModel):
    body: str
    visibility: MessageVisibility = MessageVisibility.CLIENT_VISIBLE
    parent_id: Optional[UUID] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class ConversationMessageEditRequest(BaseModel):
    new_body: str
    edit_reason: Optional[str] = None


# =============================================================================
# 4. Deliveries & Audit Schemas
# =============================================================================

class DeliveryRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    notification_id: Optional[UUID] = None
    recipient_id: UUID
    channel: DeliveryChannel
    status: DeliveryStatus
    provider: Optional[str] = None
    provider_message_id: Optional[str] = None
    retry_count: int
    max_retries: int
    next_retry_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_details: Optional[Dict[str, Any]] = None
    created_at: datetime


class DeliveryRetryRequest(BaseModel):
    delivery_id: UUID


class RealtimeEventEnvelope(BaseModel):
    event_type: str
    channel: str
    tenant_id: UUID
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
