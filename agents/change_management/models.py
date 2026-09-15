"""Pydantic schemas and output models for Change Management AI subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChangeClassificationResult(BaseModel):
    """Result of change request classification & triage."""

    change_request_id: str
    classification: str  # IN_SCOPE, OUT_OF_SCOPE, CLARIFICATION, DEFECT, CLIENT_CHANGE, INTERNAL_CHANGE, DEPENDENCY_CHANGE, CONTRACT_CHANGE, COMMERCIAL_CHANGE, UNKNOWN
    confidence_score: float = Field(default=0.85, ge=0.0, le=1.0)
    reasoning: str
    is_out_of_scope: bool = False
    suggested_action: str = "PROCEED_TO_IMPACT_ANALYSIS"


class ChangeImpactItem(BaseModel):
    """Individual impact analysis item."""

    impact_type: str  # REQUIREMENT, SOLUTION, DELIVERABLE, TASK, MILESTONE, DEPENDENCY, RESOURCE, RISK, SCHEDULE, EFFORT, COMMERCIAL, CONTRACT
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    impact_action: str = "AFFECTED"  # ADDED, REMOVED, MODIFIED, AFFECTED, NO_IMPACT, UNKNOWN
    impact_description: str
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW, UNKNOWN
    evidence_reference: Optional[str] = None


class ImpactAnalysisResult(BaseModel):
    """Aggregate multi-dimensional impact analysis result."""

    change_request_id: str
    overall_impact_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    impacts: List[ChangeImpactItem] = Field(default_factory=list)
    requires_contract_amendment: bool = False
    requires_commercial_adjustment: bool = False
    risk_level: str = "MEDIUM"


class ChangeEffortEstimate(BaseModel):
    """PERT 3-point effort re-estimation for change requests."""

    change_request_id: str
    optimistic_hours: float = 0.0
    most_likely_hours: float = 0.0
    pessimistic_hours: float = 0.0
    expected_hours: float = 0.0
    confidence: float = 0.85
    assumptions: List[str] = Field(default_factory=list)


class ChangeCommercialAnalysis(BaseModel):
    """Commercial delta analysis for change requests."""

    change_request_id: str
    currency: str = "PKR"
    original_value: float = 0.0
    change_value: float = 0.0
    revised_value: float = 0.0
    commercial_recommendation: str = "ADDITIONAL_COST_REQUIRED"
    pricing_policy_version: str = "1.0"


class ChangeProposalSummary(BaseModel):
    """Internal & client-facing proposal summary."""

    change_request_id: str
    change_number: str
    title: str
    executive_summary: str
    scope_delta_description: str
    estimated_schedule_impact_days: int = 0
    commercial_impact_summary: str
    client_safe_summary: str
