"""Unit Tests for Phase 57: Unified Customer Experience, Journey Intelligence & Optimization Platform."""
import pytest
from typing import Any, Dict

from backend.app.services.customer_experience.base import (
    AlertType,
    EffortTier,
    FrictionSeverity,
    HealthState,
    JourneyStage,
    JourneyType,
    LifecycleStatus,
    SentimentType,
)
from backend.app.services.customer_experience.service import CustomerExperiencePlatformService
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.core.context import AgentContext
from agents.customer_experience import (
    JourneyAnalysisAgent,
    FrictionAnalysisAgent,
    ExperienceHealthAgent,
    ChurnAnalysisAgent,
    VoiceOfCustomerAgent,
    ExpectationGapAgent,
    CustomerExperienceCopilot,
)


@pytest.fixture
def cx_service():
    """Provides a fresh instance of CustomerExperiencePlatformService."""
    return CustomerExperiencePlatformService()


class TestCustomerJourneysAnd360:
    def test_create_and_advance_journey(self, cx_service):
        journey = cx_service.journeys.create_journey(
            customer_id="cust-101",
            customer_name="Starlight Energy Systems",
            journey_type="sales",
            initial_stage="discovery",
        )
        assert journey["id"] is not None
        assert journey["customer_id"] == "cust-101"
        assert journey["current_stage"] == "discovery"
        assert journey["health_status"] == "healthy"

        # Advance to onboarding
        advanced = cx_service.journeys.advance_stage(journey["id"], "onboarding", notes="Signed enterprise MSA")
        assert advanced["current_stage"] == "onboarding"
        assert len(advanced["stage_history"]) >= 2

    def test_customer_360_aggregation(self, cx_service):
        profile = cx_service.journeys.get_customer_360("cust-demo-001")
        assert profile["customer_id"] == "cust-demo-001"
        assert profile["identity"]["name"] is not None
        assert profile["organization"]["industry"] is not None
        assert profile["health_summary"]["overall_score"] > 0
        assert profile["effort_summary"]["tier"] is not None


class TestReconstructionAndVariants:
    def test_record_events_and_reconstruct(self, cx_service):
        journey = cx_service.journeys.create_journey(
            customer_id="cust-202",
            journey_type="product",
            initial_stage="onboarding",
        )
        cx_service.reconstruction.record_event(
            journey_id=journey["id"],
            customer_id="cust-202",
            event_type="PAGE_VIEWED",
            stage="discovery",
        )
        cx_service.reconstruction.record_event(
            journey_id=journey["id"],
            customer_id="cust-202",
            event_type="CONTRACT_SIGNED",
            stage="purchase",
        )
        cx_service.reconstruction.record_touchpoint(
            journey_id=journey["id"],
            customer_id="cust-202",
            channel="portal",
            touchpoint_type="live_demo",
            sentiment="positive",
        )

        reconstructed = cx_service.reconstruction.reconstruct_journey_path(journey["id"])
        assert reconstructed["journey_id"] == journey["id"]
        assert reconstructed["event_count"] >= 2
        assert reconstructed["touchpoint_count"] >= 1
        assert "discovery" in reconstructed["reconstructed_stages"]

    def test_discover_variants(self, cx_service):
        variants = cx_service.reconstruction.discover_variants()
        assert len(variants) >= 2
        assert any(v["is_optimal"] for v in variants)


class TestFrictionEffortSentiment:
    def test_record_friction_and_calculate_effort(self, cx_service):
        friction = cx_service.friction_effort_sentiment.record_friction(
            customer_id="cust-303",
            stage="onboarding",
            friction_type="repeated_data_entry",
            severity="medium",
            description="Redundant API key confirmation",
        )
        assert friction["id"] is not None
        assert friction["severity"] == "medium"

        effort = cx_service.friction_effort_sentiment.calculate_effort(
            customer_id="cust-303",
            stage="onboarding",
            step_count=4,
            form_count=2,
            repeated_info_instances=1,
            waiting_time_minutes=30.0,
        )
        assert effort["ces_score"] >= 1.0
        assert effort["effort_tier"] in [EffortTier.LOW_EFFORT.value, EffortTier.MODERATE_EFFORT.value, EffortTier.HIGH_EFFORT.value]

    def test_record_sentiment(self, cx_service):
        snt = cx_service.friction_effort_sentiment.record_sentiment(
            customer_id="cust-303",
            source_channel="email",
            sentiment="positive",
            confidence=0.92,
            excerpt="Seamless onboarding process.",
            is_customer_stated=True,
        )
        assert snt["sentiment"] == "positive"
        assert snt["is_customer_stated"] is True


