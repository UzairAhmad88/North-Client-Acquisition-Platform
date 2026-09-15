"""Pydantic schemas for Support Intelligence AI Subsystem."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SupportClassificationResult(BaseModel):
    """Output for Support Request triage classification."""

    request_id: Optional[str] = None
    title: str
    category: str = "APPLICATION"
    classification: str = "SUPPORT"  # DEFECT, SUPPORT, MAINTENANCE, CONFIGURATION, INCIDENT, CHANGE_REQUEST, NEW_PROJECT, QUESTION, TRAINING, BILLING, UNKNOWN
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    severity: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    confidence: float = 0.90
    reasoning: str
    is_change_request: bool = False
    is_new_project: bool = False
    is_incident: bool = False


class WarrantyEvaluationResult(BaseModel):
    """Output for warranty coverage eligibility evaluation."""

    project_id: str
    is_covered: str = "UNKNOWN"  # COVERED, NOT_COVERED, REVIEW_REQUIRED, UNKNOWN
    confidence: float = 0.85
    reasoning: str
    contract_reference: Optional[str] = None
    requires_human_approval: bool = True


class TroubleshootingSuggestionResult(BaseModel):
    """Structured diagnostic recommendations."""

    request_id: Optional[str] = None
    observed_symptoms: List[str] = Field(default_factory=list)
    inferred_causes: List[str] = Field(default_factory=list)
    possible_solutions: List[str] = Field(default_factory=list)
    confirmed_findings: List[str] = Field(default_factory=list)
    recommended_next_steps: List[str] = Field(default_factory=list)


class OpportunityDetectionResult(BaseModel):
    """Detected expansion opportunity draft from support dialogue."""

    project_id: str
    opportunity_detected: bool = False
    opportunity_type: str = "NEW_FEATURE"  # NEW_FEATURE, RETRACTED_SCOPE, AUTOMATION, UPGRADE, NEW_PROJECT
    title: str
    description: str
    estimated_value_range: str = "PKR 50,000 - 150,000"
    confidence: float = 0.80
    requires_sales_review: bool = True


class IncidentSummaryResult(BaseModel):
    """Executive incident summary and root cause breakdown."""

    incident_id: str
    severity: str = "SEV-2"
    impact_level: str = "MAJOR"
    executive_summary: str
    root_cause_hypothesis: str
    mitigation_recommendations: List[str] = Field(default_factory=list)
