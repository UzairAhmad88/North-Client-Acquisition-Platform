import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import BaseModel


class Service(BaseModel):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="WEB_DEVELOPMENT", index=True
    )
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE", index=True)
    delivery_model: Mapped[str] = mapped_column(String(50), nullable=False, default="FIXED_PROJECT")
    pricing_model: Mapped[str] = mapped_column(String(50), nullable=False, default="CUSTOM")

    base_price: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    price_min: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    price_max: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")

    estimated_duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    features: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    requirements: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    target_business_types: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)

    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_services_category_status", "category", "status"),
        Index("ix_services_created_at", "created_at"),
        Index("ix_services_updated_at", "updated_at"),
    )


class LeadService(BaseModel):
    __tablename__ = "lead_services"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False, default="CONSIDERED")
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="HUMAN")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")
    service = relationship("Service", foreign_keys=[service_id], lazy="joined")

    __table_args__ = (
        UniqueConstraint("lead_id", "service_id", name="uq_lead_services_lead_service"),
    )
