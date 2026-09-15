"""Unit Tests for Phase 60: Unified Product Management, Product Intelligence, Roadmap & Lifecycle OS Platform."""

import pytest
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
)
from backend.app.services.product_os.service import ProductOperatingSystemService
from backend.app.services.product_os.base import (
    ProductLifecycleState,
    ProblemValidationStatus,
    PrioritizationFramework,
    RoadmapHorizon,
    ProductHealthState,
    ReleaseStrategy,
    RiskSeverity,
)
from agents.product_os import (
    ProductStrategyAgent,
    CustomerProblemAgent,
    OpportunityScoringAgent,
    RoadmapPrioritizationAgent,
    RequirementsTraceabilityAgent,
    ProductAnalyticsAgent,
    ProductHealthAgent,
    ProductCopilotAgent,
)


class TestPortfolioVisionStrategy:
    def test_product_lifecycle_and_hierarchy(self):
        service = ProductOperatingSystemService()
        prod = service.portfolio_service.create_product(
            tenant_id="test_tenant",
            name="Autonomous Agent Mesh",
            product_line="Agent Operations",
            code="UZAII-MESH-01",
            lifecycle_state=ProductLifecycleState.DISCOVERY.value,
            target_icp="Global 2000 Chief Information Security Officers",
            owner_email="pm-mesh@uzaii.com",
            description="Autonomous multi-agent governance layer.",
        )
        assert prod.name == "Autonomous Agent Mesh"
        assert prod.lifecycle_state == "DISCOVERY"

        pline = service.portfolio_service.create_product_line(
            tenant_id="test_tenant",
            name="Enterprise Core AI",
            description="Tier 1 AI automation line",
        )
        assert pline.name == "Enterprise Core AI"

    def test_vision_and_strategy(self):
        service = ProductOperatingSystemService()
        prod = service.portfolio_service.create_product(
            tenant_id="test_tenant",
            name="Decision Twin Core",
            product_line="Digital Twin",
        )
        vision = service.portfolio_service.create_product_vision(
            tenant_id="test_tenant",
            product_id=prod.product_id,
            target_users="Supply chain & ops directors",
            core_problem="High inventory waste due to unpredictable demand shifts",
            value_proposition="Deterministic discrete-event real-time simulation",
            differentiation="Sub-second scenario evaluation with P10-P90 certainty",
        )
        assert vision.target_users == "Supply chain & ops directors"

        strat = service.portfolio_service.create_product_strategy(
            tenant_id="test_tenant",
            product_id=prod.product_id,
            positioning="Sovereign enterprise simulation platform",
            growth_strategy="Direct sales into Fortune 500 manufacturing",
            product_bets=["Real-time telemetry streaming", "Continuous P10-P90 risk bounds"],
        )
        assert len(strat.product_bets) == 2

    def test_objectives_and_key_results(self):
        service = ProductOperatingSystemService()
        obj = service.portfolio_service.create_objective(
            tenant_id="test_tenant",
            product_id="prod_001",
            title="Accelerate Enterprise Time-to-First-Value",
            timeframe="2026-Q3",
        )
        assert obj.title == "Accelerate Enterprise Time-to-First-Value"

        kr = service.portfolio_service.add_key_result(
            tenant_id="test_tenant",
            objective_id=obj.objective_id,
            title="Reduce onboarding TTFV to under 15 minutes",
            baseline_value=45.0,
            target_value=15.0,
            current_value=22.0,
            unit="minutes",
        )
        assert kr.progress_pct == round(((45.0 - 22.0) / (45.0 - 15.0)) * 100.0, 2)


