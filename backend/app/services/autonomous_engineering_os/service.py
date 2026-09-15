"""Phase 64 — Unified Autonomous Engineering Operating System Master Service."""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

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


class AutonomousEngineeringOsService:
    """Unified Facade aggregating all sub-services for Autonomous Engineering OS."""

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.projects_requirements = ProjectsRequirementsSpecsService(db)
        self.architecture_code = ArchitectureCodeIntelligenceService(db)
        self.tasks_sandbox = TaskPlannerCodingSandboxService(db)
        self.pull_requests = PullRequestsCodeReviewsService(db)
        self.ci_cd = CiCdBuildsArtifactsService(db)
        self.testing = TestingFlakinessImpactService(db)
        self.security_sbom = SecuritySbomDependenciesService(db)
        self.deployments = DeploymentsVerificationRollbackService(db)
        self.observability_sre = ObservabilitySreSloService(db)
        self.incidents_self_healing = IncidentsRootCauseSelfHealingService(db)
        self.finops_twin = FinopsTwinCopilotService(db)

    def get_engineering_command_center_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Aggregate high-level metrics for the Engineering Command Center Dashboard."""
        projects = self.projects_requirements.list_project_workspaces(tenant_id)
        requirements = self.projects_requirements.list_requirements(tenant_id)
        tasks = self.tasks_sandbox.list_tasks(tenant_id)
        pull_requests = self.pull_requests.list_pull_requests(tenant_id)
        build_runs = self.ci_cd.list_build_runs(tenant_id)
        test_suites = self.testing.list_test_suites(tenant_id)
        sbom_packages = self.security_sbom.list_sbom_packages(tenant_id)
        deployments = self.deployments.list_deployments(tenant_id)
        services = self.observability_sre.list_service_catalog(tenant_id)
        incidents = self.incidents_self_healing.list_incidents(tenant_id)
        runbooks = self.incidents_self_healing.list_self_healing_runbooks(tenant_id)
        finops_costs = self.finops_twin.list_finops_costs(tenant_id)

        total_spend_usd = sum(c.amount_usd for c in finops_costs)
        open_prs = [pr for pr in pull_requests if pr.status == "OPEN"]
        active_incidents = [inc for inc in incidents if inc.remediation_status in ("INVESTIGATING", "OPEN")]
        healthy_services = [s for s in services if s.status == "HEALTHY"]

        return {
            "active_projects_count": len(projects),
            "requirements_count": len(requirements),
            "tasks_count": len(tasks),
            "open_pull_requests_count": len(open_prs),
            "total_build_runs_count": len(build_runs),
            "test_suites_count": len(test_suites),
            "sbom_packages_count": len(sbom_packages),
            "deployments_count": len(deployments),
            "services_count": len(services),
            "healthy_services_count": len(healthy_services),
            "active_incidents_count": len(active_incidents),
            "self_healing_runbooks_count": len(runbooks),
            "total_finops_spend_usd": round(total_spend_usd, 2),
            "status": "OPERATIONAL",
        }
