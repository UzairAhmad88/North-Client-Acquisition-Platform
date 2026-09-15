"""Mock AI Provider for deterministic testing."""

import json
import time
from typing import Any, Dict, Optional

from integrations.ai.base import BaseAIProvider
from integrations.ai.models import AICompletionRequest, AICompletionResponse


class MockAIProvider(BaseAIProvider):
    provider_name: str = "mock"
    model_name: str = "mock-agentic-v1"

    def __init__(self, mock_response_data: Optional[Dict[str, Any]] = None) -> None:
        self.mock_response_data = mock_response_data or {
            "status": "completed",
            "result": {"summary": "Mock completion result successfully generated."},
            "confidence": "HIGH",
            "evidence": [],
            "warnings": [],
        }

    async def generate_completion(
        self, request: AICompletionRequest
    ) -> AICompletionResponse:
        start = time.time()
        content = json.dumps(self.mock_response_data)
        latency = int((time.time() - start) * 1000)

        in_tokens = len(request.prompt.split()) * 2
        out_tokens = len(content.split()) * 2

        return AICompletionResponse(
            content=content,
            structured_data=self.mock_response_data,
            input_tokens=in_tokens,
            output_tokens=out_tokens,
            total_tokens=in_tokens + out_tokens,
            estimated_cost=0.0001,
            latency_ms=latency,
            provider=self.provider_name,
            model=self.model_name,
            status="SUCCESS",
        )