class TestGoalsHealthChurn:
    def test_create_goal_and_evaluate_health(self, cx_service):
        goal = cx_service.goals_health_churn.create_goal(
            customer_id="cust-404",
            title="Deploy 5 AI agents to production",
            target_value="5",
            current_value="4",
            progress_pct=80.0,
        )
        assert goal["id"] is not None
        assert goal["progress_pct"] == 80.0

        health = cx_service.goals_health_churn.evaluate_health(
            customer_id="cust-404",
            engagement_score=95.0,
            adoption_score=90.0,
            support_score=92.0,
            effort_score=85.0,
            sentiment_score=90.0,
        )
        assert health["overall_health_score"] >= 85.0
        assert health["health_state"] == HealthState.EXCELLENT.value
        assert health["churn_probability"] < 0.20

    def test_predict_churn(self, cx_service):
        churn = cx_service.goals_health_churn.predict_churn(
            customer_id="cust-404",
            churn_probability=0.05,
            risk_level="low",
            confidence=0.94,
        )
        assert churn["churn_probability"] == 0.05
        assert churn["is_confirmed_by_human"] is False


class TestExpansionAdvocacyReferrals:
    def test_expansion_and_referral(self, cx_service):
        exp = cx_service.expansion_advocacy_referrals.create_expansion_opportunity(
            customer_id="cust-505",
            title="Additional 10 autonomous workforce seats",
            estimated_arr_value=45000.0,
        )
        assert exp["id"] is not None
        assert exp["estimated_arr_value"] == 45000.0

        ref = cx_service.expansion_advocacy_referrals.create_referral(
            referrer_customer_id="cust-505",
            referred_company_name="Apex Global FinTech",
        )
        assert ref["id"] is not None
        assert ref["referred_company_name"] == "Apex Global FinTech"


class TestVoiceAndExpectations:
    def test_voice_and_expectation_gap(self, cx_service):
        voc = cx_service.voc_expectations.record_voice(
            customer_id="cust-606",
            source_channel="meeting_notes",
            quote_text="The automated audit trails saved our team weeks.",
            feedback_category="praise",
        )
        assert voc["id"] is not None
        assert voc["feedback_category"] == "praise"

        gap = cx_service.voc_expectations.record_expectation_gap(
            customer_id="cust-606",
            area="API Webhook Latency",
            promised_capability="Delivery within 500ms",
            customer_expected="Real-time under 200ms",
            delivered_reality="350ms average delivery",
            gap_severity="low",
        )
        assert gap["id"] is not None
        assert gap["gap_severity"] == "low"


class TestExperimentsAndAlerts:
    def test_experiments_and_simulations(self, cx_service):
        exp = cx_service.experiments_alerts.create_experiment(
            name="Automated Key Delegation",
            hypothesis="Single-step provisioning reduces time to first event by 30%",
            control_variant={"steps": 3},
            treatment_variant={"steps": 1},
        )
        assert exp["id"] is not None
        assert exp["status"] == "running"

        sim = cx_service.experiments_alerts.simulate_journey_changes("onboarding", reduction_in_steps=2)
        assert sim["projected_conversion_delta_pct"] > 0

    def test_alerts_and_bottlenecks(self, cx_service):
        bottlenecks = cx_service.experiments_alerts.detect_bottlenecks()
        assert len(bottlenecks) >= 1

        alert = cx_service.experiments_alerts.create_alert(
            customer_id="cust-707",
            alert_type=AlertType.HEALTH_DECLINE.value,
            severity="warning",
            title="Usage Drop Detected",
        )
        assert alert["id"] is not None
        assert alert["is_resolved"] is False


