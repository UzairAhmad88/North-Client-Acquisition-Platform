"""Pydantic data models for Contract Intelligence Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ContractSectionSchema(BaseModel):
    title: str
    section_type: str = Field(..., description="PARTIES, OVERVIEW, SCOPE, DELIVERABLES, EXCLUSIONS, ASSUMPTIONS, DEPENDENCIES, COMMERCIAL, PAYMENT, RESPONSIBILITIES, PRIVACY, IP, TERMINATION, SIGNATURES")
    content: str
    order_index: int = Field(0)


class ContractDiscrepancySchema(BaseModel):
    discrepancy_type: str = Field(..., description="SCOPE_MISMATCH, COMMERCIAL_MISMATCH, REQUIREMENT_COVERAGE_WARNING, TIMELINE_MISMATCH")
    description: str
    severity: str = Field("HIGH", description="INFO, LOW, MEDIUM, HIGH, CRITICAL")
    status: str = Field("DETECTED")


class ContractCompletenessSchema(BaseModel):
    completeness_score: float = Field(..., ge=0.0, le=100.0)
    missing_sections: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class ContractGenerationResult(BaseModel):
    contract_number: str
    title: str
    summary: str
    status: str = Field("DRAFT")
    pricing_status: str = Field("PRICING_REQUIRES_HUMAN_REVIEW")
    risk_status: str = Field("PENDING_REVIEW")
    sections: List[ContractSectionSchema] = Field(default_factory=list)
    discrepancies: List[ContractDiscrepancySchema] = Field(default_factory=list)
    completeness: ContractCompletenessSchema
    content_hash: str
