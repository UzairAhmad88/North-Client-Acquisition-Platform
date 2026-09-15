"""AI Router managing model selection and completion execution."""

from typing import Optional

from integrations.ai.base import BaseAIProvider
from integrations.ai.models import AICompletionRequest, AICompletionResponse
from integrations.ai.providers.mock import MockAIProvider


class AIRouter:
    """Router handling AI completion requests and fallback policies."""

    def __init__(self, provider: Optional[BaseAIProvider] = None) -> None:
        self.provider = provider or MockAIProvider()

    async def complete(self, request: AICompletionRequest) -> AICompletionResponse:
        """Route completion request to provider."""
        return await self.provider.generate_completion(request)
