"""
Phase 54: Unified Autonomous Research, Intelligence & Continuous Discovery Engine module.
"""

from backend.app.services.research_intelligence.base import (
    ResearchStatus,
    ResearchType,
    SourceTrustLevel,
    FactStatus,
    ClaimVerificationStatus,
    IntelligenceEventType,
    SignificanceLevel,
    ResearchSource,
    ResearchFact,
    ResearchClaim,
    ResearchConflict,
    IntelligenceEvent,
)
from backend.app.services.research_intelligence.workspaces import ResearchWorkspaceManager
from backend.app.services.research_intelligence.sources import SourceRegistryManager
from backend.app.services.research_intelligence.extraction_verification import ExtractionVerificationManager
from backend.app.services.research_intelligence.domains import DomainIntelligenceManager
from backend.app.services.research_intelligence.monitoring import ContinuousMonitoringManager
from backend.app.services.research_intelligence.synthesis_reports import SynthesisReportManager
from backend.app.services.research_intelligence.service import (
    ResearchIntelligencePlatformService,
    global_research_intelligence_service,
)

__all__ = [
    "ResearchStatus",
    "ResearchType",
    "SourceTrustLevel",
    "FactStatus",
    "ClaimVerificationStatus",
    "IntelligenceEventType",
    "SignificanceLevel",
    "ResearchSource",
    "ResearchFact",
    "ResearchClaim",
    "ResearchConflict",
    "IntelligenceEvent",
    "ResearchWorkspaceManager",
    "SourceRegistryManager",
    "ExtractionVerificationManager",
    "DomainIntelligenceManager",
    "ContinuousMonitoringManager",
    "SynthesisReportManager",
    "ResearchIntelligencePlatformService",
    "global_research_intelligence_service",
]
