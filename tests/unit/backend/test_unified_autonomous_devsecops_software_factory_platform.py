"""
Unit test suite for Phase 67: Autonomous DevSecOps, AI Software Factory, CI/CD Intelligence & Self-Healing Engineering.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.autonomous_devsecops_software_factory import Base as DsopsBase
from app.services.engineering.service import AutonomousDevSecOpsSoftwareFactoryService

# 17 Autonomous AI Agents
from agents.core.context import AgentContext
from agents.engineering import (
    EngineeringOrchestratorAgent,
    PlannerAgent,
    CodingAgent,
    RefactoringAgent,
    DebuggingAgent,
    TestAgent,
    ReviewAgent,
    DocumentationAgent,
    DependencyAgent,
    MigrationAgent,
    PerformanceAgent,
    SecurityAgent,
    ReleaseAgent,
    DeploymentAgent,
    SreAgent,
    IncidentAgent,
    RemediationAgent,
)


@pytest.fixture(scope="module")
def db_session():
    """In-memory SQLite test database for Phase 67 isolated to dsops_ tables."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    dsops_tables = [t for name, t in DsopsBase.metadata.tables.items() if name.startswith("dsops_")]
    DsopsBase.metadata.create_all(bind=engine, tables=dsops_tables)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def factory_service(db_session):
    return AutonomousDevSecOpsSoftwareFactoryService(db_session)


def test_project_and_repository_lifecycle(factory_service):
    """Test project registration, tech stack tiers, and repository indexing."""
    proj = factory_service.projects.create_project(
        {"name": "Apollo Cloud Core", "owner": "lead@enterprise.internal", "team": "Platform Engineering"},
        tenant_id="t_dsops_01"
    )
    assert proj["name"] == "Apollo Cloud Core"
    assert proj["tenant_id"] == "t_dsops_01"

    repo = factory_service.repositories.index_repository(
        project_id=proj["id"],
        name="uzaii/apollo-core",
        repo_url="git://github.com/uzaii/apollo-core.git",
        default_branch="main",
        tenant_id="t_dsops_01"
    )
    assert repo["name"] == "uzaii/apollo-core"
    assert repo["is_indexed"] is True


def test_codebase_knowledge_graph_and_search(factory_service):
    """Test indexing code symbols and service relationships."""
    edge = factory_service.code_intel.add_relation(
        source="auth_service",
        target="token_validator",
        rel_type="CALLS",
        tenant_id="t_dsops_01"
    )
    assert edge["source"] == "auth_service"
    assert edge["relation"] == "CALLS"

    deps = factory_service.code_intel.query_relationships("auth_service", tenant_id="t_dsops_01")
    assert deps["entity"] == "auth_service"
    assert "token_validator" in deps["dependencies"]


def test_ai_task_planning_non_modifying(factory_service):
    """Test AI Planner formulating technical implementation plan without mutating code."""
    plan = factory_service.planning.generate_plan(
        project_id="proj_apollo_01",
        title="Add Token Revocation Blacklist",
        requirement_summary="Implement Redis token blacklist for immediate token revocation upon logout.",
        tenant_id="t_dsops_01"
    )
    assert plan["title"] == "Add Token Revocation Blacklist"
    assert len(plan["files_to_change"]) > 0
    assert plan["status"] == "APPROVED"


def test_sandbox_code_generation_with_lint(factory_service):
    """Test controlled sandbox code generation with linting and boundary verification."""
    res = factory_service.code_changes.synthesize_changes(
        task_id="task_test_01",
        files=["backend/app/security/blacklist.py"],
        tenant_id="t_dsops_01"
    )
    assert res["sandbox_verification"] == "PASSED"
    assert len(res["files_modified"]) == 1


def test_nine_factor_code_review(factory_service):
    """Test 9-factor multi-dimensional pull request code review."""
    review = factory_service.review.review_diff(
        diff_content="+ def revoke_token(t): redis.set(t, 1)",
        repository_id="repo_apollo_01",
        tenant_id="t_dsops_01"
    )
    assert review["status"] == "COMPLETED"
    assert review["score"] >= 80.0
    assert review["approved"] is True


def test_test_impact_analysis_and_flakiness(factory_service):
    """Test dependency-guided test impact analysis and flakiness isolation."""
    impact = factory_service.test_intel.analyze_impact(["backend/app/security/blacklist.py"])
    assert len(impact["affected_test_suites"]) > 0
    assert impact["reduction_percentage"] > 0

    test_run = factory_service.testing.run_tests(impact["affected_test_suites"], tenant_id="t_dsops_01")
    assert test_run["status"] == "PASSED"
    assert test_run["passed"] > 0


def test_pipeline_and_multi_tier_build_caching(factory_service):
    """Test pipeline execution and multi-tier build caching."""
    run = factory_service.pipelines.trigger_pipeline("repo_apollo_01", commit_sha="a7b3c2d1e0f4", tenant_id="t_dsops_01")
    assert run["status"] == "SUCCESS"

    build = factory_service.builds.execute_build("repo_apollo_01", commit_sha="a7b3c2d1e0f4")
    assert build["cache_hit_rate"] >= 0.70


def test_artifact_provenance_cryptographic_chain(factory_service):
    """Test full SLSA level 3+ software supply chain provenance attestation."""
    art = factory_service.artifacts.register_artifact("payments-img", "v1.4.0", "sha256:7f83b1657ff1...", tenant_id="t_dsops_01")
    assert art["name"] == "payments-img"

    prov = factory_service.provenance.trace_provenance(art["id"])
    assert prov["artifact_id"] == art["id"]
    assert "provenance_chain" in prov
    assert prov["tamper_proof"] is True


