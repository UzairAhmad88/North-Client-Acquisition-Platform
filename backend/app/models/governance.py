"""SQLAlchemy Models for Phase 33: AI Agent Evaluation, Observability, Governance & Continuous Improvement."""

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


class TraceStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"
    PARTIAL = "PARTIAL"


class AgentRolloutStatus(str, Enum):
    DESIGN = "DESIGN"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    EVALUATION = "EVALUATION"
    APPROVED = "APPROVED"
    SHADOW = "SHADOW"
    CANARY_10 = "CANARY_10"
    CANARY_50 = "CANARY_50"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class PromptStatus(str, Enum):
    DRAFT = "DRAFT"
    TESTING = "TESTING"
    APPROVED = "APPROVED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class EvaluationType(str, Enum):
    OFFLINE_EVALUATION = "OFFLINE_EVALUATION"
    REGRESSION_EVALUATION = "REGRESSION_EVALUATION"
    PRODUCTION_EVALUATION = "PRODUCTION_EVALUATION"
    HUMAN_EVALUATION = "HUMAN_EVALUATION"
    AUTOMATED_EVALUATION = "AUTOMATED_EVALUATION"
    PAIRWISE_COMPARISON = "PAIRWISE_COMPARISON"
    OUTCOME_EVALUATION = "OUTCOME_EVALUATION"


class AIFailureCategory(str, Enum):
    MODEL_ERROR = "MODEL_ERROR"
    TOOL_ERROR = "TOOL_ERROR"
    TIMEOUT = "TIMEOUT"
    SCHEMA_ERROR = "SCHEMA_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RISK_BLOCK = "RISK_BLOCK"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    PROMPT_FAILURE = "PROMPT_FAILURE"
    CONTEXT_FAILURE = "CONTEXT_FAILURE"
    DATA_FAILURE = "DATA_FAILURE"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class AIIncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    TRIAGED = "TRIAGED"
    CONTAINED = "CONTAINED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    POST_INCIDENT_REVIEW = "POST_INCIDENT_REVIEW"


class KillSwitchLevel(str, Enum):
    GLOBAL_AI_OFF = "GLOBAL_AI_OFF"
    AGENT_OFF = "AGENT_OFF"
    MODEL_OFF = "MODEL_OFF"
    WORKFLOW_OFF = "WORKFLOW_OFF"
    TOOL_OFF = "TOOL_OFF"


class AgentHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"


# ==============================================================================
# 1. Unified AI Tracing & Structured Spans
# ==============================================================================

class AITrace(Base):
    """Unified distributed trace container for an end-to-end AI execution workflow."""
    __tablename__ = "ai_traces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workflow_id = Column(String(100), nullable=False, index=True)
    project_id = Column(String(36), nullable=True, index=True)
    lead_id = Column(String(36), nullable=True, index=True)
    agent_id = Column(String(100), nullable=False, index=True)
    agent_version = Column(String(20), nullable=False)
    model_id = Column(String(100), nullable=False)
    model_version = Column(String(20), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    total_tokens = Column(Integer, nullable=False, default=0)
    estimated_cost = Column(Float, nullable=False, default=0.0)
    total_duration_ms = Column(Float, nullable=False, default=0.0)
    status = Column(SQLEnum(TraceStatus), nullable=False, default=TraceStatus.RUNNING, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)

    events = relationship("AITraceEvent", back_populates="trace", cascade="all, delete-orphan")


class AITraceEvent(Base):
    """Structured span/event within an AI trace (no private chain-of-thought stored)."""
    __tablename__ = "ai_trace_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), ForeignKey("ai_traces.id", ondelete="CASCADE"), nullable=False, index=True)
    span_type = Column(String(50), nullable=False)  # "AGENT_START", "MODEL_CALL", "TOOL_CALL", "VALIDATION", "RISK_CHECK"
    name = Column(String(255), nullable=False)
    input_summary = Column(JSON, nullable=False, default=dict)
    output_summary = Column(JSON, nullable=False, default=dict)
    tokens_consumed = Column(Integer, nullable=False, default=0)
    duration_ms = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="SUCCESS")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    trace = relationship("AITrace", back_populates="events")


# ==============================================================================
# 2. Agent Versioning & Rollout Deployments
# ==============================================================================

