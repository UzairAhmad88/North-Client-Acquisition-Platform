"""
Phase 56 Product Management Platform Module Exports.
"""

from backend.app.services.product_management.base import (
    ProductType,
    LifecycleStage,
    FeedbackType,
    RequirementCategory,
    RequirementPriority,
    BacklogItemType,
    PrioritizationFramework,
    RoadmapHorizon,
    RoadmapScenario,
    SprintStatus,
    ReleaseReadinessStatus,
    FeatureFlagState,
    ProductHealthStatus,
    SunsetStage,
)
from backend.app.services.product_management.products import ProductManager
from backend.app.services.product_management.vision_strategy import VisionStrategyManager
from backend.app.services.product_management.feedback_intelligence import FeedbackIntelligenceManager
from backend.app.services.product_management.requirements_traceability import RequirementsTraceabilityManager
from backend.app.services.product_management.backlog_prioritization import BacklogPrioritizationManager
from backend.app.services.product_management.roadmaps_capacity import RoadmapCapacityManager
from backend.app.services.product_management.sprints_releases import SprintReleaseManager
from backend.app.services.product_management.deployments_launches import DeploymentLaunchManager
from backend.app.services.product_management.analytics_experimentation import AnalyticsExperimentationManager
from backend.app.services.product_management.health_sunset import HealthSunsetManager
from backend.app.services.product_management.service import (
    ProductManagementPlatformService,
    global_product_management_service,
    AttrDict,
)

__all__ = [
    "ProductType",
    "LifecycleStage",
    "FeedbackType",
    "RequirementCategory",
    "RequirementPriority",
    "BacklogItemType",
    "PrioritizationFramework",
    "RoadmapHorizon",
    "RoadmapScenario",
    "SprintStatus",
    "ReleaseReadinessStatus",
    "FeatureFlagState",
    "ProductHealthStatus",
    "SunsetStage",
    "ProductManager",
    "VisionStrategyManager",
    "FeedbackIntelligenceManager",
    "RequirementsTraceabilityManager",
    "BacklogPrioritizationManager",
    "RoadmapCapacityManager",
    "SprintReleaseManager",
    "DeploymentLaunchManager",
    "AnalyticsExperimentationManager",
    "HealthSunsetManager",
    "ProductManagementPlatformService",
    "global_product_management_service",
    "AttrDict",
]
