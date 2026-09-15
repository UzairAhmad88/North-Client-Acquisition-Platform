"""Risk & Quality Engine ORM models."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class RiskAssessment(BaseModel):
    """Stores risk and quality assessment evaluation results for artifacts."""

    __tablename__ = "risk_assessments"

    artifact_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    artifact_type: Mapped[str] = mapped_column(String(64), default="OUTREACH", nullable=False, index=True)

    business_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    decision: Mapped[str] = mapped_column(String(32), default="REVIEW", nullable=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False, index=True)
    quality_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    evidence_coverage: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    engine_version: Mapped[str] = mapped_column(String(32), default="1.0.0", nullable=False)
    policy_version: Mapped[str] = mapped_column(String(32), default="v1", nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    artifact_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    is_stale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="COMPLETED", nullable=False)

    human_override_decision: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    human_override_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    human_override_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    human_override_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    findings = relationship("RiskFinding", back_populates="assessment", cascade="all, delete-orphan")
    quality_checks = relationship("QualityCheck", back_populates="assessment", cascade="all, delete-orphan")


class RiskFinding(BaseModel):
    """Specific risk finding or policy violation detail recorded during evaluation."""

    __tablename__ = "risk_findings"

    risk_assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("risk_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rule_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_reference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    assessment = relationship("RiskAssessment", back_populates="findings")


class QualityCheck(BaseModel):
    """Quality metric measurement detail recorded during evaluation."""

    __tablename__ = "quality_checks"

    risk_assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("risk_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    check_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    assessment = relationship("RiskAssessment", back_populates="quality_checks")