class AgentVersion(Base):
    """Immutable version configuration snapshot of an AI agent."""
    __tablename__ = "agent_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    model_key = Column(String(100), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    allowed_tools = Column(JSON, nullable=False, default=list)
    permissions = Column(JSON, nullable=False, default=list)
    configuration = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AgentDeployment(Base):
    """Lifecycle deployment tracking rollout channels and shadow/canary states."""
    __tablename__ = "agent_deployments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    status = Column(SQLEnum(AgentRolloutStatus), nullable=False, default=AgentRolloutStatus.DESIGN, index=True)
    rollout_percentage = Column(Integer, nullable=False, default=0)
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    deployed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    retired_at = Column(DateTime, nullable=True)


# ==============================================================================
# 3. Prompt Registry & Versioning
# ==============================================================================

class PromptRegistryItem(Base):
    """Catalog of registered AI prompts with purpose and governance metadata."""
    __tablename__ = "prompt_registry_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    prompt_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    agent_target = Column(String(100), nullable=False)
    purpose = Column(Text, nullable=False)
    current_version = Column(String(20), nullable=False, default="v1.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    versions = relationship("PromptVersion", back_populates="prompt_item", cascade="all, delete-orphan")


class PromptVersion(Base):
    """Versioned prompt content with SHA-256 integrity hash and approval state."""
    __tablename__ = "prompt_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    prompt_id = Column(String(36), ForeignKey("prompt_registry_items.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)
    status = Column(SQLEnum(PromptStatus), nullable=False, default=PromptStatus.DRAFT, index=True)
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prompt_item = relationship("PromptRegistryItem", back_populates="versions")


# ==============================================================================
# 4. Model & Tool Usage Observability
# ==============================================================================

class ModelUsageRecord(Base):
    """Aggregated tracking of model token usage, provider charges, and latency."""
    __tablename__ = "model_usage_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), nullable=False, index=True)
    provider = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=False)
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    estimated_cost = Column(Float, nullable=False, default=0.0)
    latency_ms = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class ToolUsageRecord(Base):
    """Audited log of tool invocations and authorization results."""
    __tablename__ = "tool_usage_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), nullable=False, index=True)
    agent_id = Column(String(100), nullable=False, index=True)
    tool_name = Column(String(100), nullable=False, index=True)
    is_authorized = Column(Boolean, nullable=False, default=True)
    denial_reason = Column(String(255), nullable=True)
    latency_ms = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="SUCCESS")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


# ==============================================================================
# 5. Evaluation Datasets, Cases & Runs
# ==============================================================================

