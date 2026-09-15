"""Customer Friction & Effort Analysis Agent for Phase 57."""
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


class FrictionAnalysisAgent(BaseAgent):
    """Evaluates friction points, measures Customer Effort Score (CES), and surfaces root cause candidates."""

    agent_id = "friction_analysis_agent"
    name = "Friction & Effort Analysis Agent"
    version = "1.0"
    description = "Detects bottlenecks, scores customer effort, and performs deterministic friction triage."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.ANALYZE_CUSTOMER_FRICTION,
        AgentPermission.CALCULATE_CUSTOMER_EFFORT,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        customer_id = context.metadata.get("customer_id")
        stage = context.metadata.get("stage", "onboarding")
        description = context.metadata.get("description", "High friction detected in verification")
        friction_type = context.metadata.get("friction_type", "repeated_data_entry")

        if not customer_id:
            return {"status": "FAILED", "error": "customer_id is required"}

        friction = self.service.friction_effort_sentiment.record_friction(
            customer_id=customer_id,
            stage=stage,
            friction_type=friction_type,
            description=description,
        )

        effort = self.service.friction_effort_sentiment.calculate_effort(
            customer_id=customer_id,
            stage=stage,
            step_count=context.metadata.get("step_count", 3),
            form_count=context.metadata.get("form_count", 1),
            repeated_info_instances=context.metadata.get("repeated_info_instances", 1),
        )

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "friction_recorded": friction,
            "effort_evaluation": effort,
        }