class TestProblemsFeedbackOpportunities:
    def test_record_problem_and_validation(self):
        service = ProductOperatingSystemService()
        prob = service.problems_feedback_service.record_problem(
            tenant_id="test_tenant",
            product_id="prod_001",
            title="Inability to audit automated multi-agent actions across cloud tenants",
            reported_by_count=24,
            severity="HIGH",
            validation_status=ProblemValidationStatus.VALIDATED.value,
            cost_of_inaction_usd=180000.0,
        )
        assert prob.validation_status == "VALIDATED"
        assert prob.cost_of_inaction_usd == 180000.0

    def test_feedback_theme_clustering(self):
        service = ProductOperatingSystemService()
        service.problems_feedback_service.ingest_feedback_item(
            tenant_id="test_tenant",
            product_id="prod_001",
            source_type="SUPPORT_TICKET",
            raw_content="Audit logging export is too slow for compliance reviews.",
        )
        themes = service.problems_feedback_service.cluster_feedback_themes("test_tenant", "prod_001")
        assert len(themes) > 0
        assert themes[0].theme_name == "Telemetry & Audit Export Performance"

    def test_opportunity_solution_tree_scoring(self):
        service = ProductOperatingSystemService()
        opp = service.problems_feedback_service.create_opportunity(
            tenant_id="test_tenant",
            product_id="prod_001",
            title="Streaming Audit Telemetry Connector",
            customer_value_score=9.0,
            business_value_score=8.5,
            confidence_score=9.0,
            effort_score=4.0,
            strategic_fit_score=9.5,
            revenue_potential_usd=500000.0,
        )
        assert opp.score > 8.0
        assert opp.revenue_potential_usd == 500000.0


class TestPrioritizationAndRoadmaps:
    def test_rice_scoring(self):
        service = ProductOperatingSystemService()
        # RICE = (Reach * Impact * Confidence / 100) / Effort
        # Reach = 10,000, Impact = 3.0, Confidence = 80%, Effort = 4.0
        # Expected = (10000 * 3.0 * 0.80) / 4.0 = 6000.0
        score_res = service.prioritization_roadmap_service.score_prioritization(
            tenant_id="test_tenant",
            item_id="item_001",
            framework=PrioritizationFramework.RICE.value,
            reach=10000.0,
            impact=3.0,
            confidence=80.0,
            effort=4.0,
        )
        assert score_res.framework == "RICE"
        assert score_res.score == 6000.0

    def test_wsjf_scoring(self):
        service = ProductOperatingSystemService()
        # WSJF = (User/Business Value + Time Criticality + Risk Reduction) / Job Size
        # (8.0 + 7.0 + 6.0) / 3.0 = 21.0 / 3.0 = 7.0
        score_res = service.prioritization_roadmap_service.score_prioritization(
            tenant_id="test_tenant",
            item_id="item_002",
            framework=PrioritizationFramework.WSJF.value,
            user_business_value=8.0,
            time_criticality=7.0,
            risk_reduction=6.0,
            effort=3.0,
        )
        assert score_res.framework == "WSJF"
        assert score_res.score == 7.0

    def test_priority_override_governance_logging(self):
        service = ProductOperatingSystemService()
        gov_log = service.prioritization_roadmap_service.log_priority_override(
            tenant_id="test_tenant",
            item_id="item_001",
            old_priority="MEDIUM",
            new_priority="CRITICAL",
            reason="P0 enterprise customer security audit requirement",
            evidence="Compliance review memo #402",
            owner_email="cpo@uzaii.com",
            approval_signature="SIGNED_EXECUTIVE_CPO",
        )
        assert gov_log.is_approved is True
        assert gov_log.new_priority == "CRITICAL"

    def test_roadmap_horizons_and_dependencies(self):
        service = ProductOperatingSystemService()
        rdm = service.prioritization_roadmap_service.create_roadmap(
            tenant_id="test_tenant",
            product_id="prod_001",
            title="2026 Core Platform Delivery",
            horizon_type="QUARTERLY",
        )
        item1 = service.prioritization_roadmap_service.add_roadmap_item(
            tenant_id="test_tenant",
            roadmap_id=rdm.roadmap_id,
            title="Core Ingestion Pipeline",
            horizon=RoadmapHorizon.NOW.value,
            engineering_effort_weeks=4.0,
        )
        item2 = service.prioritization_roadmap_service.add_roadmap_item(
            tenant_id="test_tenant",
            roadmap_id=rdm.roadmap_id,
            title="Downstream Decision Room Sync",
            horizon=RoadmapHorizon.NEXT.value,
            dependencies=[item1.item_id],
            engineering_effort_weeks=3.0,
        )
        board = service.prioritization_roadmap_service.get_roadmap_board("test_tenant")
        assert board.total_initiatives >= 2
        assert len(board.horizons["NOW"]) >= 1


