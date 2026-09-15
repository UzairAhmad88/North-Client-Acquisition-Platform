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
from app.services.seed_catalog import seed_service_catalog
from app.services.service import ServiceCatalogService
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
        "email": "catalog_admin@uzaii.com",
        "password": "SecurePassword123!",
        "full_name": "Catalog Admin",
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    return res.json()["data"]["token"]["access_token"]


def test_slugify_helper():
    assert ServiceCatalogService.slugify("Business Website & Portal!") == "business-website-portal"
    assert ServiceCatalogService.slugify("AI Support Agent v2.0") == "ai-support-agent-v20"


def test_service_crud_workflow():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Service
    payload = {
        "name": "Custom Executive Dashboard",
        "category": "SOFTWARE_DEVELOPMENT",
        "short_description": "Interactive reporting dashboard visualizing key KPIs.",
        "description": "Custom business analytics portal.",
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 1500.0,
        "currency": "USD",
        "estimated_duration_days": 20,
        "features": ["Real-time Charts", "CSV Exports"],
    }
    create_res = client.post("/api/v1/services", json=payload, headers=headers)
    assert create_res.status_code == 201
    srv = create_res.json()["data"]
    srv_id = srv["id"]

    assert srv["name"] == "Custom Executive Dashboard"
    assert srv["slug"] == "custom-executive-dashboard"
    assert srv["category"] == "SOFTWARE_DEVELOPMENT"
    assert srv["base_price"] == 1500.0

    # 2. Get by Slug
    slug_res = client.get("/api/v1/services/slug/custom-executive-dashboard")
    assert slug_res.status_code == 200
    assert slug_res.json()["data"]["id"] == srv_id

    # 3. Update Service
    update_res = client.patch(
        f"/api/v1/services/{srv_id}",
        json={"base_price": 1800.0, "short_description": "Updated dashboard summary."},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["base_price"] == 1800.0

    # 4. Archive & Restore
    archive_res = client.post(f"/api/v1/services/{srv_id}/archive", headers=headers)
    assert archive_res.status_code == 200
    assert archive_res.json()["data"]["status"] == "ARCHIVED"

    restore_res = client.post(f"/api/v1/services/{srv_id}/restore", headers=headers)
    assert restore_res.status_code == 200
    assert restore_res.json()["data"]["status"] == "ACTIVE"


def test_pricing_validation():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Negative price rejected by Pydantic schema validation (422)
    res1 = client.post(
        "/api/v1/services",
        json={"name": "Invalid Price Srv", "base_price": -50.0},
        headers=headers,
    )
    assert res1.status_code == 422

    # Price min > price max rejected by service layer domain validation (400)
    res2 = client.post(
        "/api/v1/services",
        json={"name": "Invalid Range Srv", "price_min": 5000.0, "price_max": 2000.0},
        headers=headers,
    )
    assert res2.status_code == 400
    assert res2.json()["error"]["code"] == "INVALID_PRICING"


def test_seed_catalog_framework():
    db = TestingSessionLocal()
    count1 = seed_service_catalog(db)
    assert count1 >= 5

    # Verify idempotency (re-running creates 0 duplicate services)
    count2 = seed_service_catalog(db)
    assert count2 == 0
    db.close()


def test_lead_service_association():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create business & lead
    biz_res = client.post(
        "/api/v1/businesses",
        json={"name": "Tech Corp", "city": "Peshawar"},
        headers=headers,
    )
    biz_id = biz_res.json()["data"]["id"]

    lead_res = client.post(
        "/api/v1/leads",
        json={"business_id": biz_id, "title": "Web & AI Integration"},
        headers=headers,
    )
    lead_id = lead_res.json()["data"]["id"]

    # Create catalog service
    srv_res = client.post(
        "/api/v1/services",
        json={"name": "AI Qualification Agent", "category": "AI_SYSTEMS"},
        headers=headers,
    )
    srv_id = srv_res.json()["data"]["id"]

    # Attach service to lead
    attach_res = client.post(
        f"/api/v1/leads/{lead_id}/services",
        json={"service_id": srv_id, "relationship_type": "RECOMMENDED"},
        headers=headers,
    )
    assert attach_res.status_code == 201
    assert attach_res.json()["data"]["relationship_type"] == "RECOMMENDED"

    # List lead services
    list_res = client.get(f"/api/v1/leads/{lead_id}/services", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()["data"]) == 1

    # Remove service from lead
    del_res = client.delete(
        f"/api/v1/leads/{lead_id}/services/{srv_id}", headers=headers
    )
    assert del_res.status_code == 200
    assert del_res.json()["data"]["success"] is True


def test_unauthenticated_service_admin_blocked():
    assert client.post("/api/v1/services", json={"name": "Test"}).status_code == 401
    assert client.patch(f"/api/v1/services/{uuid.uuid4()}", json={"name": "X"}).status_code == 401
    assert client.delete(f"/api/v1/services/{uuid.uuid4()}").status_code == 401
