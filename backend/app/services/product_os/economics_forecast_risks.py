"""Economics, Probabilistic Forecasting, Digital Twin Simulations, and Risk Register Service.

Evaluates product unit economics, computes P10-P90 probabilistic forecasts,
simulates digital twin resource/schedule scenarios, and maintains the comprehensive product risk register.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        RiskSeverity,
    )
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        generate_product_id,
        RiskSeverity,
    )


logger = logging.getLogger(__name__)


class EconomicsForecastRisksService:
    """Manages unit economics, probabilistic forecasting, digital twin simulations, and risk register."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._unit_economics: Dict[str, Dict[str, Any]] = {}
        self._forecasts: Dict[str, Dict[str, Any]] = {}
        self._risks: Dict[str, Dict[str, Any]] = {}

    def calculate_unit_economics(
        self,
        tenant_id: str,
        product_id: str,
        active_customers: int,
        mrr_usd: float,
        infrastructure_cost_usd: float,
        support_cost_usd: float,
        r_and_d_allocated_usd: float,
        cac_usd: float,
        churn_rate_monthly: float,
    ) -> AttrDict:
        """Calculate product gross margins, LTV, CAC payback, and profit per customer."""
        eco_id = generate_product_id("eco")
        now = datetime.now(timezone.utc).isoformat()

        total_cogs = infrastructure_cost_usd + support_cost_usd
        gross_profit_usd = mrr_usd - total_cogs
        gross_margin_pct = (gross_profit_usd / max(1.0, mrr_usd)) * 100.0

        arpu_monthly = mrr_usd / max(1, active_customers)
        cost_per_customer = total_cogs / max(1, active_customers)

        # LTV = ARPU * Gross Margin / Churn Rate
        effective_churn = max(0.005, churn_rate_monthly)
        customer_lifetime_months = 1.0 / effective_churn
        ltv_usd = arpu_monthly * (gross_margin_pct / 100.0) * customer_lifetime_months

        # CAC Payback = CAC / (ARPU * Gross Margin)
        monthly_gp_per_user = arpu_monthly * (gross_margin_pct / 100.0)
        cac_payback_months = cac_usd / max(1.0, monthly_gp_per_user)
        ltv_to_cac_ratio = ltv_usd / max(1.0, cac_usd)

        record = {
            "economics_id": eco_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "active_customers": active_customers,
            "mrr_usd": round(mrr_usd, 2),
            "arr_usd": round(mrr_usd * 12.0, 2),
            "infrastructure_cost_usd": round(infrastructure_cost_usd, 2),
            "support_cost_usd": round(support_cost_usd, 2),
            "r_and_d_allocated_usd": round(r_and_d_allocated_usd, 2),
            "gross_profit_usd": round(gross_profit_usd, 2),
            "gross_margin_pct": round(gross_margin_pct, 2),
            "arpu_monthly": round(arpu_monthly, 2),
            "cost_per_customer": round(cost_per_customer, 2),
            "cac_usd": round(cac_usd, 2),
            "ltv_usd": round(ltv_usd, 2),
            "cac_payback_months": round(cac_payback_months, 2),
            "ltv_to_cac_ratio": round(ltv_to_cac_ratio, 2),
            "is_healthy_unit_economics": ltv_to_cac_ratio >= 3.0 and gross_margin_pct >= 70.0,
            "calculated_at": now,
        }
        self._unit_economics[eco_id] = record
        return AttrDict(record)

    def generate_probabilistic_forecast(
        self,
        tenant_id: str,
        product_id: str,
        metric_name: str,
        time_horizon_months: int = 12,
        baseline_value: float = 100000.0,
        growth_rate_base: float = 0.08,
    ) -> AttrDict:
        """Compute probabilistic forecast distribution across P10, P25, P50, P75, P90 percentiles."""
        fc_id = generate_product_id("fc")
        now = datetime.now(timezone.utc).isoformat()

        # Uncertainty expansion over time horizon
        p10 = baseline_value * ((1 + (growth_rate_base - 0.05)) ** time_horizon_months)
        p25 = baseline_value * ((1 + (growth_rate_base - 0.02)) ** time_horizon_months)
        p50 = baseline_value * ((1 + growth_rate_base) ** time_horizon_months)
        p75 = baseline_value * ((1 + (growth_rate_base + 0.03)) ** time_horizon_months)
        p90 = baseline_value * ((1 + (growth_rate_base + 0.07)) ** time_horizon_months)

        record = {
            "forecast_id": fc_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "metric_name": metric_name,
            "time_horizon_months": time_horizon_months,
            "baseline_value": baseline_value,
            "percentiles": {
                "p10_pessimistic": round(p10, 2),
                "p25_conservative": round(p25, 2),
                "p50_median": round(p50, 2),
                "p75_optimistic": round(p75, 2),
                "p90_high_growth": round(p90, 2),
            },
            "confidence_band_width_pct": round(((p90 - p10) / max(1.0, p50)) * 100.0, 2),
            "assumptions": [
                f"Historical monthly growth trend of {round(growth_rate_base * 100, 1)}%",
                "Zero catastrophic platform downtime incidents",
                "Competitive pricing parity maintained",
            ],
            "created_at": now,
        }
        self._forecasts[fc_id] = record
        return AttrDict(record)

    def log_product_risk(
        self,
        tenant_id: str,
        product_id: str,
        category: str,
        title: str,
        probability: float,
        impact_score: float,
        severity: str = RiskSeverity.HIGH.value,
        mitigation_strategy: str = "",
        owner: str = "product-lead@uzaii.com",
    ) -> AttrDict:
        """Add risk record to the governed product risk register."""
        risk_id = generate_product_id("rsk")
        now = datetime.now(timezone.utc).isoformat()

        exposure_score = round(probability * impact_score, 2)

        record = {
            "risk_id": risk_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "category": category,
            "title": title,
            "probability": probability,
            "impact_score": impact_score,
            "exposure_score": exposure_score,
            "severity": severity,
            "mitigation_strategy": mitigation_strategy,
            "owner": owner,
            "status": "OPEN",
            "created_at": now,
            "updated_at": now,
        }
        self._risks[risk_id] = record
        return AttrDict(record)

    def run_twin_scenario_simulation(
        self,
        tenant_id: str,
        product_id: str,
        scenario_type: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Simulate Digital Twin scenario: scope cut, capacity surge, or delay trade-off."""
        delay_weeks = parameters.get("delay_weeks", 0)
        added_engineers = parameters.get("added_engineers", 0)
        price_change_pct = parameters.get("price_change_pct", 0.0)

        revenue_impact = (price_change_pct * 12000.0) - (delay_weeks * 25000.0)
        delivery_acceleration_weeks = added_engineers * 1.5
        net_schedule_shift = delay_weeks - delivery_acceleration_weeks

        return {
            "scenario_id": generate_product_id("sim"),
            "tenant_id": tenant_id,
            "product_id": product_id,
            "scenario_type": scenario_type,
            "inputs": parameters,
            "simulated_outcomes": {
                "net_schedule_shift_weeks": round(net_schedule_shift, 1),
                "estimated_revenue_delta_usd": round(revenue_impact, 2),
                "risk_exposure_change_pct": round(delay_weeks * 4.5 - added_engineers * 2.0, 1),
                "capacity_utilization_pct": min(100.0, max(40.0, 85.0 - (added_engineers * 5.0))),
            },
            "recommendation": (
                "Slight scope reduction or team augmentation recommended to protect launch window."
                if net_schedule_shift > 2.0
                else "Scenario within acceptable variance thresholds."
            ),
        }
