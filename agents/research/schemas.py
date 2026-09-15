"""Data schemas for Research Agent requests, findings, evidence, and results."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    """Structured research job request parameters."""

    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID] = None
    sections: List[str] = Field(
        default_factory=lambda: [
            "identity",
            "services",
            "digital_presence",
            "contact_information",
            "business_activity",
        ]
    )
    max_age_days: int = 30
    prefer_official: bool = True
    minimum_trust: str = "MEDIUM_TRUST"


class ResearchFindingItem(BaseModel):
    """Single evidence-backed research finding."""

    field: str
    value: Any
    source_type: str = "OFFICIAL"  # OFFICIAL, HIGH_TRUST, MEDIUM_TRUST, LOW_TRUST, UNKNOWN
    source_url: Optional[str] = None
    source_trust: str = "OFFICIAL"
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW
    evidence: str = ""
    observed_at: Optional[str] = None
    freshness: str = "CURRENT"  # CURRENT, RECENT, STALE, UNKNOWN


class ResearchConflictItem(BaseModel):
    """Conflicting information finding across sources."""

    field: str
    competing_values: List[Dict[str, Any]] = Field(default_factory=list)
    resolution_notes: Optional[str] = None
    confidence: str = "LOW"


class ResearchAgentResult(BaseModel):
    """Structured output returned by Research Agent."""

    status: str = "COMPLETED"  # COMPLETED, PARTIAL, FAILED
    confidence: str = "HIGH"
    business_summary: Dict[str, Any] = Field(default_factory=dict)
    findings: List[ResearchFindingItem] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    conflicts: List[ResearchConflictItem] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    next_action: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
