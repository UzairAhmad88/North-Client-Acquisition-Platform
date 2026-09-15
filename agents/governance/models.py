"""Pydantic data structures for AI Evaluation, Observability & Governance Subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SpanRecord(BaseModel):
    span_type: str = Field(..., description="AGENT_START, MODEL_CALL, TOOL_CALL, VALIDATION, RISK_CHECK")
    name: str
    input_summary: Dict[str, Any] = Field(default_factory=dict)
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    tokens_consumed: int = Field(default=0)
    duration_ms: float = Field(default=0.0)
    status: str = Field(default="SUCCESS")
    error_message: Optional[str] = None


class TracePayload(BaseModel):
    workflow_id: str
    tenant_id: str = Field(default="default_tenant")
    project_id: Optional[str] = None
    lead_id: Optional[str] = None
    agent_id: str
    agent_version: str = Field(default="v1.0")
    model_id: str = Field(default="default_model")
    model_version: str = Field(default="v1.0")
    prompt_version: str = Field(default="v1.0")
    spans: List[SpanRecord] = Field(default_factory=list)


class PromptDraft(BaseModel):
    prompt_key: str
    name: str
    agent_target: str
    purpose: str
    content: str
    version: str = Field(default="v1.0")
    status: str = Field(default="DRAFT")


class EvaluationCaseSpec(BaseModel):
    title: str
    input_context: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Dict[str, Any] = Field(default_factory=dict)
    evaluation_criteria: List[str] = Field(default_factory=list)
    difficulty: str = Field(default="MEDIUM")


class EvaluationBenchmarkResult(BaseModel):
    agent_key: str
    agent_version: str
    prompt_version: str
    model_version: str
    overall_score: float = Field(..., ge=0.0, le=100.0)
    passed_cases_count: int = Field(default=0)
    failed_cases_count: int = Field(default=0)
    regression_detected: bool = Field(default=False)
    regression_details: Dict[str, Any] = Field(default_factory=dict)


class HumanReviewEvaluation(BaseModel):
    trace_id: str
    reviewer: str = Field(default="user")
    correctness_score: int = Field(default=5, ge=1, le=5)
    completeness_score: int = Field(default=5, ge=1, le=5)
    evidence_score: int = Field(default=5, ge=1, le=5)
    safety_score: int = Field(default=5, ge=1, le=5)
    usefulness_score: int = Field(default=5, ge=1, le=5)
    notes: Optional[str] = None


class KillSwitchCommand(BaseModel):
    level: str = Field(default="GLOBAL_AI_OFF", description="GLOBAL_AI_OFF, AGENT_OFF, MODEL_OFF, TOOL_OFF")
    target_key: str = Field(default="GLOBAL")
    is_active: bool = Field(default=True)
    activated_by: str = Field(default="admin")
    reason: str


class BudgetCheckResult(BaseModel):
    allowed: bool = Field(default=True)
    enforcement_action: str = Field(default="ALLOW")  # "ALLOW", "BLOCK", "FALLBACK", "REQUIRE_REVIEW"
    current_daily_cost: float = Field(default=0.0)
    daily_limit: float = Field(default=50.0)
    reason: Optional[str] = None
