import sys
from datetime import datetime, timedelta, timezone
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
        email="operator@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Uzair North",
        role="ADMIN",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    db.close()
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_summary_requires_authentication():
    client = TestClient(app)
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401


def test_dashboard_summary_empty_database(auth_headers):
    client = TestClient(app)
    response = client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]

    assert data["businesses"]["active_count"] == 0
    assert data["businesses"]["total_count"] == 0
    assert data["leads"]["open_count"] == 0
    assert data["leads"]["qualified_count"] == 0
    assert data["leads"]["high_priority_count"] == 0
    assert data["leads"]["total_count"] == 0
    assert data["attention"]["high_priority_leads_count"] == 0
    assert data["attention"]["overdue_actions_count"] == 0
    assert len(data["overdue_actions"]) == 0
    assert len(data["upcoming_actions"]) == 0
    assert len(data["recent_leads"]) == 0
    assert len(data["recent_businesses"]) == 0
    assert data["services"]["active_services_count"] == 0


def test_dashboard_summary_with_seeded_data(auth_headers):
    db = TestingSessionLocal()
    now = datetime.now(timezone.utc)

    # 1. Active & Archived Business
    b1 = Business(
        name="Apex Solutions",
        normalized_name="apex solutions",
        industry="Technology",
        city="Austin",
        status="ACTIVE",
        phone="+15125550199",
        email="info@apexsolutions.com",
        website_url="https://apexsolutions.com",
    )
    b2 = Business(
        name="Legacy Corp",
        normalized_name="legacy corp",
        industry="Manufacturing",
        city="Chicago",
        status="ARCHIVED",
    )
    db.add_all([b1, b2])
    db.commit()
    db.refresh(b1)
    db.refresh(b2)

    # 2. Leads: Overdue, Upcoming, Qualified, Lost
    l1 = Lead(
        title="Apex Web Redesign",
        business_id=b1.id,
        status="NEW",
        priority="HIGH",
        qualification_status="QUALIFIED",
        next_action="Prepare Proposal",
        next_action_at=now - timedelta(days=2),  # Overdue
    )
    l2 = Lead(
        title="Apex AI Chatbot",
        business_id=b1.id,
        status="QUALIFIED",
        priority="URGENT",
        qualification_status="QUALIFIED",
        next_action="Client Demo",
        next_action_at=now + timedelta(days=3),  # Upcoming
    )
    l3 = Lead(
        title="Legacy System Maintenance",
        business_id=b2.id,
        status="LOST",
        priority="LOW",
        qualification_status="UNQUALIFIED",
    )
    db.add_all([l1, l2, l3])

    # 3. Services
    s1 = Service(
        name="Custom AI Agent System",
        slug="custom-ai-agent-system",
        category="AI_SYSTEMS",
        status="ACTIVE",
        is_active=True,
        is_featured=True,
    )
    db.add(s1)
    db.commit()
    db.close()

    client = TestClient(app)
    response = client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]

    # Verify Business Metrics
    assert data["businesses"]["active_count"] == 1
    assert data["businesses"]["total_count"] == 2

    # Verify Lead Metrics
    # Open leads: l1 (NEW) + l2 (QUALIFIED) = 2. l3 (LOST) is not open.
    assert data["leads"]["open_count"] == 2
    assert data["leads"]["qualified_count"] == 2  # l1 and l2 are QUALIFIED
    assert data["leads"]["high_priority_count"] == 2  # l1 (HIGH) and l2 (URGENT)
    assert data["leads"]["total_count"] == 3

    # Pipeline counts
    assert data["pipeline"]["counts"]["NEW"] == 1
    assert data["pipeline"]["counts"]["QUALIFIED"] == 1
    assert data["pipeline"]["counts"]["LOST"] == 1

    # Overdue and Upcoming Actions
    assert len(data["overdue_actions"]) == 1
    assert data["overdue_actions"][0]["lead_title"] == "Apex Web Redesign"
    assert data["overdue_actions"][0]["business_name"] == "Apex Solutions"

    assert len(data["upcoming_actions"]) == 1
    assert data["upcoming_actions"][0]["lead_title"] == "Apex AI Chatbot"

    # Services
    assert data["services"]["active_services_count"] == 1
    assert data["services"]["featured_services_count"] == 1
