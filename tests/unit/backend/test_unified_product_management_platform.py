"""
Unit Tests for Phase 56:
Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
"""

import pytest
from typing import Dict, Any

from backend.app.services.product_management.base import (
    ProductType,
    LifecycleStage,
    FeedbackType,
    RequirementCategory,
    RequirementPriority,
    BacklogItemType,
    PrioritizationFramework,
    RoadmapHorizon,
    RoadmapScenario,
    SprintStatus,
    ReleaseReadinessStatus,
    FeatureFlagState,
    ProductHealthStatus,
    SunsetStage,
)
from backend.app.services.product_management.service import (
    ProductManagementPlatformService,
    global_product_management_service,
)
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.core.context import AgentContext
from agents.product_management import (
    ProductManagerAgent,
    RequirementsAgent,
    RoadmapAgent,
    ReleaseReadinessAgent,
    ProductHealthAgent,
    ProductAnalyticsAgent,
)


@pytest.fixture
def product_service():
    """Provides a fresh instance of ProductManagementPlatformService."""
    return ProductManagementPlatformService()


class TestProductPortfolioAndLifecycle:
    def test_create_and_retrieve_product(self, product_service):
        prod = product_service.products.create_product(
            name="Uzaii Logistics AI Platform",
            type="platform",
            description="Continuous route optimization platform",
            target_market="Enterprise 3PL Fleets",
            owner="VP of Product",
        )
        assert prod["id"] is not None
        assert prod["name"] == "Uzaii Logistics AI Platform"
        assert prod["lifecycle_stage"] == "discovery"
        assert prod["health"] == "healthy"

        retrieved = product_service.products.get_product(prod["id"])
        assert retrieved["name"] == "Uzaii Logistics AI Platform"

    def test_lifecycle_stage_transitions(self, product_service):
        prod = product_service.products.create_product(
            name="Uzaii FinOps Intelligence",
            type="software",
            owner="Product Lead",
        )
        updated = product_service.products.transition_lifecycle_stage(
            product_id=prod["id"],
            new_stage="concept",
            actor="Lead PM",
            rationale="Approved discovery validation in Phase 55 gate review",
        )
        assert updated["lifecycle_stage"] == "concept"

        # Invalid transition checks
        with pytest.raises(ValueError):
            product_service.products.transition_lifecycle_stage(
                product_id=prod["id"],
                new_stage="invalid_stage_name",
            )


class TestVisionStrategyAndNorthStar:
    def test_product_vision_and_okrs(self, product_service):
        prod_id = "prod-demo-001"
        vision = product_service.vision_strategy.set_product_vision(
            product_id=prod_id,
            target_customer="Enterprise Tech Operators",
            problem_statement="Fragmented delivery pipelines lead to release rollbacks and orphaned requirements.",
            desired_future_state="Zero-rollback automated continuous delivery OS.",
            value_proposition="Traceable PRDs to release gates with 100% deterministic quality verification.",
            differentiation="Full architectural lineage with AI safety constraints",
            strategic_alignment="Phase 51 Strategic Alignment & Phase 56 Product Operating System",
            success_definition="99.99% successful continuous deployments",
        )
        assert vision["target_customer"] == "Enterprise Tech Operators"

        # Create Objective & Key Result
        obj = product_service.vision_strategy.create_objective(
            product_id=prod_id,
            name="Increase Enterprise Feature Adoption",
            metric="monthly_active_feature_users",
            baseline=150.0,
            target=500.0,
            time_window="Q4-2026",
            confidence=0.88,
        )
        assert obj["id"] is not None
        assert obj["target"] == 500.0

    def test_north_star_metric_registry(self, product_service):
        prod_id = "prod-demo-001"
        metric = product_service.vision_strategy.register_metric(
            product_id=prod_id,
            name="Successful Customer Workflows Completed",
            definition="Count of automated end-to-end continuous deliveries without rollback",
            formula="SUM(deployments_successful_without_incident)",
            source="Continuous Delivery Telemetry",
            owner="Reliability Engineering",
            current_value=4820.0,
            target_value=10000.0,
            is_north_star=True,
        )
        assert metric["is_north_star"] is True
        assert metric["current_value"] == 4820.0


class TestCustomerFeedbackAndClustering:
    def test_feedback_intake_and_theming(self, product_service):
        prod_id = "prod-demo-001"
        fb1 = product_service.feedback_intelligence.ingest_feedback(
            product_id=prod_id,
            source="client",
            feedback_type="feature_request",
            customer_segment="enterprise",
            content="We need real-time streaming webhook notifications on release gate failures.",
            sentiment_score=0.75,
            revenue_impact_usd=50000.0,
        )
        assert fb1["id"] is not None

        fb2 = product_service.feedback_intelligence.ingest_feedback(
            product_id=prod_id,
            source="customer_support",
            feedback_type="bug",
            customer_segment="mid_market",
            content="Deployment logs time out when trace graphs exceed 1000 nodes.",
            sentiment_score=0.20,
            revenue_impact_usd=12000.0,
        )
        assert fb2["id"] is not None

        themes = product_service.feedback_intelligence.cluster_feedback_into_themes(product_id=prod_id)
        assert len(themes) > 0
        assert "theme" in themes[0]
        assert "urgency_level" in themes[0]


