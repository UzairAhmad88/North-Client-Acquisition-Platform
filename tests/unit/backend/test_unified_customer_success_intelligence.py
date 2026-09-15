"""Unit tests for Phase 41 — Unified Client Relationship Intelligence & Customer Success Platform."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from datetime import datetime, timezone
from decimal import Decimal
import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.customer_success.base import (
    ClientLifecycleStage,
    DecisionRole,
    GoalStatus,
    HealthBand,
    OpportunityType,
    RelationshipStrength,
    RiskCategory,
    SentimentLabel,
    SurveyType,
    TimelineEventData,
)
from app.customer_success.health_engine import HealthScoringEngine
from app.customer_success.timeline import ClientTimelineAggregator
from app.customer_success.client_360 import Client360Synthesizer
from app.customer_success.authorization import CustomerSuccessAuthorizationManager
from app.customer_success.service import CustomerSuccessPlatformService

from app.models.base import Base
from app.models.customer_success import (
    ClientAccountPlanModel,
    ClientGoalModel,
    ClientHealthHistoryModel,
    ClientHealthScoreModel,
    ClientOpportunityModel,
    ClientProfileModel,
    ClientReferralModel,
    ClientRelationshipModel,
    ClientReviewModel,
    ClientRiskModel,
    ClientSentimentAnalysisModel,
    ClientSuccessPlanModel,
    ClientSuccessTaskModel,
    ClientSurveyModel,
    ClientSurveyResponseModel,
    ClientTimelineEventModel,
)
from app.repositories.customer_success import CustomerSuccessRepository

from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.customer_success.agent import CustomerSuccessAgent
from agents.customer_success.health import CustomerSuccessHealthEvaluator
from agents.customer_success.opportunity import CustomerSuccessOpportunityFinder
from agents.customer_success.recommendations import CustomerSuccessRecommendationEngine
from agents.customer_success.risk import CustomerSuccessRiskDetector
from agents.customer_success.validation import CustomerSuccessSafetyValidator


@pytest.fixture
def db_session():
    """Create in-memory SQLite database session for unit testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ==============================================================================
# 1. Health Scoring Engine Tests
# ==============================================================================

def test_health_scoring_engine_full_data():
    engine = HealthScoringEngine()
    factors = {
        "engagement": Decimal("80.00"),
        "project_health": Decimal("85.00"),
        "support_health": Decimal("90.00"),
        "financial_health": Decimal("95.00"),
        "satisfaction": Decimal("90.00"),
        "relationship": Decimal("75.00"),
        "goal_progress": Decimal("80.00"),
    }
    res = engine.calculate_health_score(
        client_id="client-001",
        factors_input=factors,
    )

    assert res.health_band in (HealthBand.HEALTHY, HealthBand.EXCELLENT, HealthBand.GOOD)
    assert res.overall_score >= Decimal("80.00")
    assert res.confidence == "HIGH"
    assert "Overall health is" in res.explanation


def test_health_scoring_engine_insufficient_data():
    engine = HealthScoringEngine()
    factors = {
        "engagement": Decimal("80.00"),
        # Only 1 factor provided
    }
    res = engine.calculate_health_score(
        client_id="client-002",
        factors_input=factors,
    )
    assert res.health_band == HealthBand.INSUFFICIENT_DATA
    assert res.confidence == "LOW"
    assert "insufficient" in res.explanation.lower()


def test_health_scoring_engine_missing_factors_renormalization():
    engine = HealthScoringEngine()
    factors = {
        "engagement": Decimal("90.00"),
        "project_health": Decimal("90.00"),
    }
    res = engine.calculate_health_score(
        client_id="client-003",
        factors_input=factors,
    )
    assert res.health_band in (HealthBand.HEALTHY, HealthBand.EXCELLENT, HealthBand.GOOD)
    assert res.overall_score == Decimal("90.00")


def test_health_scoring_trend_detection():
    engine = HealthScoringEngine()
    # Improving trend: past was 60, 65, 70 -> current is 85
    factors = {
        "engagement": Decimal("85.00"),
        "project_health": Decimal("85.00"),
    }
    res_improving = engine.calculate_health_score(
        client_id="client-004",
        factors_input=factors,
        historical_scores=[Decimal("60.00"), Decimal("65.00"), Decimal("70.00")],
    )
    assert res_improving.trend == "IMPROVING"

    # Declining trend: past was 90, 85, 80 -> current is 60
    factors_declining = {
        "engagement": Decimal("60.00"),
        "project_health": Decimal("60.00"),
    }
    res_declining = engine.calculate_health_score(
        client_id="client-005",
        factors_input=factors_declining,
        historical_scores=[Decimal("90.00"), Decimal("85.00"), Decimal("80.00")],
    )
    assert res_declining.trend == "DECLINING"


# ==============================================================================
# 2. Timeline Aggregator & 360 Synthesizer Tests
# ==============================================================================

