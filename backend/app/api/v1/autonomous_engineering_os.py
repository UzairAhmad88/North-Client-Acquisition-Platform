"""Phase 64 — Autonomous Engineering OS & Software Factory FastAPI Router."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.autonomous_engineering_os import (
    EngineeringProjectWorkspaceCreate,
    EngineeringRequirementCreate,
    RequirementAcceptanceCriteriaCreate,
    ArchitectureComponentCreate,
    CodeRepositoryCreate,
    CodeSymbolCreate,
    TaskPlanningRequest,
    SandboxedCodingRequest,
    PullRequestCreate,
    MergePullRequestRequest,
    CiPipelineCreate,
    CiBuildRunCreate,
    TestSuiteCreate,
    TestImpactRequest,
    SbomPackageCreate,
    DeploymentCreate,
    VerifyDeploymentRequest,
    ServiceCatalogEntryCreate,
    IncidentCreate,
    SelfHealingRunbookCreate,
    ExecuteSelfHealingRequest,
    FinopsCostCreate,
    DigitalTwinSimulationRequest,
    SoftwareFactoryCopilotRequest,
)
from backend.app.services.autonomous_engineering_os.service import AutonomousEngineeringOsService

router = APIRouter(prefix="/engineering-factory", tags=["Autonomous Engineering OS & AI Software Factory"])


def get_service(db: Session = Depends(get_db)) -> AutonomousEngineeringOsService:
    return AutonomousEngineeringOsService(db)


@router.get("/overview", response_model=Dict[str, Any])
async def get_command_center_overview(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    """Retrieve top-level Engineering Command Center metrics."""
    return service.get_engineering_command_center_metrics(tenant_id)


# Projects & Requirements
@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: EngineeringProjectWorkspaceCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.projects_requirements.create_project_workspace(
        tenant_id=tenant_id,
        name=payload.name,
        owner=payload.owner,
        team=payload.team,
        description=payload.description,
        repository_url=payload.repository_url,
        tech_stack=payload.tech_stack,
        budget_allocated_usd=payload.budget_allocated_usd,
    )


@router.get("/projects")
async def list_projects(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.projects_requirements.list_project_workspaces(tenant_id)


@router.post("/requirements", status_code=status.HTTP_201_CREATED)
async def create_requirement(
    payload: EngineeringRequirementCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.projects_requirements.create_requirement(
        tenant_id=tenant_id,
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        owner=payload.owner,
        requirement_type=payload.requirement_type,
        priority=payload.priority,
        dependencies=payload.dependencies,
    )


@router.get("/requirements")
async def list_requirements(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.projects_requirements.list_requirements(tenant_id, project_id)


@router.post("/requirements/acceptance-criteria", status_code=status.HTTP_201_CREATED)
async def add_acceptance_criteria(
    payload: RequirementAcceptanceCriteriaCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.projects_requirements.add_acceptance_criteria(
        tenant_id=tenant_id,
        requirement_id=payload.requirement_id,
        given_clause=payload.given_clause,
        when_clause=payload.when_clause,
        then_clause=payload.then_clause,
        is_automated_test_created=payload.is_automated_test_created,
    )


@router.get("/requirements/{requirement_id}/technical-spec")
async def get_technical_specification(
    requirement_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.projects_requirements.generate_technical_specification(tenant_id, requirement_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Architecture & Code Intelligence
@router.post("/architecture/components", status_code=status.HTTP_201_CREATED)
async def register_architecture_component(
    payload: ArchitectureComponentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.register_architecture_component(
        tenant_id=tenant_id,
        project_id=payload.project_id,
        name=payload.name,
        component_type=payload.component_type,
        owner_team=payload.owner_team,
        runtime_environment=payload.runtime_environment,
        slo_target_latency_p95_ms=payload.slo_target_latency_p95_ms,
        slo_target_availability_pct=payload.slo_target_availability_pct,
        dependencies=payload.dependencies,
    )


@router.get("/architecture/components")
async def list_architecture_components(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.list_architecture_components(tenant_id, project_id)


@router.get("/architecture/graph")
async def get_architecture_graph(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.get_architecture_graph(tenant_id, project_id)


@router.post("/repositories", status_code=status.HTTP_201_CREATED)
async def register_repository(
    payload: CodeRepositoryCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.register_code_repository(
        tenant_id=tenant_id,
        name=payload.name,
        organization=payload.organization,
        provider=payload.provider,
        default_branch=payload.default_branch,
        language=payload.language,
    )


@router.post("/code-symbols", status_code=status.HTTP_201_CREATED)
async def index_symbol(
    payload: CodeSymbolCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.index_code_symbol(
        tenant_id=tenant_id,
        repository_id=payload.repository_id,
        name=payload.name,
        file_path=payload.file_path,
        symbol_type=payload.symbol_type,
        line_start=payload.line_start,
        line_end=payload.line_end,
        docstring=payload.docstring,
        called_by=payload.called_by,
        calls=payload.calls,
    )


@router.get("/code-symbols/search")
async def search_symbols(
    q: str = Query(..., description="Symbol query"),
    symbol_type: Optional[str] = Query(None),
    repository_id: Optional[str] = Query(None),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.architecture_code.search_code_symbols(tenant_id, q, symbol_type, repository_id)


# Task Planner & Sandboxed Coding Agent
@router.post("/tasks/plan-from-requirement", status_code=status.HTTP_201_CREATED)
async def plan_tasks(
    payload: TaskPlanningRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.tasks_sandbox.plan_tasks_from_requirement(
            tenant_id=tenant_id,
            requirement_id=payload.requirement_id,
            task_breakdown=payload.task_breakdown,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/tasks")
async def list_tasks(
    tenant_id: str = Query("default_tenant"),
    requirement_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.tasks_sandbox.list_tasks(tenant_id, requirement_id, status_filter)


@router.post("/coding-sessions/execute", status_code=status.HTTP_201_CREATED)
async def execute_coding_session(
    payload: SandboxedCodingRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.tasks_sandbox.execute_sandboxed_coding_session(
            tenant_id=tenant_id,
            task_id=payload.task_id,
            agent_id=payload.agent_id,
            modified_files=payload.modified_files,
            diff_additions=payload.diff_additions,
            diff_deletions=payload.diff_deletions,
            tokens_used=payload.tokens_used,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/coding-sessions")
async def list_coding_sessions(
    tenant_id: str = Query("default_tenant"),
    task_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.tasks_sandbox.list_coding_sessions(tenant_id, task_id)


# Pull Requests & Code Reviews
@router.post("/pull-requests", status_code=status.HTTP_201_CREATED)
async def create_pull_request(
    payload: PullRequestCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.pull_requests.create_pull_request(
        tenant_id=tenant_id,
        repository_id=payload.repository_id,
        title=payload.title,
        source_branch=payload.source_branch,
        author=payload.author,
        task_id=payload.task_id,
        target_branch=payload.target_branch,
        session_id=payload.session_id,
    )


@router.get("/pull-requests")
async def list_pull_requests(
    tenant_id: str = Query("default_tenant"),
    repository_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.pull_requests.list_pull_requests(tenant_id, repository_id, status_filter)


@router.post("/pull-requests/{pr_id}/ai-review")
async def review_pull_request(
    pr_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.pull_requests.generate_ai_code_review(tenant_id, pr_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/pull-requests/{pr_id}/merge")
async def merge_pull_request(
    pr_id: str,
    payload: MergePullRequestRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.pull_requests.merge_pull_request(tenant_id, pr_id, payload.merged_by)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# CI/CD & Builds
@router.post("/ci-cd/pipelines", status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    payload: CiPipelineCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.ci_cd.create_pipeline(
        tenant_id=tenant_id,
        repository_id=payload.repository_id,
        pipeline_name=payload.pipeline_name,
        trigger_event=payload.trigger_event,
        stages=payload.stages,
    )


@router.get("/ci-cd/pipelines")
async def list_pipelines(
    tenant_id: str = Query("default_tenant"),
    repository_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.ci_cd.list_pipelines(tenant_id, repository_id)


@router.post("/ci-cd/build-runs", status_code=status.HTTP_201_CREATED)
async def execute_build(
    payload: CiBuildRunCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.ci_cd.execute_build_run(
            tenant_id=tenant_id,
            pipeline_id=payload.pipeline_id,
            commit_sha=payload.commit_sha,
            branch=payload.branch,
            build_number=payload.build_number,
            duration_seconds=payload.duration_seconds,
            status=payload.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/ci-cd/build-runs")
async def list_build_runs(
    tenant_id: str = Query("default_tenant"),
    pipeline_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.ci_cd.list_build_runs(tenant_id, pipeline_id)


# Testing Platform & Impact Analysis
@router.post("/testing/suites", status_code=status.HTTP_201_CREATED)
async def register_test_suite(
    payload: TestSuiteCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.testing.register_test_suite(
        tenant_id=tenant_id,
        repository_id=payload.repository_id,
        suite_name=payload.suite_name,
        suite_type=payload.suite_type,
        total_tests=payload.total_tests,
        passed_tests=payload.passed_tests,
        failed_tests=payload.failed_tests,
        flaky_rate_pct=payload.flaky_rate_pct,
        duration_seconds=payload.duration_seconds,
    )


@router.get("/testing/suites")
async def list_test_suites(
    tenant_id: str = Query("default_tenant"),
    repository_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.testing.list_test_suites(tenant_id, repository_id)


@router.post("/testing/impact-analysis")
async def analyze_test_impact(
    payload: TestImpactRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.testing.run_test_impact_analysis(tenant_id, payload.repository_id, payload.changed_files)


# Security Pipeline & SBOM
@router.post("/security/sbom-packages", status_code=status.HTTP_201_CREATED)
async def register_sbom_package(
    payload: SbomPackageCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.security_sbom.register_sbom_package(
        tenant_id=tenant_id,
        repository_id=payload.repository_id,
        package_name=payload.package_name,
        version=payload.version,
        license_type=payload.license_type,
        is_license_compliant=payload.is_license_compliant,
        vulnerabilities_count=payload.vulnerabilities_count,
    )


@router.get("/security/sbom-packages")
async def list_sbom_packages(
    tenant_id: str = Query("default_tenant"),
    repository_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.security_sbom.list_sbom_packages(tenant_id, repository_id)


@router.post("/security/supply-chain-scan")
async def scan_supply_chain(
    repository_id: str = Query(...),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.security_sbom.run_software_supply_chain_scan(tenant_id, repository_id)


# Deployments & Verification
@router.post("/deployments", status_code=status.HTTP_201_CREATED)
async def create_deployment(
    payload: DeploymentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.deployments.create_deployment(
        tenant_id=tenant_id,
        service_name=payload.service_name,
        version=payload.version,
        environment=payload.environment,
        strategy=payload.strategy,
        traffic_weight_pct=payload.traffic_weight_pct,
        rollback_target_version=payload.rollback_target_version,
    )


@router.get("/deployments")
async def list_deployments(
    tenant_id: str = Query("default_tenant"),
    service_name: Optional[str] = Query(None),
    environment: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.deployments.list_deployments(tenant_id, service_name, environment)


@router.post("/deployments/{deployment_id}/verify")
async def verify_deployment(
    deployment_id: str,
    payload: VerifyDeploymentRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.deployments.verify_deployment(
            tenant_id=tenant_id,
            deployment_id=deployment_id,
            synthetic_error_rate_pct=payload.synthetic_error_rate_pct,
            synthetic_latency_p95_ms=payload.synthetic_latency_p95_ms,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/deployments/{deployment_id}/rollback")
async def rollback_deployment(
    deployment_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.deployments.rollback_deployment(tenant_id, deployment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Observability & SRE SLO
@router.post("/service-catalog", status_code=status.HTTP_201_CREATED)
async def register_service(
    payload: ServiceCatalogEntryCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.observability_sre.register_service_catalog_entry(
        tenant_id=tenant_id,
        name=payload.name,
        owner_team=payload.owner_team,
        repository_id=payload.repository_id,
        slo_target_availability_pct=payload.slo_target_availability_pct,
        current_availability_pct=payload.current_availability_pct,
        error_budget_remaining_pct=payload.error_budget_remaining_pct,
        p95_latency_ms=payload.p95_latency_ms,
    )


@router.get("/service-catalog")
async def list_service_catalog(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.observability_sre.list_service_catalog(tenant_id)


@router.get("/service-catalog/{service_id}/error-budget")
async def get_error_budget_burn(
    service_id: str,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.observability_sre.calculate_error_budget_burn_rate(tenant_id, service_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Incidents & Self-Healing
@router.post("/incidents", status_code=status.HTTP_201_CREATED)
async def create_incident(
    payload: IncidentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.incidents_self_healing.create_incident(
        tenant_id=tenant_id,
        service_name=payload.service_name,
        title=payload.title,
        severity=payload.severity,
        description=payload.description,
        correlated_root_cause=payload.correlated_root_cause,
    )


@router.get("/incidents")
async def list_incidents(
    tenant_id: str = Query("default_tenant"),
    service_name: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.incidents_self_healing.list_incidents(tenant_id, service_name, severity)


@router.post("/self-healing/runbooks", status_code=status.HTTP_201_CREATED)
async def register_runbook(
    payload: SelfHealingRunbookCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.incidents_self_healing.register_self_healing_runbook(
        tenant_id=tenant_id,
        name=payload.name,
        trigger_condition=payload.trigger_condition,
        target_service=payload.target_service,
        action_type=payload.action_type,
        is_autonomous_approved=payload.is_autonomous_approved,
    )


@router.get("/self-healing/runbooks")
async def list_runbooks(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.incidents_self_healing.list_self_healing_runbooks(tenant_id)


@router.post("/self-healing/execute")
async def execute_remediation(
    payload: ExecuteSelfHealingRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    try:
        return service.incidents_self_healing.execute_self_healing_remediation(
            tenant_id=tenant_id,
            incident_id=payload.incident_id,
            runbook_id=payload.runbook_id,
        )
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# FinOps & Digital Twin
@router.post("/finops/costs", status_code=status.HTTP_201_CREATED)
async def record_finops_cost(
    payload: FinopsCostCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.finops_twin.record_finops_cost(
        tenant_id=tenant_id,
        project_id=payload.project_id,
        cost_category=payload.cost_category,
        amount_usd=payload.amount_usd,
        units_consumed=payload.units_consumed,
        period_date=payload.period_date,
    )


@router.get("/finops/costs")
async def list_finops_costs(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = Query(None),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.finops_twin.list_finops_costs(tenant_id, project_id)


@router.post("/digital-twin/simulate")
async def simulate_scenario(
    payload: DigitalTwinSimulationRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.finops_twin.simulate_digital_twin_scenario(
        tenant_id=tenant_id,
        scenario_type=payload.scenario_type,
        target_service=payload.target_service,
        simulated_parameters=payload.simulated_parameters,
    )


@router.post("/copilot/query")
async def ask_copilot(
    payload: SoftwareFactoryCopilotRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousEngineeringOsService = Depends(get_service),
):
    return service.finops_twin.ask_software_factory_copilot(tenant_id, payload.query)
