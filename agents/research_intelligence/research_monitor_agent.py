"""
Continuous Research Monitor Agent for Phase 54.
Monitors competitive, market, AI, and regulatory changes and emits prioritized intelligence events.
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
    from backend.app.services.research_intelligence.base import IntelligenceEventType, SignificanceLevel
except ImportError:
    from app.services.research_intelligence.service import (
        ResearchIntelligencePlatformService,
        global_research_intelligence_service,
    )
    from app.services.research_intelligence.base import IntelligenceEventType, SignificanceLevel

logger = logging.getLogger(__name__)


class ResearchMonitorAgent(BaseAgent):
    """Monitors watched entities and triggers significant intelligence alerts."""

    agent_id = "research_monitor_agent"
    name = "Research Monitor Agent"
    version = "1.0"
    description = "Monitors external entities, detects meaningful state shifts, and records intelligence events."
    permissions = {
        AgentPermission.READ_RESEARCH_INTELLIGENCE,
        AgentPermission.CONFIGURE_MONITORING_RULES,
    }

    def __init__(self, service: Optional[ResearchIntelligencePlatformService] = None):
        super().__init__()
        self.service = service or global_research_intelligence_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        target = context.metadata.get("target_entity", "Competitor Inc")
        event_type = context.metadata.get("event_type", IntelligenceEventType.CHANGED)
        summary = context.metadata.get("summary", "State shift observed.")
        significance = context.metadata.get("significance", SignificanceLevel.MEDIUM)

        evt = self.service.monitoring.record_intelligence_event(
            target_entity=target,
            event_type=event_type,
            summary=summary,
            significance=significance,
        )
        return {"status": "SUCCESS", "intelligence_event": evt}
