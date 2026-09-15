"""Customer Experience Health Agent for Phase 57."""
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


class ExperienceHealthAgent(BaseAgent):
    """Calculates multi-factor customer experience health indices and evaluates lifecycle risks."""

    agent_id = "experience_health_agent"
    name = "Customer Experience Health Agent"
    version = "1.0"
    description = "Evaluates composite experience health across engagement, adoption, support, effort, and sentiment."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.EVALUATE_EXPERIENCE_HEALTH,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        customer_id = context.metadata.get("customer_id")
        if not customer_id:
            return {"status": "FAILED", "error": "customer_id is required"}

        engagement = context.metadata.get("engagement_score", 85.0)
        adoption = context.metadata.get("adoption_score", 88.0)
        support = context.metadata.get("support_score", 92.0)
        effort = context.metadata.get("effort_score", 80.0)
        sentiment = context.metadata.get("sentiment_score", 85.0)

        health = self.service.goals_health_churn.evaluate_health(
            customer_id=customer_id,
            engagement_score=engagement,
            adoption_score=adoption,
            support_score=support,
            effort_score=effort,
            sentiment_score=sentiment,
        )

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "overall_health_score": health["overall_health_score"],
            "health_state": health["health_state"],
            "health_breakdown": health,
        }
