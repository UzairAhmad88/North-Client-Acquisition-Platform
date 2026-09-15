import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Business(BaseModel):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    business_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default="OTHER", index=True
    )
    industry: Mapped[str] = mapped_column(String(100), nullable=False, default="OTHER", index=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    normalized_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    normalized_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    website_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, index=True)
    normalized_website: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, index=True
    )

    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Pakistan")
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE", index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="MANUAL", index=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)

    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_businesses_source_external_id", "source", "external_id"),
        Index("ix_businesses_created_at", "created_at"),
        Index("ix_businesses_updated_at", "updated_at"),
    )