class TestRequirementsTraceabilityAndBacklog:
    def test_prd_requirements_and_traceability_matrix(self, product_service):
        prod_id = "prod-demo-001"
        req = product_service.requirements_traceability.create_requirement(
            product_id=prod_id,
            title="Zero Critical Defect Release Gate Validation",
            description="System must block automated release whenever critical defect count > 0.",
            category="security",
            priority="critical",
            acceptance_criteria=[
                "Deterministic gate checks blocking reasons",
                "Human override required if defects present",
            ],
            source="Governance Policy",
        )
        assert req["id"] is not None
        assert req["priority"] == "critical"

        # Check traceability matrix
        matrix = product_service.requirements_traceability.get_traceability_matrix(product_id=prod_id)
        assert matrix["product_id"] == prod_id
        assert "requirements" in matrix
        assert "orphaned_requirements" in matrix
        assert matrix["traceability_score"] >= 0.0

    def test_backlog_epics_features_and_rice_wsjf_scoring(self, product_service):
        prod_id = "prod-demo-001"
        epic = product_service.backlog_prioritization.create_epic(
            product_id=prod_id,
            title="Continuous Release Governance Hub",
            objective="Ensure zero unapproved deployments across production environments",
        )
        assert epic["id"] is not None

        feat = product_service.backlog_prioritization.create_feature(
            product_id=prod_id,
            epic_id=epic["id"],
            title="Deterministic Gate Evaluator",
        )
        assert feat["id"] is not None

        item = product_service.backlog_prioritization.create_backlog_item(
            product_id=prod_id,
            epic_id=epic["id"],
            feature_id=feat["id"],
            title="Implement gate verification engine",
            story_points=5,
        )
        assert item["id"] is not None

        # Score item with RICE: (Reach * Impact * Confidence) / Effort
        rice_score = product_service.backlog_prioritization.score_item(
            item_id=item["id"],
            product_id=prod_id,
            framework="RICE",
            inputs={"reach": 500, "impact": 3.0, "confidence": 0.8, "effort": 5},
        )
        assert rice_score["score"] == (500 * 3.0 * 0.8) / 5  # 240.0
        assert "formula" in rice_score["calculation_breakdown"]

        # Score item with WSJF: Cost of Delay / Job Size
        wsjf_score = product_service.backlog_prioritization.score_item(
            item_id=item["id"],
            product_id=prod_id,
            framework="WSJF",
            inputs={"user_business_value": 8, "time_criticality": 9, "risk_reduction": 7, "job_size": 4},
        )
        assert wsjf_score["score"] == (8 + 9 + 7) / 4  # 6.0


class TestRoadmapsAndCapacityPlanning:
    def test_multi_scenario_roadmaps(self, product_service):
        prod_id = "prod-demo-001"
        roadmap = product_service.roadmaps_capacity.create_roadmap(
            product_id=prod_id,
            title="2026 Core Platform Delivery Roadmap",
            scenario="base_plan",
        )
        assert roadmap["id"] is not None

        item = product_service.roadmaps_capacity.add_roadmap_item(
            roadmap_id=roadmap["id"],
            title="Unified PRD Traceability Engine",
            horizon="now",
            confidence=0.90,
        )
        assert item["id"] is not None
        assert item["horizon"] == "now"

        # Check capacity bottleneck analysis
        cap = product_service.roadmaps_capacity.create_capacity_plan(
            product_id=prod_id,
            team_name="Core Backend Squad",
            available_fte=6.0,
            allocated_fte=7.5,
            period="Q3-2026",
        )
        assert cap["is_overallocated"] is True
        assert cap["bottleneck_risk"] == "CRITICAL"


class TestSprintsReleasesAndDeterministicGates:
    def test_sprint_management(self, product_service):
        prod_id = "prod-demo-001"
        sprint = product_service.sprints_releases.create_sprint(
            product_id=prod_id,
            name="Sprint 56 — Product Platform Foundations",
            capacity_points=45,
        )
        assert sprint["id"] is not None
        assert sprint["status"] == "planning"

        started = product_service.sprints_releases.start_sprint(sprint["id"])
        assert started["status"] == "active"

    def test_deterministic_release_readiness_gate(self, product_service):
        prod_id = "prod-demo-001"
        release = product_service.sprints_releases.create_release(
            product_id=prod_id,
            version="v2.0.0-GA",
            scope_description="Phase 56 Unified Product Management Release",
        )
        assert release["id"] is not None

        # Case A: Blocked by critical defects
        gate_blocked = product_service.sprints_releases.evaluate_release_readiness(
            release_id=release["id"],
            product_id=prod_id,
            qa_passed=True,
            critical_defects=2,
            security_reviewed=True,
            performance_benchmarked=True,
            rollback_tested=True,
        )
        assert gate_blocked["readiness_status"] == "blocked"
        assert len(gate_blocked["blocking_reasons"]) > 0
        assert "critical defect" in gate_blocked["blocking_reasons"][0].lower()

        # Case B: All criteria passing
        gate_ready = product_service.sprints_releases.evaluate_release_readiness(
            release_id=release["id"],
            product_id=prod_id,
            qa_passed=True,
            critical_defects=0,
            security_reviewed=True,
            performance_benchmarked=True,
            rollback_tested=True,
        )
        assert gate_ready["readiness_status"] == "ready"
        assert gate_ready["launch_readiness_score"] == 1.0


