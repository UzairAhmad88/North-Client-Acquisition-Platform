import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class LeadQualification(BaseModel):
    __tablename__ = "lead_qualifications"

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
        index=True,
    )
    agent_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agent_runs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    decision: Mapped[str] = mapped_column(
        String(50), nullable=False, default="INSUFFICIENT_DATA", index=True
    )  # QUALIFIED, POTENTIALLY_QUALIFIED, NEEDS_REVIEW, NOT_QUALIFIED, INSUFFICIENT_DATA
    confidence: Mapped[str] = mapped_column(
        String(20), nullable=False, default="MEDIUM", index=True
    )  # HIGH, MEDIUM, LOW

    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    factors: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    reasons: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    risks: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_information: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    limitations: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)

    outreach_readiness: Mapped[str] = mapped_column(
        String(50), nullable=False, default="NOT_READY", index=True
    )  # OUTREACH_READY, NEEDS_VERIFICATION, NOT_READY, OUTREACH_BLOCKED
    recommended_internal_action: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    qualification_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    human_override_decision: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    human_override_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    overridden_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    overridden_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("ix_lead_qualifications_lead_created", "lead_id", "created_at"),
        Index("ix_lead_qualifications_biz_created", "business_id", "created_at"),
    )
