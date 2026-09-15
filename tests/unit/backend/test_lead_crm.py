import sys
import uuid
from pathlib import Path

import pytest

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.api.deps import get_db
from app.main import app
from app.models.base import Base
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
    app.dependency_overrides.pop(get_db, None)


client = TestClient(app)


def get_auth_token():
    reg_payload = {
        "email": "lead_operator@uzaii.com",
        "password": "SecurePassword123!",
        "full_name": "Lead Operator",
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    return res.json()["data"]["token"]["access_token"]


def create_sample_business(headers):
    biz_payload = {
        "name": "Khyber Tech Labs",
        "city": "Peshawar",
        "industry": "SOFTWARE",
    }
    res = client.post("/api/v1/businesses", json=biz_payload, headers=headers)
    return res.json()["data"]["id"]


def test_lead_crud_and_lifecycle():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    biz_id = create_sample_business(headers)

    # 1. Create Lead
    lead_payload = {
        "business_id": biz_id,
        "title": "Custom Enterprise CRM Development",
        "description": "Building custom AI client acquisition portal.",
        "priority": "HIGH",
        "estimated_value": 5000.0,
        "currency": "USD",
        "next_action": "Audit current workflow",
    }
    create_res = client.post("/api/v1/leads", json=lead_payload, headers=headers)
    assert create_res.status_code == 201
    lead = create_res.json()["data"]
    lead_id = lead["id"]

    assert lead["title"] == "Custom Enterprise CRM Development"
    assert lead["status"] == "NEW"
    assert lead["business"]["id"] == biz_id
    assert lead["data_quality"]["score"] >= 50

    # 2. Status Transition -> CONTACTED
    trans_res1 = client.post(
        f"/api/v1/leads/{lead_id}/transition",
        json={"status": "CONTACTED"},
        headers=headers,
    )
    assert trans_res1.status_code == 200
    updated1 = trans_res1.json()["data"]
    assert updated1["status"] == "CONTACTED"
    assert updated1["first_contacted_at"] is not None

    # 3. Status Transition -> WON
    trans_res2 = client.post(
        f"/api/v1/leads/{lead_id}/transition",
        json={"status": "WON"},
        headers=headers,
    )
    assert trans_res2.status_code == 200
    updated2 = trans_res2.json()["data"]
    assert updated2["status"] == "WON"
    assert updated2["converted_at"] is not None

    # 4. Archive & Restore
    archive_res = client.post(f"/api/v1/leads/{lead_id}/archive", headers=headers)
    assert archive_res.status_code == 200
    assert archive_res.json()["data"]["status"] == "ARCHIVED"

    restore_res = client.post(f"/api/v1/leads/{lead_id}/restore", headers=headers)
    assert restore_res.status_code == 200
    assert restore_res.json()["data"]["status"] == "NEW"


def test_invalid_business_id_rejected():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    fake_biz_id = str(uuid.uuid4())
    res = client.post(
        "/api/v1/leads",
        json={"business_id": fake_biz_id, "title": "Orphaned Opportunity"},
        headers=headers,
    )
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "BUSINESS_NOT_FOUND"


def test_contact_management_subsystem():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    biz_id = create_sample_business(headers)

    lead_res = client.post(
        "/api/v1/leads",
        json={"business_id": biz_id, "title": "Mobile App Consultation"},
        headers=headers,
    )
    lead_id = lead_res.json()["data"]["id"]

    # Add Contact 1 (Primary)
    c1_res = client.post(
        "/api/v1/contacts",
        json={
            "business_id": biz_id,
            "lead_id": lead_id,
            "name": "Jane Doe",
            "role": "CEO",
            "email": "jane@khybertech.pk",
            "is_primary": True,
        },
        headers=headers,
    )
    assert c1_res.status_code == 201
    assert c1_res.json()["data"]["is_primary"] is True

    # Add Contact 2 (Primary -> unsets Contact 1 primary)
    c2_res = client.post(
        "/api/v1/contacts",
        json={
            "business_id": biz_id,
            "lead_id": lead_id,
            "name": "John Smith",
            "role": "CTO",
            "email": "john@khybertech.pk",
            "is_primary": True,
        },
        headers=headers,
    )
    assert c2_res.status_code == 201
    assert c2_res.json()["data"]["is_primary"] is True

    # Verify contacts for lead
    contacts_res = client.get(f"/api/v1/contacts?lead_id={lead_id}", headers=headers)
    assert contacts_res.status_code == 200
    contacts = contacts_res.json()["data"]
    assert len(contacts) == 2


def test_duplicate_lead_check():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    biz_id = create_sample_business(headers)

    client.post(
        "/api/v1/leads",
        json={"business_id": biz_id, "title": "Website Redesign & SEO"},
        headers=headers,
    )

    dup_res = client.post(
        f"/api/v1/leads/check-duplicate?business_id={biz_id}&title=Website Redesign SEO",
        headers=headers,
    )
    assert dup_res.status_code == 200
    dup_data = dup_res.json()["data"]
    assert dup_data["possible_duplicate"] is True
    assert "same_business_and_title" in dup_data["signals"]


def test_unauthenticated_lead_api_blocked():
    assert client.get("/api/v1/leads").status_code == 401
    assert client.post("/api/v1/leads", json={"title": "Test"}).status_code == 401
    assert client.get(f"/api/v1/leads/{uuid.uuid4()}").status_code == 401
