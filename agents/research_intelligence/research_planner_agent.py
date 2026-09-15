"""
Research Planner Agent for Phase 54.
Decomposes high-level research questions into structured, prioritized investigation subtasks.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.research_intelligence.service import (
        ResearchIntelligencePlatformService,
        global_research_intelligence_service,
    )
except ImportError:
    from app.services.research_intelligence.service import (
        ResearchIntelligencePlatformService,
        global_research_intelligence_service,
    )

logger = logging.getLogger(__name__)


class ResearchPlannerAgent(BaseAgent):
    """Decomposes core research questions into prioritized research tasks."""

    agent_id = "research_planner_agent"
    name = "Research Planner Agent"
    version = "1.0"
    description = "Formulates comprehensive research plans and breaks down questions into subtasks."
    permissions = {
        AgentPermission.READ_RESEARCH_INTELLIGENCE,
        AgentPermission.CREATE_RESEARCH_PLAN,
    }

    def __init__(self, service: Optional[ResearchIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or global_research_intelligence_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        if not ws_id:
            return {"status": "FAILED", "error": "workspace_id is required"}

        subquestions = context.metadata.get("subquestions")
        tasks = self.service.workspaces.decompose_question(ws_id, subquestions)
        return {"status": "SUCCESS", "tasks_created": len(tasks), "tasks": tasks}
