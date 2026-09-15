"""
Base Enums, Types, and Domain Schemas for Phase 52:
Unified Autonomous Knowledge Worker & Multi-Agent Workforce Platform.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class WorkerStatus(str, Enum):
    DRAFT = "DRAFT"
    TRAINING = "TRAINING"
    TESTING = "TESTING"
    APPROVED = "APPROVED"
    SHADOW = "SHADOW"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    SUSPENDED = "SUSPENDED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class SupervisionLevel(int, Enum):
    DETERMINISTIC_0 = 0     # Fully deterministic rules
    READ_ONLY_1 = 1          # Read-only exploration
    DRAFT_GEN_2 = 2          # Generates proposals/drafts
    BOUNDED_ACTION_3 = 3     # Executes bounded internal task
    REVIEW_REQUIRED_4 = 4    # Requires human review queue
    EXPLICIT_APPROVAL_5 = 5  # Human must explicitly authorize execution


class WorkerCapability(str, Enum):
    READ = "READ"
    ANALYZE = "ANALYZE"
    CLASSIFY = "CLASSIFY"
    EXTRACT = "EXTRACT"
    SUMMARIZE = "SUMMARIZE"
    GENERATE_DRAFT = "GENERATE_DRAFT"
    PLAN = "PLAN"
    PREDICT = "PREDICT"
    SIMULATE = "SIMULATE"
    COMPARE = "COMPARE"
    VALIDATE = "VALIDATE"
    SEARCH = "SEARCH"
    RETRIEVE_KNOWLEDGE = "RETRIEVE_KNOWLEDGE"
    CREATE_INTERNAL_TASK = "CREATE_INTERNAL_TASK"
    UPDATE_DRAFT = "UPDATE_DRAFT"
    RECOMMEND = "RECOMMEND"


class SensitiveCapability(str, Enum):
    APPROVE = "APPROVE"
    SEND = "SEND"
    EXECUTE_PAYMENT = "EXECUTE_PAYMENT"
    CHANGE_CONTRACT = "CHANGE_CONTRACT"
    DEPLOY = "DEPLOY"
    MODIFY_SECURITY_POLICY = "MODIFY_SECURITY_POLICY"
    CHANGE_PERMISSION = "CHANGE_PERMISSION"
    DELETE = "DELETE"
    PRODUCTION_MUTATION = "PRODUCTION_MUTATION"


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ESCALATED = "ESCALATED"


class TaskPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CollaborationPattern(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    HIERARCHICAL = "HIERARCHICAL"
    DEBATE = "DEBATE"
    REVIEW = "REVIEW"
    CONSENSUS = "CONSENSUS"
    PIPELINE = "PIPELINE"
    SUPERVISOR_WORKER = "SUPERVISOR_WORKER"


class KillSwitchTarget(str, Enum):
    GLOBAL_WORKFORCE = "GLOBAL_WORKFORCE"
    DEPARTMENT = "DEPARTMENT"
    TEAM = "TEAM"
    WORKER = "WORKER"
    TOOL = "TOOL"
    MODEL = "MODEL"


# --- Domain Pydantic Models ---

class AIWorker(BaseModel):
    id: Optional[str] = None
    worker_code: str = Field(default_factory=lambda: f"WRK-{uuid.uuid4().hex[:6].upper()}")
    organization_id: str = "default_org"
    name: str
    description: Optional[str] = None
    role: str
    specialization: str
    status: WorkerStatus = WorkerStatus.ACTIVE
    supervision_level: SupervisionLevel = SupervisionLevel.DRAFT_GEN_2
    agent_version: str = "1.0"
    model_name: str = "gemini-1.5-pro"
    owner: str = "system_admin"
    capabilities: List[str] = Field(default_factory=list)
    tool_policy: Dict[str, Any] = Field(default_factory=dict)
    knowledge_policy: Dict[str, Any] = Field(default_factory=dict)
    permission_policy: Dict[str, Any] = Field(default_factory=dict)
    budget_policy: Dict[str, Any] = Field(default_factory=dict)
    communication_policy: Dict[str, Any] = Field(default_factory=dict)
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    total_cost_usd: float = 0.0
    average_latency_seconds: float = 0.0
    grounding_score: float = 1.0
    version: int = 1


class AIDepartment(BaseModel):
    id: Optional[str] = None
    department_code: str = Field(default_factory=lambda: f"DEPT-{uuid.uuid4().hex[:6].upper()}")
    organization_id: str = "default_org"
    name: str
    description: Optional[str] = None
    head_worker_code: Optional[str] = None
    monthly_budget_usd: float = 500.0
    current_spend_usd: float = 0.0
    status: str = "ACTIVE"


class AITeam(BaseModel):
    id: Optional[str] = None
    team_code: str = Field(default_factory=lambda: f"TEAM-{uuid.uuid4().hex[:6].upper()}")
    department_code: str
    organization_id: str = "default_org"
    name: str
    purpose: Optional[str] = None
    manager_worker_code: Optional[str] = None
    workflow_template: str = "PARALLEL_REVIEW"
    status: str = "ACTIVE"
    budget_limit_usd: float = 150.0
    current_spend_usd: float = 0.0
    members: List[str] = Field(default_factory=list)


class AIWorkTask(BaseModel):
    id: Optional[str] = None
    task_code: str = Field(default_factory=lambda: f"TSK-{uuid.uuid4().hex[:6].upper()}")
    organization_id: str = "default_org"
    parent_task_code: Optional[str] = None
    objective: str
    description: Optional[str] = None
    worker_code: Optional[str] = None
    team_code: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.CREATED
    supervision_level: SupervisionLevel = SupervisionLevel.DRAFT_GEN_2
    risk_level: str = "LOW"
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[str] = None
    result_summary: Optional[str] = None
    result_artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    cost_usd: float = 0.0
    token_count: int = 0
    runtime_seconds: float = 0.0
    confidence_score: float = 1.0
    error_message: Optional[str] = None


class AIHandoff(BaseModel):
    id: Optional[str] = None
    handoff_code: str = Field(default_factory=lambda: f"HND-{uuid.uuid4().hex[:6].upper()}")
    from_worker_code: str
    to_worker_code: str
    task_code: str
    context_summary: str
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0
    expected_next_action: str
    status: str = "DELIVERED"


class AIConsensusResult(BaseModel):
    consensus_code: str = Field(default_factory=lambda: f"CNS-{uuid.uuid4().hex[:6].upper()}")
    topic: str
    participating_workers: List[str]
    worker_opinions: List[Dict[str, Any]]
    consensus_score: float
    has_conflicts: bool
    synthesized_conclusion: str
    dissenting_views: List[Dict[str, Any]] = Field(default_factory=list)


class AIReviewResult(BaseModel):
    review_code: str = Field(default_factory=lambda: f"REV-{uuid.uuid4().hex[:6].upper()}")
    target_task_code: str
    author_worker_code: str
    critic_worker_code: str
    review_type: str = "FACT_AND_RISK"
    critique_summary: str
    findings: List[Dict[str, Any]] = Field(default_factory=list)
    quality_score: float = 1.0
    is_approved_by_critic: bool = True
