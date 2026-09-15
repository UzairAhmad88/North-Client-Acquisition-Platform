"""Message ORM model representing individual outbound or inbound communications."""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Message(BaseModel):
    """Represents an individual communication item in a conversation."""

    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outreach_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("outreach_drafts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    direction: Mapped[str] = mapped_column(String(16), default="OUTBOUND", nullable=False)  # OUTBOUND, INBOUND
    channel: Mapped[str] = mapped_column(String(32), default="EMAIL", nullable=False)
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="SENT", nullable=False)  # QUEUED, SENT, DELIVERED, FAILED, BOUNCED
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
