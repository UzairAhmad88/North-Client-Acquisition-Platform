"""Unit Test Suite for Phase 64 — Autonomous Engineering OS & AI Software Factory."""

import pytest
import pytest_asyncio
from typing import Any, Dict

from backend.app.services.autonomous_engineering_os.service import AutonomousEngineeringOsService
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
    check_tool_permission,
    PROHIBITED_PERMISSIONS,
)
from agents.autonomous_engineering_os import (
    EngineeringPlannerAgent,
    EngineeringArchitectureAgent,
    SandboxedCodingAgent,
    EngineeringCodeReviewAgent,
    EngineeringTestingAgent,
    SecuritySbomAgent,
    CicdDeploymentAgent,
    SreObservabilityAgent,
    IncidentSelfHealingAgent,
    EngineeringFinopsAgent,
    SoftwareFactoryCopilotAgent,
)


@pytest.fixture(scope="module")
def service():
    """Create AutonomousEngineeringOsService instance for test suite."""
    return AutonomousEngineeringOsService()


class TestProjectsRequirementsAndSpecifications:
    """Test Workspaces, Requirements, Acceptance Criteria, and Spec Generation."""

    def test_workspace_creation_and_listing(self, service):
        tenant = "tenant_eng_test_01"

        workspace = service.projects_requirements.create_project_workspace(
            tenant_id=tenant,
            name="Autonomous Agent Runtime",
            owner="sarah.architect@uzaii.internal",
            team="Platform AI",
            tech_stack=["Python", "FastAPI", "Docker"],
            budget_allocated_usd=30000.0,
        )

        assert workspace.id.startswith("eng_proj_")
        assert workspace.name == "Autonomous Agent Runtime"
        assert workspace.status == "ACTIVE"
        assert workspace.budget_allocated_usd == 30000.0

        workspaces = service.projects_requirements.list_project_workspaces(tenant)
        assert len(workspaces) >= 1

    def test_requirement_creation_and_ambiguity_scoring(self, service):
        tenant = "tenant_eng_test_01"
        workspace = service.projects_requirements.list_project_workspaces(tenant)[0]

        req = service.projects_requirements.create_requirement(
            tenant_id=tenant,
            project_id=workspace.id,
            title="Deterministic Memory Limits for Sandboxed Containers",
            description="Enforce cgroups v2 memory bounds (max 4GB) and cpu limits (2 vCPU) for agent containers.",
            owner="sarah.architect@uzaii.internal",
            requirement_type="SECURITY",
            priority="CRITICAL",
        )

        assert req.id.startswith("eng_req_")
        assert req.priority == "CRITICAL"
        assert req.ambiguity_score <= 0.10

    def test_acceptance_criteria_and_spec_synthesis(self, service):
        tenant = "tenant_eng_test_01"
        req = service.projects_requirements.list_requirements(tenant)[0]

        criteria = service.projects_requirements.add_acceptance_criteria(
            tenant_id=tenant,
            requirement_id=req.id,
            given_clause="An agent sandbox container is spawned",
            when_clause="Memory consumption exceeds 4096 MB",
            then_clause="Kernel OOM killer terminates the task without impacting host OS",
            is_automated_test_created=True,
        )

        assert criteria.id.startswith("eng_crit_")
        assert criteria.is_automated_test_created is True

        spec = service.projects_requirements.generate_technical_specification(tenant, req.id)
        assert spec["spec_id"].startswith("eng_spec_")
        assert spec["acceptance_criteria_count"] == 1
        assert len(spec["security_requirements"]) >= 3


