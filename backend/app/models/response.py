"""ORM models for Response & Conversation Intelligence System."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ConversationAnalysis(BaseModel):
    """Stores AI intent classification, buying signals, objections, requirements, and next action recommendations."""

    __tablename__ = "conversation_analyses"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    latest_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )
    agent_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agent_runs.id", ondelete="SET NULL"),
        nullable=True,
    )

    primary_intent: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    all_intents: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    intent_confidence: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    buying_signal_level: Mapped[str] = mapped_column(String(32), default="NONE", nullable=False)
    objection_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    extracted_requirements: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    missing_information: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)

    conversation_stage: Mapped[str] = mapped_column(String(64), default="NEW_RESPONSE", nullable=False, index=True)
    recommended_next_action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    recommended_next_action_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_action_confidence: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    sentiment_signal: Mapped[str] = mapped_column(String(32), default="NEUTRAL", nullable=False)
    priority: Mapped[str] = mapped_column(String(32), default="NORMAL", nullable=False)

    human_correction: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    human_correction_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    human_correction_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    conversation = relationship("Conversation", backref="analyses")


class InboundEventLog(BaseModel):
    """Raw provider inbound event log for idempotency and auditability."""

    __tablename__ = "inbound_event_logs"

    provider: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    provider_event_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(32), default="EMAIL", nullable=False)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)

    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="PROCESSED", nullable=False)  # PROCESSED, DUPLICATE, FAILED
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class ConversationFact(BaseModel):
    """Structured memory facts extracted from conversation history."""

    __tablename__ = "conversation_facts"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    category: Mapped[str] = mapped_column(String(64), nullable=False)  # REQUIREMENT, PREFERENCE, OBJECTION, BUDGET, TIMELINE
    fact_key: Mapped[str] = mapped_column(String(128), nullable=False)
    fact_value: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)  # ACTIVE, SUPERSEDED, CONTRADICTED

    conversation = relationship("Conversation", backref="facts")
