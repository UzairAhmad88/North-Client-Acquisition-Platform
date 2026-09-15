"""Product Operating System package exports for Phase 60."""

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        ProductLifecycleState,
        ProblemValidationStatus,
        PrioritizationFramework,
        RoadmapHorizon,
        RequirementType,
        ProductHealthState,
        ReleaseStrategy,
        RiskSeverity,
        generate_product_id,
    )
    from backend.app.services.product_os.portfolio_vision_strategy import PortfolioVisionStrategyService
    from backend.app.services.product_os.problems_feedback_opportunities import ProblemsFeedbackOpportunitiesService
    from backend.app.services.product_os.prioritization_roadmaps import PrioritizationRoadmapsService
    from backend.app.services.product_os.requirements_traceability import RequirementsTraceabilityService
    from backend.app.services.product_os.analytics_feature_value import AnalyticsFeatureValueService
    from backend.app.services.product_os.launches_flags_sunset import LaunchesFlagsSunsetService
    from backend.app.services.product_os.economics_forecast_risks import EconomicsForecastRisksService
    from backend.app.services.product_os.service import ProductOperatingSystemService
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        ProductLifecycleState,
        ProblemValidationStatus,
        PrioritizationFramework,
        RoadmapHorizon,
        RequirementType,
        ProductHealthState,
        ReleaseStrategy,
        RiskSeverity,
        generate_product_id,
    )
    from app.services.product_os.portfolio_vision_strategy import PortfolioVisionStrategyService
    from app.services.product_os.problems_feedback_opportunities import ProblemsFeedbackOpportunitiesService
    from app.services.product_os.prioritization_roadmaps import PrioritizationRoadmapsService
    from app.services.product_os.requirements_traceability import RequirementsTraceabilityService
    from app.services.product_os.analytics_feature_value import AnalyticsFeatureValueService
    from app.services.product_os.launches_flags_sunset import LaunchesFlagsSunsetService
    from app.services.product_os.economics_forecast_risks import EconomicsForecastRisksService
    from app.services.product_os.service import ProductOperatingSystemService

__all__ = [
    "AttrDict",
    "ProductLifecycleState",
    "ProblemValidationStatus",
    "PrioritizationFramework",
    "RoadmapHorizon",
    "RequirementType",
    "ProductHealthState",
    "ReleaseStrategy",
    "RiskSeverity",
    "generate_product_id",
    "PortfolioVisionStrategyService",
    "ProblemsFeedbackOpportunitiesService",
    "PrioritizationRoadmapsService",
    "RequirementsTraceabilityService",
    "AnalyticsFeatureValueService",
    "LaunchesFlagsSunsetService",
    "EconomicsForecastRisksService",
    "ProductOperatingSystemService",
]
