"""
Synthesis & Reporting Agent for Phase 54.
Synthesizes verified facts into intelligence findings and structured research reports with citations.
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


class SynthesisAgent(BaseAgent):
    """Synthesizes validated facts and claims into executive briefings and research reports."""

    agent_id = "synthesis_agent"
    name = "Synthesis & Reporting Agent"
    version = "1.0"
    description = "Generates actionable intelligence syntheses and comprehensive research reports."
    permissions = {
        AgentPermission.READ_RESEARCH_INTELLIGENCE,
        AgentPermission.SYNTHESIZE_RESEARCH_REPORT,
    }

    def __init__(self, service: Optional[ResearchIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or global_research_intelligence_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        summary = context.metadata.get("summary", "Executive intelligence summary.")
        findings = context.metadata.get("findings", [])
        actions = context.metadata.get("recommended_actions", [])

        synth = self.service.synthesis.generate_synthesis(
            workspace_id=ws_id,
            executive_summary=summary,
            key_findings=findings,
            recommended_actions=actions,
        )
        return {"status": "SUCCESS", "synthesis": synth}