class EvaluationDataset(Base):
    """Versioned benchmark datasets containing golden curated examples."""
    __tablename__ = "evaluation_datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dataset_key = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String(100), nullable=False, index=True)
    is_golden = Column(Boolean, nullable=False, default=False)
    version = Column(String(20), nullable=False, default="v1.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    cases = relationship("EvaluationCase", back_populates="dataset", cascade="all, delete-orphan")


class EvaluationCase(Base):
    """Single test case within an evaluation dataset."""
    __tablename__ = "evaluation_cases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dataset_id = Column(String(36), ForeignKey("evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    input_context = Column(JSON, nullable=False, default=dict)
    expected_output = Column(JSON, nullable=False, default=dict)
    evaluation_criteria = Column(JSON, nullable=False, default=list)
    difficulty = Column(String(50), nullable=False, default="MEDIUM")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("EvaluationDataset", back_populates="cases")


class EvaluationRun(Base):
    """Execution run of an evaluation or regression benchmark test."""
    __tablename__ = "evaluation_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    dataset_id = Column(String(36), ForeignKey("evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    agent_version = Column(String(20), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    model_version = Column(String(20), nullable=False)
    evaluation_type = Column(SQLEnum(EvaluationType), nullable=False, default=EvaluationType.AUTOMATED_EVALUATION)
    overall_score = Column(Float, nullable=False, default=0.0)  # 0.0 to 100.0
    passed_cases_count = Column(Integer, nullable=False, default=0)
    failed_cases_count = Column(Integer, nullable=False, default=0)
    regression_detected = Column(Boolean, nullable=False, default=False)
    regression_details = Column(JSON, nullable=False, default=dict)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 6. Human Evaluation, Pairwise Review & Human Revision Tracking
# ==============================================================================

class HumanEvaluation(Base):
    """Human scoring of AI outputs across quality, evidence, and safety."""
    __tablename__ = "human_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), nullable=False, index=True)
    reviewer = Column(String(100), nullable=False)
    correctness_score = Column(Integer, nullable=False, default=5)  # 1-5 scale
    completeness_score = Column(Integer, nullable=False, default=5)
    evidence_score = Column(Integer, nullable=False, default=5)
    safety_score = Column(Integer, nullable=False, default=5)
    usefulness_score = Column(Integer, nullable=False, default=5)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class HumanRevisionRecord(Base):
    """Measurement of practical AI quality through human edit magnitude."""
    __tablename__ = "human_revision_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    edit_magnitude = Column(String(50), nullable=False)  # "NO_EDIT", "MINOR_EDIT", "MAJOR_EDIT", "REJECTED", "REWRITTEN"
    levenshtein_distance = Column(Integer, nullable=False, default=0)
    similarity_score = Column(Float, nullable=False, default=1.0)
    operator = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ==============================================================================
# 7. AI Incidents, Failures & Security Events
# ==============================================================================

class AIFailureRecord(Base):
    """Standardized operational failure taxonomy records."""
    __tablename__ = "ai_failure_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    trace_id = Column(String(36), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    category = Column(SQLEnum(AIFailureCategory), nullable=False, default=AIFailureCategory.UNKNOWN_ERROR)
    error_message = Column(Text, nullable=False)
    context_data = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AIIncident(Base):
    """High-severity AI incident lifecycle tracking and triage."""
    __tablename__ = "ai_incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    incident_number = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False, default="HIGH")  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    status = Column(SQLEnum(AIIncidentStatus), nullable=False, default=AIIncidentStatus.DETECTED, index=True)
    affected_agent = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    containment_action = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    resolved_by = Column(String(100), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AISecurityEvent(Base):
    """Security logs for prompt injection attempts, unauthorized tool calls, or data leakage."""
    __tablename__ = "ai_security_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)  # "UNAUTHORIZED_TOOL", "PROMPT_INJECTION", "DATA_LEAKAGE"
    agent_key = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False, default="HIGH")
    action_taken = Column(String(50), nullable=False, default="BLOCKED")
    details = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


# ==============================================================================
# 8. Budget Policies, Health Snapshots & Emergency Kill Switch
# ==============================================================================

class AIBudgetPolicy(Base):
    """Financial ceiling and token quota configuration."""
    __tablename__ = "ai_budget_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    scope = Column(String(50), nullable=False, default="GLOBAL")  # "GLOBAL", "AGENT", "WORKFLOW"
    scope_key = Column(String(100), nullable=False, default="all")
    daily_cost_limit = Column(Float, nullable=False, default=50.0)
    monthly_cost_limit = Column(Float, nullable=False, default=500.0)
    enforcement_action = Column(String(50), nullable=False, default="BLOCK")  # "BLOCK", "FALLBACK", "REQUIRE_REVIEW"
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AIHealthSnapshot(Base):
    """System health snapshot evaluating reliability, latency, cost, and revision rate."""
    __tablename__ = "ai_health_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    agent_key = Column(String(100), nullable=False, index=True)
    status = Column(SQLEnum(AgentHealthStatus), nullable=False, default=AgentHealthStatus.HEALTHY)
    success_rate_pct = Column(Float, nullable=False, default=100.0)
    avg_latency_ms = Column(Float, nullable=False, default=0.0)
    human_acceptance_pct = Column(Float, nullable=False, default=100.0)
    daily_cost_consumed = Column(Float, nullable=False, default=0.0)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AIKillSwitchEvent(Base):
    """Independent emergency shutdown activation log with mandatory human audit trail."""
    __tablename__ = "ai_kill_switch_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    level = Column(SQLEnum(KillSwitchLevel), nullable=False, default=KillSwitchLevel.GLOBAL_AI_OFF)
    target_key = Column(String(100), nullable=False, default="GLOBAL")  # "GLOBAL", agent_key, model_key, tool_name
    is_active = Column(Boolean, nullable=False, default=True)
    activated_by = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


# ==============================================================================
# 9. Continuous Improvement Backlog & Technical Debt
# ==============================================================================

class AIImprovementItem(Base):
    """Closed-loop improvement backlog linked to evaluation evidence and human feedback."""
    __tablename__ = "ai_improvement_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    item_type = Column(String(50), nullable=False)  # "PROMPT", "MODEL", "TOOL", "DATA", "EVALUATION"
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    evidence_reference = Column(JSON, nullable=False, default=dict)
    status = Column(String(50), nullable=False, default="BACKLOG")  # "BACKLOG", "EXPERIMENTING", "VALIDATED", "DEPLOYED"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AITechnicalDebtItem(Base):
    """Tracking known agent weaknesses, missing test coverage, and model limitations."""
    __tablename__ = "ai_technical_debt_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    component = Column(String(100), nullable=False)
    debt_type = Column(String(50), nullable=False)  # "EVALUATION_GAP", "PROMPT_WEAKNESS", "TOOL_RELIABILITY"
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="MEDIUM")
    is_resolved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
