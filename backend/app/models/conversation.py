"""Conversation ORM model for grouping messages per lead/contact."""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Conversation(BaseModel):
    """Groups outbound and inbound messages for a lead opportunity."""

    __tablename__ = "conversations"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    contact_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contacts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False, index=True)  # ACTIVE, CLOSED, ARCHIVED, OPTED_OUT
    channel: Mapped[str] = mapped_column(String(32), default="EMAIL", nullable=False)

    current_intent: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    conversation_stage: Mapped[str] = mapped_column(String(64), default="NEW_RESPONSE", nullable=False)
    next_action: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    priority: Mapped[str] = mapped_column(String(32), default="NORMAL", nullable=False)
    last_inbound_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    messages = relationship("Message", backref="conversation", cascade="all, delete-orphan")
