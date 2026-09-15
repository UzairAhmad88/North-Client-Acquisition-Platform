"""Developer Copilot Agent for Phase 61."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
except ImportError:
    from app.services.engineering_os.service import EngineeringOperatingSystemService

logger = logging.getLogger(__name__)


class DeveloperCopilotAgent(BaseAgent):
    """Answers developer & SRE queries with evidence-backed FACT, INFERENCE, HYPOTHESIS, and RECOMMENDATION tags."""

    agent_id = "developer_copilot_agent"
    name = "Developer Copilot Agent"
    version = "1.0"
    description = "Provides evidence-grounded engineering intelligence across architecture, CI/CD, and incidents."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        query = context.metadata.get("query", "Explain current DORA metrics and deployment risk.")

        result = self.service.query_developer_copilot(tenant_id=tenant_id, query=query)

        return {
            "status": "COMPLETED",
            "query": query,
            "response": result.get("response"),
            "evidence_sources": result.get("evidence_sources"),
            "confidence": result.get("confidence"),
            "governance_notice": result.get("governance_notice"),
        }
