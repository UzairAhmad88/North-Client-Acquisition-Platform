"""Customer Expectation Gap Analysis Agent for Phase 57."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.customer_experience.service import CustomerExperiencePlatformService
except ImportError:
    from app.services.customer_experience.service import CustomerExperiencePlatformService

logger = logging.getLogger(__name__)


class ExpectationGapAgent(BaseAgent):
    """Compares PROMISED vs EXPECTED vs DELIVERED vs EXPERIENCED capabilities."""

    agent_id = "expectation_gap_agent"
    name = "Expectation Gap Analysis Agent"
    version = "1.0"
    description = "Surfaces alignment gaps between contractual commitments, customer expectations, and delivered reality."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
        AgentPermission.ANALYZE_EXPECTATION_GAPS,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        customer_id = context.metadata.get("customer_id")
        area = context.metadata.get("area", "SLA Delivery")
        promised = context.metadata.get("promised_capability", "99.9% uptime SLA")
        expected = context.metadata.get("customer_expected", "Zero disruption during trading hours")
        delivered = context.metadata.get("delivered_reality", "99.95% verified uptime")
        severity = context.metadata.get("gap_severity", "low")

        if not customer_id:
            return {"status": "FAILED", "error": "customer_id is required"}

        gap = self.service.voc_expectations.record_expectation_gap(
            customer_id=customer_id,
            area=area,
            promised_capability=promised,
            customer_expected=expected,
            delivered_reality=delivered,
            gap_severity=severity,
        )

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "expectation_gap": gap,
        }
