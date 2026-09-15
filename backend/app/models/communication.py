"""ORM models for Phase 37: Unified Notification, Communication, Inbox & Real-Time Collaboration."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


# -------------------------------------------------------------
# 1. Notifications & Templates
# -------------------------------------------------------------
class NotificationRecord(BaseModel):
    """Notification item delivered to a specific recipient."""

    __tablename__ = "notification_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    recipient_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="OPERATIONAL", nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(50), default="NORMAL", nullable=False)
    action_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="DELIVERED", nullable=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class NotificationTemplateRecord(BaseModel):
    """Versioned template for automated communication dispatch."""

    __tablename__ = "notification_template_records"

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(50), default="IN_APP", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    subject_template: Mapped[str] = mapped_column(String(255), nullable=False)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    required_variables: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class NotificationPreferenceRecord(BaseModel):
    """User and tenant communication and quiet-hours preferences."""

    __tablename__ = "notification_preference_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    quiet_hours_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    quiet_hours_start: Mapped[int] = mapped_column(Integer, default=22, nullable=False)
    quiet_hours_end: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    category_preferences: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


# -------------------------------------------------------------
# 2. Unified Inbox
# -------------------------------------------------------------
class InboxItemRecord(BaseModel):
    """Aggregated Unified Inbox item."""

    __tablename__ = "inbox_item_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    recipient_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    notification_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="OPERATIONAL", nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(50), default="NORMAL", nullable=False)
    state: Mapped[str] = mapped_column(String(50), default="UNREAD", nullable=False, index=True)
    source_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    action_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    snoozed_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# -------------------------------------------------------------
# 3. Conversations & Messages
# -------------------------------------------------------------
class ConversationRecord(BaseModel):
    """Conversation thread across teams or client portal."""

    __tablename__ = "conversation_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    conversation_type: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False, index=True)
    project_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    client_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    messages: Mapped[List["ConversationMessageRecord"]] = relationship(
        "ConversationMessageRecord", back_populates="conversation", cascade="all, delete-orphan"
    )


class ConversationMemberRecord(BaseModel):
    """Participant in a conversation."""

    __tablename__ = "conversation_member_records"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), default="MEMBER", nullable=False)


class ConversationMessageRecord(BaseModel):
    """Individual message with visibility boundary."""

    __tablename__ = "conversation_message_records"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sender_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sender_type: Mapped[str] = mapped_column(String(50), default="USER", nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    reply_to_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    conversation: Mapped["ConversationRecord"] = relationship("ConversationRecord", back_populates="messages")
    versions: Mapped[List["ConversationMessageVersionRecord"]] = relationship(
        "ConversationMessageVersionRecord", back_populates="message", cascade="all, delete-orphan"
    )
    attachments: Mapped[List["ConversationAttachmentRecord"]] = relationship(
        "ConversationAttachmentRecord", back_populates="message", cascade="all, delete-orphan"
    )


class ConversationMessageVersionRecord(BaseModel):
    """Historical snapshot of an edited message."""

    __tablename__ = "conversation_message_version_records"

    message_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation_message_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    editor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    edited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    message: Mapped["ConversationMessageRecord"] = relationship(
        "ConversationMessageRecord", back_populates="versions"
    )


class ConversationAttachmentRecord(BaseModel):
    """File attachment associated with a conversation message."""

    __tablename__ = "conversation_attachment_records"

    message_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation_message_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="application/pdf", nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)

    message: Mapped["ConversationMessageRecord"] = relationship(
        "ConversationMessageRecord", back_populates="attachments"
    )


# -------------------------------------------------------------
# 4. Deliveries & Audit
# -------------------------------------------------------------
class CommunicationDeliveryRecord(BaseModel):
    """Tracking record for outbound email, push, or messaging delivery."""

    __tablename__ = "communication_delivery_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    recipient_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(50), default="IN_APP", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DELIVERED", nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class CommunicationAuditRecord(BaseModel):
    """Immutable audit trail for all communication operations."""

    __tablename__ = "communication_audit_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    actor_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_recipient: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    outcome: Mapped[str] = mapped_column(String(50), default="SUCCESS", nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class RealtimeSubscriptionRecord(BaseModel):
    """Active or historical real-time channel subscription registration."""

    __tablename__ = "realtime_subscription_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    channel_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
