"""Profitability evaluation and cost intelligence assistant for Finance Agent.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.finance.profitability import ProfitabilityManager


class FinancialProfitabilityAssistant:
    """Evaluates project margins, cost overruns, and financial risk indicators."""

    @classmethod
    def evaluate_project_health(
        cls,
        project_id: str,
        contracted_revenue: Decimal,
        invoiced_revenue: Decimal,
        collected_revenue: Decimal,
        estimated_cost: Decimal,
        labor_hours_logged: Decimal = Decimal("0.00"),
        labor_hourly_cost_rate: Decimal = Decimal("0.00"),
        ai_token_cost: Decimal = Decimal("0.00"),
        infrastructure_cost: Decimal = Decimal("0.00"),
        subcontractor_cost: Decimal = Decimal("0.00"),
        other_expenses: Decimal = Decimal("0.00"),
    ) -> Dict[str, Any]:
        """Calculates commercial health and generates actionable advisory warnings."""
        analysis = ProfitabilityManager.analyze_project_profitability(
            project_id=project_id,
            contracted_revenue=contracted_revenue,
            invoiced_revenue=invoiced_revenue,
            collected_revenue=collected_revenue,
            estimated_cost=estimated_cost,
            labor_hours_logged=labor_hours_logged,
            labor_hourly_cost_rate=labor_hourly_cost_rate,
            ai_token_cost=ai_token_cost,
            infrastructure_cost=infrastructure_cost,
            subcontractor_cost=subcontractor_cost,
            other_expenses=other_expenses,
        )

        insights = []
        if analysis["commercial_health"]["is_cost_overrun"]:
            insights.append(
                f"Project {project_id} has exceeded estimated costs by "
                f"{analysis['cost_breakdown']['cost_variance_amount']} "
                f"({analysis['cost_breakdown']['cost_variance_pct']}% overrun)."
            )

        if analysis["commercial_health"]["status"] in ("at_risk", "loss_making"):
            insights.append(
                f"Commercial warning: Margin health is {analysis['commercial_health']['status'].upper()} "
                f"(Realized margin: {analysis['profitability_metrics']['realized_margin_pct']}%)."
            )

        analysis["agent_insights"] = insights
        return analysis

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "completed"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
