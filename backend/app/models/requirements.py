"""ORM models for Client Requirements & Discovery Intelligence System."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class DiscoverySession(BaseModel):
    """Tracks a client requirements discovery session lifecycle."""

    __tablename__ = "discovery_sessions"

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
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(64), default="OPEN", nullable=False, index=True
    )  # OPEN, IN_PROGRESS, WAITING_FOR_CLIENT, READY_FOR_REVIEW, CONFIRMED, ON_HOLD, CANCELLED

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    readiness_stage: Mapped[str] = mapped_column(
        String(64), default="NOT_READY", nullable=False
    )  # NOT_READY, PARTIALLY_READY, READY_FOR_REVIEW, READY_FOR_NEXT_STAGE
    readiness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    completeness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    scope_complexity: Mapped[str] = mapped_column(
        String(32), default="UNKNOWN", nullable=False
    )  # LOW, MEDIUM, HIGH, UNKNOWN

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")
    conversation = relationship("Conversation", foreign_keys=[conversation_id], lazy="joined")


class ClientRequirement(BaseModel):
    """Individual client requirement unit with source evidence, confidence, and status."""

    __tablename__ = "requirements"

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

    category: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )  # CORE_FEATURE, USER_FLOW, INTEGRATION, BUSINESS_GOAL, TECHNICAL, SECURITY, etc.
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    source_type: Mapped[str] = mapped_column(
        String(64), default="CLIENT_MESSAGE", nullable=False
    )  # CLIENT_MESSAGE, CLIENT_DOCUMENT, CLIENT_CONFIRMATION, HUMAN_NOTE, RESEARCH, AUDIT, SYSTEM_INFERENCE, AI_INFERENCE
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    explicit: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    confidence: Mapped[str] = mapped_column(
        String(32), default="HIGH", nullable=False
    )  # HIGH, MEDIUM, LOW, UNKNOWN
    status: Mapped[str] = mapped_column(
        String(64), default="PROPOSED", nullable=False, index=True
    )  # PROPOSED, IN_REVIEW, NEEDS_CLARIFICATION, CONFIRMED, REJECTED, SUPERSEDED, UNKNOWN
    priority: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    confirmed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    discovery_session = relationship("DiscoverySession", backref="requirements")


class RequirementEvidence(BaseModel):
    """Verifiable source evidence linking a requirement to source text/records."""

    __tablename__ = "requirement_evidence"

    requirement_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_type: Mapped[str] = mapped_column(String(64), nullable=False)  # MESSAGE, DOCUMENT, AUDIT, NOTE
    source_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    requirement = relationship("ClientRequirement", backref="evidence")


class RequirementDependency(BaseModel):
    """Dependency relationship graph between requirements."""

    __tablename__ = "requirement_dependencies"

    requirement_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    depends_on_requirement_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    dependency_type: Mapped[str] = mapped_column(
        String(64), default="REQUIRES", nullable=False
    )  # REQUIRES, ENHANCES, CONFLICTS_WITH, BLOCKS, RELATED_TO
    confidence: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)

    requirement = relationship(
        "ClientRequirement",
        foreign_keys=[requirement_id],
        backref="dependencies",
    )
    depends_on = relationship(
        "ClientRequirement",
        foreign_keys=[depends_on_requirement_id],
    )


class DiscoveryQuestion(BaseModel):
    """Prioritized clarification question generated during discovery."""

    __tablename__ = "requirement_questions"

    discovery_session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discovery_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_requirement_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="SET NULL"),
        nullable=True,
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="SCOPE", nullable=False)
    priority: Mapped[str] = mapped_column(
        String(32), default="HIGH", nullable=False
    )  # CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(
        String(32), default="PROPOSED", nullable=False, index=True
    )  # PROPOSED, ASKED, ANSWERED, SKIPPED, CANCELLED

    answer_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    discovery_session = relationship("DiscoverySession", backref="questions")
    source_requirement = relationship("ClientRequirement", backref="questions")


class RequirementScopeItem(BaseModel):
    """Categorized scope classification item (IN_SCOPE, OUT_OF_SCOPE, OPTIONAL, UNKNOWN)."""

    __tablename__ = "scope_items"

    discovery_session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discovery_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requirement_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("requirements.id", ondelete="SET NULL"),
        nullable=True,
    )

    scope_status: Mapped[str] = mapped_column(
        String(32), default="UNKNOWN", nullable=False, index=True
    )  # IN_SCOPE, OUT_OF_SCOPE, OPTIONAL, UNKNOWN
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    discovery_session = relationship("DiscoverySession", backref="scope_items")
    requirement = relationship("ClientRequirement", backref="scope_items")


class DiscoveryEvent(BaseModel):
    """Audit log event tracking discovery session changes."""

    __tablename__ = "discovery_events"

    discovery_session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discovery_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(String(64), nullable=False)  # DISCOVERY_STARTED, REQUIREMENT_ADDED, CONTRADICTION_DETECTED, etc.
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    discovery_session = relationship("DiscoverySession", backref="events")
