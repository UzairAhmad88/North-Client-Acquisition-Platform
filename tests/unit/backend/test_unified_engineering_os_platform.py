"""Unit Tests for Phase 61: Unified Engineering, SDLC, DevOps, CI/CD & Technical Operations OS Platform."""

import pytest
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
)
from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
from backend.app.services.engineering_os.base import (
    EnvironmentType,
    DeploymentStrategy,
    IncidentSeverity,
    ChangeRiskLevel,
    PullRequestStatus,
    ServiceHealthState,
)
from agents.engineering_os import (
    ArchitectureAgent,
    CodeReviewAgent,
    CicdDeploymentAgent,
    TestingQualityAgent,
    SreObservabilityAgent,
    IncidentResponseAgent,
    SecurityDependencyAgent,
    DoraFinopsAgent,
    DoraFinOpsAgent,
    DeveloperCopilotAgent,
)


class TestPortfolioRepositoriesCodeQuality:
    def test_organization_and_teams(self):
        service = EngineeringOperatingSystemService()
        org = service.portfolio_code_service.create_organization(
            tenant_id="t1",
            name="Global Engineering",
            slug="global-eng",
            description="Global engineering team",
            head_of_engineering_email="vp-eng@uzaii.com",
        )
        assert org.name == "Global Engineering"
        assert org.slug == "global-eng"

        team = service.portfolio_code_service.create_team(
            tenant_id="t1",
            org_id=org.org_id,
            name="Platform SRE",
            team_type="SRE",
            lead_email="sre-lead@uzaii.com",
            member_count=8,
        )
        assert team.name == "Platform SRE"
        assert team.member_count == 8

    def test_repository_and_branch_protection(self):
        service = EngineeringOperatingSystemService()
        repo = service.portfolio_code_service.register_repository(
            tenant_id="t1",
            name="payment-processor",
            provider="GITHUB",
            default_branch="main",
            primary_language="Python / FastAPI",
            is_private=True,
        )
        assert repo.name == "payment-processor"
        assert repo.branch_protection_rules["require_pull_request"] is True
        assert repo.branch_protection_rules["require_ci_pass"] is True

    def test_pull_request_and_code_quality(self):
        service = EngineeringOperatingSystemService()
        repo = service.portfolio_code_service.register_repository(
            tenant_id="t1", name="auth-service"
        )
        pr = service.portfolio_code_service.create_pull_request(
            tenant_id="t1",
            repository_id=repo.repo_id,
            pr_number=201,
            title="Implement mTLS Auth",
            author="sec@uzaii.com",
            source_branch="feature/mtls",
            target_branch="main",
            linked_work_item="REQ-SEC-01",
            files_changed_count=5,
            additions=120,
            deletions=10,
        )
        assert pr.title == "Implement mTLS Auth"
        assert pr.status == "OPEN"
        assert pr.risk_score > 0

        # Submit review
        review = service.portfolio_code_service.submit_code_review(
            tenant_id="t1",
            pr_id=pr.pr_id,
            reviewer_email="staff-eng@uzaii.com",
            decision="APPROVED",
            architecture_notes="Architecture and tests look solid.",
        )
        assert review.decision == "APPROVED"

        # Evaluate quality scorecard
        scorecard = service.portfolio_code_service.evaluate_code_quality(
            tenant_id="t1",
            repository_id=repo.repo_id,
            commit_sha="a1b2c3d4",
            static_analysis_score=92.0,
            test_coverage_pct=86.5,
            cyclomatic_complexity_avg=4.0,
            code_duplication_pct=1.2,
            dependency_vulnerability_count=0,
        )
        assert scorecard.composite_quality_score > 80.0
        assert scorecard.quality_grade in ["A", "B"]


class TestArchitectureServicesApisDatabases:
    def test_service_catalog_and_slo(self):
        service = EngineeringOperatingSystemService()
        svc = service.architecture_service.register_service(
            tenant_id="t1",
            name="user-profile-service",
            service_tier="TIER_1",
            owner_team="Core Backend",
            runtime="FASTAPI_PYTHON_311",
            target_slo_availability=99.95,
            dependencies=["postgres-main", "redis-cache"],
            description="User profile and authentication state service",
        )
        assert svc.name == "user-profile-service"
        assert svc.target_slo_availability == 99.95

    def test_api_catalog_and_database(self):
        service = EngineeringOperatingSystemService()
        api = service.architecture_service.register_api_contract(
            tenant_id="t1",
            service_id="srv_user",
            name="User Profile API",
            version="v2.1",
            protocol="REST_OPENAPI",
            auth_mechanism="BEARER_JWT",
            rate_limit_rpm=1200,
            is_deprecated=False,
        )
        assert api.name == "User Profile API"
        assert api.rate_limit_rpm == 1200

        db = service.architecture_service.register_database_catalog(
            tenant_id="t1",
            engine="POSTGRESQL_15",
            name="users_db_primary",
            environment="PRODUCTION",
            data_classification="CONFIDENTIAL_PII",
            backup_retention_days=30,
            is_encrypted=True,
        )
        assert db.engine == "POSTGRESQL_15"
        assert db.is_encrypted is True


