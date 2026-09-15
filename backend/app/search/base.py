"""Core enums, data structures, and type definitions for Unified Platform Search."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class SearchEntityType(str, Enum):
    """Supported searchable domain entity types."""

    ALL = "ALL"
    BUSINESS = "BUSINESS"
    LEAD = "LEAD"
    CONTACT = "CONTACT"
    OPPORTUNITY = "OPPORTUNITY"
    CONVERSATION = "CONVERSATION"
    MESSAGE = "MESSAGE"
    REQUIREMENT = "REQUIREMENT"
    SOLUTION = "SOLUTION"
    PROPOSAL = "PROPOSAL"
    CONTRACT = "CONTRACT"
    PROJECT = "PROJECT"
    TASK = "TASK"
    DELIVERABLE = "DELIVERABLE"
    CHANGE_REQUEST = "CHANGE_REQUEST"
    DEFECT = "DEFECT"
    UAT_SESSION = "UAT_SESSION"
    SUPPORT_REQUEST = "SUPPORT_REQUEST"
    DOCUMENT = "DOCUMENT"
    KNOWLEDGE_ITEM = "KNOWLEDGE_ITEM"
    WORKFLOW = "WORKFLOW"
    EVENT = "EVENT"
    AI_TRACE = "AI_TRACE"


class SearchType(str, Enum):
    """Retrieval mechanism applied to query."""

    KEYWORD = "KEYWORD"
    EXACT = "EXACT"
    FUZZY = "FUZZY"
    SEMANTIC = "SEMANTIC"
    FACETED = "FACETED"
    NATURAL_LANGUAGE = "NATURAL_LANGUAGE"


class IndexFreshness(str, Enum):
    """Telemetry indicator for search index state."""

    INDEX_CURRENT = "INDEX_CURRENT"
    INDEX_SLIGHTLY_STALE = "INDEX_SLIGHTLY_STALE"
    INDEX_STALE = "INDEX_STALE"
    INDEX_REBUILDING = "INDEX_REBUILDING"
    INDEX_FAILED = "INDEX_FAILED"


@dataclass
class SearchFilter:
    """Explicit field-level search constraint."""

    field: str
    operator: str  # eq, in, gte, lte, contains, between
    value: Any


@dataclass
class ParsedQuery:
    """Structured output from query parser."""

    raw_query: str
    normalized_query: str
    search_type: SearchType = SearchType.KEYWORD
    entity_types: List[SearchEntityType] = field(default_factory=lambda: [SearchEntityType.ALL])
    filters: List[SearchFilter] = field(default_factory=list)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    extracted_entities: List[str] = field(default_factory=list)


@dataclass
class SearchResultItem:
    """Individual item returned by unified search."""

    id: str
    entity_type: SearchEntityType
    entity_id: str
    tenant_id: str
    title: str
    snippet: str
    score: float
    status: Optional[str] = None
    priority: Optional[str] = None
    action_url: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
