"""Outreach Draft ORM model."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class OutreachDraft(BaseModel):
    """Stores personalized outreach context and communication drafts for leads."""

    __tablename__ = "outreach_drafts"

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
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    agent_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agent_runs.id", ondelete="SET NULL"),
        nullable=True,
    )

    channel: Mapped[str] = mapped_column(String(32), default="EMAIL", nullable=False)
    tone: Mapped[str] = mapped_column(String(32), default="PROFESSIONAL", nullable=False)
    language: Mapped[str] = mapped_column(String(8), default="en", nullable=False)
    personalization_depth: Mapped[str] = mapped_column(String(32), default="STANDARD", nullable=False)
    objective: Mapped[str] = mapped_column(String(64), default="INTRODUCE_SERVICE", nullable=False)

    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    primary_angle: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    personalization_profile: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    claims: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)

    risk_level: Mapped[str] = mapped_column(String(32), default="LOW", nullable=False)
    outreach_readiness: Mapped[str] = mapped_column(String(32), default="READY", nullable=False)
    approval_status: Mapped[str] = mapped_column(String(32), default="PENDING_APPROVAL", nullable=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    is_stale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    lead = relationship("Lead", backref="outreach_drafts")
    business = relationship("Business", backref="outreach_drafts")
