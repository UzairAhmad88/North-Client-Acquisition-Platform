"""Pydantic schemas for Project Estimation REST API."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class EstimateWorkItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    estimate_id: uuid.UUID
    requirement_id: Optional[uuid.UUID] = None
    feature_id: Optional[uuid.UUID] = None
    name: str
    category: str
    description: str
    complexity: str
    optimistic_hours: float
    most_likely_hours: float
    pessimistic_hours: float
    expected_hours: float
    confidence: str
    created_at: datetime


class EstimateCostItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    estimate_id: uuid.UUID
    cost_type: str
    description: str
    amount: float
    currency: str
    source: str
    created_at: datetime


class EstimateScenarioResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    estimate_id: uuid.UUID
    name: str
    description: str
    scope: str
    estimated_hours: float
    internal_cost: Optional[float] = None
    external_cost: Optional[float] = None
    recommended_min: Optional[float] = None
    recommended_max: Optional[float] = None
    risk_level: str
    status: str
    created_at: datetime


class ProjectEstimateCreateSchema(BaseModel):
    solution_id: uuid.UUID


class ProjectEstimateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    status: str
    complexity: str
    confidence: str
    estimated_hours: float
    minimum_hours: float
    maximum_hours: float
    risk_buffer_percent: float
    internal_cost: Optional[float] = None
    external_cost: Optional[float] = None
    recommended_min: Optional[float] = None
    recommended_max: Optional[float] = None
    requirements_version: int
    solution_version: int
    pricing_policy_version: str
    cost_model_version: str
    content_hash: Optional[str] = None
    version: int
    created_by_id: Optional[uuid.UUID] = None
    approved_by_id: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ProjectEstimateDetailSchema(ProjectEstimateResponseSchema):
    work_items: List[EstimateWorkItemResponseSchema] = Field(default_factory=list)
    costs: List[EstimateCostItemResponseSchema] = Field(default_factory=list)
    scenarios: List[EstimateScenarioResponseSchema] = Field(default_factory=list)
