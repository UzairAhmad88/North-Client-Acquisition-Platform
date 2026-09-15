"""Pydantic request and response schemas for Phase 33: AI Governance & Observability."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# =============================================================================
# 1. Traces & Spans
# =============================================================================

class TraceEventResponse(BaseModel):
    id: str
    span_type: str
    name: str
    input_summary: Dict[str, Any] = Field(default_factory=dict)
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    tokens_consumed: int
    duration_ms: float
    status: str
    error_message: Optional[str] = None
    created_at: datetime


class TraceDetailResponse(BaseModel):
    id: str
    tenant_id: str
    workflow_id: str
    project_id: Optional[str] = None
    lead_id: Optional[str] = None
    agent_id: str
    agent_version: str
    model_id: str
    model_version: str
    prompt_version: str
    total_tokens: int
    estimated_cost: float
    total_duration_ms: float
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    events: List[TraceEventResponse] = Field(default_factory=list)


class TraceCreateRequest(BaseModel):
    workflow_id: str
    project_id: Optional[str] = None
    lead_id: Optional[str] = None
    agent_id: str
    agent_version: str = "v1.0"
    model_id: str = "gpt-4o-mini"
    model_version: str = "v1.0"
    prompt_version: str = "v1.0"


# =============================================================================
# 2. Prompts & Versions
# =============================================================================

class PromptVersionResponse(BaseModel):
    id: str
    version: str
    content: str
    content_hash: str
    status: str
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime


class PromptItemResponse(BaseModel):
    id: str
    tenant_id: str
    prompt_key: str
    name: str
    agent_target: str
    purpose: str
    current_version: str
    created_at: datetime
    versions: List[PromptVersionResponse] = Field(default_factory=list)


class PromptCreateRequest(BaseModel):
    prompt_key: str
    name: str
    agent_target: str
    purpose: str
    content: str
    version: str = "v1.0"


# =============================================================================
# 3. Evaluations
# =============================================================================

class EvaluationCaseResponse(BaseModel):
    id: str
    title: str
    difficulty: str
    created_at: datetime


class EvaluationDatasetResponse(BaseModel):
    id: str
    tenant_id: str
    dataset_key: str
    name: str
    description: str
    task_type: str
    is_golden: bool
    version: str
    created_at: datetime
    cases: List[EvaluationCaseResponse] = Field(default_factory=list)


class EvaluationRunRequest(BaseModel):
    dataset_id: str
    agent_key: str
    agent_version: str = "v1.0"
    prompt_version: str = "v1.0"
    model_version: str = "v1.0"
    baseline_score: float = 90.0


class EvaluationRunResponse(BaseModel):
    id: str
    tenant_id: str
    dataset_id: str
    agent_key: str
    agent_version: str
    prompt_version: str
    model_version: str
    evaluation_type: str
    overall_score: float
    passed_cases_count: int
    failed_cases_count: int
    regression_detected: bool
    regression_details: Dict[str, Any]
    completed_at: datetime


# =============================================================================
# 4. Human Reviews, Incidents & Kill Switch
# =============================================================================

class HumanEvaluationRequest(BaseModel):
    trace_id: str
    reviewer: str = "user"
    correctness_score: int = Field(default=5, ge=1, le=5)
    completeness_score: int = Field(default=5, ge=1, le=5)
    evidence_score: int = Field(default=5, ge=1, le=5)
    safety_score: int = Field(default=5, ge=1, le=5)
    usefulness_score: int = Field(default=5, ge=1, le=5)
    notes: Optional[str] = None


class AIIncidentResponse(BaseModel):
    id: str
    tenant_id: str
    incident_number: str
    title: str
    severity: str
    status: str
    affected_agent: str
    description: str
    containment_action: Optional[str] = None
    root_cause: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime


class AIIncidentCreateRequest(BaseModel):
    title: str
    severity: str = "HIGH"
    affected_agent: str
    description: str
    containment_action: Optional[str] = None


class KillSwitchRequest(BaseModel):
    level: str = Field(default="GLOBAL_AI_OFF", description="GLOBAL_AI_OFF, AGENT_OFF, MODEL_OFF, TOOL_OFF")
    target_key: str = Field(default="GLOBAL")
    is_active: bool = True
    activated_by: str = "admin"
    reason: str


class AIHealthSnapshotResponse(BaseModel):
    id: str
    tenant_id: str
    agent_key: str
    status: str
    success_rate_pct: float
    avg_latency_ms: float
    human_acceptance_pct: float
    daily_cost_consumed: float
    captured_at: datetime
