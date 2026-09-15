"""
Source Discovery & Validation Agent for Phase 54.
Discovers authoritative primary, official, academic, and professional research sources.
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
    from backend.app.services.research_intelligence.base import SourceTrustLevel
except ImportError:
    from app.services.research_intelligence.service import (
        ResearchIntelligencePlatformService,
        global_research_intelligence_service,
    )
    from app.services.research_intelligence.base import SourceTrustLevel

logger = logging.getLogger(__name__)


class SourceDiscoveryAgent(BaseAgent):
    """Discovers, registers, and assesses the reliability and freshness of research sources."""

    agent_id = "source_discovery_agent"
    name = "Source Discovery Agent"
    version = "1.0"
    description = "Discovers and validates research sources against trust hierarchies and SSRF protections."
    permissions = {
        AgentPermission.READ_RESEARCH_INTELLIGENCE,
    }

    def __init__(self, service: Optional[ResearchIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or global_research_intelligence_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        url = context.metadata.get("url", "https://example.com/industry-report")
        source_type = context.metadata.get("source_type", SourceTrustLevel.SECONDARY)
        publisher = context.metadata.get("publisher", "Industry Publisher")

        try:
            source = self.service.sources.register_source(
                workspace_id=ws_id,
                url_or_reference=url,
                source_type=source_type,
                publisher=publisher,
            )
            return {"status": "SUCCESS", "source": source}
        except ValueError as e:
            return {"status": "FAILED", "error": str(e)}
