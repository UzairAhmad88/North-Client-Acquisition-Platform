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
from app.models.service import Service
from app.models.user import User
from app.services.recommendations import RecommendationEngine, RecommendationService
from app.services.recommendations.versions import calculate_priority, get_relevance_band
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
        email="recommender@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Norths Recommender",
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
def sample_data():
    db = TestingSessionLocal()
    biz = Business(
        name="Apex Fitness & Gym",
        normalized_name="apex fitness & gym",
        category="gym",
        city="Chicago",
        status="ACTIVE",
        website_url=None,
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)

    lead = Lead(
        business_id=biz.id,
        title="Apex Gym Digital Transformation",
        status="NEW",
        priority="HIGH",
    )
    db.add(lead)
    db.commit()

    service1 = Service(
        name="Gym Website Development",
        slug="gym-website",
        category="WEB_DEVELOPMENT",
        status="ACTIVE",
        is_active=True,
        target_business_types=["gym", "fitness"],
    )
    service2 = Service(
        name="Online Booking & Membership System",
        slug="booking-system",
        category="SOFTWARE",
        status="ACTIVE",
        is_active=True,
        target_business_types=["gym", "restaurant", "hotel"],
    )
    db.add(service1)
    db.add(service2)
    db.commit()
    db.refresh(lead)
    db.refresh(service1)
    db.refresh(service2)
    db.close()
    return biz, lead, service1, service2


# 1. Band & Priority Logic Tests
def test_relevance_band_and_priority_matrix():
    assert get_relevance_band(85) == "STRONG"
    assert get_relevance_band(75) == "GOOD"
    assert get_relevance_band(45) == "POSSIBLE"
    assert get_relevance_band(20) == "WEAK"

    assert calculate_priority(90, "HIGH") == "HIGH"
    assert calculate_priority(90, "LOW") == "MEDIUM"
    assert calculate_priority(70, "HIGH") == "MEDIUM"
    assert calculate_priority(70, "LOW") == "LOW"
    assert calculate_priority(30, "HIGH") == "LOW"


# 2. Recommendation Engine Candidate Evaluation
def test_recommendation_engine_calculation(sample_data):
    biz, lead, service1, service2 = sample_data
    rec_service = RecommendationService()
    db = TestingSessionLocal()

    context = rec_service.build_context(db, lead.id)
    engine_inst = RecommendationEngine()
    candidates = engine_inst.calculate_recommendations(context)

    assert len(candidates) == 2
    # Gym website should rank very high since business has no website and is a gym
    top_cand = candidates[0]
    assert top_cand.relevance_score > 50.0
    assert top_cand.band in ("STRONG", "GOOD", "POSSIBLE")
    assert len(top_cand.reasons) > 0
    assert len(top_cand.limitations) > 0
    db.close()


# 3. Recommendation Service Workflow (Calculate, Accept, Reject)
def test_recommendation_service_actions(sample_data):
    biz, lead, service1, service2 = sample_data
    rec_service = RecommendationService()
    db = TestingSessionLocal()

    # Calculate
    recs = rec_service.calculate_lead_recommendations(db, lead.id)
    assert len(recs) == 2
    rec = recs[0]
    assert rec.status == "SUGGESTED"

    # Accept recommendation
    user = db.query(User).first()
    if not user:
        user = User(
            email="testuser@norths.agency",
            password_hash=hash_password("Pass123!"),
            full_name="Test User",
            role="USER",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    accepted = rec_service.accept_recommendation(db, rec.id, user.id)
    assert accepted.status == "ACCEPTED"
    assert accepted.accepted_by == user.id

    # Recalculate - should preserve ACCEPTED status
    recs_after = rec_service.calculate_lead_recommendations(db, lead.id)
    accepted_after = next(r for r in recs_after if r.id == rec.id)
    assert accepted_after.status == "ACCEPTED"

    # Reject second recommendation
    rec2 = recs[1]
    rejected = rec_service.reject_recommendation(db, rec2.id, user.id, reason="Not interested in software now")
    assert rejected.status == "REJECTED"
    assert rejected.rejection_reason == "Not interested in software now"

    db.close()


# 4. REST API Endpoint Tests
def test_recommendations_api(auth_headers, sample_data):
    client = TestClient(app)
    biz, lead, service1, service2 = sample_data

    # Unauthenticated check
    unauth = client.get(f"/api/v1/leads/{lead.id}/recommendations")
    assert unauth.status_code == 401

    # Calculate via API
    calc_resp = client.post(
        f"/api/v1/leads/{lead.id}/recommendations/calculate",
        headers=auth_headers,
    )
    assert calc_resp.status_code == 200
    calc_data = calc_resp.json()["data"]
    assert len(calc_data) == 2

    rec_id = calc_data[0]["id"]

    # Get list via API
    list_resp = client.get(
        f"/api/v1/leads/{lead.id}/recommendations",
        headers=auth_headers,
    )
    assert list_resp.status_code == 200
    assert list_resp.json()["pagination"]["total"] == 2

    # Get single via API
    single_resp = client.get(
        f"/api/v1/recommendations/{rec_id}",
        headers=auth_headers,
    )
    assert single_resp.status_code == 200
    assert single_resp.json()["data"]["id"] == rec_id

    # Accept via API
    accept_resp = client.post(
        f"/api/v1/recommendations/{rec_id}/accept",
        headers=auth_headers,
    )
    assert accept_resp.status_code == 200
    assert accept_resp.json()["data"]["status"] == "ACCEPTED"

    # Reject via API
    rec_id_2 = calc_data[1]["id"]
    reject_resp = client.post(
        f"/api/v1/recommendations/{rec_id_2}/reject",
        json={"reason": "Already implemented in-house"},
        headers=auth_headers,
    )
    assert reject_resp.status_code == 200
    assert reject_resp.json()["data"]["status"] == "REJECTED"
    assert reject_resp.json()["data"]["rejection_reason"] == "Already implemented in-house"
