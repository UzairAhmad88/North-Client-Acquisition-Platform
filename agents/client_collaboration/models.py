"""Pydantic schemas for Client Collaboration AI Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RequestClassificationResult(BaseModel):
    """Result schema for client request classification."""

    request_id: str
    title: str
    classification: str = Field(..., description="IN_SCOPE, POTENTIAL_SCOPE_CHANGE, SUPPORT, BUG, CONTENT, NEEDS_REVIEW")
    reasoning: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    is_potential_scope_change: bool = False


class ExtractedClientActionSchema(BaseModel):
    """Extracted client action item requirement."""

    title: str
    description: str
    priority: str = Field("MEDIUM", description="HIGH, MEDIUM, LOW")
    due_in_days: Optional[int] = None


class FeedbackSummaryResult(BaseModel):
    """Client deliverable feedback summary result."""

    deliverable_id: str
    deliverable_name: str
    overall_sentiment: str = Field(..., description="POSITIVE, MIXED, REVISION_REQUIRED")
    key_feedback_points: List[str]
    suggested_action_items: List[ExtractedClientActionSchema]
    is_revision_requested: bool = False
