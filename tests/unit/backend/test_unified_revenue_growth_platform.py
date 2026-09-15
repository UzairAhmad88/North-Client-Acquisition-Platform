"""Unit Tests for Phase 58: Unified Revenue Growth, Go-to-Market Intelligence & Optimization Platform."""
import pytest
from typing import Any, Dict

from backend.app.services.revenue_growth.base import (
    DealRiskSeverity,
    DiscountStatus,
    ForecastScenario,
    OpportunityHealthState,
    PipelineStage,
    SalesMotion,
)
from backend.app.services.revenue_growth.service import RevenueGrowthPlatformService
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.core.context import AgentContext
from agents.revenue_growth import (
    AccountTargetingAgent,
    DealRiskAgent,
    EconomicsAgent,
    ForecastAgent,
    GtmStrategyAgent,
    NextBestActionAgent,
    PipelineAgent,
    PricingAgent,
    RevenueCopilotAgent,
)


@pytest.fixture
def rev_service():
    """Provides a fresh instance of RevenueGrowthPlatformService."""
    return RevenueGrowthPlatformService()


class TestGtmAndTargeting:
    def test_create_gtm_strategy_and_icp(self, rev_service):
        strat = rev_service.gtm.create_gtm_strategy(
            name="SaaS Enterprise Motion 2026",
            target_market="Enterprise Logistics",
            sales_motion=SalesMotion.ENTERPRISE.value,
        )
        assert strat["id"] is not None
        assert strat["name"] == "SaaS Enterprise Motion 2026"
        assert strat["sales_motion"] == "enterprise"

        seg = rev_service.gtm.create_segment(
            name="Global 3PL Fleets",
            industry="Logistics",
            strategy_id=strat["id"],
        )
        assert seg["id"] is not None
        assert seg["industry"] == "Logistics"

        icp = rev_service.gtm.create_icp(
            name="Logistics Automation ICP",
            target_industries=["Supply Chain", "Freight"],
            segment_id=seg["id"],
        )
        assert icp["id"] is not None
        assert "Supply Chain" in icp["target_industries"]

    def test_target_account_scoring(self, rev_service):
        account = rev_service.gtm.create_target_account(
            company_name="Vanguard Supply Chain",
            industry="Logistics",
            employee_count=1500,
            estimated_annual_revenue=85000000.0,
        )
        assert account["id"] is not None
        assert account["company_name"] == "Vanguard Supply Chain"

        score = rev_service.gtm.score_target_account(
            account_id=account["id"],
            icp_fit=0.92,
            business_need=0.88,
            revenue_potential=0.95,
        )
        assert score["composite_score"] > 0.80

    def test_market_coverage_and_territories(self, rev_service):
        coverage = rev_service.gtm.get_market_coverage()
        assert len(coverage) >= 1
        assert coverage[0]["coverage_percentage"] > 0

        territories = rev_service.gtm.list_territories()
        assert len(territories) >= 1


class TestPipelinesAndOpportunities:
    def test_create_and_advance_opportunity(self, rev_service):
        account = rev_service.gtm.create_target_account("Apex Global Tech")
        opp = rev_service.pipeline.create_opportunity(
            account_id=account["id"],
            title="Apex Autonomous Ops Rollout",
            estimated_arr_value=120000.0,
            stage=PipelineStage.QUALIFIED.value,
            win_probability=0.25,
        )
        assert opp["id"] is not None
        assert opp["estimated_arr_value"] == 120000.0
        assert opp["weighted_value"] == 30000.0

        advanced = rev_service.pipeline.advance_stage(opp["id"], PipelineStage.PROPOSAL.value)
        assert advanced["stage"] == "proposal"
        assert advanced["win_probability"] == 0.75
        assert advanced["weighted_value"] == 90000.0

    def test_opportunity_health_and_activity(self, rev_service):
        opps = rev_service.pipeline.list_opportunities()
        target_opp = opps[0]

        health = rev_service.pipeline.evaluate_opportunity_health(
            opportunity_id=target_opp["id"],
            engagement_score=90.0,
            decision_access_score=85.0,
            budget_evidence_score=95.0,
        )
        assert health["overall_health_score"] >= 85.0
        assert health["health_state"] == OpportunityHealthState.HEALTHY.value

        act = rev_service.pipeline.log_activity(
            activity_type="meeting",
            summary="Technical architecture review",
            opportunity_id=target_opp["id"],
        )
        assert act["id"] is not None

    def test_sales_velocity(self, rev_service):
        velocity = rev_service.pipeline.get_sales_velocity()
        assert velocity["active_opportunities_count"] >= 1
        assert velocity["total_pipeline_value_usd"] > 0


