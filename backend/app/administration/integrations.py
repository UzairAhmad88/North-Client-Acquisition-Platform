"""Centralized Integration Registry and Provider Configuration Engine."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProviderConfiguration(BaseModel):
    provider_id: str
    name: str
    category: str
    base_url: str
    secret_reference: str
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_rpm: int = 600
    is_active: bool = True
    health_status: str = "HEALTHY"
    last_health_check: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    latency_ms: float = 45.0
    error_rate_percentage: float = 0.0


class IntegrationManager:
    """Manages external provider integrations, secret reference resolution, and health telemetry."""

    def __init__(self):
        self._providers: Dict[str, ProviderConfiguration] = {}
        self._seed_default_providers()

    def _seed_default_providers(self):
        """Seed default third-party integrations with secret references."""
        providers = [
            ProviderConfiguration(
                provider_id="PROV-OPENAI",
                name="OpenAI GPT-4o / Reasoning Tier",
                category="AI / LLM",
                base_url="https://api.openai.com/v1",
                secret_reference="secret://production/ai/openai-api-key",
                timeout_seconds=45,
                latency_ms=320.0,
            ),
            ProviderConfiguration(
                provider_id="PROV-ANTHROPIC",
                name="Anthropic Claude 3.5 Sonnet",
                category="AI / LLM",
                base_url="https://api.anthropic.com/v1",
                secret_reference="secret://production/ai/anthropic-api-key",
                timeout_seconds=45,
                latency_ms=280.0,
            ),
            ProviderConfiguration(
                provider_id="PROV-SENDGRID",
                name="SendGrid Email Dispatcher",
                category="Communication / Email",
                base_url="https://api.sendgrid.com/v3",
                secret_reference="secret://production/email/sendgrid-api-key",
                timeout_seconds=15,
                latency_ms=110.0,
            ),
            ProviderConfiguration(
                provider_id="PROV-STRIPE",
                name="Stripe Payments Gateway",
                category="Finance / Payments",
                base_url="https://api.stripe.com/v1",
                secret_reference="secret://production/finance/stripe-secret-key",
                timeout_seconds=20,
                latency_ms=140.0,
            ),
            ProviderConfiguration(
                provider_id="PROV-QDRANT",
                name="Qdrant Vector Engine",
                category="Search / Vector DB",
                base_url="https://vector.cluster.internal:6333",
                secret_reference="secret://production/search/qdrant-api-key",
                timeout_seconds=10,
                latency_ms=25.0,
            ),
            ProviderConfiguration(
                provider_id="PROV-AWS-S3",
                name="Amazon S3 Document Lake",
                category="Storage / Object Store",
                base_url="https://s3.us-east-1.amazonaws.com",
                secret_reference="secret://production/storage/aws-credentials",
                timeout_seconds=15,
                latency_ms=55.0,
            ),
        ]
        for p in providers:
            self._providers[p.provider_id] = p

    def list_providers(self, category: Optional[str] = None) -> List[ProviderConfiguration]:
        """List all registered provider integrations."""
        if category:
            return [p for p in self._providers.values() if p.category.lower().startswith(category.lower())]
        return list(self._providers.values())

    def get_provider(self, provider_id: str) -> Optional[ProviderConfiguration]:
        """Get provider by ID."""
        return self._providers.get(provider_id)

    def register_provider(self, provider: ProviderConfiguration) -> ProviderConfiguration:
        """Register or update a provider integration."""
        if not provider.secret_reference.startswith("secret://"):
            raise ValueError("Secret reference must begin with 'secret://'. Raw secrets cannot be stored.")
        self._providers[provider.provider_id] = provider
        return provider

    def record_health_probe(self, provider_id: str, is_healthy: bool, latency_ms: float, error_rate: float = 0.0):
        """Update provider health telemetry."""
        p = self.get_provider(provider_id)
        if p:
            p.health_status = "HEALTHY" if is_healthy else "UNAVAILABLE"
            p.latency_ms = latency_ms
            p.error_rate_percentage = error_rate
            p.last_health_check = datetime.now(timezone.utc)