class TestRequirementsTraceability:
    def test_requirement_and_user_story_authoring(self):
        service = ProductOperatingSystemService()
        req = service.requirements_service.create_requirement(
            tenant_id="test_tenant",
            opportunity_id="opp_001",
            title="High-Throughput Audit Telemetry Kafka Pipeline",
            priority="CRITICAL",
            acceptance_criteria=["Throughput >= 20k events/sec", "Latency <= 15ms p99"],
        )
        assert req.priority == "CRITICAL"
        assert len(req.acceptance_criteria) == 2

        story = service.requirements_service.add_user_story(
            tenant_id="test_tenant",
            requirement_id=req.requirement_id,
            role="Security Auditor",
            capability="stream live permission checks into SIEM",
            benefit="prevent unauthorized lateral movement across agent swarms",
            story_points=5,
        )
        assert "Security Auditor" in story.title
        assert story.story_points == 5

    def test_traceability_matrix_construction(self):
        service = ProductOperatingSystemService()
        matrix = service.requirements_service.build_traceability_matrix(
            tenant_id="default_tenant",
            opportunity_service=service.problems_feedback_service,
            problem_service=service.problems_feedback_service,
            roadmap_service=service.prioritization_roadmap_service,
        )
        assert len(matrix) > 0
        entry = matrix[0]
        assert "requirement_id" in entry
        assert "problem" in entry
        assert "opportunity" in entry
        assert "user_stories" in entry


class TestAnalyticsFeatureValueHealth:
    def test_feature_adoption_and_value_realization(self):
        service = ProductOperatingSystemService()
        # Demonstrates principle: Feature Shipped != Adopted != Valuable
        adoption = service.analytics_service.track_feature_adoption(
            tenant_id="test_tenant",
            product_id="prod_001",
            feature_key="decision_room_sync",
            feature_name="Real-time Decision Sync",
            eligible_users=1000,
            activated_users=750,
            weekly_active_users=600,
            retention_rate_30d=85.0,
            customer_satisfaction_score=4.8,
            efficiency_gain_pct=35.0,
            revenue_influenced_usd=450000.0,
        )
        assert adoption.adoption_rate == 75.0
        assert adoption.is_high_value is True
        assert adoption.value_realization_score > 70.0

    def test_composite_7_factor_product_health(self):
        service = ProductOperatingSystemService()
        health = service.analytics_service.calculate_product_health(
            tenant_id="test_tenant",
            product_id="prod_001",
            product_name="Uzaii Decision Fabric",
            adoption_score=90.0,
            retention_score=88.0,
            reliability_score=99.5,
            feedback_sentiment_score=85.0,
            support_efficiency_score=80.0,
            quality_defect_score=92.0,
            gross_margin_score=86.0,
        )
        assert health.health_state == ProductHealthState.HEALTHY.value
        assert health.composite_score >= 80.0


class TestLaunchesFlagsSunset:
    def test_launch_readiness_checklist(self):
        service = ProductOperatingSystemService()
        launch = service.launches_service.create_launch_plan(
            tenant_id="test_tenant",
            product_id="prod_001",
            release_name="v2.4 Autonomous Mesh",
            target_release_date="2026-10-01",
            strategy=ReleaseStrategy.CANARY.value,
            checklists={
                "engineering_ready": True,
                "qa_passed": True,
                "security_cleared": True,
                "privacy_reviewed": True,
                "docs_published": True,
                "support_trained": True,
                "marketing_aligned": True,
                "rollback_verified": True,
            },
        )
        assert launch.readiness_pct == 100.0
        assert launch.status == "APPROVED_FOR_RELEASE"

    def test_governed_sunset_plan(self):
        service = ProductOperatingSystemService()
        sunset = service.launches_service.initiate_sunset_workflow(
            tenant_id="test_tenant",
            product_id="prod_legacy",
            product_name="Legacy Batch Aggregator",
            reason="Replaced by Real-time Decision Fabric",
            active_customer_count=12,
            revenue_impact_usd=45000.0,
            alternative_product_id="prod_001",
            target_sunset_date="2026-12-31",
            governance_approver="cpo@uzaii.com",
        )
        assert sunset.governance_status == "PENDING_EXECUTIVE_APPROVAL"
        assert sunset.lifecycle_stage == "SUNSET_PLANNED"