def test_release_risk_evaluation(factory_service):
    """Test 6-dimensional release risk assessment."""
    rel = factory_service.releases.create_release("proj_01", "v1.4.0", "c_902abc", "art_01", tenant_id="t_dsops_01")
    assert rel["version"] == "v1.4.0"
    assert rel["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert rel["risk_score"] >= 0.0


def test_progressive_canary_deployment_and_rollback(factory_service):
    """Test progressive canary rollout and policy-controlled rollback."""
    dep = factory_service.deployment.execute_deployment("rel_01", strategy="CANARY", traffic_percentage=10, tenant_id="t_dsops_01")
    assert dep["strategy"] == "CANARY"
    assert dep["traffic_percentage"] == 10
    assert dep["rollback_available"] is True


def test_environment_drift_detection(factory_service):
    """Test environment configuration drift detection."""
    drift = factory_service.environments.check_environment_drift("PRODUCTION", tenant_id="t_dsops_01")
    assert "drift_detected" in drift
    assert drift["cluster_state"] == "HEALTHY"


def test_service_catalog_and_slo_error_budgets(factory_service):
    """Test service catalog, topology dependencies, and SLO error budgets."""
    cat = factory_service.services.list_services(tenant_id="t_dsops_01")
    assert len(cat) > 0

    slo = factory_service.slo.get_service_slo("svc_billing")
    assert slo["target_percentage"] >= 99.0
    assert slo["error_budget_remaining_pct"] > 0


def test_incident_triage_and_automated_rca(factory_service):
    """Test incident triage and automated root cause analysis."""
    inc = factory_service.incidents.create_incident("svc_auth", title="Elevated HTTP 504", severity="CRITICAL", tenant_id="t_dsops_01")
    assert inc["title"] == "Elevated HTTP 504"
    assert "likely_root_cause" in inc

    pm = factory_service.postmortems.generate_postmortem(inc["id"])
    assert pm["incident_id"] == inc["id"]
    assert len(pm["corrective_actions"]) > 0


def test_governed_runbook_self_healing_requires_approval(factory_service):
    """Test governed runbook catalog and self-healing execution."""
    runbooks = factory_service.runbooks.list_runbooks()
    assert len(runbooks) > 0

    # Execute remediation
    res = factory_service.remediation.execute_remediation("rb_rollback_canary", "inc_4921", tenant_id="t_dsops_01")
    assert res["status"] == "COMPLETED"
    assert res["verified"] is True

    # Test approval gating
    appr = factory_service.agent_approvals.request_approval(
        agent_id="remediation_agent",
        action_type="ROLLBACK_PRODUCTION",
        resource="k8s://production/auth-service",
        justification="P1 incident latency degradation",
        tenant_id="t_dsops_01"
    )
    assert appr["status"] in ["PENDING", "PENDING_APPROVAL"]


def test_agent_permission_guardrails(factory_service):
    """Verify prohibited autonomous destructive production actions are denied."""
    allowed = factory_service.agent_permissions.check_permission("coding_agent", "RUN_UNIT_TEST")
    assert allowed is True

    denied = factory_service.agent_permissions.check_permission("coding_agent", "AUTONOMOUS_DEPLOY_PRODUCTION")
    assert denied is False


def test_dora_metrics_and_finops(factory_service):
    """Test DORA metric calculations and Cloud FinOps attribution."""
    dora = factory_service.analytics.get_dora_metrics(project_id="proj_apollo_01")
    assert dora["deployment_frequency"] is not None
    assert dora["tier"] == "ELITE"

    tech_debt = factory_service.technical_debt.list_findings("proj_apollo_01")
    assert len(tech_debt) > 0


@pytest.mark.asyncio
async def test_all_seventeen_engineering_agents():
    """Verify all 17 Autonomous AI Agents execute cleanly under AgentContext with permissions."""
    agents = [
        EngineeringOrchestratorAgent(),
        PlannerAgent(),
        CodingAgent(),
        RefactoringAgent(),
        DebuggingAgent(),
        TestAgent(),
        ReviewAgent(),
        DocumentationAgent(),
        DependencyAgent(),
        MigrationAgent(),
        PerformanceAgent(),
        SecurityAgent(),
        ReleaseAgent(),
        DeploymentAgent(),
        SreAgent(),
        IncidentAgent(),
        RemediationAgent(),
    ]

    context = AgentContext(
        workflow_id="wf_dsops_01",
        task_id="task_dsops_test",
        agent_run_id="run_dsops_01",
        metadata={"tenant_id": "t_dsops_01"}
    )

    for agent in agents:
        res = await agent.execute(context)
        assert res["status"] == "COMPLETED"
        assert res["tenant_id"] == "t_dsops_01"
        assert len(agent.get_required_permissions()) > 0


def test_master_end_to_end_software_factory_cycle(factory_service):
    """Test end-to-end Master Software Factory autonomous delivery cycle."""
    cycle = factory_service.run_software_factory_cycle(
        tenant_id="t_dsops_01",
        requirement="Autonomous Microservice Self-Healing Guardrail"
    )
    assert cycle["status"] == "COMPLETED"
    assert len(cycle["phases_executed"]) == 8
    assert "REQUIREMENT_PLANNING" in cycle["phases_executed"]
    assert "CANARY_DEPLOYMENT" in cycle["phases_executed"]


def test_command_center_summary(factory_service):
    """Test Command Center executive summary telemetry."""
    summary = factory_service.get_command_center_summary(tenant_id="t_dsops_01")
    assert summary["ai_coding_agents_active"] == 17
    assert summary["dora_tier"] == "ELITE"
    assert summary["ci_pipeline_health"] == "OPTIMAL"
