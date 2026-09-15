"""Core data models and enums for Global Command Palette and Execution Engine."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid


class CommandCategory(str, Enum):
    """Classification of command actions."""

    NAVIGATION = "NAVIGATION"
    QUERY = "QUERY"
    SAFE_CREATE = "SAFE_CREATE"
    SENSITIVE_ACTION = "SENSITIVE_ACTION"


class CommandRiskLevel(str, Enum):
    """Operational risk level of a command."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CommandExecutionStatus(str, Enum):
    """Lifecycle state of a command invocation."""

    PARSED = "PARSED"
    VALIDATED = "VALIDATED"
    CONFIRMATION_REQUIRED = "CONFIRMATION_REQUIRED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    CONFIRMED = "CONFIRMED"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass
class CommandDefinition:
    """Registered command metadata and safety policy."""

    command_id: str
    name: str
    description: str
    category: CommandCategory
    risk_level: CommandRiskLevel
    required_permission: Optional[str] = None
    requires_confirmation: bool = False
    requires_approval: bool = False
    parameters_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandObject:
    """Structured representation of an instantiated command request."""

    request_id: str
    command_id: str
    category: CommandCategory
    risk_level: CommandRiskLevel
    parameters: Dict[str, Any]
    status: CommandExecutionStatus = CommandExecutionStatus.PARSED
    requires_confirmation: bool = False
    requires_approval: bool = False
    approval_reason: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
