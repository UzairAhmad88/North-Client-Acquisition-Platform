"""
Pydantic Schemas for Phase 55 — Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class InnovationWorkspaceCreateRequest(BaseModel):
    title: str = Field(..., description="Workspace title")
    owner_id: str = Field(default="product_lead")
    theme: str = Field(default="PRODUCT_INNOVATION")
    objective: Optional[str] = None
    target_market: Optional[str] = None
    horizon: str = Field(default="H1")


class RecordProblemRequest(BaseModel):
    statement: str = Field(..., description="Problem statement")
    affected_users: Optional[str] = None
    frequency: str = Field(default="DAILY")
    severity: str = Field(default="HIGH")
    existing_solutions: Optional[List[str]] = None
    willingness_to_pay_signal: Optional[float] = None
    evidence_sources: Optional[List[str]] = None


class CreateOpportunityRequest(BaseModel):
    title: str = Field(..., description="Opportunity title")
    description: Optional[str] = None
    market_potential: str = Field(default="HIGH")
    revenue_potential_usd: Optional[float] = None
    competitive_intensity: str = Field(default="MEDIUM")
    technical_feasibility: str = Field(default="FEASIBLE")


class CreateIdeaRequest(BaseModel):
    title: str = Field(..., description="Idea title")
    description: str = Field(..., description="Idea description")
    origin_source: str = Field(default="HUMAN")
    problem_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    target_users: Optional[str] = None
    proposed_value: Optional[str] = None
    scoring_factors: Optional[Dict[str, float]] = None


class FormHypothesisRequest(BaseModel):
    idea_id: str = Field(...)
    statement: str = Field(..., description="We believe that...")
    prediction: str = Field(..., description="We expect that...")
    metric_name: str = Field(...)
    baseline_value: float = Field(default=0.0)
    target_value: float = Field(default=0.20)
    confidence: float = Field(default=0.7)


class MapAssumptionRequest(BaseModel):
    assumption_text: str = Field(...)
    category: str = Field(default="CUSTOMER")
    impact_level: str = Field(default="HIGH")
    uncertainty_level: str = Field(default="HIGH")


class DesignExperimentRequest(BaseModel):
    hypothesis_id: str = Field(...)
    title: str = Field(...)
    experiment_type: str = Field(default="PROTOTYPE")
    sample_size: int = Field(default=100)
    duration_days: int = Field(default=14)


class RecordExperimentResultRequest(BaseModel):
    control_values: List[float] = Field(...)
    treatment_values: List[float] = Field(...)
    limitations: Optional[str] = None


class CreateProductConceptRequest(BaseModel):
    name: str = Field(...)
    target_customer_persona: str = Field(...)
    value_proposition: str = Field(...)
    core_features: Optional[List[str]] = None
    differentiators: Optional[List[str]] = None
    idea_id: Optional[str] = None


class CreateBusinessCaseRequest(BaseModel):
    concept_id: str = Field(...)
    target_tam_usd: float = Field(default=1000000.0)
    projected_year1_revenue_usd: float = Field(default=250000.0)
    estimated_development_cost_usd: float = Field(default=50000.0)
    estimated_cac_usd: float = Field(default=1200.0)
    estimated_ltv_usd: float = Field(default=7200.0)


class ConductGateReviewRequest(BaseModel):
    gate_stage: str = Field(...)
    reviewer_id: str = Field(...)
    evidence_completeness_score: float = Field(default=0.85)
    decision: str = Field(default="PROCEED")
    review_notes: Optional[str] = None


class InnovationCopilotRequest(BaseModel):
    workspace_id: str = Field(...)
    query: str = Field(..., description="Innovation query or prompt")
