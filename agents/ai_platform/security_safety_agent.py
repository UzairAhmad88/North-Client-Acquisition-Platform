"""AI Security & Safety Guardrails Agent for Phase 63."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.ai_model_factory.service import AiModelFactoryService
except ImportError:
    from app.services.ai_model_factory.service import AiModelFactoryService

logger = logging.getLogger(__name__)


class SecuritySafetyAgent(BaseAgent):
    """Executes Supply Chain SBOM scans, License compliance checks, and Prompt Injection guardrail audits."""

    agent_id = "security_safety_agent"
    name = "AI Security & Safety Agent"
    version = "1.0"
    description = "Conducts model vulnerability scans, prompt injection guardrail checks, and SBOM audits."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.GOVERN_AI_MODELS,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        model_version_id = context.metadata.get("model_version_id", "aimv_default")

        scan = self.service.governance_service.run_security_and_license_scan(
            tenant_id=tenant_id,
            model_version_id=model_version_id,
            base_model_license="Apache-2.0",
        )
        return {
            "status": "COMPLETED",
            "scan_id": scan.id,
            "passed": scan.passed,
            "is_license_compliant": scan.is_license_compliant,
            "vulnerabilities_count": scan.vulnerabilities_count,
        }
