import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Lead(BaseModel):
    __tablename__ = "leads"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="NEW", index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="MANUAL", index=True)
    source_detail: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="MEDIUM", index=True)
    owner_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    qualification_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="UNQUALIFIED", index=True
    )
    contactability_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="UNKNOWN", index=True
    )

    estimated_value: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")

    next_action: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    next_action_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    first_contacted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_contacted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    converted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    lost_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    loss_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    owner = relationship("User", foreign_keys=[owner_user_id], lazy="joined")

    __table_args__ = (
        Index("ix_leads_status_priority", "status", "priority"),
        Index("ix_leads_created_at", "created_at"),
        Index("ix_leads_updated_at", "updated_at"),
    )