def test_timeline_aggregator():
    events = [
        {"event_type": "SUPPORT", "title": "Ticket #101 Resolved", "occurred_at": "2026-09-01T10:00:00Z"},
        {"event_type": "PROJECT", "title": "Milestone Alpha Done", "occurred_at": "2026-09-05T12:00:00Z"},
    ]
    aggregated = ClientTimelineAggregator.aggregate_timeline(events=events, limit=10)
    assert len(aggregated) == 2
    # Chronological descending: Milestone Alpha occurred later
    assert aggregated[0]["title"] == "Milestone Alpha Done"


def test_client_360_synthesizer_and_privacy_masking():
    synthesizer = Client360Synthesizer()
    auth_manager = CustomerSuccessAuthorizationManager()

    raw_360 = synthesizer.build_360_view(
        profile={"client_id": "client-123", "business_name": "Acme Corp", "lifecycle_stage": "ACTIVE"},
        contacts=[{"contact_name": "Jane Doe", "decision_role": "DECISION_MAKER"}],
        health_score={"overall_score": "88.00", "health_band": "HEALTHY", "confidence": "HIGH", "trend": "STABLE"},
        goals=[{"title": "Goal 1"}],
        success_plans=[],
        projects=[{"name": "App Dev", "status": "ACTIVE"}],
        financial_summary={"total_invoiced": 50000.00, "internal_margins": 15000.00},
        support_summary={"open_tickets": 0},
        risks=[{"title": "Internal Margin Squeeze", "category": "FINANCIAL", "severity": "HIGH", "status": "OPEN"}],
        opportunities=[{"title": "Cross-sell AI Ops", "estimated_value": 20000.00}],
        renewals=[{"title": "Annual SaaS", "status": "UPCOMING"}],
        surveys=[],
    )

    assert raw_360["business_name"] == "Acme Corp"
    assert raw_360["financial_overview"]["internal_margins"] == 15000.00

    # Mask for client portal
    masked = auth_manager.mask_client_360_payload(raw_360, is_client=True)
    assert "internal_margins" not in masked["financial_overview"]
    assert masked["risks_overview"]["risks"] == []


# ==============================================================================
# 3. Database Repository Tests
# ==============================================================================

def test_customer_success_repository_flow(db_session):
    repo = CustomerSuccessRepository(db_session)
    tenant_id = "tenant-001"
    client_id = "client-999"

    # Profile upsert
    profile = repo.create_or_update_profile(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "business_name": "Apex Global Solutions",
            "lifecycle_stage": "ACTIVE",
            "relationship_strength": "STRONG",
        },
    )
    assert profile.business_name == "Apex Global Solutions"

    # Relationships
    rel = repo.create_relationship(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "contact_name": "Sarah Connor",
            "contact_email": "sarah@apex.io",
            "decision_role": "DECISION_MAKER",
        },
    )
    assert rel.contact_name == "Sarah Connor"
    rels = repo.list_relationships(tenant_id=tenant_id, client_id=client_id)
    assert len(rels) == 1

    # Goals
    goal = repo.create_goal(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "title": "Migrate 100% of ERP data",
            "status": "IN_PROGRESS",
            "progress_percentage": Decimal("65.00"),
        },
    )
    assert goal.title == "Migrate 100% of ERP data"

    # Health record & history
    health = repo.record_health_score(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "composite_score": Decimal("84.50"),
            "health_band": "HEALTHY",
            "engagement_score": Decimal("80.00"),
            "project_health_score": Decimal("90.00"),
            "confidence_score": "HIGH",
            "trend": "IMPROVING",
            "explanation_summary": "Strong project performance.",
        },
    )
    assert health.overall_score == Decimal("84.50")
    history = repo.list_health_history(tenant_id=tenant_id, client_id=client_id)
    assert len(history) == 1
    assert history[0].score == Decimal("84.50")

    # Risks & Opportunities
    risk = repo.create_risk(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "category": "PAYMENT",
            "title": "Delayed Invoice Payment",
            "severity": "MEDIUM",
        },
    )
    assert risk.title == "Delayed Invoice Payment"

    opp = repo.create_opportunity(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "opportunity_type": "EXPANSION",
            "title": "Phase 2 Mobile App Extension",
            "estimated_value": Decimal("30000.00"),
        },
    )
    assert opp.estimated_value == Decimal("30000.00")

    # Renewals
    renewal = repo.create_renewal(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "current_period_end": datetime(2026, 12, 31, tzinfo=timezone.utc),
            "renewal_date": datetime(2026, 12, 31, tzinfo=timezone.utc),
            "estimated_renewal_value": Decimal("120000.00"),
            "renewal_probability": Decimal("80.00"),
        },
    )
    assert renewal.contract_value == Decimal("120000.00")

    # Surveys & Sentiment
    survey = repo.create_survey(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "survey_type": "CSAT",
            "title": "Post-Onboarding CSAT Survey",
        },
    )
    response = repo.submit_survey_response(
        data={
            "tenant_id": tenant_id,
            "survey_id": survey.id,
            "score": Decimal("9.50"),
            "feedback_text": "Excellent team and rapid onboarding experience!",
        }
    )
    assert response.score == Decimal("9.50")

    # Account Plan & Reviews
    plan = repo.create_account_plan(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "title": "Account Plan 2027",
            "fiscal_year": "2027",
            "account_strategy": "Automated Cloud Ingestion",
            "revenue_target": Decimal("250000.00"),
        },
    )
    assert plan.title == "Account Plan 2027"

    review = repo.create_review(
        tenant_id=tenant_id,
        data={
            "client_id": client_id,
            "review_type": "QBR",
            "scheduled_date": datetime(2026, 10, 15, tzinfo=timezone.utc),
            "attendees": ["Sarah Connor", "John Doe"],
        },
    )
    assert review.review_type == "QBR"