class TestArchitectureAndCodeIntelligence:
    """Test Architecture Registry, Topology Graph, and Code Symbols Indexing."""

    def test_architecture_registration_and_graph(self, service):
        tenant = "tenant_eng_test_01"
        workspace = service.projects_requirements.list_project_workspaces(tenant)[0]

        comp = service.architecture_code.register_architecture_component(
            tenant_id=tenant,
            project_id=workspace.id,
            name="Agent Sandbox Gateway",
            component_type="SERVICE",
            owner_team="Platform AI",
            runtime_environment="KUBERNETES",
            slo_target_latency_p95_ms=45.0,
            slo_target_availability_pct=99.98,
            dependencies=["PostgreSQL", "Redis EventBus"],
        )

        assert comp.id.startswith("eng_arch_")
        assert comp.slo_target_availability_pct == 99.98

        graph = service.architecture_code.get_architecture_graph(tenant, workspace.id)
        assert graph["total_nodes"] >= 1
        assert graph["total_edges"] >= 2

    def test_code_repository_and_symbol_indexing(self, service):
        tenant = "tenant_eng_test_01"

        repo = service.architecture_code.register_code_repository(
            tenant_id=tenant,
            name="ai-agent-gateway",
            language="Python",
        )
        assert repo.id.startswith("eng_repo_")

        symbol = service.architecture_code.index_code_symbol(
            tenant_id=tenant,
            repository_id=repo.id,
            name="execute_sandboxed_task",
            file_path="backend/app/services/sandbox.py",
            symbol_type="FUNCTION",
            line_start=10,
            line_end=45,
            docstring="Executes code in isolated cgroup sandbox.",
        )
        assert symbol.id.startswith("eng_sym_")

        results = service.architecture_code.search_code_symbols(tenant, "execute_sandboxed")
        assert len(results) >= 1
        assert results[0].name == "execute_sandboxed_task"


class TestTaskPlannerAndSandboxedCoding:
    """Test Requirement-to-Task Decomposition and Sandboxed Agent Coding Execution."""

    def test_task_planning_from_requirement(self, service):
        tenant = "tenant_eng_test_01"
        req = service.projects_requirements.list_requirements(tenant)[0]

        tasks = service.tasks_sandbox.plan_tasks_from_requirement(tenant, req.id)
        assert len(tasks) == 3
        assert any(t.assigned_agent == "coding_agent" for t in tasks)
        assert any(t.assigned_agent == "testing_agent" for t in tasks)

    def test_sandboxed_coding_session_execution(self, service):
        tenant = "tenant_eng_test_01"
        tasks = service.tasks_sandbox.list_tasks(tenant)
        target_task = tasks[0]

        session = service.tasks_sandbox.execute_sandboxed_coding_session(
            tenant_id=tenant,
            task_id=target_task.id,
            agent_id="coding_agent",
            modified_files=["backend/app/services/sandbox.py", "tests/unit/test_sandbox.py"],
            diff_additions=54,
            diff_deletions=4,
            tokens_used=4200,
        )

        assert session.id.startswith("eng_sess_")
        assert session.status == "COMPLETED"
        assert session.unit_tests_passed is True
        assert session.security_checks_passed is True
        assert session.session_cost_usd > 0


class TestPullRequestsAndAiCodeReview:
    """Test Pull Request Lifecycle, 6-Dimension Risk Scorecard, and Merging."""

    def test_pull_request_creation_and_risk_scorecard(self, service):
        tenant = "tenant_eng_test_01"
        repos = service.architecture_code.list_code_repositories(tenant)
        repo = repos[0]
        sessions = service.tasks_sandbox.list_coding_sessions(tenant)
        sess = sessions[0]

        pr = service.pull_requests.create_pull_request(
            tenant_id=tenant,
            repository_id=repo.id,
            title="feat: implement cgroups v2 memory bounds for agent sandbox",
            source_branch=sess.branch_created,
            author="coding_agent",
            task_id=sess.task_id,
            session_id=sess.id,
        )

        assert pr.id.startswith("eng_pr_")
        assert pr.status == "OPEN"
        assert 0.0 <= pr.risk_score_composite <= 1.0
        assert "security_risk" in pr.risk_breakdown_json
        assert "performance_risk" in pr.risk_breakdown_json

    def test_ai_code_review_generation_and_authorized_merge(self, service):
        tenant = "tenant_eng_test_01"
        prs = service.pull_requests.list_pull_requests(tenant)
        pr = prs[0]

        review = service.pull_requests.generate_ai_code_review(tenant, pr.id)
        assert review["review_status"] == "APPROVED_BY_AI"
        assert review["findings_count"] >= 1

        merged_pr = service.pull_requests.merge_pull_request(tenant, pr.id, merged_by="lead_engineer@uzaii.com")
        assert merged_pr.status == "MERGED"
        assert merged_pr.is_merged is True
        assert merged_pr.merged_by == "lead_engineer@uzaii.com"


