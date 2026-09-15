"""Pydantic schemas for Proposal REST API."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProposalItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_id: uuid.UUID
    service_id: Optional[uuid.UUID] = None
    deliverable_id: Optional[uuid.UUID] = None
    description: str
    quantity: float
    unit: str
    is_optional: bool
    price: Optional[float] = None
    created_at: datetime


class ProposalVersionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_id: uuid.UUID
    version: int
    content_hash: str
    sections_json: Dict[str, Any]
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime


class ProposalCreateSchema(BaseModel):
    solution_id: uuid.UUID
    proposal_type: str = Field("FULL", description="TECHNICAL, COMMERCIAL, FULL")
    title: Optional[str] = None


class ProposalResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    solution_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    proposal_type: str
    title: str
    summary: str
    status: str
    pricing_status: str
    version: int
    content_hash: Optional[str] = None
    created_by_id: Optional[uuid.UUID] = None
    approved_by_id: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ProposalDetailSchema(ProposalResponseSchema):
    items: List[ProposalItemResponseSchema] = Field(default_factory=list)
    versions: List[ProposalVersionResponseSchema] = Field(default_factory=list)
