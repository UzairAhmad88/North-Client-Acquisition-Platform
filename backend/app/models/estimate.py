"""ORM models for Project Estimation, Effort & Commercial Intelligence Engine."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ProjectEstimate(BaseModel):
    """Central project estimation record tracking effort, costs, risk buffer, and recommended commercial range."""

    __tablename__ = "project_estimates"

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

    status: Mapped[str] = mapped_column(
        String(64), default="DRAFT", nullable=False, index=True
    )  # DRAFT, CALCULATING, CALCULATED, REVIEW, REVISED, APPROVED, STALE, REJECTED, CANCELLED, BLOCKED

    complexity: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # TRIVIAL, LOW, MEDIUM, HIGH, VERY_HIGH, UNKNOWN

    confidence: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # HIGH, MEDIUM, LOW

    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    minimum_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    maximum_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    risk_buffer_percent: Mapped[float] = mapped_column(Float, default=20.0, nullable=False)
    internal_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    external_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    recommended_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recommended_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    requirements_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    solution_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    pricing_policy_version: Mapped[str] = mapped_column(String(32), default="v1.0", nullable=False)
    cost_model_version: Mapped[str] = mapped_column(String(32), default="v1.0", nullable=False)

    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    solution = relationship("SolutionDesign", foreign_keys=[solution_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")

    work_items = relationship("EstimateWorkItem", back_populates="estimate", cascade="all, delete-orphan")
    costs = relationship("EstimateCostItem", back_populates="estimate", cascade="all, delete-orphan")
    scenarios = relationship("EstimateScenario", back_populates="estimate", cascade="all, delete-orphan")
    versions = relationship("EstimateVersion", back_populates="estimate", cascade="all, delete-orphan")


class EstimateWorkItem(BaseModel):
    """Work Breakdown Structure (WBS) item estimated in hours."""

    __tablename__ = "estimate_work_items"

    estimate_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requirement_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True
    )
    feature_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("solution_features.id", ondelete="SET NULL"), nullable=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(
        String(64), default="BACKEND", nullable=False, index=True
    )  # DISCOVERY, DESIGN, FRONTEND, BACKEND, DATABASE, API, INTEGRATION, AI, ML, TESTING, SECURITY, DEVOPS, DEPLOYMENT, DOCUMENTATION, MAINTENANCE
    description: Mapped[str] = mapped_column(Text, nullable=False)
    complexity: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)

    optimistic_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    most_likely_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pessimistic_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    expected_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    confidence: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)

    estimate = relationship("ProjectEstimate", back_populates="work_items")


class EstimateCostItem(BaseModel):
    """Itemized labor and third-party external operating costs."""

    __tablename__ = "estimate_cost_items"

    estimate_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cost_type: Mapped[str] = mapped_column(
        String(64), default="INTERNAL", nullable=False, index=True
    )  # INTERNAL, EXTERNAL, INFRASTRUCTURE, PROVIDER, OTHER
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    source: Mapped[str] = mapped_column(String(64), default="CONFIGURED_RATE", nullable=False)

    estimate = relationship("ProjectEstimate", back_populates="costs")


class EstimateScenario(BaseModel):
    """Estimation scope and commercial scenario comparison."""

    __tablename__ = "estimate_scenarios"

    estimate_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)  # LEAN, STANDARD, EXPANDED
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(Text, nullable=False)

    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)
    internal_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    external_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    recommended_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recommended_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    risk_level: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PROPOSED", nullable=False)

    estimate = relationship("ProjectEstimate", back_populates="scenarios")


class EstimateVersion(BaseModel):
    """Historical snapshot version of project estimate."""

    __tablename__ = "estimate_versions"

    estimate_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    snapshot_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    estimate = relationship("ProjectEstimate", back_populates="versions")
