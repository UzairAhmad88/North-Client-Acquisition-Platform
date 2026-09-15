"""Pydantic request and response schemas for Phase 38 Search, Command, and Assistant."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.command.base import CommandCategory, CommandExecutionStatus, CommandRiskLevel
from app.search.base import IndexFreshness, SearchEntityType, SearchType


# =============================================================================
# 1. Search Schemas
# =============================================================================

class SearchResultItemSchema(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    tenant_id: str
    title: str
    snippet: str
    score: float
    status: Optional[str] = None
    priority: Optional[str] = None
    action_url: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponseSchema(BaseModel):
    query: str
    parsed_query: Dict[str, Any]
    total_count: int
    results: List[SearchResultItemSchema]
    facets: Dict[str, int]
    latency_ms: float
    index_freshness: str
    index_version: int


class SearchSuggestionSchema(BaseModel):
    text: str
    type: str
    category: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    query: Optional[str] = None


class SearchSavedQueryCreateRequest(BaseModel):
    name: str
    query_text: str
    filters_json: Optional[Dict[str, Any]] = None
    is_pinned: bool = False


class SearchSavedQueryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: str
    user_id: str
    name: str
    query_text: str
    filters_json: Dict[str, Any]
    is_pinned: bool
    created_at: datetime


class SearchPinCreateRequest(BaseModel):
    entity_type: str
    entity_id: str
    title: str
    action_url: str


class SearchPinResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: str
    user_id: str
    entity_type: str
    entity_id: str
    title: str
    action_url: str
    created_at: datetime


# =============================================================================
# 2. Command Palette Schemas
# =============================================================================

class CommandParseRequest(BaseModel):
    text: str


class CommandValidateRequest(BaseModel):
    command_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class CommandExecuteRequest(BaseModel):
    command_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    has_confirmation: bool = False
    has_approval: bool = False


class CommandResponseSchema(BaseModel):
    request_id: str
    command_id: str
    category: str
    risk_level: str
    parameters: Dict[str, Any]
    status: str
    requires_confirmation: bool
    requires_approval: bool
    approval_reason: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str


class CommandDefinitionSchema(BaseModel):
    command_id: str
    name: str
    description: str
    category: str
    risk_level: str
    requires_confirmation: bool
    requires_approval: bool
    parameters_schema: Dict[str, Any]


# =============================================================================
# 3. Platform Assistant Schemas
# =============================================================================

class AssistantQueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class AssistantSourceSchema(BaseModel):
    entity_type: str
    entity_id: str
    title: str
    action_url: Optional[str] = None
    snippet: Optional[str] = None
    confidence: float = 1.0


class AssistantQueryResponseSchema(BaseModel):
    session_id: str
    question: str
    answer: str
    answer_type: str
    sources: List[AssistantSourceSchema]
    suggested_actions: List[Dict[str, Any]]
    created_at: str
    ai_trace_id: Optional[str] = None
