"""ORM models for Proposal Generation & Review System."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Proposal(BaseModel):
    """Client-facing commercial and technical proposal document."""

    __tablename__ = "proposals"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    proposal_type: Mapped[str] = mapped_column(
        String(64), default="FULL", nullable=False
    )  # TECHNICAL, COMMERCIAL, FULL
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(64), default="DRAFT", nullable=False, index=True
    )  # DRAFT, IN_REVIEW, REVISION_REQUIRED, APPROVED, SENT, ACCEPTED, REJECTED, EXPIRED, CANCELLED

    pricing_status: Mapped[str] = mapped_column(
        String(64), default="PRICING_REQUIRES_HUMAN_REVIEW", nullable=False
    )  # NOT_DEFINED, DRAFT, APPROVED, PRICING_REQUIRES_HUMAN_REVIEW

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    solution = relationship("SolutionDesign", foreign_keys=[solution_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")


class ProposalItem(BaseModel):
    """Individual line item or deliverable entry in a proposal."""

    __tablename__ = "proposal_items"

    proposal_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    service_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("services.id", ondelete="SET NULL"),
        nullable=True,
    )
    deliverable_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_deliverables.id", ondelete="SET NULL"),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), default="project", nullable=False)
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    proposal = relationship("Proposal", backref="items")
    service = relationship("Service")
    deliverable = relationship("SolutionDeliverable")


class ProposalVersion(BaseModel):
    """Historical snapshot version of a proposal document."""

    __tablename__ = "proposal_versions"

    proposal_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    sections_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    proposal = relationship("Proposal", backref="versions")
