"""
Hypothesis Formation Agent for Phase 55.
Formulates testable innovation hypotheses and maps assumptions on the 2x2 impact vs uncertainty matrix.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )
except ImportError:
    from app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )

logger = logging.getLogger(__name__)


class HypothesisAgent(BaseAgent):
    """Structures testable hypotheses and prioritizes assumptions for empirical validation."""

    agent_id = "hypothesis_agent"
    name = "Hypothesis & Assumption Agent"
    version = "1.0"
    description = "Drafts falsifiable hypotheses and prioritizes high-impact/high-uncertainty assumptions."
    permissions = {
        AgentPermission.READ_INNOVATION,
    }

    def __init__(self, service: Optional[InnovationPlatformService] = None):
        super().__init__()
        self.service = service or global_innovation_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        idea_id = context.metadata.get("idea_id", "idea_default")
        statement = context.metadata.get("statement", "We believe that X will solve problem Y.")
        prediction = context.metadata.get("prediction", "We expect metric Z to improve by 20%.")
        metric = context.metadata.get("metric_name", "Conversion Rate")
        target = context.metadata.get("target_value", 0.25)

        hyp = self.service.hypotheses_assumptions.form_hypothesis(
            workspace_id=ws_id,
            idea_id=idea_id,
            statement=statement,
            prediction=prediction,
            metric_name=metric,
            target_value=target,
        )
        return {"status": "SUCCESS", "hypothesis": hyp}
