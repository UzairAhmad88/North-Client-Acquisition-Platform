"""Customer Journey Analysis & Reconstruction Agent for Phase 57."""
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


class JourneyAnalysisAgent(BaseAgent):
    """Analyzes customer journey execution, reconstructs touchpoint sequences, and identifies path variants."""

    agent_id = "journey_analysis_agent"
    name = "Journey Analysis & Reconstruction Agent"
    version = "1.0"
    description = "Reconstructs customer journey touchpoints and evaluates path velocity and variant performance."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.RECONSTRUCT_CUSTOMER_JOURNEY,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        journey_id = context.metadata.get("journey_id")
        customer_id = context.metadata.get("customer_id")

        if not journey_id and not customer_id:
            return {"status": "FAILED", "error": "journey_id or customer_id is required"}

        if not journey_id and customer_id:
            journeys = self.service.journeys.list_journeys(customer_id=customer_id)
            if not journeys:
                return {"status": "FAILED", "error": f"No journeys found for customer {customer_id}"}
            journey_id = journeys[0]["id"]

        reconstruction = self.service.reconstruction.reconstruct_journey_path(journey_id=journey_id)
        variants = self.service.reconstruction.discover_variants()

        return {
            "status": "SUCCESS",
            "journey_id": journey_id,
            "reconstructed_path": reconstruction,
            "discovered_variants": variants,
        }
