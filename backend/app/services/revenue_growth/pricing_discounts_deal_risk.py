"""Pricing Intelligence, Discount Governance, Negotiation Assistant, Deal Risk, Next-Best-Action, and Lead Routing."""
from typing import Any, Dict, List, Optional
from backend.app.services.revenue_growth.base import (
    AttrDict,
    DealRiskSeverity,
    DiscountStatus,
    generate_rev_id,
    current_utc_time,
)


class PricingDiscountsDealRiskService:
    """Manages pricing tiers, discount approval workflows, negotiation insights, deal risks, and next-best actions."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_pricing: List[Dict[str, Any]] = []
        self._in_memory_discounts: List[Dict[str, Any]] = []
        self._in_memory_deal_risks: List[Dict[str, Any]] = []
        self._in_memory_next_actions: List[Dict[str, Any]] = []
        self._in_memory_routing_rules: List[Dict[str, Any]] = []

    def set_pricing_tier(
        self,
        product_or_service: str,
        tier_name: str,
        list_price_usd: float,
        billing_frequency: str = "annual",
        average_discount_pct: float = 10.0,
        target_gross_margin_pct: float = 78.0,
        willingness_to_pay_evidence: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        prc_id = generate_rev_id("prc")
        now = current_utc_time().isoformat()
        pricing = AttrDict({
            "id": prc_id,
            "product_or_service": product_or_service,
            "tier_name": tier_name,
            "list_price_usd": list_price_usd,
            "billing_frequency": billing_frequency.lower(),
            "average_discount_pct": average_discount_pct,
            "target_gross_margin_pct": target_gross_margin_pct,
            "willingness_to_pay_evidence": willingness_to_pay_evidence or {"survey_wtp_median": list_price_usd * 1.1},
            "created_at": now,
        })
        self._in_memory_pricing.append(pricing)
        return pricing

    def list_pricing_tiers(self) -> List[AttrDict]:
        return list(self._in_memory_pricing)

    def request_discount(
        self,
        opportunity_id: str,
        requested_discount_pct: float,
        original_price_usd: float,
        justification: str,
    ) -> AttrDict:
        """Submits a discount request requiring formal governance approval."""
        proposed_price = round(original_price_usd * (1.0 - (requested_discount_pct / 100.0)), 2)
        margin_impact = round(requested_discount_pct * 1.25, 2)
        
        dsc_id = generate_rev_id("dsc")
        now = current_utc_time().isoformat()
        discount = AttrDict({
            "id": dsc_id,
            "opportunity_id": opportunity_id,
            "requested_discount_pct": requested_discount_pct,
            "original_price_usd": original_price_usd,
            "proposed_price_usd": proposed_price,
            "margin_impact_pct": margin_impact,
            "justification": justification,
            "status": DiscountStatus.PENDING_APPROVAL.value,
            "approver_name": None,
            "approval_notes": None,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_discounts.append(discount)
        return discount

    def approve_discount(
        self,
        discount_id: str,
        approver_name: str,
        approval_notes: Optional[str] = None,
    ) -> Optional[AttrDict]:
        for d in self._in_memory_discounts:
            if d["id"] == discount_id:
                d["status"] = DiscountStatus.APPROVED.value
                d["approver_name"] = approver_name
                d["approval_notes"] = approval_notes or "Approved in alignment with multi-year commitment guidelines"
                d["updated_at"] = current_utc_time().isoformat()
                return d
        return None

    def list_discount_requests(self, opportunity_id: Optional[str] = None) -> List[AttrDict]:
        if opportunity_id:
            return [d for d in self._in_memory_discounts if d.get("opportunity_id") == opportunity_id]
        return list(self._in_memory_discounts)

    def get_negotiation_insights(self, opportunity_id: str) -> AttrDict:
        """Provides commercial negotiation strategies and objection-handling guidance."""
        now = current_utc_time().isoformat()
        return AttrDict({
            "opportunity_id": opportunity_id,
            "detected_objections": ["Price sensitivity regarding seat add-ons", "Vendor security review cycle"],
            "suggested_trade_offs": [
                "Offer 2-year commitment in exchange for 12% pricing lock",
                "Include dedicated Phase 47 GRC certification fast-track",
            ],
            "walk_away_price_usd": 68000.0,
            "recommended_target_price_usd": 85000.0,
            "analyzed_at": now,
        })

    def record_deal_risk(
        self,
        opportunity_id: str,
        risk_category: str = "decision_maker",
        severity: str = DealRiskSeverity.MEDIUM.value,
        description: str = "Key champion transitioned to new role",
        mitigation_strategy: Optional[str] = "Engage newly appointed VP of Engineering with technical executive briefing",
    ) -> AttrDict:
        drsk_id = generate_rev_id("drsk")
        now = current_utc_time().isoformat()
        risk = AttrDict({
            "id": drsk_id,
            "opportunity_id": opportunity_id,
            "risk_category": risk_category.lower(),
            "severity": severity.lower(),
            "description": description,
            "mitigation_strategy": mitigation_strategy,
            "status": "open",
            "created_at": now,
        })
        self._in_memory_deal_risks.append(risk)
        return risk

    def list_deal_risks(self, opportunity_id: Optional[str] = None) -> List[AttrDict]:
        if opportunity_id:
            return [r for r in self._in_memory_deal_risks if r.get("opportunity_id") == opportunity_id]
        return list(self._in_memory_deal_risks)

    def recommend_next_best_action(
        self,
        opportunity_id: str,
        recommended_action: str,
        action_type: str = "schedule_technical_deep_dive",
        rationale: str = "Customer requested live demo of Phase 52 Autonomous Workforce delegation",
        confidence: float = 0.91,
    ) -> AttrDict:
        nba_id = generate_rev_id("nba")
        now = current_utc_time().isoformat()
        action = AttrDict({
            "id": nba_id,
            "opportunity_id": opportunity_id,
            "recommended_action": recommended_action,
            "action_type": action_type.lower(),
            "rationale": rationale,
            "evidence_signals": ["Meeting notes from discovery call", "Telemetry showing high portal documentation view count"],
            "confidence": confidence,
            "status": "recommended",
            "created_at": now,
        })
        self._in_memory_next_actions.append(action)
        return action

    def list_next_best_actions(self, opportunity_id: Optional[str] = None) -> List[AttrDict]:
        if opportunity_id:
            return [a for a in self._in_memory_next_actions if a.get("opportunity_id") == opportunity_id]
        return list(self._in_memory_next_actions)

    def create_routing_rule(
        self,
        rule_name: str,
        criteria: Dict[str, Any],
        target_rep_or_team: str = "Enterprise Strategic Team",
        priority_order: int = 1,
    ) -> AttrDict:
        rule_id = generate_rev_id("rule")
        now = current_utc_time().isoformat()
        rule = AttrDict({
            "id": rule_id,
            "rule_name": rule_name,
            "criteria": criteria,
            "target_rep_or_team": target_rep_or_team,
            "priority_order": priority_order,
            "is_active": True,
            "created_at": now,
        })
        self._in_memory_routing_rules.append(rule)
        return rule

    def list_routing_rules(self) -> List[AttrDict]:
        return list(self._in_memory_routing_rules)
