"""Base AI Provider Interface."""

from integrations.ai.models import AICompletionRequest, AICompletionResponse


class BaseAIProvider:
    provider_name: str = "base"
    model_name: str = "base-model"

    async def generate_completion(
        self, request: AICompletionRequest
    ) -> AICompletionResponse:
        raise NotImplementedError
