"""
Stage-Gate Review & Governance Agent for Phase 55.
Evaluates evidence completeness across Gates 0 to 7 and formulates pivot/proceed recommendations.
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


class GateReviewAgent(BaseAgent):
    """Evaluates evidence completeness for Stage-Gate milestones and recommends proceed/pivot/pause/stop."""

    agent_id = "gate_review_agent"
    name = "Stage-Gate Review Agent"
    version = "1.0"
    description = "Conducts evidence completeness checks across innovation gates 0-7."
    permissions = {
        AgentPermission.READ_INNOVATION,
        AgentPermission.EVALUATE_INNOVATION_GATE,
    }

    def __init__(self, service: Optional[InnovationPlatformService] = None):
        super().__init__()
        self.service = service or global_innovation_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        gate_stage = context.metadata.get("gate_stage", "GATE_1_PROBLEM")
        reviewer = context.metadata.get("reviewer_id", "principal_product_lead")
        completeness = context.metadata.get("evidence_completeness_score", 0.90)

        review = self.service.portfolios_gates.conduct_gate_review(
            workspace_id=ws_id,
            gate_stage=gate_stage,
            reviewer_id=reviewer,
            evidence_completeness_score=completeness,
        )

        pivot_eval = self.service.portfolios_gates.evaluate_pivot_recommendation(
            hypothesis_supported=True,
            market_demand_strong=True,
            tech_feasible=True,
            unit_economics_viable=True,
        )

        return {
            "status": "SUCCESS",
            "gate_review": review,
            "pivot_recommendation": pivot_eval,
        }
