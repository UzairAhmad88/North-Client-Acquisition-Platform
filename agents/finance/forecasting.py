"""Financial forecasting and cash flow projection assistant for Finance Agent.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.finance.calculator import FinancialCalculator
from app.finance.profitability import ProfitabilityManager


class FinancialForecastingEngine:
    """Provides draft cash flow forecasts, revenue projections, and burn analysis."""

    @classmethod
    def generate_cash_flow_forecast(
        cls,
        active_schedules: List[Dict[str, Any]],
        outstanding_invoices: List[Dict[str, Any]],
        projected_monthly_burn: Decimal,
        months_ahead: int = 3,
    ) -> Dict[str, Any]:
        """Generates a cash flow forecast projection draft."""
        return ProfitabilityManager.forecast_cash_flow(
            active_schedules=active_schedules,
            outstanding_invoices=outstanding_invoices,
            projected_monthly_burn=projected_monthly_burn,
            months_ahead=months_ahead,
        )

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "completed"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
