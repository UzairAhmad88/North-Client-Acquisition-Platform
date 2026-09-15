"""ORM models for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

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
from app.models.project import Project, ProjectDeliverable
from app.models.contract import Contract
from app.models.qa import ReleaseVersion
from app.models.client import ClientAccount
from app.models.business import Business


class SupportRequest(Base):
    """Client Support Ticket & Issue Request entity."""

    __tablename__ = "support_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_number = Column(String(32), nullable=False, unique=True, index=True)  # e.g. SUP-0001
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=True)
    client_account_id = Column(String(36), ForeignKey("client_accounts.id", ondelete="SET NULL"), nullable=True)
    contract_id = Column(String(36), ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True)
    release_version_id = Column(String(36), ForeignKey("release_versions.id", ondelete="SET NULL"), nullable=True)

    requester = Column(String(255), nullable=False)
    requester_email = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(64), nullable=False, default="APPLICATION")
    classification = Column(String(64), nullable=False, default="UNKNOWN", index=True)  # DEFECT, SUPPORT, MAINTENANCE, CONFIGURATION, INCIDENT, CHANGE_REQUEST, NEW_PROJECT, QUESTION, TRAINING, BILLING, UNKNOWN
    priority = Column(String(32), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    severity = Column(String(32), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(64), nullable=False, default="NEW", index=True)  # NEW, TRIAGED, ASSIGNED, IN_PROGRESS, WAITING_FOR_CLIENT, WAITING_FOR_DEPENDENCY, RESOLVED, CLIENT_VERIFICATION, CLOSED, REOPENED, CANCELLED

    warranty_status = Column(String(32), nullable=False, default="UNKNOWN")  # COVERED, NOT_COVERED, REVIEW_REQUIRED, UNKNOWN
    maintenance_status = Column(String(32), nullable=False, default="NOT_APPLICABLE")  # COVERED, BILLABLE, NOT_APPLICABLE
    sla_status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, PAUSED, BREACHED, MET, UNKNOWN

    assigned_to = Column(String(255), nullable=True)
    resolution_summary = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="support_requests")
    versions = relationship("SupportRequestVersion", back_populates="support_request", cascade="all, delete-orphan")
    events = relationship("SupportRequestEvent", back_populates="support_request", cascade="all, delete-orphan")
    evidences = relationship("SupportRequestEvidence", back_populates="support_request", cascade="all, delete-orphan")


class SupportRequestVersion(Base):
    """Immutable version snapshot history for a support request."""

    __tablename__ = "support_request_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    support_request_id = Column(String(36), ForeignKey("support_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    support_request = relationship("SupportRequest", back_populates="versions")


class SupportRequestEvent(Base):
    """Immutable audit trail log for support request lifecycle transitions."""

    __tablename__ = "support_request_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    support_request_id = Column(String(36), ForeignKey("support_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    actor_id = Column(String(255), nullable=False)
    actor_type = Column(String(32), nullable=False, default="USER")
    event_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    support_request = relationship("SupportRequest", back_populates="events")


class SupportRequestEvidence(Base):
    """Attached diagnostic evidence files, screenshots, or logs."""

    __tablename__ = "support_request_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    support_request_id = Column(String(36), ForeignKey("support_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(64), nullable=False, default="SCREENSHOT")
    sha256_hash = Column(String(64), nullable=False)
    file_size_bytes = Column(Integer, nullable=False, default=0)
    uploaded_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    support_request = relationship("SupportRequest", back_populates="evidences")


class Incident(Base):
    """Operational incident outage & degradation tracking entity."""

    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_number = Column(String(32), nullable=False, unique=True, index=True)  # e.g. INC-0001
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="SEV-2", index=True)  # SEV-1, SEV-2, SEV-3, SEV-4
    status = Column(String(64), nullable=False, default="DETECTED", index=True)  # DETECTED, ACKNOWLEDGED, INVESTIGATING, MITIGATING, RESOLVED, POST_INCIDENT_REVIEW, CLOSED
    affected_service = Column(String(128), nullable=False, default="CORE_APP")
    impact_summary = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    mitigation_steps = Column(Text, nullable=True)
    postmortem = Column(Text, nullable=True)

    detected_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    mitigated_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="incidents")
    timelines = relationship("IncidentTimeline", back_populates="incident", cascade="all, delete-orphan")


class IncidentTimeline(Base):
    """Timestamped incident milestone timeline item."""

    __tablename__ = "incident_timelines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(36), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    milestone = Column(String(64), nullable=False)  # DETECTED, ACKNOWLEDGED, MITIGATED, RESOLVED, UPDATE
    description = Column(Text, nullable=False)
    recorded_by = Column(String(255), nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    incident = relationship("Incident", back_populates="timelines")


class Warranty(Base):
    """Contractual Warranty coverage record."""

    __tablename__ = "warranties"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    contract_id = Column(String(36), ForeignKey("contracts.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False, default="Standard Deliverable Warranty")
    terms = Column(Text, nullable=True)
    exclusions = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)  # NOT_STARTED, ACTIVE, EXPIRING, EXPIRED, SUSPENDED
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="warranty")


class MaintenancePlan(Base):
    """Scheduled Maintenance Plan agreement."""

    __tablename__ = "maintenance_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    plan_type = Column(String(64), nullable=False, default="STANDARD")  # BASIC, STANDARD, PREMIUM, CUSTOM
    scope_description = Column(Text, nullable=False)
    frequency = Column(String(32), nullable=False, default="MONTHLY")  # DAILY, WEEKLY, MONTHLY, QUARTERLY
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)  # DRAFT, PROPOSED, ACTIVE, PAUSED, EXPIRED, CANCELLED
    start_date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="maintenance_plans")
    work_orders = relationship("MaintenanceWorkOrder", back_populates="maintenance_plan", cascade="all, delete-orphan")


class MaintenanceWorkOrder(Base):
    """Discrete executed maintenance work order."""

    __tablename__ = "maintenance_work_orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    maintenance_plan_id = Column(String(36), ForeignKey("maintenance_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    task_name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, default="ROUTINE_BACKUP")  # ROUTINE_BACKUP, DEPENDENCY_UPDATE, SECURITY_AUDIT, HEALTH_CHECK, DB_OPTIMIZATION
    priority = Column(String(32), nullable=False, default="MEDIUM")
    status = Column(String(32), nullable=False, default="PLANNED", index=True)  # PLANNED, IN_PROGRESS, COMPLETED, BLOCKED, FAILED, CANCELLED
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    executed_by = Column(String(255), nullable=True)
    result_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    maintenance_plan = relationship("MaintenancePlan", back_populates="work_orders")


class SLAPolicy(Base):
    """Configurable Service Level Agreement Policy."""

    __tablename__ = "sla_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(32), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    response_target_hours = Column(Float, nullable=False, default=4.0)
    resolution_target_hours = Column(Float, nullable=False, default=24.0)
    business_hours_only = Column(Boolean, nullable=False, default=True)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class KnowledgeArticle(Base):
    """Knowledge Base Article and Documentation entity."""

    __tablename__ = "knowledge_articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    article_type = Column(String(64), nullable=False, default="USER_GUIDE")  # USER_GUIDE, FAQ, TUTORIAL, TROUBLESHOOTING, RELEASE_NOTE, POLICY, DOCUMENTATION
    visibility = Column(String(32), nullable=False, default="CLIENT_VISIBLE")  # INTERNAL_ONLY, CLIENT_VISIBLE
    status = Column(String(32), nullable=False, default="PUBLISHED", index=True)  # DRAFT, REVIEW, PUBLISHED, ARCHIVED
    author = Column(String(255), nullable=False, default="System")
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class MonitoringEvent(Base):
    """Ingested observability & uptime health event."""

    __tablename__ = "monitoring_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    signal_type = Column(String(64), nullable=False)  # UPTIME, LATENCY, ERROR_RATE, CPU, MEMORY, DATABASE, API_HEALTH
    status = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, DEGRADED, AT_RISK, DOWN
    details = Column(JSON, nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class ClientHealthSnapshot(Base):
    """Multi-dimensional relationship health scoring record."""

    __tablename__ = "client_health_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=True)
    health_score = Column(Float, nullable=False, default=85.0)  # 0 to 100
    health_status = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, STABLE, AT_RISK, CRITICAL
    open_tickets_count = Column(Integer, nullable=False, default=0)
    incident_count = Column(Integer, nullable=False, default=0)
    satisfaction_score = Column(Float, nullable=True)
    recommendations = Column(JSON, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class SupportOpportunity(Base):
    """Commercial expansion opportunity detected from support signals."""

    __tablename__ = "support_opportunities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=True)
    support_request_id = Column(String(36), ForeignKey("support_requests.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    opportunity_type = Column(String(64), nullable=False, default="NEW_FEATURE")  # NEW_FEATURE, RETRACTED_SCOPE, AUTOMATION, UPGRADE, NEW_PROJECT
    estimated_value = Column(Float, nullable=True)
    confidence = Column(Float, nullable=False, default=0.85)
    status = Column(String(32), nullable=False, default="OPPORTUNITY_DRAFT", index=True)  # OPPORTUNITY_DRAFT, REVIEWED, PROPOSED, ACCEPTED, DISMISSED
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