class TestCicdTestingAndSecuritySbom:
    """Test Multi-Stage Pipelines, Test Impact Analysis, and SBOM Security Gates."""

    def test_cicd_pipeline_and_build_execution(self, service):
        tenant = "tenant_eng_test_01"
        repo = service.architecture_code.list_code_repositories(tenant)[0]

        pipeline = service.ci_cd.create_pipeline(
            tenant_id=tenant,
            repository_id=repo.id,
            pipeline_name="Main Container Build & Test",
        )
        assert pipeline.id.startswith("eng_pipe_")

        build = service.ci_cd.execute_build_run(
            tenant_id=tenant,
            pipeline_id=pipeline.id,
            commit_sha="a1b2c3d4e5f6",
            branch="main",
            build_number=1,
            duration_seconds=32.4,
            status="SUCCESS",
        )
        assert build.id.startswith("eng_build_")
        assert build.status == "SUCCESS"
        assert len(build.artifacts_generated) >= 1

    def test_testing_suite_and_impact_analysis(self, service):
        tenant = "tenant_eng_test_01"
        repo = service.architecture_code.list_code_repositories(tenant)[0]

        suite = service.testing.register_test_suite(
            tenant_id=tenant,
            repository_id=repo.id,
            suite_name="Unit & Integration Suite",
            suite_type="UNIT",
            total_tests=180,
            passed_tests=180,
            failed_tests=0,
            flaky_rate_pct=0.0,
            duration_seconds=15.0,
        )
        assert suite.id.startswith("eng_test_")
        assert suite.flaky_rate_pct == 0.0

        impact = service.testing.run_test_impact_analysis(
            tenant_id=tenant,
            repository_id=repo.id,
            changed_files=["backend/app/services/sandbox.py"],
        )
        assert impact["changed_files_count"] == 1
        assert len(impact["selected_test_suites"]) >= 1

    def test_sbom_registration_and_supply_chain_scan(self, service):
        tenant = "tenant_eng_test_01"
        repo = service.architecture_code.list_code_repositories(tenant)[0]

        pkg = service.security_sbom.register_sbom_package(
            tenant_id=tenant,
            repository_id=repo.id,
            package_name="pydantic",
            version="2.6.4",
            license_type="MIT",
            is_license_compliant=True,
            vulnerabilities_count=0,
        )
        assert pkg.id.startswith("eng_sbom_")

        scan = service.security_sbom.run_software_supply_chain_scan(tenant, repo.id)
        assert scan["total_packages_scanned"] >= 1
        assert scan["total_vulnerabilities"] == 0
        assert scan["security_gate_passed"] is True