# ==============================================================================
# 4. Agent Safety, Detectors & Recommendations Tests
# ==============================================================================

def test_customer_success_safety_guardrails():
    validator = CustomerSuccessSafetyValidator()
    
    # Allowed
    validator.validate_action("evaluate_health")
    validator.validate_action("detect_risks")
    validator.validate_action("discover_opportunities")
    validator.validate_action("generate_recommendations")

    # Prohibited actions raise AgentPermissionDeniedError
    with pytest.raises(AgentPermissionDeniedError):
        validator.validate_action("SEND_CLIENT_MESSAGE")

    with pytest.raises(AgentPermissionDeniedError):
        validator.validate_action("APPROVE_RENEWAL")

    with pytest.raises(AgentPermissionDeniedError):
        validator.validate_action("CHANGE_CLIENT_PRICING")


def test_customer_success_risk_detector():
    detector = CustomerSuccessRiskDetector()
    risks = detector.scan_for_risks(
        health_score=Decimal("40.00"),
        unpaid_invoices_count=2,
        days_since_last_contact=45,
        critical_tickets_count=1,
        negative_sentiment_ratio=0.5,
        contract_days_remaining=30,
    )

    categories = [r["category"] for r in risks]
    assert RiskCategory.CHURN.value in categories
    assert RiskCategory.PAYMENT.value in categories
    assert RiskCategory.RELATIONSHIP.value in categories
    assert RiskCategory.DELIVERY.value in categories
    assert RiskCategory.SATISFACTION.value in categories
    assert RiskCategory.CONTRACT.value in categories


def test_customer_success_opportunity_finder():
    finder = CustomerSuccessOpportunityFinder()
    opps = finder.discover_opportunities(
        health_score=Decimal("85.00"),
        completed_milestones=4,
        high_csat_responses=3,
        active_services_count=1,
        goals_completed_percentage=Decimal("90.00"),
    )

    types = [o["opportunity_type"] for o in opps]
    assert OpportunityType.EXPANSION.value in types
    assert OpportunityType.REFERRAL.value in types
    assert OpportunityType.CROSS_SELL.value in types
    assert OpportunityType.NEW_PROJECT.value in types


def test_customer_success_recommendation_engine():
    engine = CustomerSuccessRecommendationEngine()
    recs = engine.generate_recommendations(
        health_score=Decimal("90.00"),
        days_since_qbr=120,
        unmet_goals_count=2,
        renewal_days_remaining=45,
    )

    actions = [r["action"] for r in recs]
    assert "SCHEDULE_QBR" in actions
    assert "REVIEW_CLIENT_GOALS" in actions
    assert "PREPARE_RENEWAL_PACKAGE" in actions
    assert "REQUEST_TESTIMONIAL" in actions


@pytest.mark.asyncio
async def test_customer_success_agent_execution():
    agent = CustomerSuccessAgent()

    # Health evaluation task
    ctx_health = AgentContext(
        workflow_id="wf-001",
        task_id="task-001",
        agent_run_id="run-001",
        metadata={
            "task": "evaluate_health",
            "engagement_score": "80.00",
            "project_health_score": "85.00",
            "support_satisfaction_score": "90.00",
            "financial_health_score": "95.00",
            "relationship_health_score": "80.00",
            "goal_progress_score": "85.00",
        },
    )
    res_health = await agent.run(ctx_health)
    assert res_health.status == "completed"
    assert res_health.result["health_band"] in ("HEALTHY", "EXCELLENT", "GOOD")

    # Risk detection task
    ctx_risk = AgentContext(
        workflow_id="wf-001",
        task_id="task-002",
        agent_run_id="run-002",
        metadata={
            "task": "detect_risks",
            "health_score": "45.00",
            "unpaid_invoices_count": 2,
        },
    )
    res_risk = await agent.run(ctx_risk)
    assert res_risk.status == "completed"
    assert len(res_risk.result["detected_risks"]) >= 2

    # Prohibited action task
    ctx_bad = AgentContext(
        workflow_id="wf-001",
        task_id="task-003",
        agent_run_id="run-003",
        metadata={"task": "SEND_CLIENT_MESSAGE"},
    )
    with pytest.raises(AgentPermissionDeniedError):
        await agent.run(ctx_bad)
