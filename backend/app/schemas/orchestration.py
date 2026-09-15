"""Pydantic request and response schemas for Phase 34 API Layer."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


# 1. Workflows
class StartWorkflowRequest(BaseModel):
    workflow_key: str
    input_data: Optional[Dict[str, Any]] = None
    trigger_type: str = "MANUAL"
    trigger_reference: Optional[str] = None


class WorkflowRunStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_key: str
    step_type: str
    status: str
    attempt_count: int
    duration_ms: float
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    error_code: Optional[str] = None
    error_summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    workflow_key: str
    workflow_version: str
    trigger_type: str
    trigger_reference: Optional[str] = None
    status: str
    current_step: Optional[str] = None
    correlation_id: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    error_code: Optional[str] = None
    error_summary: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    paused_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None


class WorkflowTemplateResponse(BaseModel):
    workflow_key: str
    name: str
    description: str
    category: str
    version: str
    steps: List[Dict[str, Any]]
    transitions: List[Dict[str, Any]]


# 2. Events
class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_id: str
    event_type: str
    event_version: str
    aggregate_type: str
    aggregate_id: str
    tenant_id: str
    payload: Dict[str, Any]
    correlation_id: str
    causation_id: Optional[str] = None
    status: str
    attempt_count: int
    created_at: datetime


class EventReplayRequest(BaseModel):
    event_type: str
    replay_mode: str = "DRY_RUN"  # READ_ONLY, DRY_RUN, REBUILD_PROJECTION, CONTROLLED_REEXECUTION


class EventReplayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    event_type: str
    replay_mode: str
    events_replayed_count: int
    triggered_by: str
    status: str
    created_at: datetime


# 3. Human Tasks
class CompleteHumanTaskRequest(BaseModel):
    decision: str  # APPROVED, REJECTED, REVISION_REQUIRED
    decision_reason: str
    content_hash: Optional[str] = None


class HumanTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    workflow_run_id: str
    step_key: str
    title: str
    description: str
    task_type: str
    priority: str
    assigned_to: Optional[str] = None
    status: str
    deadline: Optional[datetime] = None
    input_data: Dict[str, Any]
    decision: Optional[str] = None
    decision_reason: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


# 4. Automations
class CreateAutomationRuleRequest(BaseModel):
    name: str
    description: str
    trigger_type: str = "EVENT"
    trigger_config: Dict[str, Any]
    condition_config: Dict[str, Any]
    action_config: Dict[str, Any]
    requires_human_approval: bool = True


class AutomationRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    description: str
    version: str
    trigger_type: str
    trigger_config: Dict[str, Any]
    condition_config: Dict[str, Any]
    action_config: Dict[str, Any]
    priority: str
    enabled: bool
    requires_human_approval: bool
    created_by: str
    created_at: datetime
    updated_at: datetime


# 5. Dead Letter Queue
class DeadLetterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_id: str
    event_type: str
    workflow_id: Optional[str] = None
    consumer: str
    attempt_count: int
    failure_type: str
    error_summary: str
    payload: Dict[str, Any]
    status: str
    last_error_at: datetime
    created_at: datetime
