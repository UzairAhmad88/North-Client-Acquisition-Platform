"""Phase 64 — Autonomous Engineering OS Service Exports."""

try:
    from app.services.autonomous_engineering_os.base import BaseAutonomousEngineeringOsService
    from app.services.autonomous_engineering_os.projects_requirements_specs import ProjectsRequirementsSpecsService
    from app.services.autonomous_engineering_os.architecture_code_intelligence import ArchitectureCodeIntelligenceService
    from app.services.autonomous_engineering_os.task_planner_coding_sandbox import TaskPlannerCodingSandboxService
    from app.services.autonomous_engineering_os.pull_requests_code_reviews import PullRequestsCodeReviewsService
    from app.services.autonomous_engineering_os.ci_cd_builds_artifacts import CiCdBuildsArtifactsService
    from app.services.autonomous_engineering_os.testing_flakiness_impact import TestingFlakinessImpactService
    from app.services.autonomous_engineering_os.security_sbom_dependencies import SecuritySbomDependenciesService
    from app.services.autonomous_engineering_os.deployments_verification_rollback import DeploymentsVerificationRollbackService
    from app.services.autonomous_engineering_os.observability_sre_slo import ObservabilitySreSloService
    from app.services.autonomous_engineering_os.incidents_root_cause_self_healing import IncidentsRootCauseSelfHealingService
    from app.services.autonomous_engineering_os.finops_twin_copilot import FinopsTwinCopilotService
    from app.services.autonomous_engineering_os.service import AutonomousEngineeringOsService
except ImportError:
    from backend.app.services.autonomous_engineering_os.base import BaseAutonomousEngineeringOsService
    from backend.app.services.autonomous_engineering_os.projects_requirements_specs import ProjectsRequirementsSpecsService
    from backend.app.services.autonomous_engineering_os.architecture_code_intelligence import ArchitectureCodeIntelligenceService
    from backend.app.services.autonomous_engineering_os.task_planner_coding_sandbox import TaskPlannerCodingSandboxService
    from backend.app.services.autonomous_engineering_os.pull_requests_code_reviews import PullRequestsCodeReviewsService
    from backend.app.services.autonomous_engineering_os.ci_cd_builds_artifacts import CiCdBuildsArtifactsService
    from backend.app.services.autonomous_engineering_os.testing_flakiness_impact import TestingFlakinessImpactService
    from backend.app.services.autonomous_engineering_os.security_sbom_dependencies import SecuritySbomDependenciesService
    from backend.app.services.autonomous_engineering_os.deployments_verification_rollback import DeploymentsVerificationRollbackService
    from backend.app.services.autonomous_engineering_os.observability_sre_slo import ObservabilitySreSloService
    from backend.app.services.autonomous_engineering_os.incidents_root_cause_self_healing import IncidentsRootCauseSelfHealingService
    from backend.app.services.autonomous_engineering_os.finops_twin_copilot import FinopsTwinCopilotService
    from backend.app.services.autonomous_engineering_os.service import AutonomousEngineeringOsService

__all__ = [
    "BaseAutonomousEngineeringOsService",
    "ProjectsRequirementsSpecsService",
    "ArchitectureCodeIntelligenceService",
    "TaskPlannerCodingSandboxService",
    "PullRequestsCodeReviewsService",
    "CiCdBuildsArtifactsService",
    "TestingFlakinessImpactService",
    "SecuritySbomDependenciesService",
    "DeploymentsVerificationRollbackService",
    "ObservabilitySreSloService",
    "IncidentsRootCauseSelfHealingService",
    "FinopsTwinCopilotService",
    "AutonomousEngineeringOsService",
]
