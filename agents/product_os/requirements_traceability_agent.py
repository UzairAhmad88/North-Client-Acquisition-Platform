"""Requirements & Traceability Matrix Agent for Phase 60."""

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


class RequirementsTraceabilityAgent(BaseAgent):
    """Enforces PRD structure, acceptance criteria, and full end-to-end lifecycle traceability."""

    agent_id = "requirements_traceability_agent"
    name = "Requirements & Traceability Agent"
    version = "1.0"
    description = "Tracks requirement decomposition into Given/When/Then user stories and audits orphaned initiatives."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.TRACE_PRODUCT_REQUIREMENTS,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        opp_id = context.metadata.get("opportunity_id", "opp_default")
        title = context.metadata.get("title", "Real-time Event Stream Processing")

        req = self.service.requirements_service.create_requirement(
            tenant_id=tenant_id,
            opportunity_id=opp_id,
            title=title,
            requirement_type=context.metadata.get("requirement_type", "FUNCTIONAL"),
            priority=context.metadata.get("priority", "HIGH"),
            acceptance_criteria=["Processes 50k events/sec under 20ms p99 latency"],
        )

        story = self.service.requirements_service.add_user_story(
            tenant_id=tenant_id,
            requirement_id=req.requirement_id,
            role="Data Engineer",
            capability="ingest continuous telemetry streams with zero message loss",
            benefit="downstream decision twin models receive real-time signals",
            story_points=8,
        )

        validation = self.service.requirements_service.validate_requirements_completeness(tenant_id)

        return {
            "status": "COMPLETED",
            "requirement_id": req.requirement_id,
            "story_id": story.story_id,
            "requirements_health_score": validation.get("requirements_health_score"),
        }
