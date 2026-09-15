"""Pydantic schemas for Solution Design REST API."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SolutionFeatureResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    title: str
    description: str
    category: str
    status: str
    priority: str
    created_at: datetime


class SolutionDeliverableResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    name: str
    description: str
    status: str
    priority: str
    created_at: datetime


class SolutionIntegrationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    purpose: str
    provider: str
    data_flow: str
    status: str
    created_at: datetime


class SolutionAssumptionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    assumption_text: str
    status: str
    risk_level: str
    created_at: datetime


class SolutionDesignCreateSchema(BaseModel):
    discovery_session_id: uuid.UUID
    overview: Optional[str] = None


class SolutionDesignResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    discovery_session_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    status: str
    overview: str
    architecture_summary: str
    complexity_tier: str
    version: int
    created_by_id: Optional[uuid.UUID] = None
    approved_by_id: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class SolutionDesignDetailSchema(SolutionDesignResponseSchema):
    features: List[SolutionFeatureResponseSchema] = Field(default_factory=list)
    deliverables: List[SolutionDeliverableResponseSchema] = Field(default_factory=list)
    integrations: List[SolutionIntegrationResponseSchema] = Field(default_factory=list)
    assumptions: List[SolutionAssumptionResponseSchema] = Field(default_factory=list)