class TestFacadeAndCopilot:
    def test_overview_metrics(self, cx_service):
        overview = cx_service.get_overview_metrics()
        assert overview["active_journeys_count"] >= 1
        assert overview["avg_customer_effort_score"] > 0
        assert overview["overall_experience_health"] > 0

    def test_copilot_queries(self, cx_service):
        ans_journey = cx_service.answer_copilot_query("Show me this customer journey", "cust-demo-001")
        assert "cust-demo-001" in ans_journey["answer"]
        assert len(ans_journey["supporting_evidence_sources"]) >= 1

        ans_friction = cx_service.answer_copilot_query("Where is the friction point?", "cust-demo-001")
        assert "friction" in ans_friction["answer"].lower()

        ans_churn = cx_service.answer_copilot_query("What is the churn risk?", "cust-demo-001")
        assert "churn" in ans_churn["answer"].lower() or "health" in ans_churn["answer"].lower()


@pytest.mark.asyncio
class TestCustomerExperienceAgents:
    async def test_journey_analysis_agent(self, cx_service):
        agent = JourneyAnalysisAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-001",
            task_id="task-001",
            agent_run_id="run-001",
            metadata={"customer_id": "cust-demo-001"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["reconstructed_path"] is not None

    async def test_friction_analysis_agent(self, cx_service):
        agent = FrictionAnalysisAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-002",
            task_id="task-002",
            agent_run_id="run-002",
            metadata={"customer_id": "cust-demo-001", "stage": "onboarding", "description": "Form timeout"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["friction_recorded"] is not None

    async def test_experience_health_agent(self, cx_service):
        agent = ExperienceHealthAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-003",
            task_id="task-003",
            agent_run_id="run-003",
            metadata={"customer_id": "cust-demo-001", "engagement_score": 90.0},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["overall_health_score"] >= 80.0

    async def test_churn_analysis_agent(self, cx_service):
        agent = ChurnAnalysisAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-004",
            task_id="task-004",
            agent_run_id="run-004",
            metadata={"customer_id": "cust-demo-001", "churn_probability": 0.06},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["churn_probability"] == 0.06

    async def test_voice_of_customer_agent(self, cx_service):
        agent = VoiceOfCustomerAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-005",
            task_id="task-005",
            agent_run_id="run-005",
            metadata={"customer_id": "cust-demo-001", "quote_text": "Great deterministic AI."},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["recorded_feedback"] is not None

    async def test_expectation_gap_agent(self, cx_service):
        agent = ExpectationGapAgent(service=cx_service)
        context = AgentContext(
            workflow_id="wf-006",
            task_id="task-006",
            agent_run_id="run-006",
            metadata={
                "customer_id": "cust-demo-001",
                "area": "Uptime",
                "promised_capability": "99.9%",
                "customer_expected": "99.9%",
                "delivered_reality": "99.95%",
            },
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["expectation_gap"] is not None

    async def test_customer_experience_copilot(self, cx_service):
        agent = CustomerExperienceCopilot(service=cx_service)
        context = AgentContext(
            workflow_id="wf-007",
            task_id="task-007",
            agent_run_id="run-007",
            metadata={"query": "Show me customer health", "customer_id": "cust-demo-001"},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert "cust-demo-001" in res["answer"] or "88" in res["answer"]


class TestPermissionsAndProhibitions:
    def test_prohibited_permissions(self):
        assert "AUTONOMOUS_CUSTOMER_OUTREACH" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_GRANT_DISCOUNT" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_ISSUE_REFUND" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_POLICY_CHANGE" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_PRICING_CHANGE" in PROHIBITED_PERMISSIONS
        assert "FABRICATE_CUSTOMER_FEEDBACK" in PROHIBITED_PERMISSIONS
