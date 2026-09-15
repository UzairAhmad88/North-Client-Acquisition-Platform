"""ORM models for Solution Design Intelligence System."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class SolutionDesign(BaseModel):
    """Stores high-level solution design architecture, feature mappings, and deliverables."""

    __tablename__ = "solution_designs"

    discovery_session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discovery_sessions.id", ondelete="CASCADE"),
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

    status: Mapped[str] = mapped_column(
        String(64), default="DRAFT", nullable=False, index=True
    )  # DRAFT, GENERATED, REVIEW, REVISED, APPROVED, REJECTED, CANCELLED

    overview: Mapped[str] = mapped_column(Text, nullable=False)
    architecture_summary: Mapped[str] = mapped_column(Text, nullable=False)
    complexity_tier: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # LOW, MEDIUM, HIGH, VERY_HIGH, UNKNOWN
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

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

    discovery_session = relationship("DiscoverySession", foreign_keys=[discovery_session_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")


class SolutionFeature(BaseModel):
    """Recommended solution feature mapped to client requirements."""

    __tablename__ = "solution_features"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    status: Mapped[str] = mapped_column(
        String(64), default="RECOMMENDED", nullable=False, index=True
    )  # REQUIRED, RECOMMENDED, OPTIONAL, DEFERRED, OUT_OF_SCOPE, UNKNOWN
    priority: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL

    solution = relationship("SolutionDesign", backref="features")


class SolutionDeliverable(BaseModel):
    """Concrete deliverable unit producing project outcomes."""

    __tablename__ = "solution_deliverables"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(64), default="PROPOSED", nullable=False
    )  # PROPOSED, APPROVED, INCLUDED, OPTIONAL
    priority: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    solution = relationship("SolutionDesign", backref="deliverables")


class SolutionDependency(BaseModel):
    """Dependency relationship between features in a solution."""

    __tablename__ = "solution_dependencies"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    feature_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_features.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    depends_on_feature_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_features.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    dependency_type: Mapped[str] = mapped_column(
        String(64), default="REQUIRES", nullable=False
    )  # REQUIRES, ENHANCES, BLOCKS

    feature = relationship("SolutionFeature", foreign_keys=[feature_id], backref="dependencies")
    depends_on = relationship("SolutionFeature", foreign_keys=[depends_on_feature_id])


class SolutionIntegration(BaseModel):
    """External integration specification in a solution."""

    __tablename__ = "solution_integrations"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    purpose: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(128), nullable=False)
    data_flow: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PROPOSED", nullable=False)

    solution = relationship("SolutionDesign", backref="integrations")


class SolutionAssumption(BaseModel):
    """Technical or operational assumption underpinning a solution design."""

    __tablename__ = "solution_assumptions"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    assumption_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(64), default="UNCONFIRMED", nullable=False
    )  # CONFIRMED, UNCONFIRMED, REQUIRES_CLIENT_INPUT
    risk_level: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # LOW, MEDIUM, HIGH

    solution = relationship("SolutionDesign", backref="assumptions")


class SolutionRequirementLink(BaseModel):
    """Traceability mapping link connecting solution features to confirmed requirements."""

    __tablename__ = "solution_requirement_links"

    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    feature_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_features.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requirement_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    relationship_type: Mapped[str] = mapped_column(
        String(64), default="ADDRESSES", nullable=False
    )  # ADDRESSES, IMPLEMENTS, DEPENDS_ON, OPTIONAL_FOR

    feature = relationship("SolutionFeature", backref="requirement_links")
    requirement = relationship("ClientRequirement")