class TestEconomicsForecastRisks:
    def test_product_unit_economics(self):
        service = ProductOperatingSystemService()
        eco = service.economics_service.calculate_unit_economics(
            tenant_id="test_tenant",
            product_id="prod_001",
            active_customers=100,
            mrr_usd=300000.0,
            infrastructure_cost_usd=25000.0,
            support_cost_usd=15000.0,
            r_and_d_allocated_usd=80000.0,
            cac_usd=15000.0,
            churn_rate_monthly=0.01,
        )
        assert eco.gross_margin_pct == round(((300000.0 - 40000.0) / 300000.0) * 100.0, 2)
        assert eco.is_healthy_unit_economics is True
        assert eco.ltv_to_cac_ratio >= 3.0

    def test_probabilistic_p10_p90_forecast(self):
        service = ProductOperatingSystemService()
        fc = service.economics_service.generate_probabilistic_forecast(
            tenant_id="test_tenant",
            product_id="prod_001",
            metric_name="ARR Growth",
            time_horizon_months=12,
            baseline_value=1000000.0,
            growth_rate_base=0.05,
        )
        assert fc.percentiles["p10_pessimistic"] < fc.percentiles["p50_median"]
        assert fc.percentiles["p50_median"] < fc.percentiles["p90_high_growth"]
        assert len(fc.assumptions) > 0


class TestProductAgents:
    @pytest.mark.asyncio
    async def test_product_strategy_agent(self):
        service = ProductOperatingSystemService()
        agent = ProductStrategyAgent(service)
        context = AgentContext(
            workflow_id="wf_01",
            task_id="task_01",
            agent_run_id="run_01",
            metadata={"tenant_id": "test_tenant", "name": "Cognitive Mesh"},
        )
        validate_agent_permissions(agent.permissions)
        res = await agent.execute(context)
        assert res["status"] == "COMPLETED"
        assert res["product_name"] == "Cognitive Mesh"

    @pytest.mark.asyncio
    async def test_customer_problem_agent(self):
        service = ProductOperatingSystemService()
        agent = CustomerProblemAgent(service)
        context = AgentContext(
            workflow_id="wf_02",
            task_id="task_02",
            agent_run_id="run_02",
            metadata={"tenant_id": "test_tenant", "title": "Slow batch ingestion sync"},
        )
        validate_agent_permissions(agent.permissions)
        res = await agent.execute(context)
        assert res["status"] == "COMPLETED"
        assert res["title"] == "Slow batch ingestion sync"

    @pytest.mark.asyncio
    async def test_opportunity_scoring_agent(self):
        service = ProductOperatingSystemService()
        agent = OpportunityScoringAgent(service)
        context = AgentContext(
            workflow_id="wf_03",
            task_id="task_03",
            agent_run_id="run_03",
            metadata={"tenant_id": "test_tenant", "title": "Continuous Streaming Hub"},
        )
        validate_agent_permissions(agent.permissions)
        res = await agent.execute(context)
        assert res["status"] == "COMPLETED"
        assert res["composite_score"] > 0

    @pytest.mark.asyncio
    async def test_product_copilot_evidence_grounded(self):
        service = ProductOperatingSystemService()
        agent = ProductCopilotAgent(service)
        context = AgentContext(
            workflow_id="wf_04",
            task_id="task_04",
            agent_run_id="run_04",
            metadata={"tenant_id": "default_tenant", "query": "What should we build next?"},
        )
        validate_agent_permissions(agent.permissions)
        res = await agent.execute(context)
        assert res["status"] == "COMPLETED"
        assert len(res["evidence_sources"]) > 0
        assert res["confidence"] > 0.8
        assert "AI recommendation only" in res["governance_notice"]

    def test_permission_prohibitions_denied(self):
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"AUTONOMOUS_LAUNCH_RELEASE"})
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"AUTONOMOUS_SUNSET_PRODUCT"})
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"AUTONOMOUS_MODIFY_ROADMAP_PRIORITY"})

