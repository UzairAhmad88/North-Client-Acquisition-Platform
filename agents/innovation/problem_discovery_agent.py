"""
Problem Discovery Agent for Phase 55.
Identifies and catalogs customer pain points, frequency, and willingness-to-pay evidence.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )
except ImportError:
    from app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )

logger = logging.getLogger(__name__)


class ProblemDiscoveryAgent(BaseAgent):
    """Catalogs real-world user and operational problems with evidence backing."""

    agent_id = "problem_discovery_agent"
    name = "Problem Discovery Agent"
    version = "1.0"
    description = "Captures user pain points, severity, frequency, and empirical willingness-to-pay signals."
    permissions = {
        AgentPermission.READ_INNOVATION,
    }

    def __init__(self, service: Optional[InnovationPlatformService] = None):
        super().__init__()
        self.service = service or global_innovation_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        if not ws_id:
            return {"status": "FAILED", "error": "workspace_id required in metadata"}

        statement = context.metadata.get("statement", "Observed workflow bottleneck in manual lead review.")
        severity = context.metadata.get("severity", "HIGH")
        frequency = context.metadata.get("frequency", "DAILY")
        wtp = context.metadata.get("willingness_to_pay_signal", 299.0)
        evidence = context.metadata.get("evidence_sources", ["Telemetry and support ticket logs"])

        prob = self.service.problems_opportunities.record_problem(
            workspace_id=ws_id,
            statement=statement,
            severity=severity,
            frequency=frequency,
            willingness_to_pay_signal=wtp,
            evidence_sources=evidence,
        )
        return {"status": "SUCCESS", "problem": prob}
