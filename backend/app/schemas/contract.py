"""Pydantic schemas for Contract REST API."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ContractSectionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    contract_id: uuid.UUID
    title: str
    section_type: str
    content: str
    order_index: int
    created_at: datetime


class ContractDiscrepancyResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    contract_id: uuid.UUID
    discrepancy_type: str
    description: str
    severity: str
    status: str
    created_at: datetime


class ContractBaselineResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    contract_id: uuid.UUID
    contract_version: int
    requirements_version: int
    solution_version: int
    estimate_version: int
    proposal_version: int
    scope_hash: str
    commercial_hash: str
    contract_hash: str
    is_locked: bool
    locked_at: datetime
    created_at: datetime


class ContractCreateSchema(BaseModel):
    proposal_id: uuid.UUID
    estimate_id: uuid.UUID
    title: Optional[str] = None


class ClientAcceptanceRequestSchema(BaseModel):
    client_email: str
    acceptance_statement: str


class ContractResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_id: uuid.UUID
    estimate_id: uuid.UUID
    solution_id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    contract_number: str
    title: str
    summary: str
    status: str
    pricing_status: str
    risk_status: str
    currency: str
    total_amount: Optional[float] = None
    version: int
    content_hash: Optional[str] = None
    is_stale: bool
    created_by_id: Optional[uuid.UUID] = None
    approved_by_id: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ContractDetailSchema(ContractResponseSchema):
    sections: List[ContractSectionResponseSchema] = Field(default_factory=list)
    discrepancies: List[ContractDiscrepancyResponseSchema] = Field(default_factory=list)
    baselines: List[ContractBaselineResponseSchema] = Field(default_factory=list)
