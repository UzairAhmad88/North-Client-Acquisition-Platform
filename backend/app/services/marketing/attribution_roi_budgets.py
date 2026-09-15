"""
Phase 59: Multi-Touch Marketing Attribution, ROI / Unit Economics, Budget Management, and Optimization Simulations
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, AttributionModelType, generate_id


class AttributionRoiBudgetsService:
    """Manages multi-touch marketing attribution models, ROI analytics, financial budget tracking, and optimization simulations."""

    def __init__(self):
        self._attributions: Dict[str, AttrDict] = {}
        self._roi_records: Dict[str, AttrDict] = {}
        self._budgets: Dict[str, AttrDict] = {}
        self._experiments: Dict[str, AttrDict] = {}

    def calculate_attribution(
        self,
        opportunity_id: str,
        deal_value_usd: float,
        touches: List[Dict[str, Any]],
        attribution_model: str = AttributionModelType.MULTI_TOUCH_W_SHAPED.value,
    ) -> AttrDict:
        if not touches:
            raise ValueError("Attribution requires at least one touchpoint")

        n = len(touches)
        campaign_credits: Dict[str, float] = {}
        channel_credits: Dict[str, float] = {}

        if attribution_model == AttributionModelType.FIRST_TOUCH.value:
            weights = [1.0] + [0.0] * (n - 1)
        elif attribution_model == AttributionModelType.LAST_TOUCH.value:
            weights = [0.0] * (n - 1) + [1.0]
        elif attribution_model == AttributionModelType.LINEAR.value:
            weights = [1.0 / n] * n
        elif attribution_model == AttributionModelType.MULTI_TOUCH_W_SHAPED.value:
            if n == 1:
                weights = [1.0]
            elif n == 2:
                weights = [0.5, 0.5]
            elif n == 3:
                weights = [0.30, 0.40, 0.30]
            else:
                # 30% first, 40% middle (distributed), 30% last
                mid_weight = 0.40 / (n - 2)
                weights = [0.30] + [mid_weight] * (n - 2) + [0.30]
        else:
            # Fallback linear
            weights = [1.0 / n] * n

        for i, touch in enumerate(touches):
            weight = weights[i]
            credit_usd = round(deal_value_usd * weight, 2)

            camp = touch.get("campaign_name", "Direct")
            chan = touch.get("channel", "DIRECT")

            campaign_credits[camp] = round(campaign_credits.get(camp, 0.0) + credit_usd, 2)
            channel_credits[chan] = round(channel_credits.get(chan, 0.0) + credit_usd, 2)

        attr_id = generate_id("att")
        record = AttrDict({
            "id": attr_id,
            "opportunity_id": opportunity_id,
            "deal_value_usd": deal_value_usd,
            "attribution_model": attribution_model,
            "touches": touches,
            "campaign_credits": campaign_credits,
            "channel_credits": channel_credits,
            "calculated_at": datetime.utcnow().isoformat(),
        })
        self._attributions[attr_id] = record
        return record

    def list_attributions(self) -> List[AttrDict]:
        return list(self._attributions.values())

    def calculate_marketing_roi(
        self,
        period: str = "2026-Q3",
        total_spend_usd: float = 120000.0,
        total_attributed_revenue_usd: float = 680000.0,
        leads_count: int = 1200,
        mql_count: int = 420,
        acquisitions_count: int = 38,
    ) -> AttrDict:
        cpl = round(total_spend_usd / max(1, leads_count), 2)
        cpql = round(total_spend_usd / max(1, mql_count), 2)
        cac = round(total_spend_usd / max(1, acquisitions_count), 2)
        roas = round(total_attributed_revenue_usd / max(1.0, total_spend_usd), 2)
        roi_pct = round(((total_attributed_revenue_usd - total_spend_usd) / max(1.0, total_spend_usd)) * 100.0, 2)

        roi_id = generate_id("roi")
        record = AttrDict({
            "id": roi_id,
            "period": period,
            "total_spend_usd": total_spend_usd,
            "total_attributed_revenue_usd": total_attributed_revenue_usd,
            "cost_per_lead_usd": cpl,
            "cost_per_mql_usd": cpql,
            "cost_per_acquisition_usd": cac,
            "roas": roas,
            "roi_pct": roi_pct,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._roi_records[period] = record
        return record

    def get_marketing_roi(self, period: str = "2026-Q3") -> Optional[AttrDict]:
        return self._roi_records.get(period) or self.calculate_marketing_roi(period=period)

    def create_budget(
        self,
        period: str = "2026-Q3",
        total_planned_budget_usd: float = 150000.0,
        channel_allocations: Optional[Dict[str, float]] = None,
    ) -> AttrDict:
        b_id = generate_id("bud")
        allocations = channel_allocations or {
            "ORGANIC_SEARCH": 25000.0,
            "CONTENT_MARKETING": 35000.0,
            "EMAIL_NURTURE": 20000.0,
            "LINKEDIN_ABM": 45000.0,
            "EVENTS_WEBINARS": 25000.0,
        }
        budget = AttrDict({
            "id": b_id,
            "period": period,
            "total_planned_budget_usd": total_planned_budget_usd,
            "total_committed_usd": 85000.0,
            "total_spent_usd": 62000.0,
            "channel_allocations": allocations,
            "is_locked": False,
            "approved_by": None,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._budgets[period] = budget
        return budget

    def get_budget(self, period: str = "2026-Q3") -> Optional[AttrDict]:
        return self._budgets.get(period) or self.create_budget(period=period)

    def simulate_budget_optimization(
        self,
        current_budget_usd: float = 150000.0,
        budget_shift_pct: float = 20.0,
        target_focus_channel: str = "LINKEDIN_ABM",
    ) -> Dict[str, Any]:
        """Digital twin simulation estimating downstream impact of shifting budget allocation."""
        expected_pipeline_gain = round(current_budget_usd * (budget_shift_pct / 100.0) * 4.2, 2)
        expected_revenue_gain = round(expected_pipeline_gain * 0.32, 2)
        cac_reduction_pct = 8.5

        return {
            "simulation_id": generate_id("sim"),
            "current_budget_usd": current_budget_usd,
            "budget_shift_pct": budget_shift_pct,
            "target_channel": target_focus_channel,
            "expected_additional_pipeline_usd": expected_pipeline_gain,
            "expected_additional_revenue_usd": expected_revenue_gain,
            "expected_cac_change_pct": -cac_reduction_pct,
            "confidence_pct": 86.5,
            "assumptions": [
                f"Assumes {target_focus_channel} conversion efficiency holds within +/-15%",
                "Sales team capacity accommodates 25% higher SQL intake",
                "Attribution model: Multi-Touch W-Shaped",
            ],
            "simulated_at": datetime.utcnow().isoformat(),
        }

    def create_experiment(
        self,
        name: str,
        experiment_type: str = "LANDING_PAGE_CTA",
        hypothesis: str = "Specific ROI proof point increases CTA conversions by >=15%",
        variants: Optional[List[Dict[str, Any]]] = None,
    ) -> AttrDict:
        exp_id = generate_id("exp")
        exp = AttrDict({
            "id": exp_id,
            "name": name,
            "experiment_type": experiment_type,
            "hypothesis": hypothesis,
            "variants": variants or [
                {"name": "Control", "traffic_split": 50, "conversions": 32, "visitors": 800, "cr_pct": 4.0},
                {"name": "Evidence Proof CTA", "traffic_split": 50, "conversions": 52, "visitors": 800, "cr_pct": 6.5},
            ],
            "sample_size": 1600,
            "confidence_level_pct": 95.0,
            "winner_variant": "Evidence Proof CTA",
            "status": "COMPLETED",
            "created_at": datetime.utcnow().isoformat(),
        })
        self._experiments[exp_id] = exp
        return exp

    def list_experiments(self) -> List[AttrDict]:
        return list(self._experiments.values())
