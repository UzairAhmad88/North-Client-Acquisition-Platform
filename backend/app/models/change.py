"""ORM models for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class ChangeRequest(Base):
    """Core Change Request entity tracking scope, technical, schedule, and commercial changes."""

    __tablename__ = "change_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_number = Column(String(32), nullable=False, unique=True, index=True)  # e.g. CR-0001
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=True, index=True)
    client_id = Column(String(36), ForeignKey("client_accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    contract_id = Column(String(36), ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True, index=True)
    baseline_id = Column(String(36), ForeignKey("contract_baselines.id", ondelete="SET NULL"), nullable=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(64), nullable=False, default="SCOPE")  # SCOPE, FEATURE, REQUIREMENT, DELIVERABLE, DESIGN, TECHNICAL, INTEGRATION, TIMELINE, RESOURCE, COMMERCIAL, CONTENT, SECURITY, PERFORMANCE, MAINTENANCE, OTHER
    classification = Column(String(64), nullable=False, default="UNKNOWN")  # IN_SCOPE, OUT_OF_SCOPE, CLARIFICATION, DEFECT, CLIENT_CHANGE, INTERNAL_CHANGE, DEPENDENCY_CHANGE, CONTRACT_CHANGE, COMMERCIAL_CHANGE, UNKNOWN
    status = Column(String(64), nullable=False, default="REQUESTED", index=True)  # REQUESTED, TRIAGED, IMPACT_ANALYSIS, ESTIMATION, INTERNAL_REVIEW, PENDING_CLIENT, CLIENT_APPROVED, APPROVED, BASELINE_UPDATE, IMPLEMENTATION, COMPLETED, REJECTED, CANCELLED, WITHDRAWN, EXPIRED, ON_HOLD, SUPERSEDED
    priority = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    source = Column(String(64), nullable=False, default="CLIENT_PORTAL")  # CLIENT_PORTAL, CLIENT_MESSAGE, EMAIL, MEETING, INTERNAL_USER, PROJECT_TASK, REQUIREMENT, CONTRACT, SYSTEM_DETECTION, AI_DETECTION
    reason = Column(Text, nullable=True)

    requested_by = Column(String(255), nullable=False)
    requested_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    impact_status = Column(String(64), nullable=False, default="NOT_STARTED")  # NOT_STARTED, IN_PROGRESS, COMPLETED
    approval_status = Column(String(64), nullable=False, default="PENDING")  # PENDING, INTERNAL_APPROVED, REJECTED
    client_approval_status = Column(String(64), nullable=False, default="PENDING")  # PENDING, CLIENT_APPROVED, REJECTED
    implementation_status = Column(String(64), nullable=False, default="NOT_STARTED")  # NOT_STARTED, READY, IN_PROGRESS, COMPLETED

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="change_requests")
    business = relationship("Business", backref="change_requests")
    client_account = relationship("ClientAccount", backref="change_requests")
    versions = relationship("ChangeRequestVersion", back_populates="change_request", cascade="all, delete-orphan", order_by="ChangeRequestVersion.version_number.desc()")
    evidences = relationship("ChangeEvidence", back_populates="change_request", cascade="all, delete-orphan")
    events = relationship("ChangeEvent", back_populates="change_request", cascade="all, delete-orphan", order_by="ChangeEvent.created_at.asc()")


class ChangeRequestVersion(Base):
    """Immutable version snapshot for a Change Request proposal."""

    __tablename__ = "change_request_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_id = Column(String(36), ForeignKey("change_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=False)
    scope_summary = Column(Text, nullable=True)
    commercial_summary = Column(Text, nullable=True)
    schedule_summary = Column(Text, nullable=True)
    impact_summary = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=False)  # SHA-256 hash of payload
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_request = relationship("ChangeRequest", back_populates="versions")
    impacts = relationship("ChangeImpact", back_populates="change_version", cascade="all, delete-orphan")
    estimates = relationship("ChangeEstimate", back_populates="change_version", cascade="all, delete-orphan")
    commercials = relationship("ChangeCommercial", back_populates="change_version", cascade="all, delete-orphan")
    approvals = relationship("ChangeApproval", back_populates="change_version", cascade="all, delete-orphan")


class ChangeEvidence(Base):
    """Source evidence supporting a change request."""

    __tablename__ = "change_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_id = Column(String(36), ForeignKey("change_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type = Column(String(64), nullable=False)  # CLIENT_MESSAGE, REQUIREMENT, CONTRACT_SECTION, TASK, DELIVERABLE, MEETING_NOTE, FILE
    source_id = Column(String(255), nullable=False)
    source_version = Column(String(64), nullable=True)
    evidence_excerpt = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_request = relationship("ChangeRequest", back_populates="evidences")


class ChangeImpact(Base):
    """Detailed multi-dimensional impact item of a change version."""

    __tablename__ = "change_impacts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_version_id = Column(String(36), ForeignKey("change_request_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    impact_type = Column(String(64), nullable=False)  # REQUIREMENT, SOLUTION, DELIVERABLE, TASK, MILESTONE, DEPENDENCY, RESOURCE, RISK, SCHEDULE, EFFORT, COMMERCIAL, CONTRACT
    entity_type = Column(String(64), nullable=True)
    entity_id = Column(String(255), nullable=True)
    impact_action = Column(String(32), nullable=False, default="AFFECTED")  # ADDED, REMOVED, MODIFIED, AFFECTED, NO_IMPACT, UNKNOWN
    impact_description = Column(Text, nullable=False)
    confidence = Column(String(32), nullable=False, default="HIGH")  # HIGH, MEDIUM, LOW, UNKNOWN
    evidence_reference = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_version = relationship("ChangeRequestVersion", back_populates="impacts")


class ChangeEstimate(Base):
    """PERT effort re-estimation details for a change request version."""

    __tablename__ = "change_estimates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_version_id = Column(String(36), ForeignKey("change_request_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    estimate_version_id = Column(String(36), ForeignKey("estimate_versions.id", ondelete="SET NULL"), nullable=True)
    optimistic_hours = Column(Float, nullable=False, default=0.0)
    most_likely_hours = Column(Float, nullable=False, default=0.0)
    pessimistic_hours = Column(Float, nullable=False, default=0.0)
    expected_hours = Column(Float, nullable=False, default=0.0)  # (O + 4M + P)/6
    confidence = Column(Float, nullable=False, default=0.85)
    assumptions = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_version = relationship("ChangeRequestVersion", back_populates="estimates")


class ChangeCommercial(Base):
    """Commercial impact record capturing price delta and baseline comparison."""

    __tablename__ = "change_commercials"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_version_id = Column(String(36), ForeignKey("change_request_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    currency = Column(String(10), nullable=False, default="PKR")
    original_value = Column(Float, nullable=False, default=0.0)
    change_value = Column(Float, nullable=False, default=0.0)
    revised_value = Column(Float, nullable=False, default=0.0)
    pricing_policy_version = Column(String(32), nullable=False, default="1.0")
    estimate_version_id = Column(String(36), nullable=True)
    cost_model_version = Column(String(32), nullable=False, default="1.0")
    status = Column(String(32), nullable=False, default="DRAFT")  # DRAFT, REVIEWED, APPROVED
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_version = relationship("ChangeRequestVersion", back_populates="commercials")


class ChangeApproval(Base):
    """Auditable approval record for internal and client sign-offs."""

    __tablename__ = "change_approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_version_id = Column(String(36), ForeignKey("change_request_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    approver_id = Column(String(255), nullable=False)
    approval_type = Column(String(32), nullable=False)  # INTERNAL, CLIENT, COMMERCIAL, CONTRACT
    status = Column(String(32), nullable=False, default="APPROVED")  # PENDING, APPROVED, REJECTED, REVOKED
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_at = Column(DateTime(timezone=True), nullable=True)
    reason = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_version = relationship("ChangeRequestVersion", back_populates="approvals")


class ChangeBaselineLink(Base):
    """Maps change request approval to predecessor and revised ContractBaselines."""

    __tablename__ = "change_baseline_links"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_id = Column(String(36), ForeignKey("change_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    previous_baseline_id = Column(String(36), ForeignKey("contract_baselines.id", ondelete="RESTRICT"), nullable=False)
    new_baseline_id = Column(String(36), ForeignKey("contract_baselines.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class ChangeEvent(Base):
    """Immutable audit trail log for change management events."""

    __tablename__ = "change_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_request_id = Column(String(36), ForeignKey("change_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)  # CHANGE_CREATED, CHANGE_TRIAGED, CHANGE_CLASSIFIED, IMPACT_ANALYSIS_STARTED, IMPACT_ANALYSIS_COMPLETED, CHANGE_ESTIMATED, COMMERCIAL_ANALYSIS_COMPLETED, INTERNAL_APPROVAL_GRANTED, CLIENT_APPROVAL_GRANTED, CHANGE_REJECTED, BASELINE_UPDATED, IMPLEMENTATION_STARTED, IMPLEMENTATION_COMPLETED, CHANGE_CANCELLED, CHANGE_SUPERSEDED
    actor_id = Column(String(255), nullable=False)
    actor_type = Column(String(32), nullable=False, default="USER")  # USER, CLIENT, SYSTEM, AGENT
    event_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    change_request = relationship("ChangeRequest", back_populates="events")