class TestEnvironmentsInfrastructureIac:
    def test_environment_and_secret_masking(self):
        service = EngineeringOperatingSystemService()
        env = service.environments_service.register_environment(
            tenant_id="t1",
            name="PRODUCTION",
            is_production=True,
            cluster_region="us-east-1",
            access_tier="RESTRICTED_VP_APPROVAL",
        )
        assert env.name == "PRODUCTION"
        assert env.is_production is True
        assert env.status == "READY"

    def test_iac_module(self):
        service = EngineeringOperatingSystemService()
        iac = service.environments_service.register_iac_module(
            tenant_id="t1",
            name="eks-cluster-module",
            iac_framework="TERRAFORM",
            version="v3.2.0",
            target_environment="PRODUCTION",
            has_drift=False,
        )
        assert iac.name == "eks-cluster-module"
        assert iac.has_drift is False


class TestCicdBuildsDeploymentsReleaseReadiness:
    def test_cicd_pipeline_and_provenance(self):
        service = EngineeringOperatingSystemService()
        pipe = service.cicd_service.register_pipeline(
            tenant_id="t1",
            repository_id="repo_core",
            name="core-ci-cd-main",
            pipeline_type="CI_BUILD_TEST_DEPLOY",
        )
        assert pipe.name == "core-ci-cd-main"
        assert len(pipe.stages) == 5

        art = service.cicd_service.register_container_artifact(
            tenant_id="t1",
            image_name="uzaii/core-api",
            tag="v2.4.0",
            digest_sha256="sha256:abcd1234efgh5678",
            size_mb=185.0,
            security_scan_status="CLEAN_0_CVE",
        )
        assert art.tag == "v2.4.0"
        assert art.security_scan_status == "CLEAN_0_CVE"

    def test_deployment_and_release_readiness_gate(self):
        service = EngineeringOperatingSystemService()
        dep = service.deployments_service.execute_deployment(
            tenant_id="t1",
            service_id="srv_core",
            environment="PRODUCTION",
            strategy=DeploymentStrategy.CANARY.value,
            version_tag="v2.4.0",
            commit_sha="a1b2c3d4e5f6",
            operator_email="release-manager@uzaii.com",
            approved_by="vp-eng@uzaii.com",
        )
        assert dep.strategy == "CANARY"
        assert dep.status == "DEPLOYED"
        assert dep.traffic_weight_pct == 10

        readiness = service.deployments_service.evaluate_release_readiness_gate(
            tenant_id="t1",
            version_tag="v2.4.0",
            service_name="core-service",
        )
        assert readiness.version_tag == "v2.4.0"
        assert readiness.is_approved_for_release is True
        assert readiness.readiness_pct == 100.0



class TestTestingPerformanceObservabilityIncidents:
    def test_test_suites_and_flakiness(self):
        service = EngineeringOperatingSystemService()
        suite = service.testing_service.record_test_run_summary(
            tenant_id="t1",
            suite_name="Regression Integration Suite",
            total_tests=150,
            passed_count=148,
            failed_count=2,
            flaky_count=1,
            duration_seconds=84.2,
        )
        assert suite.passed_count == 148
        assert suite.pass_rate_pct > 98.0

        flaky = service.testing_service.detect_flaky_test(
            tenant_id="t1",
            test_identifier="tests.api.test_payment_timeout",
            execution_count=50,
            flip_count=6,
        )
        assert flaky.is_quarantined is True
        assert flaky.flakiness_pct == 12.0

    def test_sre_slo_error_budget_and_incidents(self):
        service = EngineeringOperatingSystemService()
        budget = service.observability_service.calculate_slo_error_budget(
            tenant_id="t1",
            service_name="payment-service",
            slo_target_pct=99.9,
            measured_uptime_pct=99.85,
            timeframe_days=30,
        )
        assert budget.remaining_budget_pct < 100.0
        assert budget.burn_rate > 1.0

        incident = service.observability_service.declare_incident(
            tenant_id="t1",
            title="Elevated 504 Gateway Timeouts in Payment Mesh",
            severity=IncidentSeverity.SEV1.value,
            affected_service="payment-service",
            incident_commander="sre-oncall@uzaii.com",
        )
        assert incident.severity == "SEV1"
        assert incident.status == "DETECTED"

        # 5-Whys postmortem
        postmortem = service.observability_service.create_postmortem(
            tenant_id="t1",
            incident_id=incident.inc_id,
            root_cause_summary="Redis connection pool exhaustion during sudden downstream latency spike",
            five_whys=[
                "Payment mesh timed out",
                "Redis connection pool ran out of available connections",
                "Pool size was hardcoded to 50 instead of dynamic scaling",
                "Recent PR removed max-wait-timeout on pool acquisition",
                "Review gate lacked automated connection pool linting",
            ],
            corrective_actions=[{"action": "Increase pool size"}, {"action": "Add pool timeout"}],
        )
        assert postmortem.root_cause_summary != ""
        assert len(postmortem.five_whys) == 5