class TestForecastingAndTargets:
    def test_probabilistic_forecasting(self, rev_service):
        fc = rev_service.forecasting.generate_forecast(
            forecast_period="Q4-2026",
            scenario=ForecastScenario.BASE.value,
            pipeline_total_usd=4000000.0,
            weighted_pipeline_usd=1500000.0,
        )
        assert fc["p10_usd"] < fc["p50_usd"] < fc["p90_usd"]
        assert fc["p50_usd"] == 1500000.0

    def test_forecast_scenarios_and_calibration(self, rev_service):
        scenarios = rev_service.forecasting.get_forecast_scenarios("Q4-2026")
        assert len(scenarios) == 4

        cal = rev_service.forecasting.get_forecast_calibration()
        assert cal["mean_absolute_percentage_error_pct"] > 0
        assert cal["calibration_status"] == "calibrated"

    def test_revenue_targets_and_capacity(self, rev_service):
        tgt = rev_service.forecasting.create_revenue_target(
            period="Q4-2026",
            target_amount_usd=5000000.0,
            actual_amount_usd=4800000.0,
        )
        assert tgt["variance_usd"] == -200000.0

        cap = rev_service.forecasting.create_capacity_plan(
            period="Q4-2026",
            rep_count=8,
            quota_per_rep_usd=500000.0,
        )
        assert cap["total_capacity_usd"] == 4000000.0
        assert cap["effective_capacity_usd"] > 0


class TestPricingDiscountsDealRisk:
    def test_pricing_and_discount_governance(self, rev_service):
        tier = rev_service.pricing.set_pricing_tier(
            product_or_service="Uzaii Workforce Platform",
            tier_name="Enterprise Tier",
            list_price_usd=120000.0,
        )
        assert tier["id"] is not None

        disc_req = rev_service.pricing.request_discount(
            opportunity_id="opp-test-001",
            requested_discount_pct=15.0,
            original_price_usd=120000.0,
            justification="3-year prepay commitment",
        )
        assert disc_req["status"] == DiscountStatus.PENDING_APPROVAL.value
        assert disc_req["proposed_price_usd"] == 102000.0

        approved = rev_service.pricing.approve_discount(
            discount_id=disc_req["id"],
            approver_name="Chief Commercial Officer",
            approval_notes="Approved for multi-year contract",
        )
        assert approved["status"] == DiscountStatus.APPROVED.value
        assert approved["approver_name"] == "Chief Commercial Officer"

    def test_deal_risk_and_next_best_action(self, rev_service):
        risk = rev_service.pricing.record_deal_risk(
            opportunity_id="opp-test-001",
            risk_category="budget",
            severity=DealRiskSeverity.HIGH.value,
            description="Procurement freeze pending quarterly board meeting",
        )
        assert risk["severity"] == "high"

        nba = rev_service.pricing.recommend_next_best_action(
            opportunity_id="opp-test-001",
            recommended_action="Present executive business case and ROI breakdown",
        )
        assert nba["confidence"] >= 0.85


class TestChannelsAttributionEconomics:
    def test_channels_and_attribution(self, rev_service):
        channels = rev_service.economics.list_channels()
        assert len(channels) >= 1

        attr = rev_service.economics.calculate_attribution("opp-test-001")
        assert "first_touch_research" in attr["touchpoints_breakdown"]

    def test_unit_economics_and_revenue_waterfall(self, rev_service):
        econ = rev_service.economics.get_unit_economics("Q3-2026")
        assert econ["blended_cac_usd"] > 0
        assert econ["ltv_to_cac_ratio"] > 1.0

        waterfall = rev_service.economics.record_revenue_waterfall(
            period="Q3-2026",
            beginning_arr_usd=5000000.0,
            new_arr_usd=600000.0,
            expansion_arr_usd=250000.0,
            contraction_arr_usd=50000.0,
            churn_arr_usd=50000.0,
        )
        assert waterfall["ending_arr_usd"] == 5750000.0
        assert waterfall["net_retention_pct"] == 103.0


