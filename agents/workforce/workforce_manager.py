"""
Workforce Manager Agent for Phase 52.
Decomposes high-level objectives, orchestrates department squads, and coordinates worker assignments.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional, Set

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.workforce.service import WorkforcePlatformService
except ImportError:
    from app.services.workforce.service import WorkforcePlatformService

logger = logging.getLogger(__name__)


class WorkforceManagerAgent(BaseAgent):
    """Coordinates high-level workforce planning and cross-team task assignment."""

    agent_id = "workforce_manager_agent"
    name = "Workforce Manager Agent"
    version = "1.0"
    description = "Decomposes objectives into task DAGs and manages specialized AI worker squads."
    permissions = {
        AgentPermission.READ_WORKFORCE,
        AgentPermission.CREATE_WORKFORCE_PLAN,
        AgentPermission.DECOMPOSE_TASK_GRAPH,
        AgentPermission.ASSIGN_WORKFORCE_TASK,
    }

    def __init__(self, service: Optional[WorkforcePlatformService] = None):
        super().__init__()
        self.service = service or WorkforcePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        objective = context.metadata.get("objective", "Execute growth strategy")
        domain = context.metadata.get("domain", "GROWTH_EXPANSION")

        tasks = self.service.plan_and_decompose_objective(objective, domain=domain)

        return {
            "status": "SUCCESS",
            "objective": objective,
            "domain": domain,
            "action": "WORKFORCE_DECOMPOSITION_COMPLETE",
            "tasks_count": len(tasks),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
