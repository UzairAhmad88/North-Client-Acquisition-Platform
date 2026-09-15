import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class LeadScore(BaseModel):
    __tablename__ = "lead_scores"

    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    audit_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("business_audits.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    score_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0", index=True)
    total_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, index=True)
    band: Mapped[str] = mapped_column(String(20), nullable=False, default="VERY_LOW", index=True)
    website_need_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    online_presence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    lead_capture_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    automation_potential_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    business_activity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    contactability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    service_fit_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    breakdown: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM", index=True)
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    calculated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_lead_scores_biz_calc", "business_id", "calculated_at"),
        Index("ix_lead_scores_lead_calc", "lead_id", "calculated_at"),
    )
