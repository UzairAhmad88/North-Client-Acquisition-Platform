"""
Pydantic Schemas for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DecisionRoomCreateRequest(BaseModel):
    title: str = Field(..., description="Decision room title")
    question: str = Field(..., description="Core business question to resolve")
    owner_id: str = Field(default="executive_user", description="Room owner identifier")
    decision_type: str = Field(default="STRATEGIC", description="Category of decision")
    importance: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    objective: Optional[str] = Field(None, description="Clear statement of goal/objective")
    meta_info: Optional[Dict[str, Any]] = None


class DecisionStatusTransitionRequest(BaseModel):
    target_status: str = Field(..., description="Target status enum value")
    actor_id: str = Field(default="executive_user")
    notes: Optional[str] = None


class RecordDecisionRequest(BaseModel):
    selected_option_id: str = Field(...)
    decision_summary: str = Field(...)
    decided_by: str = Field(default="executive_user")


class SetContextRequest(BaseModel):
    background: str = Field(...)
    current_state: Optional[str] = None
    constraints: Optional[List[str]] = None
    entities_involved: Optional[List[str]] = None


class AddEvidenceRequest(BaseModel):
    evidence_type: str = Field(default="DATABASE")
    source: str = Field(...)
    claim: str = Field(...)
    statement_category: str = Field(default="FACT")
    authority: str = Field(default="OFFICIAL")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class AddAssumptionRequest(BaseModel):
    statement: str = Field(...)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    impact_if_false: str = Field(default="MEDIUM")


class AddUnknownRequest(BaseModel):
    question: str = Field(...)
    impact: str = Field(default="MEDIUM")
    resolution_path: Optional[str] = None


class CreateOptionRequest(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    benefits: Optional[List[str]] = None
    costs: float = Field(default=0.0)
    risks: Optional[List[str]] = None
    uncertainty_level: str = Field(default="MEDIUM")
    reversibility: str = Field(default="REVERSIBLE")


class AddCriterionRequest(BaseModel):
    name: str = Field(...)
    weight: float = Field(default=1.0, gt=0.0)
    criterion_type: str = Field(default="BENEFIT")
    description: Optional[str] = None


class ScoreOptionRequest(BaseModel):
    option_id: str = Field(...)
    criterion_id: str = Field(...)
    raw_score: float = Field(..., ge=0.0, le=100.0)
    justification: Optional[str] = None
    scored_by: str = Field(default="AI_ANALYST")


class SubmitAnalysisRequest(BaseModel):
    specialist_role: str = Field(...)
    summary: str = Field(...)
    recommendations: Optional[List[str]] = None
    key_findings: Optional[List[str]] = None
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    facts: Optional[List[str]] = None
    inferences: Optional[List[str]] = None


class SubmitAdversarialReviewRequest(BaseModel):
    critique_summary: str = Field(...)
    reviewer_role: str = Field(default="CRITICAL_ANALYST")
    weak_assumptions: Optional[List[str]] = None
    unintended_consequences: Optional[List[str]] = None
    hidden_costs: Optional[List[str]] = None


class AddCommentRequest(BaseModel):
    author_id: str = Field(...)
    content: str = Field(...)
    author_role: str = Field(default="HUMAN_DECISION_MAKER")
    is_human: bool = Field(default=True)
    parent_id: Optional[str] = None
    mentions: Optional[List[str]] = None
    annotations: Optional[List[str]] = None


class RecordApprovalRequest(BaseModel):
    step_id: str = Field(...)
    approver_id: str = Field(...)
    status: str = Field(default="APPROVED")  # APPROVED, REJECTED, WAIVED
    notes: Optional[str] = None


class CreateActionRequest(BaseModel):
    title: str = Field(...)
    target_system: str = Field(...)
    description: Optional[str] = None
    target_payload: Optional[Dict[str, Any]] = None
    assigned_to: Optional[str] = None


class RecordOutcomeRequest(BaseModel):
    metric_name: str = Field(...)
    expected_value: float = Field(...)
    actual_value: float = Field(...)


class SubmitPostReviewRequest(BaseModel):
    reviewed_by: str = Field(...)
    outcome_rating: str = Field(default="NEUTRAL")
    prediction_error: Optional[str] = None
    assumption_error: Optional[str] = None
    execution_error: Optional[str] = None
    lessons_learned: Optional[List[str]] = None


class CopilotQueryRequest(BaseModel):
    room_id: str = Field(...)
    query: str = Field(...)