class TestDeploymentsSreAndSelfHealing:
    """Test Canary Deployments, SRE SLO Error Budgets, RCA, and Runbook Remediation."""

    def test_deployment_verification_and_rollback(self, service):
        tenant = "tenant_eng_test_01"

        dep = service.deployments.create_deployment(
            tenant_id=tenant,
            service_name="Agent Execution Gateway",
            version="v2.5.0",
            strategy="CANARY",
            traffic_weight_pct=10.0,
        )
        assert dep.id.startswith("eng_deploy_")
        assert dep.verification_status == "PENDING_VERIFICATION"

        verified_dep = service.deployments.verify_deployment(
            tenant_id=tenant,
            deployment_id=dep.id,
            synthetic_error_rate_pct=0.005,
            synthetic_latency_p95_ms=36.0,
        )
        assert verified_dep.verification_status == "VERIFIED"
        assert verified_dep.traffic_weight_pct == 100.0

        rolled_back = service.deployments.rollback_deployment(tenant, dep.id)
        assert rolled_back.status == "ROLLED_BACK"
        assert rolled_back.traffic_weight_pct == 0.0

    def test_service_catalog_and_slo_burn_rate(self, service):
        tenant = "tenant_eng_test_01"

        srv = service.observability_sre.register_service_catalog_entry(
            tenant_id=tenant,
            name="Agent Execution Gateway",
            owner_team="Platform AI",
            slo_target_availability_pct=99.95,
            current_availability_pct=99.98,
            error_budget_remaining_pct=85.0,
            p95_latency_ms=29.0,
        )
        assert srv.id.startswith("eng_srv_")
        assert srv.status == "HEALTHY"

        burn = service.observability_sre.calculate_error_budget_burn_rate(tenant, srv.id)
        assert burn["release_policy_decision"] == "ALLOWED"
        assert burn["error_budget_remaining_pct"] == 85.0

    def test_incident_and_policy_checked_self_healing(self, service):
        tenant = "tenant_eng_test_01"

        incident = service.incidents_self_healing.create_incident(
            tenant_id=tenant,
            service_name="Agent Execution Gateway",
            title="504 Gateway Timeout Spike during Canary Rollout",
            severity="SEV2",
            correlated_root_cause="Telemetry correlation indicates connection pool saturation on PostgreSQL.",
        )
        assert incident.id.startswith("eng_inc_")
        assert incident.remediation_status == "INVESTIGATING"

        runbook = service.incidents_self_healing.register_self_healing_runbook(
            tenant_id=tenant,
            name="Automated Instant Canary Rollback",
            trigger_condition="5XX_SPIKE_POST_CANARY",
            target_service="Agent Execution Gateway",
            action_type="CANARY_ROLLBACK",
            is_autonomous_approved=True,
        )
        assert runbook.id.startswith("eng_runb_")

        remediation = service.incidents_self_healing.execute_self_healing_remediation(
            tenant_id=tenant,
            incident_id=incident.id,
            runbook_id=runbook.id,
        )
        assert remediation["remediation_status"] == "REMEDIATED"
        assert remediation["action_executed"] == "CANARY_ROLLBACK"


class TestFinopsDigitalTwinAndCopilot:
    """Test FinOps Cost Allocation, Digital Twin Simulation, and Software Factory Copilot."""

    def test_finops_cost_recording_and_rollup(self, service):
        tenant = "tenant_eng_test_01"
        workspace = service.projects_requirements.list_project_workspaces(tenant)[0]

        cost = service.finops_twin.record_finops_cost(
            tenant_id=tenant,
            project_id=workspace.id,
            cost_category="CI_BUILD_MINUTES",
            amount_usd=25.50,
            units_consumed=510.0,
        )
        assert cost.id.startswith("eng_cost_")
        assert cost.amount_usd == 25.50

    def test_digital_twin_scenario_simulation(self, service):
        tenant = "tenant_eng_test_01"

        sim = service.finops_twin.simulate_digital_twin_scenario(
            tenant_id=tenant,
            scenario_type="TRAFFIC_SPIKE_3X",
            target_service="Agent Execution Gateway",
            simulated_parameters={"traffic_multiplier": 3.0},
        )
        assert sim["scenario_id"].startswith("eng_scen_")
        assert sim["predicted_metrics"]["p95_latency_ms"] > 32.0
        assert "recommendation" in sim

    def test_software_factory_copilot_queries(self, service):
        tenant = "tenant_eng_test_01"

        resp = service.finops_twin.ask_software_factory_copilot(
            tenant_id=tenant,
            query="What is the current SLO and incident health?",
        )
        assert resp["category"] == "RELIABILITY"
        assert len(resp["citations"]) >= 1

    def test_command_center_aggregated_metrics(self, service):
        tenant = "tenant_eng_test_01"

        metrics = service.get_engineering_command_center_metrics(tenant)
        assert metrics["status"] == "OPERATIONAL"
        assert metrics["active_projects_count"] >= 1
        assert metrics["requirements_count"] >= 1
        assert metrics["total_build_runs_count"] >= 1


