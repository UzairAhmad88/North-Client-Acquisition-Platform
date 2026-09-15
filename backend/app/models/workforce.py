"""
SQLAlchemy ORM Models for Phase 52:
Unified Autonomous Knowledge Worker & Multi-Agent Workforce Platform.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

try:
    from app.models.base import Base
except ImportError:
    from app.models.base import Base


class AIWorkerModel(Base):
    """Governed AI Worker identity definition."""
    __tablename__ = "ai_workers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_code = Column(String(64), unique=True, nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    role = Column(String(64), nullable=False)
    specialization = Column(String(64), nullable=False, index=True)
    status = Column(String(32), default="ACTIVE", nullable=False, index=True)  # DRAFT, TESTING, APPROVED, SHADOW, ACTIVE, PAUSED, SUSPENDED, DEPRECATED
    supervision_level = Column(Integer, default=2, nullable=False)  # Level 0 to 5
    agent_version = Column(String(32), default="1.0", nullable=False)
    model_name = Column(String(64), default="gemini-1.5-pro", nullable=False)
    owner = Column(String(64), default="system_admin", nullable=False)
    
    # Policies & Configs
    capabilities = Column(JSONB, default=list, nullable=False)  # List of allowed capabilities
    tool_policy = Column(JSONB, default=dict, nullable=False)   # Allowed tools & call limits
    knowledge_policy = Column(JSONB, default=dict, nullable=False) # Knowledge scopes allowed
    permission_policy = Column(JSONB, default=dict, nullable=False)
    budget_policy = Column(JSONB, default=dict, nullable=False) # Max daily tokens, cost, runtime
    communication_policy = Column(JSONB, default=dict, nullable=False)
    
    # Operational stats
    total_tasks_completed = Column(Integer, default=0, nullable=False)
    total_tasks_failed = Column(Integer, default=0, nullable=False)
    total_cost_usd = Column(Float, default=0.0, nullable=False)
    average_latency_seconds = Column(Float, default=0.0, nullable=False)
    grounding_score = Column(Float, default=1.0, nullable=False)
    version = Column(Integer, default=1, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AIDepartmentModel(Base):
    """AI Department organizational unit."""
    __tablename__ = "ai_departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_code = Column(String(64), unique=True, nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    head_worker_code = Column(String(64), nullable=True)
    monthly_budget_usd = Column(Float, default=500.0, nullable=False)
    current_spend_usd = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AITeamModel(Base):
    """AI Team groupings within departments."""
    __tablename__ = "ai_teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_code = Column(String(64), unique=True, nullable=False, index=True)
    department_code = Column(String(64), nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    purpose = Column(Text, nullable=True)
    manager_worker_code = Column(String(64), nullable=True)
    workflow_template = Column(String(64), default="PARALLEL_REVIEW", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    budget_limit_usd = Column(Float, default=150.0, nullable=False)
    current_spend_usd = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AITeamMemberModel(Base):
    """Team membership mapping for workers."""
    __tablename__ = "ai_team_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_code = Column(String(64), nullable=False, index=True)
    worker_code = Column(String(64), nullable=False, index=True)
    role_in_team = Column(String(64), default="SPECIALIST", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIWorkTaskModel(Base):
    """Decomposed task assigned to AI workers."""
    __tablename__ = "ai_work_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_code = Column(String(64), unique=True, nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    parent_task_code = Column(String(64), nullable=True, index=True)
    objective = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    worker_code = Column(String(64), nullable=True, index=True)
    team_code = Column(String(64), nullable=True, index=True)
    priority = Column(String(32), default="MEDIUM", nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(32), default="CREATED", nullable=False, index=True)  # CREATED, QUEUED, ASSIGNED, RUNNING, WAITING, BLOCKED, REVIEW_REQUIRED, COMPLETED, FAILED, CANCELLED, ESCALATED
    supervision_level = Column(Integer, default=2, nullable=False)
    risk_level = Column(String(32), default="LOW", nullable=False)
    
    # Task Inputs & Outputs
    inputs = Column(JSONB, default=dict, nullable=False)
    expected_output = Column(Text, nullable=True)
    result_summary = Column(Text, nullable=True)
    result_artifacts = Column(JSONB, default=list, nullable=False)
    evidence = Column(JSONB, default=list, nullable=False)
    assumptions = Column(JSONB, default=list, nullable=False)
    
    # Execution metrics
    cost_usd = Column(Float, default=0.0, nullable=False)
    token_count = Column(Integer, default=0, nullable=False)
    runtime_seconds = Column(Float, default=0.0, nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class AIWorkTaskDependencyModel(Base):
    """Task DAG dependency edges."""
    __tablename__ = "ai_work_task_dependencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    predecessor_task_code = Column(String(64), nullable=False, index=True)
    successor_task_code = Column(String(64), nullable=False, index=True)
    is_hard_dependency = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIHandoffModel(Base):
    """Structured context & artifact handoff between workers."""
    __tablename__ = "ai_handoffs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    handoff_code = Column(String(64), unique=True, nullable=False, index=True)
    from_worker_code = Column(String(64), nullable=False, index=True)
    to_worker_code = Column(String(64), nullable=False, index=True)
    task_code = Column(String(64), nullable=False, index=True)
    context_summary = Column(Text, nullable=False)
    artifacts = Column(JSONB, default=list, nullable=False)
    evidence = Column(JSONB, default=list, nullable=False)
    assumptions = Column(JSONB, default=list, nullable=False)
    unknowns = Column(JSONB, default=list, nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    expected_next_action = Column(Text, nullable=False)
    status = Column(String(32), default="DELIVERED", nullable=False)  # DELIVERED, ACCEPTED, REJECTED

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIConsensusRunModel(Base):
    """Multi-worker independent analysis and consensus determination."""
    __tablename__ = "ai_consensus_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consensus_code = Column(String(64), unique=True, nullable=False, index=True)
    topic = Column(String(256), nullable=False)
    participating_workers = Column(JSONB, default=list, nullable=False)
    worker_opinions = Column(JSONB, default=list, nullable=False)
    consensus_score = Column(Float, default=1.0, nullable=False)
    has_conflicts = Column(Boolean, default=False, nullable=False)
    synthesized_conclusion = Column(Text, nullable=False)
    dissenting_views = Column(JSONB, default=list, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIReviewRunModel(Base):
    """Adversarial critic and risk reviewer inspection records."""
    __tablename__ = "ai_review_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_code = Column(String(64), unique=True, nullable=False, index=True)
    target_task_code = Column(String(64), nullable=False, index=True)
    author_worker_code = Column(String(64), nullable=False)
    critic_worker_code = Column(String(64), nullable=False)
    review_type = Column(String(64), default="FACT_AND_RISK", nullable=False)
    critique_summary = Column(Text, nullable=False)
    findings = Column(JSONB, default=list, nullable=False)
    quality_score = Column(Float, default=1.0, nullable=False)
    is_approved_by_critic = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIWorkerBudgetModel(Base):
    """Ledger for worker token and cost limits."""
    __tablename__ = "ai_worker_budgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_code = Column(String(64), nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    daily_cost_limit_usd = Column(Float, default=10.0, nullable=False)
    daily_cost_spent_usd = Column(Float, default=0.0, nullable=False)
    monthly_cost_limit_usd = Column(Float, default=100.0, nullable=False)
    monthly_cost_spent_usd = Column(Float, default=0.0, nullable=False)
    is_exceeded = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AIWorkerMetricModel(Base):
    """Evaluation telemetry for AI workers."""
    __tablename__ = "ai_worker_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_code = Column(String(64), nullable=False, index=True)
    period = Column(String(32), default="CURRENT_WEEK", nullable=False)
    task_success_rate = Column(Float, default=1.0, nullable=False)
    factuality_score = Column(Float, default=1.0, nullable=False)
    grounding_score = Column(Float, default=1.0, nullable=False)
    policy_compliance_rate = Column(Float, default=1.0, nullable=False)
    human_override_rate = Column(Float, default=0.0, nullable=False)
    average_latency_sec = Column(Float, default=1.5, nullable=False)
    total_tokens_consumed = Column(Integer, default=0, nullable=False)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AIWorkforcePlanModel(Base):
    """Capacity planning for AI workforce integration."""
    __tablename__ = "ai_workforce_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_code = Column(String(64), unique=True, nullable=False, index=True)
    organization_id = Column(String(64), nullable=False, index=True)
    strategic_objective_id = Column(String(64), nullable=True)
    title = Column(String(128), nullable=False)
    required_departments = Column(JSONB, default=list, nullable=False)
    required_workers = Column(JSONB, default=list, nullable=False)
    estimated_monthly_cost_usd = Column(Float, default=0.0, nullable=False)
    estimated_human_hours_saved = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="DRAFT", nullable=False)  # DRAFT, APPROVED, ACTIVE, ARCHIVED

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
