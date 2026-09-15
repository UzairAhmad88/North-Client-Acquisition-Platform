"""
Process Intelligence & Discovery Agent (Phase 49).
Analyzes process maps, discovered variants, and conformance violations.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService
except ImportError:
    from app.process_intelligence.service import ProcessIntelligencePlatformService


class ProcessIntelligenceAgent(BaseAgent):
    """
    AI agent for process discovery, variant comparison, and conformance audit.
    Cannot autonomously modify production workflows or deploy changes.
    """

    agent_id = "process_intelligence_agent"
    name = "Process Intelligence Agent"
    version = "1.0"
    description = "Analyzes business process event logs, discovers execution variants, and detects conformance deviations."

    def __init__(self, service: Optional[ProcessIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or ProcessIntelligencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROCESS_INTELLIGENCE,
            AgentPermission.ANALYZE_PROCESSES,
            AgentPermission.READ_EVENT_LOG,
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

        proc = self.service.get_process(process_id, tenant_id)
        if not proc:
            return {
                "status": "ERROR",
                "message": f"Process '{process_id}' not found.",
            }

        variants = self.service.discovery_engine.discover_variants(process_id, tenant_id)
        process_map = self.service.discovery_engine.build_process_map(process_id, tenant_id=tenant_id)
        violations = self.service.conformance_checker.check_process_conformance(process_id, tenant_id)
        health = self.service.get_process_health(process_id, tenant_id)

        analysis_summary = (
            f"Process '{proc.name}' ({proc.domain.value}) analyzed across {len(variants)} execution variants. "
            f"Health state: {health.health_status.value}. Detected {len(violations)} conformance violations."
        )

        return {
            "status": "SUCCESS",
            "process_id": process_id,
            "process_name": proc.name,
            "domain": proc.domain.value,
            "variants_count": len(variants),
            "top_variants": [v.model_dump() if hasattr(v, 'model_dump') else v.dict() for v in variants[:3]],
            "conformance_violations_count": len(violations),
            "violations": [v.model_dump() if hasattr(v, 'model_dump') else v.dict() for v in violations[:5]],
            "health_report": health.model_dump() if hasattr(health, 'model_dump') else health.dict(),
            "summary": analysis_summary,
            "autonomous_actions_allowed": False,
        }
