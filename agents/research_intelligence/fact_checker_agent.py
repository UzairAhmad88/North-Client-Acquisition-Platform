"""
Fact Extraction & Claim Verification Agent for Phase 54.
Verifies claims via independent source corroboration, extracts atomic facts, and flags contradictions.
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


class FactCheckerAgent(BaseAgent):
    """Extracts facts, corroborates claims across independent sources, and flags contradictions."""

    agent_id = "fact_checker_agent"
    name = "Fact Checker Agent"
    version = "1.0"
    description = "Extracts verified facts, checks claims against evidence, and surfaces conflicting data."
    permissions = {
        AgentPermission.READ_RESEARCH_INTELLIGENCE,
        AgentPermission.EXTRACT_RESEARCH_FACTS,
        AgentPermission.VERIFY_RESEARCH_CLAIMS,
    }

    def __init__(self, service: Optional[ResearchIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or global_research_intelligence_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        claim_text = context.metadata.get("claim_text", "")
        sources = context.metadata.get("supporting_sources", [])
        contradictions = context.metadata.get("contradicting_sources", [])

        claim = self.service.extraction.verify_claim(
            workspace_id=ws_id,
            claim_text=claim_text,
            supporting_sources=sources,
            contradicting_sources=contradictions,
        )
        return {"status": "SUCCESS", "claim_verification": claim}
