"""SQLAlchemy Models for Phase 34: Unified Workflow Orchestration, Event Bus & Automation Control Plane."""

import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    Float,
    Integer,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class EventSensitivity(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class EventDeliveryStatus(str, Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    DEAD_LETTER = "DEAD_LETTER"


class WorkflowStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class WorkflowStepStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


class TaskType(str, Enum):
    AGENT_TASK = "AGENT_TASK"
    WORKER_TASK = "WORKER_TASK"
    HUMAN_TASK = "HUMAN_TASK"
    SYSTEM_TASK = "SYSTEM_TASK"
    INTEGRATION_TASK = "INTEGRATION_TASK"


class TaskPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"
    BACKGROUND = "BACKGROUND"


class DLQStatus(str, Enum):
    PENDING = "PENDING"
    INVESTIGATING = "INVESTIGATING"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    REPLAYED = "REPLAYED"
    RESOLVED = "RESOLVED"
    DISCARDED = "DISCARDED"


class HumanTaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class ReplayMode(str, Enum):
    READ_ONLY = "READ_ONLY"
    DRY_RUN = "DRY_RUN"
    REBUILD_PROJECTION = "REBUILD_PROJECTION"
    CONTROLLED_REEXECUTION = "CONTROLLED_REEXECUTION"


# ==============================================================================
# 1. Event Registry & Version Contracts
# ==============================================================================

class EventRegistryItem(Base):
    """Central registry of registered domain events across all subsystems."""
    __tablename__ = "event_registry_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_name = Column(String(100), nullable=False, unique=True, index=True)
    current_version = Column(String(20), nullable=False, default="v1")
    description = Column(Text, nullable=False)
    aggregate_type = Column(String(100), nullable=False, index=True)
    producer = Column(String(100), nullable=False)
    consumers = Column(JSON, nullable=False, default=list)
    sensitivity = Column(SQLEnum(EventSensitivity), nullable=False, default=EventSensitivity.INTERNAL)
    retention_policy = Column(String(100), nullable=False, default="90_DAYS")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    versions = relationship("EventVersion", back_populates="registry_item", cascade="all, delete-orphan")


class EventVersion(Base):
    """Immutable contract version defining JSON payload schema for a domain event."""
    __tablename__ = "event_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(36), ForeignKey("event_registry_items.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    payload_schema = Column(JSON, nullable=False, default=dict)
    status = Column(String(50), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    registry_item = relationship("EventRegistryItem", back_populates="versions")


# ==============================================================================
# 2. Transactional Outbox, Inbox & Event Delivery
# ==============================================================================

class EventOutbox(Base):
    """Reliable outbox buffer ensuring transactional event dispatch."""
    __tablename__ = "event_outbox"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(100), nullable=False, unique=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_version = Column(String(20), nullable=False, default="v1")
    aggregate_type = Column(String(100), nullable=False, index=True)
    aggregate_id = Column(String(100), nullable=False, index=True)
    tenant_id = Column(String(36), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    correlation_id = Column(String(100), nullable=False, index=True)
    causation_id = Column(String(100), nullable=True)
    status = Column(SQLEnum(EventDeliveryStatus), nullable=False, default=EventDeliveryStatus.PENDING, index=True)
    attempt_count = Column(Integer, nullable=False, default=0)
    next_attempt_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    attempts = relationship("EventDeliveryAttempt", back_populates="outbox_event", cascade="all, delete-orphan")


class EventInbox(Base):
    """Consumer inbox ensuring idempotent, deduplicated event consumption."""
    __tablename__ = "event_inbox"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(100), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    consumer_name = Column(String(100), nullable=False, index=True)
    tenant_id = Column(String(36), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="PROCESSED")
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_event_inbox_dedup", "event_id", "consumer_name", unique=True),
    )


class EventDeliveryAttempt(Base):
    """Audited dispatch attempts with latency and error summaries."""
    __tablename__ = "event_delivery_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    outbox_id = Column(String(36), ForeignKey("event_outbox.id", ondelete="CASCADE"), nullable=False, index=True)
    attempt_number = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="SUCCESS")
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Float, nullable=False, default=0.0)
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    outbox_event = relationship("EventOutbox", back_populates="attempts")


class EventSubscription(Base):
    """Topic-to-handler subscription definitions."""
    __tablename__ = "event_subscriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    handler_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DeadLetterMessage(Base):
    """Triage container for poisoned or permanently failing event messages."""
    __tablename__ = "dead_letter_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(100), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    workflow_id = Column(String(100), nullable=True, index=True)
    consumer = Column(String(100), nullable=False)
    attempt_count = Column(Integer, nullable=False, default=1)
    failure_type = Column(String(100), nullable=False)
    error_summary = Column(Text, nullable=False)
    payload = Column(JSON, nullable=False, default=dict)
    status = Column(SQLEnum(DLQStatus), nullable=False, default=DLQStatus.PENDING, index=True)
    last_error_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class EventReplay(Base):
    """Controlled replay execution records with side-effect safeguards."""
    __tablename__ = "event_replays"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    filter_criteria = Column(JSON, nullable=False, default=dict)
    replay_mode = Column(SQLEnum(ReplayMode), nullable=False, default=ReplayMode.DRY_RUN)
    events_replayed_count = Column(Integer, nullable=False, default=0)
    triggered_by = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)


