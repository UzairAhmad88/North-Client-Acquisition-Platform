"""Core data models and enums for Secure Natural-Language Platform Assistant."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class AssistantRole(str, Enum):
    """Message sender role."""

    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class AnswerType(str, Enum):
    """Categorization of generated answer components."""

    FACT = "FACT"
    INFERENCE = "INFERENCE"
    CALCULATION = "CALCULATION"
    UNKNOWN = "UNKNOWN"


@dataclass
class AssistantSource:
    """Attributed source reference for assistant answer."""

    entity_type: str
    entity_id: str
    title: str
    authority_level: str = "CANONICAL"
    confidence: float = 1.0
    action_url: Optional[str] = None
    snippet: Optional[str] = None


@dataclass
class AssistantMessage:
    """Individual conversation turn in an assistant session."""

    id: str
    session_id: str
    role: AssistantRole
    content: str
    answer_type: AnswerType = AnswerType.FACT
    sources: List[AssistantSource] = field(default_factory=list)
    suggested_actions: List[Dict[str, Any]] = field(default_factory=list)
    ai_trace_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
