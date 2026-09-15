import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import BaseModel


class AgentRun(BaseModel):
    __tablename__ = "agent_runs"

    workflow_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    agent_run_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    agent_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    business_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="CREATED", index=True)
    input_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    output_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM")

    tool_calls_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    steps_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    estimated_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    events = relationship("AgentEvent", back_populates="agent_run", cascade="all, delete-orphan", lazy="selectin")
    user = relationship("User", foreign_keys=[user_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")


class AgentEvent(BaseModel):
    __tablename__ = "agent_events"

    agent_run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agent_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    agent_run = relationship("AgentRun", back_populates="events")


class AIUsage(BaseModel):
    __tablename__ = "ai_usage"

    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    agent_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agent_runs.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="SUCCESS")
