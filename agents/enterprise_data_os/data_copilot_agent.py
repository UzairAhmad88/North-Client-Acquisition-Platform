"""Enterprise Data Copilot Agent for Phase 62."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService
except ImportError:
    from app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService

logger = logging.getLogger(__name__)


class DataCopilotAgent(BaseAgent):
    """Evidence-grounded conversational Data Copilot distinguishing facts, hypotheses, and recommendations."""

    agent_id = "data_copilot_agent"
    name = "Enterprise Data Copilot Agent"
    version = "1.0"
    description = "Provides evidence-grounded answers on lineage, metrics, datasets, schemas, and FinOps."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        query = context.metadata.get("query", "Where does ARR come from and who owns it?")

        copilot_resp = self.service.copilot_service.query_data_copilot(
            tenant_id=tenant_id,
            query=query,
        )
        facts = copilot_resp.get("facts", [])
        inferences = copilot_resp.get("inferences", [])
        hypotheses = copilot_resp.get("hypotheses", [])
        recommendations = copilot_resp.get("recommendations", [])
        response_summary = "\n".join(facts + inferences + hypotheses + recommendations)

        return {
            "status": "COMPLETED",
            "query": copilot_resp["query"],
            "response": response_summary,
            "facts": facts,
            "inferences": inferences,
            "hypotheses": hypotheses,
            "recommendations": recommendations,
            "confidence_score": copilot_resp["confidence_score"],
            "facts_count": len(facts),
            "governance_notice": copilot_resp.get("governance_notice", ""),
            "timestamp": copilot_resp["timestamp"],
        }
