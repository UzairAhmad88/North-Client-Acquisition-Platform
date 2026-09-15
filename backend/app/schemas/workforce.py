"""
Pydantic API Schemas for Phase 52:
Unified Autonomous Knowledge Worker & Multi-Agent Workforce Platform.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkerRegisterRequest(BaseModel):
    name: str
    role: str
    specialization: str
    description: Optional[str] = None
    supervision_level: int = 2
    capabilities: Optional[List[str]] = None
    model_name: str = "gemini-1.5-pro"


class WorkerResponse(BaseModel):
    id: Optional[str] = None
    worker_code: str
    organization_id: str
    name: str
    description: Optional[str] = None
    role: str
    specialization: str
    status: str
    supervision_level: int
    agent_version: str
    model_name: str
    capabilities: List[str]
    total_tasks_completed: int
    grounding_score: float
    version: int


class DepartmentResponse(BaseModel):
    id: Optional[str] = None
    department_code: str
    name: str
    description: Optional[str] = None
    monthly_budget_usd: float
    current_spend_usd: float
    status: str


class TeamResponse(BaseModel):
    id: Optional[str] = None
    team_code: str
    department_code: str
    name: str
    purpose: Optional[str] = None
    workflow_template: str
    status: str
    budget_limit_usd: float
    members: List[str]


class TaskDecomposeRequest(BaseModel):
    objective: str
    domain: str = "GROWTH_EXPANSION"


class TaskResponse(BaseModel):
    id: Optional[str] = None
    task_code: str
    objective: str
    description: Optional[str] = None
    worker_code: Optional[str] = None
    priority: str
    status: str
    supervision_level: int
    risk_level: str
    inputs: Dict[str, Any]
    expected_output: Optional[str] = None
    result_summary: Optional[str] = None
    dependencies: List[str]
    cost_usd: float
    confidence_score: float


class HandoffCreateRequest(BaseModel):
    from_worker_code: str
    to_worker_code: str
    task_code: str
    context_summary: str
    artifacts: List[Dict[str, Any]]
    expected_next_action: str
    evidence: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None


class HandoffResponse(BaseModel):
    id: Optional[str] = None
    handoff_code: str
    from_worker_code: str
    to_worker_code: str
    task_code: str
    context_summary: str
    artifacts: List[Dict[str, Any]]
    expected_next_action: str
    confidence_score: float
    status: str


class ConsensusRequest(BaseModel):
    topic: str
    worker_evaluations: List[Dict[str, Any]]


class ConsensusResponse(BaseModel):
    consensus_code: str
    topic: str
    participating_workers: List[str]
    consensus_score: float
    has_conflicts: bool
    synthesized_conclusion: str
    dissenting_views: List[Dict[str, Any]]


class ReviewResolveRequest(BaseModel):
    approved: bool
    reviewer_id: str
    rationale: str


class KillSwitchTriggerRequest(BaseModel):
    target_type: str = "WORKER"  # GLOBAL_WORKFORCE, DEPARTMENT, TEAM, WORKER
    target_identifier: str
    reason: str
    operator_id: str = "security_admin"


class WorkforceCopilotQueryRequest(BaseModel):
    query: str


class WorkforceCopilotQueryResponse(BaseModel):
    query: str
    answer: str
    evidence: List[str]
    suggested_actions: List[str]
    governance_notice: str = "AI Workforce operates under strict supervision levels. Sensitive capabilities require explicit human authorization."
