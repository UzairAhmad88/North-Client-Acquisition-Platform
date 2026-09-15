"""Customer Churn & Retention Intelligence Agent for Phase 57."""
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


class ChurnAnalysisAgent(BaseAgent):
    """Predicts customer churn probability and surfaces non-autonomous retention recommendations."""

    agent_id = "churn_analysis_agent"
    name = "Churn & Retention Intelligence Agent"
    version = "1.0"
    description = "Computes predictive churn risk based on usage signals, support escalations, and goal velocity."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.PREDICT_CHURN_RISK,
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

        churn_prob = context.metadata.get("churn_probability", 0.08)
        risk_level = context.metadata.get("risk_level", "low")

        prediction = self.service.goals_health_churn.predict_churn(
            customer_id=customer_id,
            churn_probability=churn_prob,
            risk_level=risk_level,
        )

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "churn_probability": prediction["churn_probability"],
            "risk_level": prediction["risk_level"],
            "prediction_details": prediction,
        }
