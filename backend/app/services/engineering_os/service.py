"""Unified Engineering, SDLC, DevOps, CI/CD & Technical Operations OS Master Service.

Phase 61 Architectural Core orchestrating Organizations, Repositories, PRs, Architecture,
Service Catalog, Environments, CI/CD, Deployments, SRE/Observability, Incidents,
Changes, Vulnerabilities, DORA Metrics, FinOps, and Developer Copilot.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.engineering_os.base import AttrDict
    from backend.app.services.engineering_os.portfolio_repositories_code import PortfolioRepositoriesCodeService
    from backend.app.services.engineering_os.architecture_services_apis_db import ArchitectureServicesApisDbService
    from backend.app.services.engineering_os.environments_infrastructure_iac import EnvironmentsInfrastructureIacService
    from backend.app.services.engineering_os.cicd_builds_artifacts_k8s import CicdBuildsArtifactsK8sService
    from backend.app.services.engineering_os.deployments_releases_readiness import DeploymentsReleasesReadinessService
    from backend.app.services.engineering_os.testing_flakiness_performance import TestingFlakinessPerformanceService
    from backend.app.services.engineering_os.observability_sre_incidents import ObservabilitySreIncidentsService
    from backend.app.services.engineering_os.changes_migrations_dependencies import ChangesMigrationsDependenciesService
    from backend.app.services.engineering_os.tech_debt_capacity_dora_finops import TechDebtCapacityDoraFinopsService
    from backend.app.services.engineering_os.twin_simulations_risks_copilot import TwinSimulationsRisksCopilotService
except ImportError:
    from app.services.engineering_os.base import AttrDict
    from app.services.engineering_os.portfolio_repositories_code import PortfolioRepositoriesCodeService
    from app.services.engineering_os.architecture_services_apis_db import ArchitectureServicesApisDbService
    from app.services.engineering_os.environments_infrastructure_iac import EnvironmentsInfrastructureIacService
    from app.services.engineering_os.cicd_builds_artifacts_k8s import CicdBuildsArtifactsK8sService
    from app.services.engineering_os.deployments_releases_readiness import DeploymentsReleasesReadinessService
    from app.services.engineering_os.testing_flakiness_performance import TestingFlakinessPerformanceService
    from app.services.engineering_os.observability_sre_incidents import ObservabilitySreIncidentsService
    from app.services.engineering_os.changes_migrations_dependencies import ChangesMigrationsDependenciesService
    from app.services.engineering_os.tech_debt_capacity_dora_finops import TechDebtCapacityDoraFinopsService
    from app.services.engineering_os.twin_simulations_risks_copilot import TwinSimulationsRisksCopilotService

logger = logging.getLogger(__name__)


class EngineeringOperatingSystemService:
    """Master orchestrator for Phase 61 Engineering Operating System."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self.portfolio_code_service = PortfolioRepositoriesCodeService(db_session)
        self.portfolio_service = self.portfolio_code_service
        self.architecture_service = ArchitectureServicesApisDbService(db_session)
        self.arch_service = self.architecture_service
        self.environments_service = EnvironmentsInfrastructureIacService(db_session)
        self.infra_service = self.environments_service
        self.cicd_service = CicdBuildsArtifactsK8sService(db_session)
        self.deployments_service = DeploymentsReleasesReadinessService(db_session)
        self.deploy_service = self.deployments_service
        self.testing_service = TestingFlakinessPerformanceService(db_session)
        self.test_service = self.testing_service
        self.observability_service = ObservabilitySreIncidentsService(db_session)
        self.obs_service = self.observability_service
        self.changes_service = ChangesMigrationsDependenciesService(db_session)
        self.change_service = self.changes_service
        self.dora_finops_service = TechDebtCapacityDoraFinopsService(db_session)
        self.tech_debt_service = self.dora_finops_service
        self.twin_copilot_service = TwinSimulationsRisksCopilotService(db_session)
        self.twin_service = self.twin_copilot_service

        # Seed rich baseline ecosystem for demonstration
        self._seed_default_engineering_ecosystem("default_tenant")


    def _seed_default_engineering_ecosystem(self, tenant_id: str):
        """Populate initial representative engineering ecosystem."""
        # 1. Organization & Team & Repository
        org = self.portfolio_code_service.create_organization(
            tenant_id=tenant_id,
            name="Uzaii Global Engineering",
            slug="uzaii-global-eng",
        )
        team = self.portfolio_code_service.create_team(
            tenant_id=tenant_id,
            org_id=org.org_id,
            name="Core Platform & Decision Architecture",
            team_type="PLATFORM",
            member_count=12,
        )
        repo = self.portfolio_code_service.register_repository(
            tenant_id=tenant_id,
            name="uzaii-develop-by-norths",
            provider="GITHUB",
            default_branch="main",
            primary_language="Python / TypeScript",
            is_private=True,
        )

        # 2. Pull Request & Code Quality
        pr = self.portfolio_code_service.create_pull_request(
            tenant_id=tenant_id,
            repository_id=repo.repo_id,
            pr_number=142,
            title="feat(phase-61): unified engineering & technical operations OS",
            author="staff-architect@uzaii.com",
            source_branch="feat/phase-61-engineering-os",
            target_branch="main",
            linked_work_item="REQ-ENG-6101",
            files_changed_count=22,
            additions=1450,
            deletions=45,
        )
        self.portfolio_code_service.evaluate_code_quality(
            tenant_id=tenant_id,
            repository_id=repo.repo_id,
            commit_sha="c7f8a9e01234",
            static_analysis_score=96.5,
            test_coverage_pct=92.4,
            cyclomatic_complexity_avg=3.8,
            code_duplication_pct=1.2,
            dependency_vulnerability_count=0,
        )

        # 3. Service Catalog & API
        srv = self.architecture_service.register_service(
            tenant_id=tenant_id,
            name="decision-fabric-service",
            service_tier="TIER_0",
            owner_team=team.name,
            runtime="FASTAPI_PYTHON_311",
            target_slo_availability=99.99,
            dependencies=["postgres-primary", "redis-session", "kafka-cluster"],
        )
        self.architecture_service.register_api_contract(
            tenant_id=tenant_id,
            service_id=srv.service_id,
            name="Decision Fabric REST API",
            version="v1",
        )

        # 4. Environments & CI/CD
        self.environments_service.register_environment(
            tenant_id=tenant_id,
            name="PRODUCTION",
            is_production=True,
            cluster_region="us-east-1",
        )
        pipe = self.cicd_service.register_pipeline(
            tenant_id=tenant_id,
            repository_id=repo.repo_id,
            name="Production CI/CD Release Pipeline",
        )
        self.cicd_service.trigger_pipeline_run(
            tenant_id=tenant_id,
            pipeline_id=pipe.pipe_id,
            commit_sha="c7f8a9e01234",
        )

        # 5. Deployment & Release Readiness
        self.deployments_service.execute_deployment(
            tenant_id=tenant_id,
            service_id=srv.service_id,
            environment="PRODUCTION",
            strategy="CANARY",
            version_tag="v2.4.0",
            commit_sha="c7f8a9e01234",
            operator_email="release-manager@uzaii.com",
            approved_by="vp-eng@uzaii.com",
        )
        self.deployments_service.evaluate_release_readiness_gate(
            tenant_id=tenant_id,
            version_tag="v2.4.0",
            service_name=srv.name,
        )

        # 6. SRE & Incidents
        self.observability_service.calculate_slo_error_budget(
            tenant_id=tenant_id,
            service_name=srv.name,
            slo_target_pct=99.95,
            measured_uptime_pct=99.98,
        )
        inc = self.observability_service.declare_incident(
            tenant_id=tenant_id,
            title="Transient p99 latency elevation on simulation ingestion stream",
            severity="SEV2",
            affected_service=srv.name,
        )
        self.observability_service.create_postmortem(
            tenant_id=tenant_id,
            incident_id=inc.inc_id,
            root_cause_summary="Connection pool exhaustion resolved by increasing async worker connections.",
            five_whys=[
                "High latency on /simulate endpoint",
                "Requests queued waiting for DB pool connection",
                "Pool exhausted by burst telemetry job",
                "Burst job was unthrottled during peak hour",
                "Missing rate limiter on async backfill worker",
            ],
            corrective_actions=[
                {"action": "Rate limit backfill worker to 250 rps", "status": "COMPLETED"},
                {"action": "Increase DB pool size from 20 to 50", "status": "COMPLETED"},
            ],
        )

        # 7. DORA, FinOps & Risks
        self.dora_finops_service.calculate_dora_metrics(
            tenant_id=tenant_id,
            deployment_frequency_per_day=4.8,
            lead_time_for_changes_hours=1.9,
            change_failure_rate_pct=1.2,
            time_to_restore_service_minutes=18.0,
        )
        self.dora_finops_service.log_technical_debt_item(
            tenant_id=tenant_id,
            title="Refactor legacy synchronous ingestion worker",
            area="ARCHITECTURE",
            effort_person_days=6.0,
        )
        self.dora_finops_service.record_cloud_finops_cost(
            tenant_id=tenant_id,
            service_name=srv.name,
            monthly_cost_usd=16800.0,
            waste_estimate_usd=1400.0,
        )
        self.twin_copilot_service.log_engineering_risk(
            tenant_id=tenant_id,
            category="DELIVERY",
            title="Kafka partition rebalance latency during node upgrade",
            probability=0.25,
            impact_score=6.5,
        )

    def get_overview_metrics(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        """Aggregate executive level engineering operating system overview."""
        repos = [r for r in self.portfolio_code_service._repositories.values() if r.get("tenant_id") == tenant_id]
        prs = [p for p in self.portfolio_code_service._pull_requests.values() if p.get("tenant_id") == tenant_id]
        services = [s for s in self.architecture_service._services.values() if s.get("tenant_id") == tenant_id]
        deployments = [d for d in self.deployments_service._deployments.values() if d.get("tenant_id") == tenant_id]
        incidents = [i for i in self.observability_service._incidents.values() if i.get("tenant_id") == tenant_id]
        vulns = [v for v in self.changes_service._vulnerabilities.values() if v.get("tenant_id") == tenant_id]
        costs = [c for c in self.dora_finops_service._cloud_costs.values() if c.get("tenant_id") == tenant_id]
        tech_debt = [t for t in self.dora_finops_service._tech_debt.values() if t.get("tenant_id") == tenant_id]

        total_cloud_cost = sum(c.get("monthly_cost_usd", 0.0) for c in costs)
        active_incidents = len([i for i in incidents if i.get("status") in ["DETECTED", "MITIGATED"]])

        dora = self.dora_finops_service.calculate_dora_metrics(tenant_id)

        return {
            "tenant_id": tenant_id,
            "repositories_count": len(repos),
            "open_pull_requests_count": len([p for p in prs if p.get("status") == "OPEN"]),
            "services_count": len(services),
            "deployments_count": len(deployments),
            "active_incidents_count": active_incidents,
            "open_vulnerabilities_count": len([v for v in vulns if v.get("status") == "OPEN"]),
            "technical_debt_items_count": len(tech_debt),
            "monthly_cloud_cost_usd": round(total_cloud_cost, 2),
            "dora_performance_tier": dora.dora_performance_tier,
            "deployment_frequency_per_day": dora.deployment_frequency_per_day,
            "change_failure_rate_pct": dora.change_failure_rate_pct,
            "time_to_restore_service_minutes": dora.time_to_restore_service_minutes,
            "system_health": "OPTIMAL",
            "last_evaluated": datetime.now(timezone.utc).isoformat(),
        }

    def query_developer_copilot(self, tenant_id: str, query: str) -> Dict[str, Any]:
        """Delegates query to conversational Developer Copilot."""
        return self.twin_copilot_service.query_developer_copilot(tenant_id, query)
