"""ORM models for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

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
from app.models.requirements import ClientRequirement
from app.models.project import Project, ProjectDeliverable, ProjectTask
from app.models.client import ClientAccount


class TestPlan(Base):
    """Project Test Plan and Strategy specification."""

    __test__ = False
    __tablename__ = "test_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    plan_type = Column(String(64), nullable=False, default="SYSTEM", index=True)
    status = Column(String(64), nullable=False, default="DRAFT", index=True)
    created_by = Column(String(255), nullable=False, default="QA Lead")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="test_plans")
    test_cases = relationship("TestCase", back_populates="test_plan", cascade="all, delete-orphan")


class TestCase(Base):
    """Reusable Test Case specification."""

    __test__ = False
    __tablename__ = "test_cases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(64), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    requirement_id = Column(String(36), ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True)
    deliverable_id = Column(String(36), ForeignKey("project_deliverables.id", ondelete="SET NULL"), nullable=True)
    category = Column(String(64), nullable=False, default="FUNCTIONAL")
    priority = Column(String(32), nullable=False, default="MEDIUM")
    execution_type = Column(String(32), nullable=False, default="MANUAL")
    preconditions = Column(Text, nullable=True)
    steps = Column(JSON, nullable=True)
    expected_results = Column(Text, nullable=False)
    is_regression = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(255), nullable=False, default="QA Engineer")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    test_plan = relationship("TestPlan", back_populates="test_cases")
    test_results = relationship("TestResult", back_populates="test_case", cascade="all, delete-orphan")


class TestRun(Base):
    """Executed test suite run session."""

    __test__ = False
    __tablename__ = "test_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    test_plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    environment = Column(String(64), nullable=False, default="STAGING")
    status = Column(String(64), nullable=False, default="PLANNED")
    executed_by = Column(String(255), nullable=True)
    passed_count = Column(Integer, nullable=False, default=0)
    failed_count = Column(Integer, nullable=False, default=0)
    blocked_count = Column(Integer, nullable=False, default=0)
    skipped_count = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")


class TestResult(Base):
    """Execution result for an individual test case."""

    __test__ = False
    __tablename__ = "test_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_run_id = Column(String(36), ForeignKey("test_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    test_case_id = Column(String(36), ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="UNTESTED")
    actual_results = Column(Text, nullable=True)
    execution_notes = Column(Text, nullable=True)
    executed_by = Column(String(255), nullable=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    test_run = relationship("TestRun", back_populates="results")
    test_case = relationship("TestCase", back_populates="test_results")
    evidence = relationship("TestEvidence", back_populates="test_result", cascade="all, delete-orphan")


class TestEvidence(Base):
    """Verification evidence file or screenshot reference."""

    __test__ = False
    __tablename__ = "test_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_result_id = Column(String(36), ForeignKey("test_results.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(32), nullable=False, default="SCREENSHOT")
    file_path = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    sha256_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    test_result = relationship("TestResult", back_populates="evidence")


class Defect(Base):
    """Tracked software flaw or defect entity."""

    __tablename__ = "defects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    defect_number = Column(String(32), nullable=False, unique=True, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    test_case_id = Column(String(36), ForeignKey("test_cases.id", ondelete="SET NULL"), nullable=True)
    test_run_id = Column(String(36), ForeignKey("test_runs.id", ondelete="SET NULL"), nullable=True)
    deliverable_id = Column(String(36), ForeignKey("project_deliverables.id", ondelete="SET NULL"), nullable=True)
    requirement_id = Column(String(36), ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="MEDIUM")
    priority = Column(String(32), nullable=False, default="MEDIUM")
    status = Column(String(32), nullable=False, default="OPEN", index=True)
    classification = Column(String(32), nullable=False, default="DEFECT")
    reported_by = Column(String(255), nullable=False)
    assigned_to = Column(String(255), nullable=True)
    resolution_summary = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="defects")


class UATSession(Base):
    """Client User Acceptance Testing (UAT) Session."""

    __tablename__ = "uat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    client_account_id = Column(String(36), ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    scope_description = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="PREPARING", index=True)
    scheduled_start = Column(DateTime(timezone=True), nullable=True)
    scheduled_end = Column(DateTime(timezone=True), nullable=True)
    approved_by_client = Column(Boolean, nullable=False, default=False)
    client_signoff_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="uat_sessions")
    feedbacks = relationship("UATFeedback", back_populates="uat_session", cascade="all, delete-orphan")


class UATFeedback(Base):
    """Structured Client UAT Feedback item."""

    __tablename__ = "uat_feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uat_session_id = Column(String(36), ForeignKey("uat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    deliverable_id = Column(String(36), ForeignKey("project_deliverables.id", ondelete="SET NULL"), nullable=True)
    feedback_type = Column(String(32), nullable=False, default="COMMENT")
    comments = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    submitted_by = Column(String(255), nullable=False)
    defect_id = Column(String(36), ForeignKey("defects.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    uat_session = relationship("UATSession", back_populates="feedbacks")


class AcceptanceCriteria(Base):
    """Deliverable Acceptance Criteria verification record."""

    __tablename__ = "acceptance_criteria"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    deliverable_id = Column(String(36), ForeignKey("project_deliverables.id", ondelete="SET NULL"), nullable=True)
    criterion_text = Column(Text, nullable=False)
    is_met = Column(Boolean, nullable=False, default=False)
    verified_by = Column(String(255), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class ReleaseVersion(Base):
    """Release Version readiness gate record."""

    __tablename__ = "release_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    version_tag = Column(String(64), nullable=False)
    target_environment = Column(String(64), nullable=False, default="PRODUCTION")
    status = Column(String(32), nullable=False, default="DRAFT")
    release_notes = Column(Text, nullable=True)
    qa_approval_status = Column(String(32), nullable=False, default="PENDING")
    client_approval_status = Column(String(32), nullable=False, default="PENDING")
    released_at = Column(DateTime(timezone=True), nullable=True)
    released_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="releases")
    packages = relationship("DeliveryPackage", back_populates="release", cascade="all, delete-orphan")


class DeliveryPackage(Base):
    """Formal Delivery Package manifest."""

    __tablename__ = "delivery_packages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    release_version_id = Column(String(36), ForeignKey("release_versions.id", ondelete="SET NULL"), nullable=True)
    package_name = Column(String(255), nullable=False)
    storage_url = Column(String(512), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    file_size_bytes = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    release = relationship("ReleaseVersion", back_populates="packages")


class HandoverChecklist(Base):
    """Structured Handover checklist & Client Final Acceptance record."""

    __tablename__ = "handover_checklists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False, default="Final Project Handover")
    code_repository_transferred = Column(Boolean, nullable=False, default=False)
    documentation_delivered = Column(Boolean, nullable=False, default=False)
    credentials_transferred = Column(Boolean, nullable=False, default=False)
    training_completed = Column(Boolean, nullable=False, default=False)
    deployment_verified = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="IN_PROGRESS")
    signed_off_by_client = Column(Boolean, nullable=False, default=False)
    client_signoff_hash = Column(String(64), nullable=True)
    signed_off_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("Project", backref="handover_checklist")


class QAEvent(Base):
    """Immutable audit trail log for QA, UAT, Acceptance, and Handover events."""

    __tablename__ = "qa_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    actor_id = Column(String(255), nullable=False)
    actor_type = Column(String(32), nullable=False, default="USER")
    event_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
