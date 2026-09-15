"""
Automation Candidate Agent (Phase 49).
Evaluates manual repetitive tasks for workflow automation potential.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService
except ImportError:
    from app.process_intelligence.service import ProcessIntelligencePlatformService


class AutomationCandidateAgent(BaseAgent):
    """
    AI agent analyzing process event logs to identify candidates for safe workflow automation.
    Requires human review; cannot autonomously implement automations.
    """

    agent_id = "automation_candidate_agent"
    name = "Automation Candidate Agent"
    version = "1.0"
    description = "Scans event histories for high-frequency, deterministic tasks and calculates 8-factor suitability scores."

    def __init__(self, service: Optional[ProcessIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or ProcessIntelligencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROCESS_INTELLIGENCE,
            AgentPermission.ANALYZE_PROCESSES,
            AgentPermission.CREATE_AUTOMATION_CANDIDATE,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        process_id = str(params.get("process_id") or "")
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")

        if not process_id:
            return {
                "status": "ERROR",
                "message": "process_id is required.",
            }

        candidates = self.service.automation_evaluator.scan_for_candidates(process_id, tenant_id)

        return {
            "status": "SUCCESS",
            "process_id": process_id,
            "candidates_found": len(candidates),
            "candidates": [c.model_dump() if hasattr(c, 'model_dump') else c.dict() for c in candidates],
            "human_oversight_required": True,
            "autonomous_implementation_blocked": True,
        }
