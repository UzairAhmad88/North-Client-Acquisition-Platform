"""Pricing Intelligence & Discount Governance Agent for Phase 58."""
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


class PricingAgent(BaseAgent):
    """Analyzes packaging tiers, evaluates gross margin impacts, and audits discount governance requests."""

    agent_id = "pricing_agent"
    name = "Pricing & Discount Governance Agent"
    version = "1.0"
    description = "Evaluates pricing tiers and verifies discount requests against margin thresholds and governance rules."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.EVALUATE_PRICING_INTELLIGENCE,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        opportunity_id = context.metadata.get("opportunity_id", "opp-demo-001")
        discount_pct = context.metadata.get("requested_discount_pct", 10.0)
        original_price = context.metadata.get("original_price_usd", 150000.0)
        justification = context.metadata.get("justification", "Multi-year commitment discount")

        discount_req = self.service.pricing.request_discount(
            opportunity_id=opportunity_id,
            requested_discount_pct=discount_pct,
            original_price_usd=original_price,
            justification=justification,
        )

        return {
            "status": "SUCCESS",
            "discount_request_id": discount_req["id"],
            "proposed_price_usd": discount_req["proposed_price_usd"],
            "margin_impact_pct": discount_req["margin_impact_pct"],
            "governance_status": discount_req["status"],
        }
