import sys
from pathlib import Path

import pytest

root_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.user import User
from app.services.scoring import ScoringService
from app.services.scoring.engine import ScoringEngine
from app.services.scoring.models import ScoringContext
from app.services.scoring.versions import get_band_for_score
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_headers():
    db = TestingSessionLocal()
    user = User(
        email="scorer@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Norths Scorer",
        role="ADMIN",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_business_and_lead():
    db = TestingSessionLocal()
    biz = Business(
        name="Vortex Automation Systems",
        normalized_name="vortex automation systems",
        industry="Technology",
        city="Dallas",
        status="ACTIVE",
        website_url=None,
        normalized_website=None,
        phone="+1-214-555-0177",
        email="contact@vortex.test",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)

    lead = Lead(
        business_id=biz.id,
        title="Enterprise Automation & Web Retainer Opportunity",
        status="NEW",
        priority="HIGH",
        qualification_status="QUALIFIED",
        contactability_status="CONTACTABLE",
        estimated_value=15000.0,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    db.close()
    return biz, lead


# 1. Score Band Boundary Testing
def test_score_band_boundary_assignments():
    assert get_band_for_score(0) == "VERY_LOW"
    assert get_band_for_score(39) == "VERY_LOW"
    assert get_band_for_score(40) == "LOW"
    assert get_band_for_score(59) == "LOW"
    assert get_band_for_score(60) == "MEDIUM"
    assert get_band_for_score(79) == "MEDIUM"
    assert get_band_for_score(80) == "HIGH"
    assert get_band_for_score(100) == "HIGH"


# 2. Weighted Formula Verification
def test_scoring_engine_weighted_formula_calculation(sample_business_and_lead):
    biz, lead = sample_business_and_lead
    ctx = ScoringContext(business=biz, lead=lead)

    result = ScoringEngine.calculate_opportunity_score(ctx)

    # Business has no website, so Website Need is 100 (weighted 25% = +25 pts)
    # Business is ACTIVE (+80, weighted 10% = +8 pts)
    # Phone + Email (+80, weighted 10% = +8 pts)
    # Industry Technology (+15 automation, +75 service fit)
    assert result.total_score > 50.0
    assert result.score_version == "1.0"
    assert result.band in ("HIGH", "MEDIUM", "LOW", "VERY_LOW")
    assert result.confidence in ("HIGH", "MEDIUM", "LOW")


# 3. Component Rules - No Website Opportunity Signal
def test_website_need_max_score_when_no_website(sample_business_and_lead):
    biz, lead = sample_business_and_lead
    ctx = ScoringContext(business=biz, lead=lead)

    result = ScoringEngine.calculate_opportunity_score(ctx)
    c_web = result.component_scores["website_need"]

    assert c_web.score == 100.0
    assert c_web.weighted_contribution == 25.0
    assert "No official website recorded for business" in c_web.reasons


# 4. Service Layer Workflow & History
def test_scoring_service_workflow(sample_business_and_lead):
    db = TestingSessionLocal()
    biz, lead = sample_business_and_lead

    # Calculate initial score
    score1 = ScoringService.calculate_lead_score(db, lead.id)
    assert score1.total_score > 0
    assert score1.is_stale is False

    # Recalculate score (should mark previous score stale and add history)
    score2 = ScoringService.calculate_lead_score(db, lead.id)
    assert score2.id != score1.id
    assert score2.is_stale is False

    history = ScoringService.get_lead_score_history(db, lead.id)
    assert len(history) == 2
    db.close()


# 5. REST API Endpoint Tests
def test_scoring_api_endpoints(auth_headers, sample_business_and_lead):
    client = TestClient(app)
    biz, lead = sample_business_and_lead

    # Require auth
    unauth_resp = client.get(f"/api/v1/scoring/leads/{lead.id}")
    assert unauth_resp.status_code == 401

    # Calculate score via API
    calc_resp = client.post(
        f"/api/v1/scoring/leads/{lead.id}/calculate",
        headers=auth_headers,
    )
    assert calc_resp.status_code == 200
    assert calc_resp.json()["data"]["total_score"] > 0
    assert calc_resp.json()["data"]["band"] in ("HIGH", "MEDIUM", "LOW", "VERY_LOW")

    # Get lead score via API
    get_resp = client.get(
        f"/api/v1/scoring/leads/{lead.id}",
        headers=auth_headers,
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["lead_id"] == str(lead.id)

    # Get lead score history via API
    hist_resp = client.get(
        f"/api/v1/scoring/leads/{lead.id}/history",
        headers=auth_headers,
    )
    assert hist_resp.status_code == 200
    assert hist_resp.json()["data"]["total_scores"] == 1
