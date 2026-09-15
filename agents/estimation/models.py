"""Pydantic data models for Estimation & Commercial Intelligence Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EstimateWorkItemSchema(BaseModel):
    name: str
    category: str = Field("BACKEND", description="DISCOVERY, DESIGN, FRONTEND, BACKEND, DATABASE, API, INTEGRATION, AI, ML, TESTING, SECURITY, DEVOPS, DEPLOYMENT, DOCUMENTATION, MAINTENANCE")
    description: str
    complexity: str = Field("MEDIUM", description="TRIVIAL, LOW, MEDIUM, HIGH, VERY_HIGH, UNKNOWN")
    optimistic_hours: float = Field(..., ge=0.0)
    most_likely_hours: float = Field(..., ge=0.0)
    pessimistic_hours: float = Field(..., ge=0.0)
    expected_hours: float = Field(0.0, ge=0.0)
    confidence: str = Field("MEDIUM", description="HIGH, MEDIUM, LOW")
    supporting_requirement_title: Optional[str] = None
    supporting_feature_title: Optional[str] = None


class EstimateCostItemSchema(BaseModel):
    cost_type: str = Field("INTERNAL", description="INTERNAL, EXTERNAL, INFRASTRUCTURE, PROVIDER, OTHER")
    description: str
    amount: float
    currency: str = Field("USD")
    source: str = Field("CONFIGURED_RATE")


class EstimateScenarioSchema(BaseModel):
    name: str = Field(..., description="LEAN, STANDARD, EXPANDED")
    description: str
    scope: str
    estimated_hours: float
    internal_cost: Optional[float] = None
    external_cost: Optional[float] = None
    recommended_min: Optional[float] = None
    recommended_max: Optional[float] = None
    risk_level: str = Field("MEDIUM")


class EstimationResult(BaseModel):
    summary: str
    complexity: str = Field("MEDIUM")
    confidence: str = Field("MEDIUM")
    estimated_hours: float
    minimum_hours: float
    maximum_hours: float
    risk_buffer_percent: float = Field(20.0)
    internal_cost: float
    external_cost: float
    recommended_min: float
    recommended_max: float
    work_items: List[EstimateWorkItemSchema] = Field(default_factory=list)
    costs: List[EstimateCostItemSchema] = Field(default_factory=list)
    scenarios: List[EstimateScenarioSchema] = Field(default_factory=list)
    role_breakdown: Dict[str, float] = Field(default_factory=dict)
    content_hash: str
