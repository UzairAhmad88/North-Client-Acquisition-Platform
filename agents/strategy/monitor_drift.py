"""
Strategic Drift & Monitoring Agent (Phase 51).
Monitors live operational metrics against planned strategic baselines to trigger early drift warnings.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService


class StrategyMonitorDriftAgent(BaseAgent):
    """
    Agent for detecting divergence between strategic plan assumptions and operational telemetry.
    Prohibited from unilaterally modifying strategic plans without human governance review.
    """

    agent_id = "strategy_monitor_drift_agent"
    name = "Strategy Monitor & Drift Agent"
    version = "1.0"
    description = "Monitors strategic execution and flags divergence or drift from planned targets."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
            AgentPermission.TRACK_STRATEGY_DRIFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        metric = str(params.get("metric_name") or "monthly_recurring_revenue_usd")
        expected = float(params.get("expected_value") or 180000.0)
        actual = float(params.get("actual_value") or 145000.0)

        drift_event = self.service.check_drift(metric_name=metric, expected_value=expected, actual_value=actual)

        return {
            "status": "SUCCESS",
            "metric_evaluated": metric,
            "has_drift": drift_event is not None,
            "drift_event": drift_event,
        }