# ==============================================================================
# 3. Declarative Workflow Definitions & Graph Versioning
# ==============================================================================

class WorkflowDefinition(Base):
    """Catalog of declarative workflow types across business lifecycles."""
    __tablename__ = "workflow_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    current_version = Column(String(20), nullable=False, default="v1.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    versions = relationship("WorkflowVersion", back_populates="definition", cascade="all, delete-orphan")


class WorkflowVersion(Base):
    """Immutable graph definition for a workflow version."""
    __tablename__ = "workflow_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(36), ForeignKey("workflow_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    steps_config = Column(JSON, nullable=False, default=list)
    transitions_config = Column(JSON, nullable=False, default=list)
    status = Column(String(50), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    definition = relationship("WorkflowDefinition", back_populates="versions")
    steps = relationship("WorkflowStep", back_populates="workflow_version", cascade="all, delete-orphan")
    transitions = relationship("WorkflowTransition", back_populates="workflow_version", cascade="all, delete-orphan")


class WorkflowStep(Base):
    """Step node definition within a workflow graph."""
    __tablename__ = "workflow_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_version_id = Column(String(36), ForeignKey("workflow_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    step_key = Column(String(100), nullable=False)
    step_type = Column(SQLEnum(TaskType), nullable=False, default=TaskType.AGENT_TASK)
    name = Column(String(255), nullable=False)
    config = Column(JSON, nullable=False, default=dict)
    timeout_seconds = Column(Integer, nullable=False, default=3600)
    order_index = Column(Integer, nullable=False, default=0)

    workflow_version = relationship("WorkflowVersion", back_populates="steps")


class WorkflowTransition(Base):
    """Directed edge / transition rule between workflow steps."""
    __tablename__ = "workflow_transitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_version_id = Column(String(36), ForeignKey("workflow_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    from_step_key = Column(String(100), nullable=False)
    to_step_key = Column(String(100), nullable=False)
    condition = Column(String(255), nullable=True)
    is_default = Column(Boolean, nullable=False, default=True)

    workflow_version = relationship("WorkflowVersion", back_populates="transitions")


# ==============================================================================
# 4. Durable Workflow Runs, Steps & Wait States
# ==============================================================================

class WorkflowRun(Base):
    """Instantiated workflow execution tracking live state and durable progress."""
    __tablename__ = "workflow_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_key = Column(String(100), nullable=False, index=True)
    workflow_version = Column(String(20), nullable=False, default="v1.0")
    trigger_type = Column(String(50), nullable=False, default="EVENT")  # EVENT, SCHEDULE, MANUAL, WEBHOOK
    trigger_reference = Column(String(100), nullable=True)
    status = Column(SQLEnum(WorkflowStatus), nullable=False, default=WorkflowStatus.CREATED, index=True)
    current_step = Column(String(100), nullable=True)
    correlation_id = Column(String(100), nullable=False, index=True)
    input_data = Column(JSON, nullable=False, default=dict)
    output_data = Column(JSON, nullable=False, default=dict)
    error_code = Column(String(100), nullable=True)
    error_summary = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    paused_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    run_steps = relationship("WorkflowRunStep", back_populates="run", cascade="all, delete-orphan")
    run_events = relationship("WorkflowRunEvent", back_populates="run", cascade="all, delete-orphan")


class WorkflowRunStep(Base):
    """Individual step execution record within a workflow run."""
    __tablename__ = "workflow_run_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(String(36), ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    step_key = Column(String(100), nullable=False, index=True)
    step_type = Column(SQLEnum(TaskType), nullable=False, default=TaskType.AGENT_TASK)
    status = Column(SQLEnum(WorkflowStepStatus), nullable=False, default=WorkflowStepStatus.PENDING, index=True)
    attempt_count = Column(Integer, nullable=False, default=0)
    duration_ms = Column(Float, nullable=False, default=0.0)
    input_data = Column(JSON, nullable=False, default=dict)
    output_data = Column(JSON, nullable=False, default=dict)
    error_code = Column(String(100), nullable=True)
    error_summary = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    run = relationship("WorkflowRun", back_populates="run_steps")


class WorkflowRunEvent(Base):
    """Traceability link binding domain events directly to workflow runs."""
    __tablename__ = "workflow_run_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(String(36), ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(String(100), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    step_key = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    run = relationship("WorkflowRun", back_populates="run_events")


class WorkflowWaitState(Base):
    """Suspended workflow wait state (e.g. awaiting human decision, delay, or event)."""
    __tablename__ = "workflow_wait_states"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_run_id = Column(String(36), nullable=False, index=True)
    step_key = Column(String(100), nullable=False)
    wait_type = Column(String(50), nullable=False, default="HUMAN_APPROVAL")  # HUMAN_APPROVAL, TIMER, EVENT_CONDITION
    condition_data = Column(JSON, nullable=False, default=dict)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="WAITING")  # WAITING, RESUMED, TIMED_OUT, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 5. Tasks, Locks, Human Queue & Approvals
