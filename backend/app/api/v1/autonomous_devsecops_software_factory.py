"""
API Router for Phase 67 — Autonomous DevSecOps, AI Software Factory, CI/CD Intelligence & Self-Healing Engineering.
Mounted at /devsecops-software-factory.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from backend.app.core.database import get_db
except ImportError:
    from app.core.database import get_db

from backend.app.services.engineering.service import AutonomousDevSecOpsSoftwareFactoryService
from backend.app.schemas.autonomous_devsecops_software_factory import (
    DsopsProjectCreate,
    DsopsProjectResponse,
    DsopsRepositoryRegister,
    DsopsRepositoryResponse,
    DsopsTaskPlanCreate,
    DsopsTaskPlanResponse,
    DsopsCodeGenerationRequest,
    DsopsCodeGenerationResponse,
    DsopsCodeReviewRequest,
    DsopsCodeReviewResponse,
    DsopsTestRunRequest,
    DsopsTestRunResponse,
    DsopsPipelineCreate,
    DsopsPipelineResponse,
    DsopsBuildRequest,
    DsopsBuildResponse,
    DsopsArtifactProvenanceCreate,
    DsopsArtifactProvenanceResponse,
    DsopsReleaseCreate,
    DsopsReleaseResponse,
    DsopsDeploymentCreate,
    DsopsDeploymentResponse,
    DsopsServiceCatalogCreate,
    DsopsServiceCatalogResponse,
    DsopsSloCreate,
    DsopsSloResponse,
    DsopsIncidentCreate,
    DsopsIncidentResponse,
    DsopsRunbookCreate,
    DsopsRunbookResponse,
    DsopsRunbookExecuteRequest,
    DsopsAgentApprovalCreate,
    DsopsAgentApprovalResponse,
    DsopsCycleRunRequest,
    DsopsCycleRunResponse,
)

router = APIRouter(
    prefix="/devsecops-software-factory",
    tags=["Phase 67 — Autonomous DevSecOps & AI Software Factory"]
)


def get_factory_service(db: Session = Depends(get_db)) -> AutonomousDevSecOpsSoftwareFactoryService:
    return AutonomousDevSecOpsSoftwareFactoryService(db)


# 1. Health & Command Center Summary
@router.get("/health", response_model=Dict[str, Any])
def get_factory_health(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    summary = service.get_command_center_summary(tenant_id)
    return {
        "status": "HEALTHY",
        "platform": "Autonomous DevSecOps, AI Software Factory & Self-Healing Engineering",
        "telemetry": summary,
    }


@router.get("/command-center/summary", response_model=Dict[str, Any])
def get_command_center_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.get_command_center_summary(tenant_id)


# 2. Projects Management
@router.post("/projects", response_model=Dict[str, Any])
def create_project(
    req: DsopsProjectCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.projects.create_project(
        name=req.name,
        description=req.description,
        owner=req.owner,
        team=req.team,
        repository_url=req.repository_url,
        architecture_tier=req.architecture_tier,
        tenant_id=tenant_id
    )


@router.get("/projects", response_model=List[Dict[str, Any]])
def list_projects(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.projects.list_projects(tenant_id)


# 3. Repositories Intelligence
@router.post("/repositories", response_model=Dict[str, Any])
def register_repository(
    req: DsopsRepositoryRegister,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.repositories.register_repository(
        project_id=req.project_id,
        name=req.name,
        vcs_type=req.vcs_type,
        default_branch=req.default_branch,
        primary_language=req.primary_language,
        tenant_id=tenant_id
    )


@router.get("/repositories", response_model=List[Dict[str, Any]])
def list_repositories(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.repositories.list_repositories(tenant_id)


# 4. Codebase Knowledge Graph & Engineering Search
@router.post("/graph/nodes", response_model=Dict[str, Any])
def add_graph_node(
    node_data: Dict[str, Any],
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.code_intelligence.index_graph_node(
        repository_id=node_data.get("repository_id", "default_repo"),
        node_type=node_data.get("node_type", "FILE"),
        node_identifier=node_data.get("node_identifier", "src/main.py"),
        symbol_name=node_data.get("symbol_name"),
        semantic_embedding=node_data.get("semantic_embedding"),
        relationships=node_data.get("relationships", {}),
        metadata=node_data.get("metadata", {}),
        tenant_id=tenant_id
    )


@router.get("/search", response_model=Dict[str, Any])
def search_engineering_assets(
    query: str = Query(..., description="Semantic or keyword query across code, issues, PRs, architecture"),
    mode: str = Query("SEMANTIC"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.code_intelligence.search_codebase(query=query, mode=mode, tenant_id=tenant_id)


# 5. Requirements Intelligence & AI Task Planning
@router.post("/tasks/plan", response_model=Dict[str, Any])
def plan_engineering_task(
    req: DsopsTaskPlanCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.planning.formulate_plan(
        requirement_id=req.requirement_id,
        project_id=req.project_id,
        title=req.title,
        description=req.description,
        tenant_id=tenant_id
    )


# 6. Sandbox Code Generation
@router.post("/sandbox/code-generation", response_model=Dict[str, Any])
def execute_sandbox_code_generation(
    req: DsopsCodeGenerationRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.code_changes.execute_sandbox_generation(
        plan_id=req.plan_id,
        file_path=req.file_path,
        prompt_instruction=req.prompt_instruction,
        tenant_id=tenant_id
    )


# 7. 9-Factor Multi-Dimensional Code Review
@router.post("/reviews", response_model=Dict[str, Any])
def review_code_change(
    req: DsopsCodeReviewRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.review.evaluate_pull_request(
        pull_request_id=req.pull_request_id,
        code_diff=req.code_diff,
        tenant_id=tenant_id
    )


# 8. Test Intelligence & Flakiness Tracking
@router.post("/tests/runs", response_model=Dict[str, Any])
def run_tests(
    req: DsopsTestRunRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.testing.execute_test_suite(
        test_suite_id=req.test_suite_id,
        environment=req.environment,
        tenant_id=tenant_id
    )


# 9. Pipelines & Builds
@router.post("/pipelines", response_model=Dict[str, Any])
def create_pipeline(
    req: DsopsPipelineCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.pipelines.create_pipeline(
        project_id=req.project_id,
        repository_id=req.repository_id,
        name=req.name,
        trigger_event=req.trigger_event,
        stages=req.stages,
        tenant_id=tenant_id
    )


@router.post("/builds", response_model=Dict[str, Any])
def trigger_build(
    req: DsopsBuildRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.builds.trigger_build(
        pipeline_run_id=req.pipeline_run_id,
        source_commit_sha=req.source_commit_sha,
        tenant_id=tenant_id
    )


# 10. Artifact Provenance (Supply Chain)
@router.post("/artifacts/provenance", response_model=Dict[str, Any])
def register_artifact_provenance(
    req: DsopsArtifactProvenanceCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.provenance.record_provenance(
        artifact_id=req.artifact_id,
        requirement_id=req.requirement_id,
        commit_sha=req.commit_sha,
        build_id=req.build_id,
        sbom_digest=req.sbom_digest,
        cryptographic_signature=req.cryptographic_signature,
        tenant_id=tenant_id
    )


# 11. Releases & Progressive Deployment
@router.post("/releases", response_model=Dict[str, Any])
def create_release(
    req: DsopsReleaseCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.releases.create_release(
        project_id=req.project_id,
        version=req.version,
        artifact_id=req.artifact_id,
        deployment_strategy=req.deployment_strategy,
        tenant_id=tenant_id
    )


@router.post("/deployments", response_model=Dict[str, Any])
def trigger_deployment(
    req: DsopsDeploymentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.deployment.trigger_deployment(
        release_id=req.release_id,
        environment=req.environment,
        strategy=req.strategy,
        tenant_id=tenant_id
    )


@router.post("/deployments/{deployment_id}/rollback", response_model=Dict[str, Any])
def rollback_deployment(
    deployment_id: str,
    reason: str = Query("Automated health regression detected"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.deployment.execute_rollback(deployment_id=deployment_id, reason=reason, tenant_id=tenant_id)


# 12. Service Catalog, SLOs & Error Budgets
@router.post("/services/catalog", response_model=Dict[str, Any])
def register_service(
    req: DsopsServiceCatalogCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.services.register_service(
        name=req.name,
        tier=req.tier,
        owner_team=req.owner_team,
        repository_id=req.repository_id,
        dependencies=req.dependencies,
        tenant_id=tenant_id
    )


@router.post("/services/slo", response_model=Dict[str, Any])
def create_slo(
    req: DsopsSloCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.slo.create_slo(
        service_id=req.service_id,
        name=req.name,
        target_percentage=req.target_percentage,
        time_window=req.time_window,
        tenant_id=tenant_id
    )


# 13. Incident Management & Automated RCA
@router.post("/incidents", response_model=Dict[str, Any])
def report_incident(
    req: DsopsIncidentCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.incidents.report_incident(
        service_id=req.service_id,
        title=req.title,
        severity=req.severity,
        symptoms=req.symptoms,
        tenant_id=tenant_id
    )


# 14. Governed Runbooks & Self-Healing
@router.post("/runbooks", response_model=Dict[str, Any])
def create_runbook(
    req: DsopsRunbookCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.runbooks.create_runbook(
        title=req.title,
        target_service=req.target_service,
        steps=req.steps,
        tenant_id=tenant_id
    )


@router.post("/runbooks/execute", response_model=Dict[str, Any])
def execute_runbook(
    req: DsopsRunbookExecuteRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.remediation.execute_runbook(
        runbook_id=req.runbook_id,
        incident_id=req.incident_id,
        parameters=req.parameters,
        approval_id=req.approval_id,
        tenant_id=tenant_id
    )


# 15. Agent Human Approvals Gate
@router.post("/agent-approvals", response_model=Dict[str, Any])
def submit_agent_approval(
    req: DsopsAgentApprovalCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.agent_approvals.record_approval_decision(
        approval_id=req.approval_id,
        decision=req.decision,
        approver=req.approver,
        notes=req.notes,
        tenant_id=tenant_id
    )


# 16. DORA Metrics & Engineering Analytics
@router.get("/metrics/dora", response_model=Dict[str, Any])
def get_dora_metrics(
    project_id: str = Query("default_project"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.engineering_analytics.calculate_dora_metrics(project_id=project_id, tenant_id=tenant_id)


# 17. Master End-to-End Autonomous Software Factory Cycle
@router.post("/cycle/run", response_model=Dict[str, Any])
def run_autonomous_software_factory_cycle(
    req: DsopsCycleRunRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousDevSecOpsSoftwareFactoryService = Depends(get_factory_service)
):
    return service.run_software_factory_cycle(
        project_name=req.project_name,
        requirement_title=req.requirement_title,
        service_name=req.service_name,
        tenant_id=tenant_id
    )
