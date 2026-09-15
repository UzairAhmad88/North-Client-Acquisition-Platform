"""ORM models for Project Initiation, Delivery Planning & Execution Management."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Project(BaseModel):
    """Central project execution workspace tracking initiation, WBS, health, and baseline linkage."""

    __tablename__ = "projects"

    project_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    baseline_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contract_baselines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(64), default="INITIATED", nullable=False, index=True
    )  # INITIATED, PLANNING, READY, IN_PROGRESS, ON_HOLD, COMPLETED, CANCELLED, ARCHIVED
    health: Mapped[str] = mapped_column(
        String(32), default="HEALTHY", nullable=False, index=True
    )  # HEALTHY, AT_RISK, CRITICAL, BLOCKED, COMPLETED
    priority: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # CRITICAL, HIGH, MEDIUM, LOW

    planned_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    planned_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    progress_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_actual_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # Optimistic concurrency lock

    # Relationships
    contract = relationship("Contract", backref="projects")
    baseline = relationship("ContractBaseline", backref="projects")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")
    deliverables = relationship("ProjectDeliverable", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("ProjectRisk", back_populates="project", cascade="all, delete-orphan")
    blockers = relationship("ProjectBlocker", back_populates="project", cascade="all, delete-orphan")
    client_dependencies = relationship("ClientDependency", back_populates="project", cascade="all, delete-orphan")
    assumptions = relationship("ProjectAssumption", back_populates="project", cascade="all, delete-orphan")
    scope_signals = relationship("ProjectScopeSignal", back_populates="project", cascade="all, delete-orphan")
    effort_entries = relationship("EffortEntry", back_populates="project", cascade="all, delete-orphan")
    health_snapshots = relationship("ProjectHealthSnapshot", back_populates="project", cascade="all, delete-orphan")


class ProjectMember(BaseModel):
    """Team role assignment within a project workspace."""

    __tablename__ = "project_members"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(64), default="DEVELOPER", nullable=False
    )  # OWNER, PROJECT_MANAGER, DEVELOPER, DESIGNER, AI_ENGINEER, QA, DEVOPS, SECURITY, CLIENT, VIEWER
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    project = relationship("Project", back_populates="members")
    user = relationship("User")


class ProjectTask(BaseModel):
    """WBS task or subtask within a delivery project."""

    __tablename__ = "project_tasks"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parent_task_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_tasks.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    deliverable_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_deliverables.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    milestone_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_milestones.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    task_number: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(32), default="TODO", nullable=False, index=True
    )  # TODO, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, COMPLETED, CANCELLED
    priority: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # CRITICAL, HIGH, MEDIUM, LOW

    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    planned_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    planned_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    actual_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    dependency_status: Mapped[str] = mapped_column(
        String(32), default="CLEAR", nullable=False
    )  # CLEAR, BLOCKED_BY_PREDECESSOR
    blocked_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    project = relationship("Project", back_populates="tasks")
    subtasks = relationship("ProjectTask", backref="parent_task", remote_side="ProjectTask.id")
    deliverable = relationship("ProjectDeliverable", back_populates="tasks")
    milestone = relationship("ProjectMilestone", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id])


class TaskDependency(BaseModel):
    """Dependency relationship between predecessor and successor tasks."""

    __tablename__ = "task_dependencies"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    predecessor_task_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    successor_task_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    dependency_type: Mapped[str] = mapped_column(
        String(32), default="FINISH_TO_START", nullable=False
    )  # FINISH_TO_START, START_TO_START, FINISH_TO_FINISH, START_TO_FINISH

    predecessor = relationship("ProjectTask", foreign_keys=[predecessor_task_id])
    successor = relationship("ProjectTask", foreign_keys=[successor_task_id])


class ProjectMilestone(BaseModel):
    """Milestone target within delivery timeline."""

    __tablename__ = "project_milestones"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[str] = mapped_column(
        String(32), default="UPCOMING", nullable=False, index=True
    )  # UPCOMING, IN_PROGRESS, AT_RISK, COMPLETED, MISSED, CANCELLED
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    project = relationship("Project", back_populates="milestones")
    tasks = relationship("ProjectTask", back_populates="milestone")


class ProjectDeliverable(BaseModel):
    """Project deliverable spec linked to committed baseline scope."""

    __tablename__ = "project_deliverables"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_baseline_item: Mapped[str] = mapped_column(String(255), nullable=False)
    acceptance_criteria: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False, index=True
    )  # PENDING, IN_PROGRESS, READY_FOR_REVIEW, ACCEPTED, REJECTED
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="deliverables")
    tasks = relationship("ProjectTask", back_populates="deliverable")


class ProjectRisk(BaseModel):
    """Project delivery risk item."""

    __tablename__ = "project_risks"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    probability: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH
    impact: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # LOW, MEDIUM, HIGH, CRITICAL
    severity: Mapped[str] = mapped_column(
        String(32), default="MEDIUM", nullable=False
    )  # LOW, MEDIUM, HIGH, CRITICAL
    mitigation_plan: Mapped[str] = mapped_column(Text, nullable=False)

    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(32), default="IDENTIFIED", nullable=False
    )  # IDENTIFIED, MITIGATING, RESOLVED, CLOSED

    project = relationship("Project", back_populates="risks")


class ProjectBlocker(BaseModel):
    """Active issue or constraint blocking project progress."""

    __tablename__ = "project_blockers"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(
        String(32), default="HIGH", nullable=False
    )  # LOW, MEDIUM, HIGH, CRITICAL

    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(32), default="OPEN", nullable=False
    )  # OPEN, IN_PROGRESS, RESOLVED, CANCELLED
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="blockers")


class ClientDependency(BaseModel):
    """Required client inputs or resources (assets, domain access, approvals)."""

    __tablename__ = "client_dependencies"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    required_by_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[str] = mapped_column(
        String(32), default="REQUESTED", nullable=False, index=True
    )  # REQUESTED, RECEIVED, OVERDUE, BLOCKED, CANCELLED

    project = relationship("Project", back_populates="client_dependencies")


class ProjectAssumption(BaseModel):
    """Execution assumptions tracked for baseline validity."""

    __tablename__ = "project_assumptions"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="VALID", nullable=False
    )  # VALID, INVALIDATED, UNDER_REVIEW
    invalidation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    project = relationship("Project", back_populates="assumptions")


class ProjectScopeSignal(BaseModel):
    """Detected scope expansion or change request signal during execution."""

    __tablename__ = "project_scope_signals"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    signal_type: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # FEATURE_ADDED, FEATURE_REMOVED, DELIVERABLE_CHANGED, REQUIREMENT_CHANGED, TIMELINE_CHANGED
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)  # CLIENT_REQUEST, AI_DETECTION, OPERATOR
    severity: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="DETECTED", nullable=False
    )  # DETECTED, UNDER_REVIEW, APPROVED_CHANGE_ORDER, REJECTED

    project = relationship("Project", back_populates="scope_signals")


class EffortEntry(BaseModel):
    """Manual or system time entry logging actual effort against tasks."""

    __tablename__ = "effort_entries"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    log_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    hours: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(32), default="MANUAL", nullable=False)  # MANUAL, IMPORTED, SYSTEM

    project = relationship("Project", back_populates="effort_entries")
    task = relationship("ProjectTask")
    user = relationship("User")


class ProjectHealthSnapshot(BaseModel):
    """Deterministic snapshot of project health and variance metrics."""

    __tablename__ = "project_health_snapshots"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    health: Mapped[str] = mapped_column(String(32), nullable=False)
    reasons: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    schedule_variance_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    effort_variance_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    overdue_task_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    blocked_task_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unresolved_blocker_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    project = relationship("Project", back_populates="health_snapshots")
