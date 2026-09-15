"""Revenue Forecasting & Scenario Calibration Agent for Phase 58."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.revenue_growth.service import RevenueGrowthPlatformService
except ImportError:
    from app.services.revenue_growth.service import RevenueGrowthPlatformService

logger = logging.getLogger(__name__)


class ForecastAgent(BaseAgent):
    """Computes probabilistic revenue forecasts (P10..P90) and evaluates forecast scenario calibration."""

    agent_id = "forecast_agent"
    name = "Revenue Forecasting Agent"
    version = "1.0"
    description = "Generates calibrated P10 to P90 revenue projections across conservative, base, optimistic, and stress scenarios."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.GENERATE_REVENUE_FORECAST,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        period = context.metadata.get("forecast_period", "Q4-2026")
        scenario = context.metadata.get("scenario", "base")

        forecast = self.service.forecasting.generate_forecast(
            forecast_period=period,
            scenario=scenario,
        )

        return {
            "status": "SUCCESS",
            "forecast_period": period,
            "scenario": scenario,
            "p50_usd": forecast["p50_usd"],
            "p90_usd": forecast["p90_usd"],
            "p10_usd": forecast["p10_usd"],
            "forecast_details": forecast,
        }
