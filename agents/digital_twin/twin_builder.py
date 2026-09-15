"""
Twin Builder Agent (Phase 50).
Captures point-in-time enterprise digital twin state snapshots across business domains.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.digital_twin.service import DigitalTwinPlatformService
except ImportError:
    from app.services.digital_twin.service import DigitalTwinPlatformService


class TwinBuilderAgent(BaseAgent):
    """
    Agent responsible for capturing state snapshots, modeling cross-domain entities,
    and verifying cryptographic snapshot integrity.
    Cannot mutate live production databases.
    """

    agent_id = "twin_builder_agent"
    name = "Twin Builder Agent"
    version = "1.0"
    description = "Captures holistic enterprise state snapshots and builds digital twin representations."

    def __init__(self, service: Optional[DigitalTwinPlatformService] = None):
        super().__init__()
        self.service = service or DigitalTwinPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_TWIN_STATE,
            AgentPermission.READ_TWIN_MODELS,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        title = str(params.get("title") or "Enterprise Point-in-Time Snapshot")

        state = self.service.capture_enterprise_state(tenant_id=tenant_id, title=title)
        is_valid = self.service.verify_state_integrity(state)

        return {
            "status": "SUCCESS",
            "snapshot_code": state.snapshot_code,
            "title": state.title,
            "composite_health_score": state.composite_health_score,
            "state_hash": state.state_hash,
            "is_cryptographically_verified": is_valid,
            "commercial_summary": state.commercial_state,
            "financial_summary": state.financial_state,
            "delivery_summary": state.delivery_state,
        }