# ==============================================================================

class WorkflowTask(Base):
    """Dispatched executable task assigned to priority queues."""
    __tablename__ = "workflow_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_run_id = Column(String(36), nullable=False, index=True)
    step_key = Column(String(100), nullable=False)
    task_type = Column(SQLEnum(TaskType), nullable=False, default=TaskType.AGENT_TASK)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.NORMAL, index=True)
    queue_name = Column(String(100), nullable=False, default="default")
    payload = Column(JSON, nullable=False, default=dict)
    status = Column(String(50), nullable=False, default="QUEUED", index=True)  # QUEUED, RUNNING, COMPLETED, FAILED
    max_attempts = Column(Integer, nullable=False, default=3)
    current_attempt = Column(Integer, nullable=False, default=0)
    scheduled_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowTaskAttempt(Base):
    """Execution attempt log for a dispatched task."""
    __tablename__ = "workflow_task_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("workflow_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    attempt_number = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="SUCCESS")
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Float, nullable=False, default=0.0)
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowTaskLock(Base):
    """Distributed lock ensuring atomic single-worker execution on shared resources."""
    __tablename__ = "workflow_task_locks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lock_key = Column(String(255), nullable=False, unique=True, index=True)
    owner_id = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class HumanTask(Base):
    """Unified human-in-the-loop task review queue."""
    __tablename__ = "human_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_run_id = Column(String(36), nullable=False, index=True)
    step_key = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String(100), nullable=False, index=True)  # APPROVE_OUTREACH, APPROVE_CONTRACT, etc.
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.HIGH, index=True)
    assigned_to = Column(String(100), nullable=True)
    status = Column(SQLEnum(HumanTaskStatus), nullable=False, default=HumanTaskStatus.PENDING, index=True)
    deadline = Column(DateTime, nullable=True)
    input_data = Column(JSON, nullable=False, default=dict)
    decision = Column(String(50), nullable=True)  # APPROVED, REJECTED, REVISION_REQUIRED
    decision_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)


class WorkflowApproval(Base):
    """Audited human approval record bound to content hash."""
    __tablename__ = "workflow_approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_run_id = Column(String(36), nullable=False, index=True)
    step_key = Column(String(100), nullable=False)
    approved_by = Column(String(100), nullable=False)
    content_hash = Column(String(64), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowCancellation(Base):
    """Audited cancellation event log."""
    __tablename__ = "workflow_cancellations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_run_id = Column(String(36), nullable=False, index=True)
    cancelled_by = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 6. Automation Rules, Versions & Execution Schedules
# ==============================================================================

class AutomationRule(Base):
    """Controlled event-driven and condition-based automation rules."""
    __tablename__ = "automation_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    version = Column(String(20), nullable=False, default="v1.0")
    trigger_type = Column(String(50), nullable=False, default="EVENT")  # EVENT, SCHEDULE, CONDITION
    trigger_config = Column(JSON, nullable=False, default=dict)
    condition_config = Column(JSON, nullable=False, default=dict)
    action_config = Column(JSON, nullable=False, default=dict)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.NORMAL)
    enabled = Column(Boolean, nullable=False, default=True, index=True)
    requires_human_approval = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    versions = relationship("AutomationRuleVersion", back_populates="rule", cascade="all, delete-orphan")


class AutomationRuleVersion(Base):
    """Versioned logic snapshot for an automation rule."""
    __tablename__ = "automation_rule_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = Column(String(36), ForeignKey("automation_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    trigger_config = Column(JSON, nullable=False, default=dict)
    condition_config = Column(JSON, nullable=False, default=dict)
    action_config = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    rule = relationship("AutomationRule", back_populates="versions")


class AutomationRuleRun(Base):
    """Execution history log for triggered automation rules."""
    __tablename__ = "automation_rule_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    rule_id = Column(String(36), ForeignKey("automation_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    trigger_event_id = Column(String(100), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="SUCCESS")
    result_summary = Column(Text, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class WorkflowSchedule(Base):
    """Time-based and cron-driven trigger schedules."""
    __tablename__ = "workflow_schedules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_key = Column(String(100), nullable=False, index=True)
    cron_expression = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    next_run_at = Column(DateTime, nullable=True, index=True)
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
