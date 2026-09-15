"""Pydantic data models for Client Requirements & Discovery Intelligence Agent."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ExtractedRequirementSchema(BaseModel):
    category: str = Field(..., description="Category code (e.g. CORE_FEATURE, BOOKING, INTEGRATION)")
    title: str = Field(..., description="Short title of the requirement")
    description: str = Field(..., description="Detailed description")
    source_type: str = Field("CLIENT_MESSAGE", description="CLIENT_MESSAGE, AI_INFERENCE, etc.")
    source_reference: Optional[str] = Field(None, description="Message ID or document reference")
    explicit: bool = Field(True, description="True if explicitly requested by client; False if inferred")
    confidence: str = Field("HIGH", description="HIGH, MEDIUM, LOW, UNKNOWN")
    status: str = Field("PROPOSED", description="PROPOSED, IN_REVIEW, CONFIRMED, etc.")
    priority: str = Field("MEDIUM", description="CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL")
    evidence_text: Optional[str] = Field(None, description="Supporting quote or evidence snippet")


class RequirementDependencySchema(BaseModel):
    requirement_title: str
    depends_on_title: str
    dependency_type: str = Field("REQUIRES", description="REQUIRES, ENHANCES, CONFLICTS_WITH, BLOCKS, RELATED_TO")
    confidence: str = Field("HIGH")


class DiscoveryQuestionSchema(BaseModel):
    question: str
    category: str = Field("SCOPE")
    priority: str = Field("HIGH", description="CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL")
    reason: Optional[str] = None
    related_requirement_title: Optional[str] = None


class ScopeItemSchema(BaseModel):
    description: str
    scope_status: str = Field("UNKNOWN", description="IN_SCOPE, OUT_OF_SCOPE, OPTIONAL, UNKNOWN")
    priority: str = Field("MEDIUM")
    confirmed: bool = Field(False)


class ContradictionSchema(BaseModel):
    requirement_a: str
    requirement_b: str
    conflict_description: str
    recommended_clarification: str


class ReadinessEvaluationSchema(BaseModel):
    readiness_stage: str = Field("NOT_READY", description="NOT_READY, PARTIALLY_READY, READY_FOR_REVIEW, READY_FOR_NEXT_STAGE")
    readiness_score: float = Field(0.0, ge=0.0, le=100.0)
    completeness_score: float = Field(0.0, ge=0.0, le=100.0)
    scope_complexity: str = Field("UNKNOWN", description="LOW, MEDIUM, HIGH, UNKNOWN")
    missing_critical_areas: List[str] = Field(default_factory=list)


class RequirementsAnalysisResult(BaseModel):
    business_goal: Optional[str] = None
    business_problem: Optional[str] = None
    target_users: List[str] = Field(default_factory=list)
    project_type: Optional[str] = None

    requirements: List[ExtractedRequirementSchema] = Field(default_factory=list)
    dependencies: List[RequirementDependencySchema] = Field(default_factory=list)
    questions: List[DiscoveryQuestionSchema] = Field(default_factory=list)
    scope_items: List[ScopeItemSchema] = Field(default_factory=list)
    contradictions: List[ContradictionSchema] = Field(default_factory=list)
    readiness: ReadinessEvaluationSchema = Field(default_factory=ReadinessEvaluationSchema)

    scope_expansion_detected: bool = Field(False)
    unsupported_assumptions: List[str] = Field(default_factory=list)