class TestChangesMigrationsSupplyChainFinOps:
    def test_change_risk_and_database_migration(self):
        service = EngineeringOperatingSystemService()
        change = service.changes_service.submit_change_request(
            tenant_id="t1",
            title="Migrate User Shard to Postgres 16",
            change_type="DATABASE_INFRASTRUCTURE",
            risk_level=ChangeRiskLevel.HIGH.value,
            rollback_plan="Execute down-migration script and restore WAL snapshot",
            owner_email="dba-lead@uzaii.com",
        )
        assert change.risk_level == "HIGH"
        assert change.status == "PENDING_CAB_APPROVAL"

    def test_secret_detection_and_vulnerabilities(self):
        service = EngineeringOperatingSystemService()
        # Test secret scanning with masking
        raw_code = 'AWS_SECRET_KEY = "AKIA1234567890EXAMPLE"'
        findings = service.changes_service.scan_for_secret_leaks(raw_code)
        assert findings["has_secret_leak"] is True
        assert findings["findings_count"] > 0
        # Ensure secret value is masked
        assert "AKIA1234567890EXAMPLE" not in str(findings["findings"])

        vuln = service.changes_service.record_vulnerability(
            tenant_id="t1",
            cve_id="CVE-2026-4412",
            package_name="cryptography",
            current_version="41.0.1",
            fixed_version="42.0.0",
            severity="HIGH",
            status="OPEN",
        )
        assert vuln.cve_id == "CVE-2026-4412"

    def test_dora_metrics_and_finops(self):
        service = EngineeringOperatingSystemService()
        dora = service.dora_finops_service.calculate_dora_metrics(
            tenant_id="t1",
            timeframe_days=30,
            deployment_frequency_per_day=4.2,
            lead_time_for_changes_hours=3.5,
            change_failure_rate_pct=4.1,
            time_to_restore_service_minutes=45.0,
        )
        assert dora.dora_performance_tier == "ELITE"

        finops = service.dora_finops_service.record_cloud_finops_cost(
            tenant_id="t1",
            service_name="decision-room-cluster",
            environment="PRODUCTION",
            monthly_cost_usd=14500.0,
            waste_estimate_usd=1800.0,
            cost_trend_pct=-4.2,
        )
        assert finops.monthly_cost_usd == 14500.0
        assert finops.waste_estimate_usd == 1800.0


class TestDeveloperCopilotAndSimulations:
    def test_developer_copilot_grounded_response(self):
        service = EngineeringOperatingSystemService()
        resp = service.twin_copilot_service.query_developer_copilot(
            tenant_id="t1",
            query="Why did the build fail on the payment service pipeline?",
        )
        assert "FACT" in resp["response"]
        assert len(resp["evidence_sources"]) > 0
        assert resp["confidence"] > 0.8
        assert "require human authorization" in resp["governance_notice"]

    def test_digital_twin_simulation(self):
        service = EngineeringOperatingSystemService()
        sim = service.twin_copilot_service.run_engineering_twin_simulation(
            tenant_id="t1",
            scenario_type="TRAFFIC_SPIKE_5X",
            parameters={"traffic_multiplier": 3.0, "duration_minutes": 30},
        )
        assert sim.scenario_type == "TRAFFIC_SPIKE_5X"
        assert sim.simulated_outcomes["projected_p99_latency_ms"] > 0


class TestEngineeringAiWorkforceAndPermissions:
    @pytest.mark.asyncio
    async def test_agents_permission_and_execution(self):
        ctx = AgentContext(
            workflow_id="wf_eng_01",
            task_id="task_eng_01",
            agent_run_id="run_eng_01",
            metadata={"tenant_id": "test_tenant", "name": "auth-service", "query": "Find risky changes"},
        )

        agents = [
            ArchitectureAgent(),
            CodeReviewAgent(),
            CicdDeploymentAgent(),
            TestingQualityAgent(),
            SreObservabilityAgent(),
            IncidentResponseAgent(),
            SecurityDependencyAgent(),
            DoraFinopsAgent(),
            DoraFinOpsAgent(),
            DeveloperCopilotAgent(),
        ]

        for agent in agents:
            # Validate permissions against platform permission definitions
            validate_agent_permissions(agent.permissions)
            assert len(agent.permissions) > 0

            # Execute agent task
            result = await agent.execute(ctx)
            assert result is not None
            assert result.get("status") == "COMPLETED"

    def test_prohibited_actions_enforcement(self):
        agent = CicdDeploymentAgent()

        # Prohibited actions cannot be granted
        prohibited_ops = [
            "AUTONOMOUS_MERGE_PULL_REQUEST",
            "AUTONOMOUS_DEPLOY_PRODUCTION",
            "AUTONOMOUS_EXECUTE_DATABASE_MIGRATION",
            "AUTONOMOUS_DELETE_PRODUCTION_INFRASTRUCTURE",
            "BYPASS_CHANGE_APPROVAL_GATE",
            "EXPOSE_SECRET_VALUES",
        ]
        for op in prohibited_ops:
            assert op not in [p.value for p in agent.permissions]
