import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import BaseModel


class ServiceRecommendation(BaseModel):
    __tablename__ = "service_recommendations"

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
    service_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    recommendation_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0", index=True)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, index=True)
    band: Mapped[str] = mapped_column(String(20), nullable=False, default="POSSIBLE", index=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM", index=True)
    confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM", index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUGGESTED", index=True)

    reasons: Mapped[List[Any]] = mapped_column(JSON, nullable=False, default=list)
    evidence: Mapped[List[Any]] = mapped_column(JSON, nullable=False, default=list)
    limitations: Mapped[List[Any]] = mapped_column(JSON, nullable=False, default=list)

    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rejected_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    rejected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    accepted_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    service = relationship("Service", foreign_keys=[service_id], lazy="joined")
    accepted_by_user = relationship("User", foreign_keys=[accepted_by], lazy="selectin")
    rejected_by_user = relationship("User", foreign_keys=[rejected_by], lazy="selectin")

    __table_args__ = (
        Index("ix_service_recommendations_lead_status", "lead_id", "status"),
        Index("ix_service_recommendations_lead_service", "lead_id", "service_id"),
    )
