"""Unit test suite for Phase 24 — Project Estimation, Effort & Commercial Intelligence Engine."""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.user import User
from app.services.requirements import RequirementsService
from app.services.solution import SolutionService
from app.services.estimate import EstimateService
from agents.estimation.agent import estimation_agent
from agents.estimation.estimator import PERTEstimator
from agents.estimation.costing import CostEngine
from agents.estimation.pricing import PricingRecommendationEngine
from agents.estimation.scenarios import ScenarioGenerator
from agents.estimation.validator import EstimationValidator
from agents.estimation.models import EstimateWorkItemSchema

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_estimation_agent_permissions():
    """Verify EstimationAgent holds zero send, pricing policy modification, or autonomous approval permissions."""
    perms = [p.value if hasattr(p, "value") else str(p) for p in estimation_agent.get_permissions()]

    for p in ("SEND_EMAIL", "SEND_MESSAGE", "SEND_WHATSAPP", "APPROVE_ESTIMATE", "MODIFY_PRICING_POLICY", "SIGN_CONTRACT", "MAKE_PAYMENT"):
        assert p not in perms


def test_pert_estimator_calculation():
    """Verify PERT three-point formula (O + 4M + P) / 6."""
    expected = PERTEstimator.calculate_expected_hours(optimistic=10.0, most_likely=20.0, pessimistic=40.0)
    # (10 + 80 + 40) / 6 = 130 / 6 = 21.6666... -> 21.7
    assert expected == 21.7


def test_costing_and_pricing_engine():
    """Verify internal labor costing and commercial recommendation range calculation."""
    labor_cost = CostEngine.calculate_internal_labor_cost(total_hours=100.0, hourly_rate=50.0)
    assert labor_cost == 5000.0

    buffer, rec_min, rec_max = PricingRecommendationEngine.calculate_commercial_range(
        internal_cost=5000.0, external_cost=200.0, risk_buffer_percent=20.0, min_margin=0.30, target_margin=0.50
    )
    # Base cost = 5200. Buffer = 1040. Total cost basis = 6240.
    # Min = 6240 * 1.30 = 8112. Max = 6240 * 1.50 = 9360.
    assert buffer == 1040.0
    assert rec_min == 8112.0
    assert rec_max == 9360.0


def test_scenario_generation():
    """Verify Lean, Standard, and Expanded project scenarios."""
    items = [
        EstimateWorkItemSchema(name="Web Frontend", category="FRONTEND", description="Web interface", optimistic_hours=10.0, most_likely_hours=15.0, pessimistic_hours=25.0, expected_hours=15.8),
        EstimateWorkItemSchema(name="Booking API", category="BACKEND", description="Booking endpoint", optimistic_hours=15.0, most_likely_hours=25.0, pessimistic_hours=40.0, expected_hours=25.8),
    ]

    scenarios = ScenarioGenerator.generate_scenarios(items, external_cost=100.0)
    assert len(scenarios) == 3
    names = [s.name for s in scenarios]
    assert "LEAN" in names
    assert "STANDARD" in names
    assert "EXPANDED" in names


def test_estimation_validator_safety():
    """Verify validator flags scope mismatches when solution features lack corresponding work items."""
    items = [EstimateWorkItemSchema(name="Web Frontend", category="FRONTEND", description="Web", optimistic_hours=5, most_likely_hours=10, pessimistic_hours=15, expected_hours=10)]
    sol_data = {"features": [{"title": "Web Frontend"}, {"title": "AI Assistant Bot"}]}

    warnings = EstimationValidator.validate_estimate_safety(items, sol_data)
    assert len(warnings) > 0
    assert "SCOPE_ESTIMATION_MISMATCH" in warnings[0]


@pytest.mark.asyncio
async def test_full_estimation_workflow(db_session: Session):
    """Verify end-to-end discovery -> solution design -> estimate calculation -> approval workflow."""
    biz = Business(name="Delta Software", normalized_name="delta software", email="info@deltasoftware.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Delta Web Portal", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="estimator@norths.com", password_hash="hashed_pwd", full_name="Estimator User", is_active=True)
    db_session.add(user)
    db_session.commit()

    # 1. Discovery & Solution Design
    disc_session = RequirementsService.create_discovery_session(
        db_session, business_id=biz.id, lead_id=lead.id, user_id=user.id
    )
    await RequirementsService.analyze_discovery_session(db_session, disc_session.id)

    sol_obj = SolutionService.create_solution_design(db_session, discovery_session_id=disc_session.id, user_id=user.id)
    await SolutionService.analyze_solution_design(db_session, sol_obj.id)
    SolutionService.approve_solution_design(db_session, sol_obj.id, user.id)

    # 2. Create Estimate Workspace
    est_obj = EstimateService.create_estimate(db_session, solution_id=sol_obj.id, user_id=user.id)
    assert est_obj.status == "DRAFT"

    # 3. Calculate Estimate with EstimationAgent
    calculated_est = await EstimateService.calculate_estimate(db_session, est_obj.id)
    assert calculated_est.status == "REVIEW"
    assert calculated_est.estimated_hours > 0
    assert calculated_est.recommended_min is not None
    assert len(calculated_est.work_items) > 0

    # 4. Approve Commercial Estimate
    approved_est = EstimateService.approve_estimate(db_session, est_obj.id, user.id)
    assert approved_est.status == "APPROVED"
    assert approved_est.approved_by_id == user.id
