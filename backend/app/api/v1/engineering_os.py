"""Phase 61: FastAPI Router for Unified Engineering, SDLC, DevOps, CI/CD & Tech Ops OS."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

try:
    from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
except ImportError:
    from app.services.engineering_os.service import EngineeringOperatingSystemService

from backend.app.schemas.engineering_os import (
    OrganizationCreateRequest,
    TeamCreateRequest,
    RepositoryCreateRequest,
    PullRequestCreateRequest,
    CodeReviewSubmitRequest,
    CodeQualityEvaluateRequest,
    ServiceRegisterRequest,
    ApiContractRegisterRequest,
    EnvironmentRegisterRequest,
    PipelineRegisterRequest,
    DeploymentExecuteRequest,
    ReleaseReadinessEvaluateRequest,
    FlakyTestDetectRequest,
    SloBudgetCalculateRequest,
    IncidentDeclareRequest,
    PostmortemCreateRequest,
    ChangeRequestSubmitRequest,
    VulnerabilityRecordRequest,
    SecretScanRequest,
    TechnicalDebtLogRequest,
    DoraMetricsCalculateRequest,
    CloudCostRecordRequest,
    EngineeringRiskLogRequest,
    TwinSimulationRunRequest,
    DeveloperCopilotQueryRequest,
)

router = APIRouter(prefix="/engineering-os", tags=["Engineering Operating System"])
service = EngineeringOperatingSystemService()


@router.get("/overview")
def get_overview(tenant_id: str = Query("default_tenant")):
    """Executive overview metrics for Engineering OS."""
    return service.get_overview_metrics(tenant_id)


# Organizations & Teams
@router.post("/organizations")
def create_organization(req: OrganizationCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.create_organization(
        tenant_id=tenant_id,
        name=req.name,
        slug=req.slug,
        description=req.description,
        head_of_engineering_email=req.head_of_engineering_email,
    )


@router.post("/teams")
def create_team(req: TeamCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.create_team(
        tenant_id=tenant_id,
        org_id=req.org_id,
        name=req.name,
        team_type=req.team_type,
        lead_email=req.lead_email,
        member_count=req.member_count,
    )


# Repositories, PRs & Code Quality
@router.get("/repositories")
def list_repositories(tenant_id: str = Query("default_tenant")):
    return [r for r in service.portfolio_code_service._repositories.values() if r.get("tenant_id") == tenant_id]


@router.post("/repositories")
def register_repository(req: RepositoryCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.register_repository(
        tenant_id=tenant_id,
        project_id=req.project_id,
        name=req.name,
        provider=req.provider,
        default_branch=req.default_branch,
        primary_language=req.primary_language,
        is_private=req.is_private,
    )


@router.get("/pull-requests")
def list_pull_requests(tenant_id: str = Query("default_tenant")):
    return [p for p in service.portfolio_code_service._pull_requests.values() if p.get("tenant_id") == tenant_id]


@router.post("/pull-requests")
def create_pull_request(req: PullRequestCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.create_pull_request(
        tenant_id=tenant_id,
        repository_id=req.repository_id,
        pr_number=req.pr_number,
        title=req.title,
        author=req.author,
        source_branch=req.source_branch,
        target_branch=req.target_branch,
        linked_work_item=req.linked_work_item,
        files_changed_count=req.files_changed_count,
        additions=req.additions,
        deletions=req.deletions,
    )


@router.post("/pull-requests/reviews")
def submit_code_review(req: CodeReviewSubmitRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.submit_code_review(
        tenant_id=tenant_id,
        pr_id=req.pr_id,
        reviewer_email=req.reviewer_email,
        decision=req.decision,
        findings=req.findings,
        security_findings_count=req.security_findings_count,
        architecture_notes=req.architecture_notes,
    )


@router.post("/code-quality/evaluate")
def evaluate_code_quality(req: CodeQualityEvaluateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_code_service.evaluate_code_quality(
        tenant_id=tenant_id,
        repository_id=req.repository_id,
        commit_sha=req.commit_sha,
        static_analysis_score=req.static_analysis_score,
        test_coverage_pct=req.test_coverage_pct,
        cyclomatic_complexity_avg=req.cyclomatic_complexity_avg,
        code_duplication_pct=req.code_duplication_pct,
        dependency_vulnerability_count=req.dependency_vulnerability_count,
    )


# Service Catalog & APIs
@router.get("/services")
def list_services(tenant_id: str = Query("default_tenant")):
    return [s for s in service.architecture_service._services.values() if s.get("tenant_id") == tenant_id]


@router.post("/services")
def register_service(req: ServiceRegisterRequest, tenant_id: str = Query("default_tenant")):
    return service.architecture_service.register_service(
        tenant_id=tenant_id,
        name=req.name,
        service_tier=req.service_tier,
        owner_team=req.owner_team,
        runtime=req.runtime,
        target_slo_availability=req.target_slo_availability,
        dependencies=req.dependencies,
        description=req.description,
    )


@router.post("/apis")
def register_api_contract(req: ApiContractRegisterRequest, tenant_id: str = Query("default_tenant")):
    return service.architecture_service.register_api_contract(
        tenant_id=tenant_id,
        service_id=req.service_id,
        name=req.name,
        version=req.version,
        protocol=req.protocol,
        auth_mechanism=req.auth_mechanism,
        rate_limit_rpm=req.rate_limit_rpm,
        is_deprecated=req.is_deprecated,
    )


# Deployments & Releases
@router.post("/deployments")
def execute_deployment(req: DeploymentExecuteRequest, tenant_id: str = Query("default_tenant")):
    return service.deployments_service.execute_deployment(
        tenant_id=tenant_id,
        service_id=req.service_id,
        environment=req.environment,
        strategy=req.strategy,
        version_tag=req.version_tag,
        commit_sha=req.commit_sha,
        operator_email=req.operator_email,
        approved_by=req.approved_by,
    )


@router.post("/releases/readiness-gate")
def evaluate_release_readiness(req: ReleaseReadinessEvaluateRequest, tenant_id: str = Query("default_tenant")):
    return service.deployments_service.evaluate_release_readiness_gate(
        tenant_id=tenant_id,
        version_tag=req.version_tag,
        service_name=req.service_name,
        checklists=req.checklists,
    )


# Testing & Flakiness
@router.post("/testing/flakiness")
def detect_flaky_test(req: FlakyTestDetectRequest, tenant_id: str = Query("default_tenant")):
    return service.testing_service.detect_flaky_test(
        tenant_id=tenant_id,
        test_identifier=req.test_identifier,
        execution_count=req.execution_count,
        flip_count=req.flip_count,
    )


# SRE & Incidents
@router.post("/sre/slo-budget")
def calculate_slo_budget(req: SloBudgetCalculateRequest, tenant_id: str = Query("default_tenant")):
    return service.observability_service.calculate_slo_error_budget(
        tenant_id=tenant_id,
        service_name=req.service_name,
        slo_target_pct=req.slo_target_pct,
        measured_uptime_pct=req.measured_uptime_pct,
        timeframe_days=req.timeframe_days,
    )


@router.get("/incidents")
def list_incidents(tenant_id: str = Query("default_tenant")):
    return [i for i in service.observability_service._incidents.values() if i.get("tenant_id") == tenant_id]


@router.post("/incidents")
def declare_incident(req: IncidentDeclareRequest, tenant_id: str = Query("default_tenant")):
    return service.observability_service.declare_incident(
        tenant_id=tenant_id,
        title=req.title,
        severity=req.severity,
        affected_service=req.affected_service,
        incident_commander=req.incident_commander,
    )


@router.post("/incidents/postmortems")
def create_postmortem(req: PostmortemCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.observability_service.create_postmortem(
        tenant_id=tenant_id,
        incident_id=req.incident_id,
        root_cause_summary=req.root_cause_summary,
        five_whys=req.five_whys,
        corrective_actions=req.corrective_actions,
        author_email=req.author_email,
    )


# Changes & Security
@router.post("/changes")
def submit_change_request(req: ChangeRequestSubmitRequest, tenant_id: str = Query("default_tenant")):
    return service.changes_service.submit_change_request(
        tenant_id=tenant_id,
        title=req.title,
        change_type=req.change_type,
        risk_level=req.risk_level,
        rollback_plan=req.rollback_plan,
        owner_email=req.owner_email,
    )


@router.post("/security/vulnerabilities")
def record_vulnerability(req: VulnerabilityRecordRequest, tenant_id: str = Query("default_tenant")):
    return service.changes_service.record_vulnerability(
        tenant_id=tenant_id,
        cve_id=req.cve_id,
        package_name=req.package_name,
        current_version=req.current_version,
        fixed_version=req.fixed_version,
        severity=req.severity,
        status=req.status,
    )


@router.post("/security/scan-secrets")
def scan_secrets(req: SecretScanRequest):
    return service.changes_service.scan_for_secret_leaks(req.content_snippet)


# DORA, FinOps & Tech Debt
@router.post("/dora/calculate")
def calculate_dora(req: DoraMetricsCalculateRequest, tenant_id: str = Query("default_tenant")):
    return service.dora_finops_service.calculate_dora_metrics(
        tenant_id=tenant_id,
        timeframe_days=req.timeframe_days,
        deployment_frequency_per_day=req.deployment_frequency_per_day,
        lead_time_for_changes_hours=req.lead_time_for_changes_hours,
        change_failure_rate_pct=req.change_failure_rate_pct,
        time_to_restore_service_minutes=req.time_to_restore_service_minutes,
    )


@router.post("/technical-debt")
def log_technical_debt(req: TechnicalDebtLogRequest, tenant_id: str = Query("default_tenant")):
    return service.dora_finops_service.log_technical_debt_item(
        tenant_id=tenant_id,
        title=req.title,
        area=req.area,
        severity=req.severity,
        effort_person_days=req.effort_person_days,
        remediation_strategy=req.remediation_strategy,
    )


@router.post("/finops/costs")
def record_cloud_cost(req: CloudCostRecordRequest, tenant_id: str = Query("default_tenant")):
    return service.dora_finops_service.record_cloud_finops_cost(
        tenant_id=tenant_id,
        service_name=req.service_name,
        environment=req.environment,
        monthly_cost_usd=req.monthly_cost_usd,
        waste_estimate_usd=req.waste_estimate_usd,
        cost_trend_pct=req.cost_trend_pct,
    )


# Twin Simulation & Copilot
@router.post("/simulations/twin")
def run_twin_simulation(req: TwinSimulationRunRequest, tenant_id: str = Query("default_tenant")):
    return service.twin_copilot_service.run_engineering_twin_simulation(
        tenant_id=tenant_id,
        scenario_type=req.scenario_type,
        parameters=req.parameters,
    )


@router.post("/copilot/query")
def query_developer_copilot(req: DeveloperCopilotQueryRequest):
    return service.query_developer_copilot(tenant_id=req.tenant_id or "default_tenant", query=req.query)
