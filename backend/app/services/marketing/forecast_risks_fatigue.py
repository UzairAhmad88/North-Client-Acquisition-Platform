"""
Phase 59: Probabilistic Demand Forecasting (P10-P90), Marketing Risks, and Audience Fatigue Monitoring
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, RiskSeverity, FatigueLevel, generate_id


class ForecastRisksFatigueService:
    """Manages probabilistic marketing demand forecasting, marketing risks, and audience fatigue monitoring."""

    def __init__(self):
        self._forecasts: Dict[str, AttrDict] = {}
        self._risks: Dict[str, AttrDict] = {}
        self._fatigue_records: Dict[str, AttrDict] = {}

    def generate_demand_forecast(
        self,
        period: str = "2026-Q4",
        scenario: str = "BASE",
        baseline_leads: int = 1500,
        pipeline_multiplier_usd: float = 450.0,
    ) -> AttrDict:
        """Generates probabilistic distribution (P10, P25, P50, P75, P90) for marketing demand."""
        if scenario == "CONSERVATIVE":
            p10 = int(baseline_leads * 0.70)
            p25 = int(baseline_leads * 0.80)
            p50 = int(baseline_leads * 0.90)
            p75 = int(baseline_leads * 1.00)
            p90 = int(baseline_leads * 1.10)
        elif scenario == "OPTIMISTIC":
            p10 = int(baseline_leads * 0.95)
            p25 = int(baseline_leads * 1.10)
            p50 = int(baseline_leads * 1.25)
            p75 = int(baseline_leads * 1.40)
            p90 = int(baseline_leads * 1.60)
        elif scenario == "STRESS":
            p10 = int(baseline_leads * 0.45)
            p25 = int(baseline_leads * 0.55)
            p50 = int(baseline_leads * 0.65)
            p75 = int(baseline_leads * 0.75)
            p90 = int(baseline_leads * 0.85)
        else:  # BASE
            p10 = int(baseline_leads * 0.80)
            p25 = int(baseline_leads * 0.90)
            p50 = int(baseline_leads * 1.05)
            p75 = int(baseline_leads * 1.20)
            p90 = int(baseline_leads * 1.35)

        p50_pipe = round(p50 * pipeline_multiplier_usd, 2)
        p50_rev = round(p50_pipe * 0.28, 2)

        fc_id = generate_id("mfc")
        forecast = AttrDict({
            "id": fc_id,
            "period": period,
            "scenario": scenario,
            "p10_leads": p10,
            "p25_leads": p25,
            "p50_leads": p50,
            "p75_leads": p75,
            "p90_leads": p90,
            "p50_pipeline_usd": p50_pipe,
            "p50_revenue_usd": p50_rev,
            "model_version": "v1.0-monte-carlo",
            "created_at": datetime.utcnow().isoformat(),
        })
        self._forecasts[f"{period}_{scenario}"] = forecast
        return forecast

    def get_forecast(self, period: str = "2026-Q4", scenario: str = "BASE") -> AttrDict:
        key = f"{period}_{scenario}"
        if key not in self._forecasts:
            return self.generate_demand_forecast(period=period, scenario=scenario)
        return self._forecasts[key]

    def list_forecasts(self) -> List[AttrDict]:
        if not self._forecasts:
            self.generate_demand_forecast(period="2026-Q4", scenario="BASE")
            self.generate_demand_forecast(period="2026-Q4", scenario="CONSERVATIVE")
            self.generate_demand_forecast(period="2026-Q4", scenario="OPTIMISTIC")
        return list(self._forecasts.values())

    def record_risk(
        self,
        risk_category: str,
        description: str,
        severity: str = RiskSeverity.MEDIUM.value,
        mitigation_strategy: str = "Rebalance channel allocation and expand content production.",
    ) -> AttrDict:
        r_id = generate_id("mrk")
        risk = AttrDict({
            "id": r_id,
            "risk_category": risk_category,
            "description": description,
            "severity": severity,
            "mitigation_strategy": mitigation_strategy,
            "status": "OPEN",
            "created_at": datetime.utcnow().isoformat(),
        })
        self._risks[r_id] = risk
        return risk

    def list_risks(self) -> List[AttrDict]:
        if not self._risks:
            self.record_risk(
                risk_category="Channel Dependency",
                description="Over 45% of qualified pipeline currently originates from a single paid social channel.",
                severity=RiskSeverity.HIGH.value,
                mitigation_strategy="Diversify spend into organic search content assets and webinar partner co-marketing.",
            )
            self.record_risk(
                risk_category="Content Freshness",
                description="3 foundational whitepapers contain 2024 industry statistics that require scheduled refreshment.",
                severity=RiskSeverity.LOW.value,
                mitigation_strategy="Trigger Content Refactor brief targeting updated Q3 2026 benchmarks.",
            )
        return list(self._risks.values())

    def monitor_audience_fatigue(
        self,
        audience_id: Optional[str] = None,
        channel: str = "EMAIL",
        weekly_frequency: float = 2.4,
        unsubscribe_rate_pct: float = 0.35,
        engagement_decay_pct: float = 6.2,
    ) -> AttrDict:
        fatigue_level = FatigueLevel.NORMAL.value
        if weekly_frequency > 4.0 or unsubscribe_rate_pct > 1.0 or engagement_decay_pct > 20.0:
            fatigue_level = FatigueLevel.CRITICAL.value
        elif weekly_frequency > 3.0 or unsubscribe_rate_pct > 0.5 or engagement_decay_pct > 10.0:
            fatigue_level = FatigueLevel.ELEVATED.value

        rec_id = generate_id("fat")
        rec = AttrDict({
            "id": rec_id,
            "audience_id": audience_id,
            "channel": channel,
            "weekly_frequency": weekly_frequency,
            "unsubscribe_rate_pct": unsubscribe_rate_pct,
            "engagement_decay_pct": engagement_decay_pct,
            "fatigue_level": fatigue_level,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._fatigue_records[f"{audience_id}_{channel}"] = rec
        return rec

    def list_fatigue_records(self) -> List[AttrDict]:
        if not self._fatigue_records:
            self.monitor_audience_fatigue(channel="EMAIL", weekly_frequency=1.8, unsubscribe_rate_pct=0.18, engagement_decay_pct=3.5)
            self.monitor_audience_fatigue(channel="LINKEDIN_OUTREACH", weekly_frequency=3.2, unsubscribe_rate_pct=0.65, engagement_decay_pct=11.0)
        return list(self._fatigue_records.values())
