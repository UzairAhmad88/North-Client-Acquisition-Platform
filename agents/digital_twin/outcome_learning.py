"""
Outcome Learning Agent (Phase 50).
Compares simulated predictions with actual observed outcomes to generate model calibration reports.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.digital_twin.service import DigitalTwinPlatformService
except ImportError:
    from app.services.digital_twin.service import DigitalTwinPlatformService


class OutcomeLearningAgent(BaseAgent):
    """
    Agent for continuous model calibration and error variance tracking.
    Prohibited from silently modifying production models without governance review.
    """

    agent_id = "outcome_learning_agent"
    name = "Outcome Learning Agent"
    version = "1.0"
    description = "Tracks historical forecast variances and generates parameter calibration proposals."

    def __init__(self, service: Optional[DigitalTwinPlatformService] = None):
        super().__init__()
        self.service = service or DigitalTwinPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.RECORD_TWIN_OUTCOME,
            AgentPermission.GENERATE_CALIBRATION_REPORT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        observed_period = str(params.get("observed_period") or "2026-Q1")
        pred_metrics = params.get("predicted_metrics") or {"cumulative_revenue_usd": 150000.0}
        act_metrics = params.get("actual_metrics") or {"cumulative_revenue_usd": 162000.0}

        outcome_rec = self.service.track_outcome(
            observed_period=observed_period,
            predicted_metrics=pred_metrics,
            actual_metrics=act_metrics,
        )

        calibration_report = self.service.calibrate_twin_models([outcome_rec])

        return {
            "status": "SUCCESS",
            "observed_period": observed_period,
            "variance_percentage": outcome_rec.variance_percentage,
            "model_error": outcome_rec.model_error,
            "calibration_report": calibration_report.model_dump() if hasattr(calibration_report, "model_dump") else calibration_report.dict(),
        }
