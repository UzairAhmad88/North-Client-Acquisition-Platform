import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AgentSpecRead(BaseModel):
    name: str
    version: str
    description: str
    enabled: bool
    permissions: List[str]
    max_steps: int
    max_tool_calls: int
    max_runtime_seconds: int


class AgentEventRead(BaseModel):
    id: uuid.UUID
    agent_run_id: uuid.UUID
    event_type: str
    message: str
    payload: Dict[str, Any]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentRunRead(BaseModel):
    id: uuid.UUID
    workflow_id: str
    task_id: str
    agent_run_id: str
    agent_name: str
    agent_version: str
    user_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None
    business_id: Optional[uuid.UUID] = None
    status: str
    input_summary: Dict[str, Any]
    output_summary: Dict[str, Any]
    confidence: str
    tool_calls_count: int
    steps_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    estimated_tokens: int
    estimated_cost: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentRunDetailRead(AgentRunRead):
    events: List[AgentEventRead] = Field(default_factory=list)


class AgentRunCreateRequest(BaseModel):
    agent_name: str
    lead_id: Optional[uuid.UUID] = None
    business_id: Optional[uuid.UUID] = None
    input_data: Optional[Dict[str, Any]] = None