class TestDeploymentsFeatureFlagsAndLaunches:
    def test_feature_flags_and_launch_checklist(self, product_service):
        prod_id = "prod-demo-001"
        flag = product_service.deployments_launches.create_flag(
            product_id=prod_id,
            key="enable_ai_prd_traceability",
            state="CANARY",
            rollout_percentage=20,
        )
        assert flag["key"] == "enable_ai_prd_traceability"
        assert flag["rollout_percentage"] == 20

        launch = product_service.deployments_launches.create_launch(
            product_id=prod_id,
            target_release_version="v2.0.0-GA",
            positioning="Next-Gen Continuous Delivery OS",
        )
        assert launch["id"] is not None
        assert "checklist" in launch


class TestAnalyticsExperimentationAndHealth:
    def test_adoption_cohorts_and_experiments(self, product_service):
        prod_id = "prod-demo-001"
        adoption = product_service.analytics_experimentation.get_adoption_overview(prod_id)
        assert "active_users" in adoption
        assert "cohort_retention" in adoption

        exp = product_service.analytics_experimentation.create_experiment(
            product_id=prod_id,
            name="One-Click PRD Traceability UI vs Multi-step Form",
            hypothesis="One-click wizard increases requirement linkage by 35%",
            primary_metric="requirement_linkage_rate",
            guardrail_metrics=["error_rate", "latency"],
        )
        assert exp["id"] is not None
        assert exp["guardrail_metrics"] == ["error_rate", "latency"]

    def test_composite_product_health(self, product_service):
        prod_id = "prod-demo-001"
        health = product_service.health_sunset.record_health_snapshot(
            product_id=prod_id,
            factors={
                "adoption": 0.92,
                "satisfaction": 0.90,
                "reliability": 0.99,
                "velocity": 0.85,
                "revenue": 0.95,
                "security": 1.00,
            },
        )
        assert health["composite_score"] > 0.90
        assert health["status"] == "healthy"


class TestProductCopilot:
    def test_product_copilot_grounded_response(self, product_service):
        res = product_service.query_product_copilot(
            product_id="prod-demo-001",
            query="Why is this feature important?",
        )
        assert "answer" in res
        assert "evidence" in res
        assert res["confidence"] >= 0.85


class TestAgentsAndSecurityGovernance:
    def test_security_permission_boundaries(self):
        # Assert Phase 56 Prohibitions
        assert "AUTONOMOUS_DEPLOY_RELEASE" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_PRICE_CHANGE" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_SUNSET_PRODUCT" in PROHIBITED_PERMISSIONS

        # Assert Phase 56 Permissions
        assert AgentPermission.READ_PRODUCT.value == "READ_PRODUCT"
        assert AgentPermission.CREATE_REQUIREMENT.value == "CREATE_REQUIREMENT"
        assert AgentPermission.PRIORITIZE_BACKLOG.value == "PRIORITIZE_BACKLOG"
        assert AgentPermission.PLAN_RELEASE.value == "PLAN_RELEASE"
        assert AgentPermission.EVALUATE_RELEASE_READINESS.value == "EVALUATE_RELEASE_READINESS"
        assert AgentPermission.EVALUATE_PRODUCT_HEALTH.value == "EVALUATE_PRODUCT_HEALTH"

    @pytest.mark.asyncio
    async def test_product_manager_agent(self, product_service):
        agent = ProductManagerAgent(service=product_service)
        context = AgentContext(
            workflow_id="wf-prod-01",
            task_id="task-prod-01",
            agent_run_id="run-prod-01",
            metadata={
                "product_id": "prod-demo-001",
                "query": "Is this release ready?",
            },
        )
        result = await agent.execute(context)
        assert result["status"] == "SUCCESS"
        assert "copilot_response" in result
        assert "health_summary" in result

    @pytest.mark.asyncio
    async def test_release_readiness_agent(self, product_service):
        agent = ReleaseReadinessAgent(service=product_service)
        context = AgentContext(
            workflow_id="wf-rel-01",
            task_id="task-rel-01",
            agent_run_id="run-rel-01",
            metadata={
                "product_id": "prod-demo-001",
                "release_id": "rel-demo-001",
                "qa_passed": True,
                "critical_defects": 0,
                "security_reviewed": True,
                "performance_benchmarked": True,
                "rollback_tested": True,
            },
        )
        result = await agent.execute(context)
        assert result["status"] == "SUCCESS"
        assert result["is_ready_for_approval"] is True
        assert len(result["blocking_reasons"]) == 0
