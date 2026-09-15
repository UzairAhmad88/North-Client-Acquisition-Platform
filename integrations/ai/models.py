"""Data models for AI Provider completion requests and responses."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AICompletionRequest:
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 2000
    expected_schema: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AICompletionResponse:
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    latency_ms: int = 0
    provider: str = "mock"
    model: str = "mock-model"
    status: str = "SUCCESS"
    error_message: Optional[str] = None
