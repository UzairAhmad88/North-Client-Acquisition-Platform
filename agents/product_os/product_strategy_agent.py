"""Product Strategy & Portfolio Agent for Phase 60."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.product_os.service import ProductOperatingSystemService
except ImportError:
    from app.services.product_os.service import ProductOperatingSystemService

logger = logging.getLogger(__name__)


class ProductStrategyAgent(BaseAgent):
    """Orchestrates product portfolio creation, vision definitions, and strategy alignment."""

    agent_id = "product_strategy_agent"
    name = "Product Strategy & Portfolio Agent"
    version = "1.0"
    description = "Formulates evidence-grounded product visions, strategic positioning, and OKR linkages."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.MANAGE_PRODUCT_PORTFOLIO,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_name = context.metadata.get("name", "Uzaii Cognitive Platform")
        product_line = context.metadata.get("product_line", "Enterprise Intelligence")
        target_icp = context.metadata.get("target_icp", "Fortune 500 Enterprises")

        product = self.service.portfolio_service.create_product(
            tenant_id=tenant_id,
            name=product_name,
            product_line=product_line,
            code=f"UZAII-PRD-{hash(product_name) % 1000:03d}",
            lifecycle_state="DISCOVERY",
            target_icp=target_icp,
            owner_email="chief-product@uzaii.com",
            description="Intelligent evidence-driven enterprise product.",
        )

        vision = self.service.portfolio_service.create_product_vision(
            tenant_id=tenant_id,
            product_id=product.product_id,
            target_users=target_icp,
            core_problem="Inefficient coordination across product strategy, engineering, and adoption.",
            value_proposition="Unified sensory, analytical, and governance operating layer.",
            differentiation="Zero ungrounded hallucinations, human-in-the-loop governance guarantees.",
        )

        return {
            "status": "COMPLETED",
            "product_id": product.product_id,
            "product_name": product.name,
            "lifecycle_state": product.lifecycle_state,
            "vision_id": vision.vision_id,
        }
