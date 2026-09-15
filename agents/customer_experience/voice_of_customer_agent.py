"""Voice of Customer (VoC) Analysis & Clustering Agent for Phase 57."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.customer_experience.service import CustomerExperiencePlatformService
except ImportError:
    from app.services.customer_experience.service import CustomerExperiencePlatformService

logger = logging.getLogger(__name__)


class VoiceOfCustomerAgent(BaseAgent):
    """Extracts customer feedback signals, maps topics, and aggregates VoC themes."""

    agent_id = "voice_of_customer_agent"
    name = "Voice of Customer (VoC) Agent"
    version = "1.0"
    description = "Ingests feedback, quotes, and unstructured exchanges into structured thematic VoC intelligence."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.CLUSTER_VOICE_OF_CUSTOMER,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        customer_id = context.metadata.get("customer_id")
        quote_text = context.metadata.get("quote_text", "The workflow automation has saved us countless hours.")
        source_channel = context.metadata.get("source_channel", "survey")
        feedback_category = context.metadata.get("feedback_category", "praise")
        sentiment = context.metadata.get("sentiment", "positive")

        if not customer_id:
            return {"status": "FAILED", "error": "customer_id is required"}

        record = self.service.voc_expectations.record_voice(
            customer_id=customer_id,
            source_channel=source_channel,
            quote_text=quote_text,
            feedback_category=feedback_category,
            sentiment=sentiment,
        )

        themes = self.service.voc_expectations.list_voice_themes()

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "recorded_feedback": record,
            "active_themes": themes,
        }
