"""Schemas for Project Execution AI Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DraftWBSItemSchema(BaseModel):
    """Suggested Work Breakdown Structure (WBS) task item."""

    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Detailed work description")
    category: str = Field("GENERAL", description="Deliverable or engineering category")
    priority: str = Field("MEDIUM", description="Task priority (CRITICAL, HIGH, MEDIUM, LOW)")
    estimated_hours: float = Field(..., ge=0.0, description="Estimated work effort in hours")
    predecessor_temp_ids: List[int] = Field(default_factory=list, description="Temporary indices of predecessor tasks")
    deliverable_name: Optional[str] = Field(None, description="Linked deliverable name")
    milestone_name: Optional[str] = Field(None, description="Linked milestone target")


class DraftMilestoneSchema(BaseModel):
    """Suggested project milestone."""

    name: str = Field(..., description="Milestone title")
    description: str = Field(..., description="Milestone criteria and objective")
    target_days_from_start: int = Field(..., description="Relative days from project start")


class ProjectPlanDraftResult(BaseModel):
    """AI suggested delivery plan draft."""

    project_name: str
    suggested_wbs: List[DraftWBSItemSchema]
    suggested_milestones: List[DraftMilestoneSchema]
    planning_notes: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class ProjectStatusSummaryResult(BaseModel):
    """Executive project status summary."""

    project_id: str
    status: str
    health: str
    progress_percent: float
    executive_summary: str
    key_achievements: List[str]
    active_blockers: List[str]
    risks: List[str]
    overdue_items: List[str]
    recommended_next_actions: List[str]


class ScopeSignalResult(BaseModel):
    """Detected scope expansion signal."""

    signal_type: str  # FEATURE_ADDED, FEATURE_REMOVED, DELIVERABLE_CHANGED
    description: str
    source: str
    severity: str
    recommended_action: str