class TestAiWorkforceAgentsAndSafetyProhibitions:
    """Test AI Agents execution, permission boundaries, and safety prohibitions."""

    @pytest.mark.asyncio
    async def test_engineering_planner_agent_run(self):
        agent = EngineeringPlannerAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_planner",
            task_id="task_eng_planner",
            agent_run_id="run_eng_planner",
            metadata={"tenant_id": "test_tenant", "requirement_title": "Distributed Caching Layer"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["decomposed_tasks_count"] == 3

    @pytest.mark.asyncio
    async def test_engineering_architecture_agent_run(self):
        agent = EngineeringArchitectureAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_arch",
            task_id="task_eng_arch",
            agent_run_id="run_eng_arch",
            metadata={"tenant_id": "test_tenant", "service_name": "payment-router"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["topology_status"] == "VALIDATED"

    @pytest.mark.asyncio
    async def test_sandboxed_coding_agent_run(self):
        agent = SandboxedCodingAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_coding",
            task_id="task_eng_coding",
            agent_run_id="run_eng_coding",
            metadata={"tenant_id": "test_tenant", "task_id": "task_12345"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["sandboxed_execution_status"] == "SUCCESS"

    @pytest.mark.asyncio
    async def test_engineering_code_review_agent_run(self):
        agent = EngineeringCodeReviewAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_review",
            task_id="task_eng_review",
            agent_run_id="run_eng_review",
            metadata={"tenant_id": "test_tenant", "pr_id": "pr_12345"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert "composite_risk_score" in res.result

    @pytest.mark.asyncio
    async def test_engineering_testing_agent_run(self):
        agent = EngineeringTestingAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_test",
            task_id="task_eng_test",
            agent_run_id="run_eng_test",
            metadata={"tenant_id": "test_tenant", "repository_id": "repo_01"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["coverage_estimate_pct"] > 90.0

    @pytest.mark.asyncio
    async def test_security_sbom_agent_run(self):
        agent = SecuritySbomAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_sec",
            task_id="task_eng_sec",
            agent_run_id="run_eng_sec",
            metadata={"tenant_id": "test_tenant", "repository_id": "repo_01"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["security_gate_status"] == "PASSED"

    @pytest.mark.asyncio
    async def test_incident_self_healing_agent_run(self):
        agent = IncidentSelfHealingAgent()
        ctx = AgentContext(
            workflow_id="wf_eng_incident",
            task_id="task_eng_incident",
            agent_run_id="run_eng_incident",
            metadata={"tenant_id": "test_tenant", "incident_id": "inc_01"},
        )
        res = await agent.run(ctx)
        assert res.status == "completed"
        assert res.result["mitigation_action"] == "CANARY_ROLLBACK"

    def test_prohibited_permissions_safety_enforcement(self):
        """Ensure prohibited actions raise AgentPermissionDeniedError."""
        prohibited_actions = [
            "AUTONOMOUS_MERGE_PR",
            "AUTONOMOUS_DEPLOY_PRODUCTION_UNCHECKED",
            "AUTONOMOUS_EXECUTE_DESTRUCTIVE_REMEDIATION",
            "AUTONOMOUS_MODIFY_SECURITY_POLICY",
            "BYPASS_CI_TEST_SUITE",
            "BYPASS_SECURITY_SCAN",
            "EXPOSE_SECRET_CREDENTIALS",
            "FABRICATE_TEST_RESULTS",
        ]

        for action in prohibited_actions:
            assert action in PROHIBITED_PERMISSIONS
            with pytest.raises(AgentPermissionDeniedError):
                validate_agent_permissions({action})

            with pytest.raises(AgentPermissionDeniedError):
                check_tool_permission(set(), action)
