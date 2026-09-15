"""Pydantic data models for Proposal Generation & Review Intelligence Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProposalSectionSchema(BaseModel):
    title: str
    section_type: str = Field(..., description="COVER, SUMMARY, NEEDS, SOLUTION, SCOPE, DELIVERABLES, ASSUMPTIONS, EXCLUSIONS, OPTIONAL, TERMS")
    content: str


class ProposalClaimSchema(BaseModel):
    statement: str
    supporting_requirement_title: Optional[str] = None
    supporting_feature_title: Optional[str] = None
    is_supported: bool = Field(True)


class ProposalItemDraftSchema(BaseModel):
    description: str
    quantity: float = Field(1.0)
    unit: str = Field("project")
    is_optional: bool = Field(False)
    price: Optional[float] = Field(None, description="Null if pricing requires human review")


class ProposalGenerationResult(BaseModel):
    title: str
    proposal_type: str = Field("FULL", description="TECHNICAL, COMMERCIAL, FULL")
    summary: str
    sections: List[ProposalSectionSchema] = Field(default_factory=list)
    items: List[ProposalItemDraftSchema] = Field(default_factory=list)
    claims: List[ProposalClaimSchema] = Field(default_factory=list)
    pricing_status: str = Field("PRICING_REQUIRES_HUMAN_REVIEW", description="NOT_DEFINED, DRAFT, APPROVED, PRICING_REQUIRES_HUMAN_REVIEW")
    content_hash: str
    requirement_coverage_percentage: float = Field(100.0, ge=0.0, le=100.0)
