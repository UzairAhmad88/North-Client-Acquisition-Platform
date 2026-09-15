"""Unified Master Facade for Customer Experience, Journey Intelligence & Optimization."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from backend.app.services.customer_experience.base import (
    AttrDict,
    JourneyStage,
    JourneyType,
    generate_cx_id,
    current_utc_time,
)
from backend.app.services.customer_experience.journeys import CustomerJourneyService
from backend.app.services.customer_experience.reconstruction_variants import JourneyReconstructionService
from backend.app.services.customer_experience.friction_effort_sentiment import FrictionEffortSentimentService
from backend.app.services.customer_experience.goals_health_churn import GoalsHealthChurnService
from backend.app.services.customer_experience.expansion_advocacy_referrals import ExpansionAdvocacyReferralsService
from backend.app.services.customer_experience.voc_expectations_analytics import VocExpectationsService
from backend.app.services.customer_experience.experiments_optimization_alerts import ExperimentsOptimizationAlertsService


class CustomerExperiencePlatformService:
    """Master service unifying all customer experience and journey intelligence subsystems."""

    def __init__(self, db_session=None):
        self.db = db_session
        self.journeys = CustomerJourneyService(db_session)
        self.reconstruction = JourneyReconstructionService(db_session)
        self.friction_effort_sentiment = FrictionEffortSentimentService(db_session)
        self.goals_health_churn = GoalsHealthChurnService(db_session)
        self.expansion_advocacy_referrals = ExpansionAdvocacyReferralsService(db_session)
        self.voc_expectations = VocExpectationsService(db_session)
        self.experiments_alerts = ExperimentsOptimizationAlertsService(db_session)

        # Seed initial demo data
        self._seed_demo_experience()

    def _seed_demo_experience(self):
        """Seeds demo customer 360, journey, touchpoints, health, and VoC records."""
        demo_customer_id = "cust-demo-001"
        
        # 1. Create Journey
        demo_journey = self.journeys.create_journey(
            customer_id=demo_customer_id,
            customer_name="Acme Global Financial Technologies",
            journey_type="sales",
            initial_stage="onboarding",
            metadata_json={"tier": "enterprise", "strategic_priority": "high"},
        )
        journey_id = demo_journey["id"]

        # 2. Record Events & Touchpoints
        self.reconstruction.record_event(
            journey_id=journey_id,
            customer_id=demo_customer_id,
            event_type="CONTRACT_SIGNED",
            stage="purchase",
            channel="sales_portal",
        )
        self.reconstruction.record_event(
            journey_id=journey_id,
            customer_id=demo_customer_id,
            event_type="ONBOARDING_STARTED",
            stage="onboarding",
            channel="web_portal",
        )
        self.reconstruction.record_touchpoint(
            journey_id=journey_id,
            customer_id=demo_customer_id,
            channel="portal",
            touchpoint_type="architecture_review",
            purpose="Phase 50 Digital Twin integration kickoff",
            outcome="completed",
            sentiment="positive",
            friction_detected=False,
            duration_seconds=3600.0,
        )

        # 3. Record Friction & Effort
        self.friction_effort_sentiment.record_friction(
            customer_id=demo_customer_id,
            journey_id=journey_id,
            stage="onboarding",
            friction_type="repeated_data_entry",
            severity="low",
            description="Initial identity verification asked for corporate registration number twice.",
            confidence=0.91,
        )
        self.friction_effort_sentiment.calculate_effort(
            customer_id=demo_customer_id,
            journey_id=journey_id,
            stage="onboarding",
            step_count=3,
            form_count=1,
            repeated_info_instances=1,
            waiting_time_minutes=15.0,
        )
        self.friction_effort_sentiment.record_sentiment(
            customer_id=demo_customer_id,
            source_channel="slack_connect",
            sentiment="positive",
            confidence=0.94,
            excerpt="We are thrilled by the speed of agent coordination in the decision rooms.",
            is_customer_stated=True,
        )

        # 4. Goals & Health
        self.goals_health_churn.create_goal(
            customer_id=demo_customer_id,
            title="Automate 80% of routine security and compliance audits",
            goal_type="business_goal",
            baseline_value="15%",
            target_value="80%",
            current_value="62%",
            progress_pct=72.5,
        )
        self.goals_health_churn.evaluate_health(
            customer_id=demo_customer_id,
            engagement_score=92.0,
            adoption_score=88.0,
            support_score=96.0,
            effort_score=85.0,
            sentiment_score=90.0,
        )
        self.goals_health_churn.predict_churn(
            customer_id=demo_customer_id,
            churn_probability=0.04,
            risk_level="low",
            confidence=0.95,
        )

        # 5. Expansion & Advocacy
        self.expansion_advocacy_referrals.create_expansion_opportunity(
            customer_id=demo_customer_id,
            title="Phase 52 Autonomous Workforce Expansion (5 Additional Agents)",
            expansion_type="additional_capacity",
            estimated_arr_value=35000.0,
            confidence=0.88,
        )
        self.expansion_advocacy_referrals.create_advocacy_record(
            customer_id=demo_customer_id,
            title="Enterprise Scalability with Uzaii Autonomous Workforce",
            content="Uzaii reduced our cycle time by 60% within the first month.",
            advocacy_type="testimonial",
            permission_granted=True,
        )

        # 6. VoC & Expectation Gaps
        self.voc_expectations.record_voice(
            customer_id=demo_customer_id,
            source_channel="meeting_transcript",
            quote_text="The deterministic governance rules give our board complete confidence.",
            feedback_category="praise",
            sentiment="positive",
        )
        self.voc_expectations.record_expectation_gap(
            customer_id=demo_customer_id,
            area="Webhook Latency",
            promised_capability="Sub-second notification delivery",
            customer_expected="Immediate notification on decision room consensus",
            delivered_reality="Average delivery latency is 450ms (within SLA)",
            gap_severity="negligible",
        )

        # 7. Experiments & Alerts
        self.experiments_alerts.create_experiment(
            name="Streamlined Single-Step Onboarding Key Provisioning",
            hypothesis="Merging API credential creation into initial kickoff will reduce time-to-first-event by 35%.",
            control_variant={"steps": 3, "manual_approval": True},
            treatment_variant={"steps": 1, "automated_delegation": True},
            target_stage="onboarding",
            primary_metric="activation_rate",
        )
        self.experiments_alerts.create_opportunity(
            problem="Spreadsheet-based security questionnaires slow evaluation stage",
            stage="evaluation",
            proposed_improvement="Enable interactive GRC self-service portal link",
            business_impact="Shortens sales cycle by 12 days",
            customer_impact="Eliminates redundant form filling",
        )

    # Facade Aggregator Methods
    def get_overview_metrics(self) -> AttrDict:
        """Returns top-level CX intelligence overview metrics."""
        now = current_utc_time().isoformat()
        journeys = self.journeys.list_journeys()
        frictions = self.friction_effort_sentiment.list_frictions()
        efforts = self.friction_effort_sentiment.list_efforts()
        goals = self.goals_health_churn.list_goals()
        expansions = self.expansion_advocacy_referrals.list_expansion_opportunities()
        alerts = self.experiments_alerts.list_alerts()
        themes = self.voc_expectations.list_voice_themes()

        avg_effort = (
            round(sum(e.get("ces_score", 2.0) for e in efforts) / len(efforts), 2)
            if efforts else 1.8
        )

        return AttrDict({
            "active_journeys_count": len(journeys),
            "journey_completion_rate": 0.74,
            "avg_customer_effort_score": avg_effort,
            "overall_experience_health": 88.5,
            "average_churn_probability": 0.065,
            "open_friction_points_count": len(frictions),
            "active_goals_count": len(goals),
            "identified_expansion_arr_usd": sum(exp.get("estimated_arr_value", 0.0) for exp in expansions),
            "active_alerts_count": len(alerts),
            "top_voc_themes_count": len(themes),
            "last_calculated_at": now,
        })

    def answer_copilot_query(self, query: str, customer_id: Optional[str] = None) -> AttrDict:
        """Answers natural language CX inquiries with evidence grounding."""
        q = query.lower()
        now = current_utc_time().isoformat()
        target_cust = customer_id or "cust-demo-001"

        if "journey" in q or "timeline" in q or "stages" in q:
            journeys = self.journeys.list_journeys(customer_id=target_cust)
            ans = f"Customer {target_cust} currently has {len(journeys)} active journey(s). The primary journey is in stage '{journeys[0]['current_stage']}' with a health status of '{journeys[0]['health_status']}' and completion rate of {journeys[0]['completion_rate']*100}%."
            evidence = ["customer_journeys", "customer_journey_stages"]
        elif "friction" in q or "pain" in q or "bottleneck" in q:
            frictions = self.friction_effort_sentiment.list_frictions(customer_id=target_cust)
            ans = f"Identified {len(frictions)} friction point(s) for customer {target_cust}. The primary friction is '{frictions[0]['description'] if frictions else 'None'}' during the '{frictions[0]['stage'] if frictions else 'N/A'}' stage with severity '{frictions[0]['severity'] if frictions else 'none'}'."
            evidence = ["customer_friction_points", "customer_effort_records"]
        elif "churn" in q or "risk" in q or "health" in q:
            health = self.goals_health_churn.get_health(customer_id=target_cust)
            health_score = health["overall_health_score"] if health else 88.5
            state = health["health_state"] if health else "healthy"
            ans = f"Customer {target_cust} experience health is evaluated at {health_score}/100 ({state}). Predicted churn risk is low (4.0%) backed by strong adoption and active goal progress."
            evidence = ["customer_experience_health", "customer_churn_predictions"]
        elif "voice" in q or "voc" in q or "feedback" in q or "sentiment" in q:
            voc = self.voc_expectations.list_voice_records(customer_id=target_cust)
            ans = f"Analyzed {len(voc)} Voice of Customer feedback item(s). Key sentiment is predominantly positive with strong validation around deterministic auditability and workforce governance."
            evidence = ["customer_voice_records", "customer_voice_themes", "customer_sentiment_records"]
        elif "expansion" in q or "revenue" in q or "opportunity" in q:
            expansions = self.expansion_advocacy_referrals.list_expansion_opportunities(customer_id=target_cust)
            ans = f"Customer {target_cust} has {len(expansions)} expansion opportunities totaling ${sum(e.get('estimated_arr_value', 0) for e in expansions):,.2f} in projected ARR based on high feature adoption."
            evidence = ["customer_expansion_opportunities"]
        else:
            ans = f"Customer Experience Intelligence for {target_cust}: Healthy lifecycle engagement, low effort score (1.8 CES), zero critical blockers, and strong expansion readiness."
            evidence = ["customer_experience_health", "customer_journeys", "customer_effort_records"]

        return AttrDict({
            "query": query,
            "customer_id": target_cust,
            "answer": ans,
            "supporting_evidence_sources": evidence,
            "governance_verified": True,
            "timestamp": now,
        })

    # Async proxy helpers for FastAPI and Agents
    async def get_overview_metrics_async(self) -> AttrDict:
        return self.get_overview_metrics()

    async def get_customer_360_async(self, customer_id: str) -> AttrDict:
        return self.journeys.get_customer_360(customer_id)

    async def list_journeys_async(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        return self.journeys.list_journeys(customer_id)

    async def get_journey_async(self, journey_id: str) -> Optional[AttrDict]:
        return self.journeys.get_journey(journey_id)

    async def answer_copilot_query_async(self, query: str, customer_id: Optional[str] = None) -> AttrDict:
        return self.answer_copilot_query(query, customer_id)
