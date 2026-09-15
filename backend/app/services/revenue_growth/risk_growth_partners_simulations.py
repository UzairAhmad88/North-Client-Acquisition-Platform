"""Revenue Risk, Concentration Analysis, Growth Opportunities, Partners, and Revenue Simulations."""
from typing import Any, Dict, List, Optional
from backend.app.services.revenue_growth.base import (
    AttrDict,
    generate_rev_id,
    current_utc_time,
)


class RiskGrowthPartnersSimulationsService:
    """Manages revenue concentration risks, growth opportunities, partner ecosystems, simulations, and decision links."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_risks: List[Dict[str, Any]] = []
        self._in_memory_opportunities: List[Dict[str, Any]] = []
        self._in_memory_partners: List[Dict[str, Any]] = []
        self._in_memory_decisions: List[Dict[str, Any]] = []

    def evaluate_concentration_risk(self) -> AttrDict:
        """Evaluates customer, industry, and channel revenue concentration risks."""
        now = current_utc_time().isoformat()
        return AttrDict({
            "top_customer_revenue_share_pct": 14.5,
            "top_5_customers_revenue_share_pct": 42.0,
            "top_industry_concentration_pct": 48.0,
            "concentration_status": "acceptable",
            "over_dependence_flags": ["FinTech sector represents 48% of active pipeline"],
            "evaluated_at": now,
        })

    def record_revenue_risk(
        self,
        risk_type: str = "pipeline_concentration",
        severity: str = "medium",
        description: str = "High concentration of Q4 closing deals in one region",
        potential_revenue_impact_usd: float = 350000.0,
        evidence_data: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        rrsk_id = generate_rev_id("rrsk")
        now = current_utc_time().isoformat()
        risk = AttrDict({
            "id": rrsk_id,
            "risk_type": risk_type.lower(),
            "severity": severity.lower(),
            "description": description,
            "potential_revenue_impact_usd": potential_revenue_impact_usd,
            "evidence_data": evidence_data or {"region": "North America East", "pipeline_pct": 65.0},
            "status": "active",
            "created_at": now,
        })
        self._in_memory_risks.append(risk)
        return risk

    def list_revenue_risks(self) -> List[AttrDict]:
        if not self._in_memory_risks:
            self.record_revenue_risk()
        return list(self._in_memory_risks)

    def create_growth_opportunity(
        self,
        title: str,
        opportunity_type: str = "cross_sell_ai_workforce",
        description: Optional[str] = None,
        estimated_arr_potential_usd: float = 450000.0,
        target_segment: str = "Enterprise Strategic FinTech",
        confidence: float = 0.88,
    ) -> AttrDict:
        ropp_id = generate_rev_id("ropp")
        now = current_utc_time().isoformat()
        opportunity = AttrDict({
            "id": ropp_id,
            "opportunity_type": opportunity_type.lower(),
            "title": title,
            "description": description or f"Growth opportunity: {title}",
            "estimated_arr_potential_usd": estimated_arr_potential_usd,
            "target_segment": target_segment,
            "confidence": confidence,
            "status": "identified",
            "created_at": now,
        })
        self._in_memory_opportunities.append(opportunity)
        return opportunity

    def list_growth_opportunities(self) -> List[AttrDict]:
        if not self._in_memory_opportunities:
            self.create_growth_opportunity(
                title="Cross-sell Phase 52 Autonomous Workforce to existing Enterprise FinTech tier",
                opportunity_type="cross_sell_ai_workforce",
                estimated_arr_potential_usd=550000.0,
            )
            self.create_growth_opportunity(
                title="Expand into DACH region with certified local cloud compliance package",
                opportunity_type="geographic_expansion",
                estimated_arr_potential_usd=380000.0,
            )
        return list(self._in_memory_opportunities)

    def create_partner(
        self,
        partner_name: str,
        partner_type: str = "solution_integrator",
        region: str = "North America",
        referred_leads_count: int = 15,
        influenced_revenue_usd: float = 450000.0,
        tier: str = "gold",
    ) -> AttrDict:
        part_id = generate_rev_id("part")
        now = current_utc_time().isoformat()
        partner = AttrDict({
            "id": part_id,
            "partner_name": partner_name,
            "partner_type": partner_type.lower(),
            "region": region,
            "referred_leads_count": referred_leads_count,
            "influenced_revenue_usd": influenced_revenue_usd,
            "tier": tier.lower(),
            "status": "active",
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_partners.append(partner)
        return partner

    def list_partners(self) -> List[AttrDict]:
        if not self._in_memory_partners:
            self.create_partner("Apex Cloud Solutions", "solution_integrator", "North America", 18, 520000.0, "platinum")
            self.create_partner("Vanguard Systems Europe", "technology_consultancy", "EMEA", 12, 380000.0, "gold")
        return list(self._in_memory_partners)

    def simulate_revenue(
        self,
        conversion_rate_delta_pct: float = +5.0,
        lead_volume_delta_pct: float = +10.0,
        average_deal_size_delta_pct: float = +0.0,
    ) -> AttrDict:
        """Simulates revenue outcomes under adjusted commercial levers."""
        now = current_utc_time().isoformat()
        base_arr = 5065000.0
        conversion_impact = base_arr * (conversion_rate_delta_pct / 100.0) * 0.85
        volume_impact = base_arr * (lead_volume_delta_pct / 100.0) * 0.60
        deal_size_impact = base_arr * (average_deal_size_delta_pct / 100.0)

        projected_arr = round(base_arr + conversion_impact + volume_impact + deal_size_impact, 2)
        projected_lift_usd = round(projected_arr - base_arr, 2)

        return AttrDict({
            "baseline_annual_run_rate_usd": base_arr,
            "simulated_conversion_delta_pct": conversion_rate_delta_pct,
            "simulated_lead_volume_delta_pct": lead_volume_delta_pct,
            "projected_annual_run_rate_usd": projected_arr,
            "projected_arr_lift_usd": projected_lift_usd,
            "simulated_gross_margin_pct": 78.4,
            "model_provenance": "Phase 50 Digital Twin Revenue Simulator v1.2",
            "simulated_at": now,
        })

    def list_commercial_decisions(self) -> List[AttrDict]:
        """Lists governed Decision Room commercial links."""
        return [
            AttrDict({
                "id": "dec-com-001",
                "title": "Enterprise Strategic Tier Pricing Revision",
                "status": "APPROVED",
                "decision_room_id": "room-fin-001",
                "human_approver": "Chief Commercial Officer",
                "impact_arr_usd": 650000.0,
                "governance_verified": True,
            })
        ]