class TestRiskGrowthSimulations:
    def test_concentration_and_growth_opportunities(self, rev_service):
        conc = rev_service.risk_growth.evaluate_concentration_risk()
        assert conc["top_customer_revenue_share_pct"] > 0

        growth = rev_service.risk_growth.list_growth_opportunities()
        assert len(growth) >= 1

    def test_revenue_simulation(self, rev_service):
        sim = rev_service.risk_growth.simulate_revenue(
            conversion_rate_delta_pct=10.0,
            lead_volume_delta_pct=15.0,
        )
        assert sim["projected_annual_run_rate_usd"] > sim["baseline_annual_run_rate_usd"]
        assert sim["projected_arr_lift_usd"] > 0


class TestFacadeAndCopilot:
    def test_overview_metrics(self, rev_service):
        overview = rev_service.get_overview_metrics()
        assert overview["current_annual_run_rate_usd"] > 0
        assert overview["active_pipeline_total_usd"] > 0
        assert overview["target_accounts_count"] >= 1

    def test_copilot_queries(self, rev_service):
        ans_fc = rev_service.answer_copilot_query("What is our expected revenue?")
        assert "expected revenue" in ans_fc["answer"].lower()
        assert len(ans_fc["supporting_evidence_sources"]) >= 1

        ans_pipe = rev_service.answer_copilot_query("Show me active pipeline opportunities")
        assert "pipeline" in ans_pipe["answer"].lower()

        ans_risk = rev_service.answer_copilot_query("Which deals are risky?")
        assert "risk" in ans_risk["answer"].lower()


@pytest.mark.asyncio
class TestRevenueGrowthAgents:
    async def test_gtm_strategy_agent(self, rev_service):
        agent = GtmStrategyAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-001",
            task_id="task-rev-001",
            agent_run_id="run-rev-001",
            metadata={"strategy_name": "Autonomous GTM 2026", "target_market": "FinTech"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["strategy"] is not None

    async def test_account_targeting_agent(self, rev_service):
        agent = AccountTargetingAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-002",
            task_id="task-rev-002",
            agent_run_id="run-rev-002",
            metadata={"company_name": "Apex Digital", "industry": "FinTech"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["composite_score"] > 0

    async def test_pipeline_agent(self, rev_service):
        agent = PipelineAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-003",
            task_id="task-rev-003",
            agent_run_id="run-rev-003",
            metadata={"engagement_score": 90.0},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["overall_health_score"] >= 80.0

    async def test_forecast_agent(self, rev_service):
        agent = ForecastAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-004",
            task_id="task-rev-004",
            agent_run_id="run-rev-004",
            metadata={"forecast_period": "Q4-2026", "scenario": "base"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["p50_usd"] > 0

    async def test_pricing_agent(self, rev_service):
        agent = PricingAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-005",
            task_id="task-rev-005",
            agent_run_id="run-rev-005",
            metadata={"requested_discount_pct": 12.0, "original_price_usd": 100000.0},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["proposed_price_usd"] == 88000.0

    async def test_deal_risk_agent(self, rev_service):
        agent = DealRiskAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-006",
            task_id="task-rev-006",
            agent_run_id="run-rev-006",
            metadata={"risk_category": "timeline", "severity": "medium"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["risk_id"] is not None

    async def test_next_best_action_agent(self, rev_service):
        agent = NextBestActionAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-007",
            task_id="task-rev-007",
            agent_run_id="run-rev-007",
            metadata={"recommended_action": "Schedule security architecture sync"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["confidence"] >= 0.85

    async def test_economics_agent(self, rev_service):
        agent = EconomicsAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-008",
            task_id="task-rev-008",
            agent_run_id="run-rev-008",
            metadata={"period": "Q3-2026"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["ltv_to_cac_ratio"] > 1.0

    async def test_revenue_copilot_agent(self, rev_service):
        agent = RevenueCopilotAgent(service=rev_service)
        context = AgentContext(
            workflow_id="wf-rev-009",
            task_id="task-rev-009",
            agent_run_id="run-rev-009",
            metadata={"query": "What is our revenue target?"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert len(res["supporting_evidence"]) >= 1


class TestPermissionsAndProhibitions:
    def test_prohibited_permissions(self):
        assert "AUTONOMOUS_SEND_SALES_MESSAGE" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_NEGOTIATE_CONTRACT" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_FINANCIAL_EXECUTION" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_SALES_POLICY_CHANGE" in PROHIBITED_PERMISSIONS
        assert "FABRICATE_REVENUE_DATA" in PROHIBITED_PERMISSIONS
        assert "FABRICATE_PIPELINE_DATA" in PROHIBITED_PERMISSIONS
