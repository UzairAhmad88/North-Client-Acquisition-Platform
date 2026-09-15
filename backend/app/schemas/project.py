"""Pydantic schemas for Project Execution API endpoints."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProjectCreateSchema(BaseModel):
    """Request schema for creating a delivery project."""

    name: str = Field(..., description="Project title")
    description: str = Field(..., description="Project description")
    business_id: uuid.UUID
    contract_id: uuid.UUID
    baseline_id: uuid.UUID
    owner_id: Optional[uuid.UUID] = None
    priority: str = Field("MEDIUM", description="Priority tier (CRITICAL, HIGH, MEDIUM, LOW)")


class ProjectStatusUpdateSchema(BaseModel):
    """Request schema for updating project lifecycle status."""

    status: str = Field(..., description="New lifecycle state (PLANNING, READY, IN_PROGRESS, ON_HOLD, COMPLETED)")


class TaskCreateSchema(BaseModel):
    """Request schema for creating a project task."""

    name: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed description")
    priority: str = Field("MEDIUM", description="Task priority")
    estimated_hours: float = Field(0.0, ge=0.0, description="Estimated effort hours")
    parent_task_id: Optional[uuid.UUID] = None
    deliverable_id: Optional[uuid.UUID] = None
    milestone_id: Optional[uuid.UUID] = None
    assignee_id: Optional[uuid.UUID] = None


class TaskStatusUpdateSchema(BaseModel):
    """Request schema for updating task status or progress."""

    status: str = Field(..., description="Task status (TODO, IN_PROGRESS, BLOCKED, COMPLETED)")
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    blocked_reason: Optional[str] = None


class TaskDependencyCreateSchema(BaseModel):
    """Request schema for adding task dependency."""

    predecessor_id: uuid.UUID
    successor_id: uuid.UUID


class MilestoneCreateSchema(BaseModel):
    """Request schema for creating a project milestone."""

    name: str
    description: str
    target_date: Optional[datetime] = None
    owner_id: Optional[uuid.UUID] = None


class RiskCreateSchema(BaseModel):
    """Request schema for logging a project risk."""

    title: str
    description: str
    probability: str = "MEDIUM"
    impact: str = "MEDIUM"
    severity: str = "MEDIUM"
    mitigation_plan: str


class BlockerCreateSchema(BaseModel):
    """Request schema for logging a blocker."""

    title: str
    description: str
    severity: str = "HIGH"
    task_id: Optional[uuid.UUID] = None


class ClientDependencyCreateSchema(BaseModel):
    """Request schema for adding client dependency."""

    title: str
    description: str
    required_by_date: Optional[datetime] = None


class EffortEntryCreateSchema(BaseModel):
    """Request schema for logging manual effort."""

    task_id: uuid.UUID
    hours: float = Field(..., gt=0.0)
    description: str


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    parent_task_id: Optional[uuid.UUID] = None
    deliverable_id: Optional[uuid.UUID] = None
    milestone_id: Optional[uuid.UUID] = None
    task_number: str
    name: str
    description: str
    status: str
    priority: str
    assignee_id: Optional[uuid.UUID] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    estimated_hours: float
    actual_hours: float
    progress_percent: float
    dependency_status: str
    blocked_reason: Optional[str] = None
    version: int
    created_at: datetime


class MilestoneResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    description: str
    target_date: Optional[datetime] = None
    status: str
    progress_percent: float
    created_at: datetime


class DeliverableResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    description: str
    source_baseline_item: str
    acceptance_criteria: List[str]
    status: str
    target_date: Optional[datetime] = None
    created_at: datetime


class ProjectResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_number: str
    name: str
    description: str
    business_id: uuid.UUID
    client_id: Optional[uuid.UUID] = None
    contract_id: uuid.UUID
    baseline_id: uuid.UUID
    owner_id: Optional[uuid.UUID] = None
    status: str
    health: str
    priority: str
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    progress_percent: float
    total_estimated_hours: float
    total_actual_hours: float
    version: int
    created_at: datetime
    updated_at: datetime


class ProjectDetailResponseSchema(ProjectResponseSchema):
    tasks: List[TaskResponseSchema] = []
    milestones: List[MilestoneResponseSchema] = []
    deliverables: List[DeliverableResponseSchema] = []
