"""
Phase 82 Enterprise Data Platform Services Module.
"""

from app.services.data_platform.sources import DataPlatformSourcesService
from app.services.data_platform.pipelines import DataPlatformPipelinesService
from app.services.data_platform.catalog import DataPlatformCatalogService
from app.services.data_platform.lineage import DataPlatformLineageService
from app.services.data_platform.governance import DataPlatformGovernanceService
from app.services.data_platform.quality import DataPlatformQualityService
from app.services.data_platform.mdm import DataPlatformMdmService
from app.services.data_platform.copilot import DataPlatformCopilotService
from app.services.data_platform.agents import DataPlatformAgentsService
from app.services.data_platform.costs import DataPlatformCostsService

__all__ = [
    "DataPlatformSourcesService",
    "DataPlatformPipelinesService",
    "DataPlatformCatalogService",
    "DataPlatformLineageService",
    "DataPlatformGovernanceService",
    "DataPlatformQualityService",
    "DataPlatformMdmService",
    "DataPlatformCopilotService",
    "DataPlatformAgentsService",
    "DataPlatformCostsService",
]
