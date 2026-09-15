"""Profitability analysis, project cost tracking, margin variance, and cash flow forecasting.
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.finance.calculator import FinancialCalculator


class ProfitabilityManager:
    """Calculates project margins, cost rollups (labor, AI, infrastructure), and commercial health."""

    @classmethod
    def analyze_project_profitability(
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
        """Performs comprehensive profitability, cost breakdown, and health diagnosis for a project."""
        direct_labor_cost = FinancialCalculator.round_currency(labor_hours_logged * labor_hourly_cost_rate)
        actual_total_cost = direct_labor_cost + ai_token_cost + infrastructure_cost + subcontractor_cost + other_expenses
        actual_total_cost = FinancialCalculator.round_currency(actual_total_cost)

        # Estimated Gross Margin (Contracted vs Estimated Cost)
        est_gross_profit = contracted_revenue - estimated_cost
        est_margin_pct = FinancialCalculator.calculate_margin_pct(est_gross_profit, contracted_revenue)

        # Invoiced Gross Margin (Invoiced vs Actual Cost)
        invoiced_gross_profit = invoiced_revenue - actual_total_cost
        invoiced_margin_pct = FinancialCalculator.calculate_margin_pct(invoiced_gross_profit, invoiced_revenue)

        # Realized/Collected Gross Margin (Collected vs Actual Cost)
        realized_gross_profit = collected_revenue - actual_total_cost
        realized_margin_pct = FinancialCalculator.calculate_margin_pct(realized_gross_profit, collected_revenue)

        # Cost Variance (Actual Cost - Estimated Cost)
        cost_variance = actual_total_cost - estimated_cost
        cost_variance_pct = FinancialCalculator.calculate_variance_pct(actual_total_cost, estimated_cost)

        # Health status determination
        if collected_revenue > Decimal("0.00") and realized_gross_profit < Decimal("0.00"):
            health_status = "loss_making"
            health_badge = "CRITICAL"
        elif cost_variance_pct > Decimal("15.00") or invoiced_margin_pct < Decimal("20.00"):
            health_status = "at_risk"
            health_badge = "WARNING"
        elif invoiced_margin_pct >= Decimal("40.00"):
            health_status = "highly_profitable"
            health_badge = "EXCELLENT"
        else:
            health_status = "profitable"
            health_badge = "HEALTHY"

        return {
            "project_id": project_id,
            "financial_summary": {
                "contracted_revenue": str(contracted_revenue),
                "invoiced_revenue": str(invoiced_revenue),
                "collected_revenue": str(collected_revenue),
                "unbilled_contract_balance": str(contracted_revenue - invoiced_revenue),
                "outstanding_receivables": str(invoiced_revenue - collected_revenue),
            },
            "cost_breakdown": {
                "estimated_cost": str(estimated_cost),
                "actual_total_cost": str(actual_total_cost),
                "labor_hours_logged": str(labor_hours_logged),
                "direct_labor_cost": str(direct_labor_cost),
                "ai_token_cost": str(ai_token_cost),
                "infrastructure_cost": str(infrastructure_cost),
                "subcontractor_cost": str(subcontractor_cost),
                "other_expenses": str(other_expenses),
                "cost_variance_amount": str(cost_variance),
                "cost_variance_pct": str(cost_variance_pct),
            },
            "profitability_metrics": {
                "estimated_gross_profit": str(est_gross_profit),
                "estimated_margin_pct": str(est_margin_pct),
                "invoiced_gross_profit": str(invoiced_gross_profit),
                "invoiced_margin_pct": str(invoiced_margin_pct),
                "realized_gross_profit": str(realized_gross_profit),
                "realized_margin_pct": str(realized_margin_pct),
            },
            "commercial_health": {
                "status": health_status,
                "badge": health_badge,
                "is_cost_overrun": cost_variance > Decimal("0.00"),
                "is_margin_compressed": invoiced_margin_pct < est_margin_pct,
            },
            "calculated_at": datetime.now(timezone.utc).isoformat(),
        }

    @classmethod
    def forecast_cash_flow(
        cls,
        active_schedules: List[Dict[str, Any]],
        outstanding_invoices: List[Dict[str, Any]],
        projected_monthly_burn: Decimal,
        months_ahead: int = 3,
    ) -> Dict[str, Any]:
        """Generates cash flow projections combining expected milestone billing, recurring retainers, and receivables."""
        # Total immediate receivables (uncollected invoices)
        immediate_receivables = sum(
            (Decimal(str(inv.get("balance_due", "0.00"))) for inv in outstanding_invoices),
            Decimal("0.00")
        )

        # Expected recurring / milestone revenue over projection period
        scheduled_inflow = sum(
            (Decimal(str(item.get("amount", "0.00"))) for item in active_schedules),
            Decimal("0.00")
        )

        total_projected_inflow = immediate_receivables + scheduled_inflow
        total_projected_burn = projected_monthly_burn * Decimal(str(months_ahead))
        net_cash_flow = total_projected_inflow - total_projected_burn

        return {
            "months_ahead": months_ahead,
            "projected_inflows": {
                "outstanding_receivables": str(FinancialCalculator.round_currency(immediate_receivables)),
                "scheduled_billings": str(FinancialCalculator.round_currency(scheduled_inflow)),
                "total_expected_inflow": str(FinancialCalculator.round_currency(total_projected_inflow)),
            },
            "projected_outflows": {
                "monthly_burn_rate": str(FinancialCalculator.round_currency(projected_monthly_burn)),
                "total_expected_burn": str(FinancialCalculator.round_currency(total_projected_burn)),
            },
            "net_projected_cash_flow": str(FinancialCalculator.round_currency(net_cash_flow)),
            "runway_indicator": "positive" if net_cash_flow >= Decimal("0.00") else "deficit",
            "calculated_at": datetime.now(timezone.utc).isoformat(),
        }
