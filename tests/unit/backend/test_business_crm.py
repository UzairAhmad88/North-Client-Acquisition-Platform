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
from app.services.business import BusinessService
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
        "email": "biz_operator@uzaii.com",
        "password": "SecurePassword123!",
        "full_name": "Business Operator",
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    return res.json()["data"]["token"]["access_token"]


def test_data_normalization_unit():
    assert BusinessService.normalize_name("  Iron Gym & Fitness!  ") == "iron gym fitness"
    assert BusinessService.normalize_phone("+92 (300) 123-4567") == "+923001234567"
    assert BusinessService.normalize_email(" INFO@IronGym.PK ") == "info@irongym.pk"
    assert (
        BusinessService.normalize_website("https://www.irongym.pk/about/")
        == "irongym.pk/about"
    )


def test_business_crud_workflow():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Business
    create_payload = {
        "name": "Khyber Fitness Center",
        "legal_name": "Khyber Fitness Pvt Ltd",
        "description": "Premium health and fitness club in Peshawar.",
        "business_type": "GYM",
        "industry": "FITNESS",
        "phone": "+92 300 9876543",
        "email": "contact@khyberfitness.pk",
        "website_url": "https://khyberfitness.pk",
        "city": "Peshawar",
        "country": "Pakistan",
        "address": "University Road",
        "source": "MANUAL",
    }

    create_res = client.post("/api/v1/businesses", json=create_payload, headers=headers)
    assert create_res.status_code == 201
    biz = create_res.json()["data"]
    biz_id = biz["id"]

    assert biz["name"] == "Khyber Fitness Center"
    assert biz["normalized_name"] == "khyber fitness center"
    assert biz["status"] == "ACTIVE"
    assert biz["data_quality"]["score"] >= 80

    # 2. Get Business
    get_res = client.get(f"/api/v1/businesses/{biz_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["id"] == biz_id

    # 3. Update Business
    update_payload = {"city": "Islamabad", "industry": "HEALTH_FITNESS"}
    patch_res = client.patch(
        f"/api/v1/businesses/{biz_id}", json=update_payload, headers=headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["data"]["city"] == "Islamabad"

    # 4. Archive Business
    archive_res = client.post(f"/api/v1/businesses/{biz_id}/archive", headers=headers)
    assert archive_res.status_code == 200
    assert archive_res.json()["data"]["status"] == "ARCHIVED"
    assert archive_res.json()["data"]["archived_at"] is not None

    # 5. Restore Business
    restore_res = client.post(f"/api/v1/businesses/{biz_id}/restore", headers=headers)
    assert restore_res.status_code == 200
    assert restore_res.json()["data"]["status"] == "ACTIVE"
    assert restore_res.json()["data"]["archived_at"] is None


def test_business_search_filter_pagination():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create 3 businesses
    client.post(
        "/api/v1/businesses",
        json={"name": "Alpha Cafe", "city": "Peshawar", "industry": "RESTAURANT"},
        headers=headers,
    )
    client.post(
        "/api/v1/businesses",
        json={"name": "Beta Gym", "city": "Lahore", "industry": "FITNESS"},
        headers=headers,
    )
    client.post(
        "/api/v1/businesses",
        json={"name": "Gamma Clinic", "city": "Peshawar", "industry": "HEALTHCARE"},
        headers=headers,
    )

    # Filter by city
    res_city = client.get(
        "/api/v1/businesses?city=Peshawar", headers=headers
    )
    assert res_city.status_code == 200
    assert res_city.json()["pagination"]["total"] == 2

    # Search keyword
    res_search = client.get("/api/v1/businesses?search=Gym", headers=headers)
    assert res_search.status_code == 200
    assert res_search.json()["pagination"]["total"] == 1
    assert res_search.json()["data"][0]["name"] == "Beta Gym"

    # Sorting
    res_sort = client.get(
        "/api/v1/businesses?sort=name&order=asc", headers=headers
    )
    assert res_sort.status_code == 200
    names = [b["name"] for b in res_sort.json()["data"]]
    assert names == ["Alpha Cafe", "Beta Gym", "Gamma Clinic"]


def test_duplicate_detection_endpoint():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/businesses",
        json={
            "name": "Peshawar Bakery",
            "email": "orders@peshawarbakery.pk",
            "website_url": "https://peshawarbakery.pk",
            "city": "Peshawar",
        },
        headers=headers,
    )

    # Check duplicate with same website
    dup_res = client.post(
        "/api/v1/businesses/check-duplicate?name=New Bakery&website_url=https://www.peshawarbakery.pk",
        headers=headers,
    )
    assert dup_res.status_code == 200
    dup_data = dup_res.json()["data"]
    assert dup_data["possible_duplicate"] is True
    assert "same_website_domain" in dup_data["signals"]
    assert dup_data["confidence"] >= 0.90


def test_unauthenticated_requests_blocked():
    assert client.get("/api/v1/businesses").status_code == 401
    assert client.post("/api/v1/businesses", json={"name": "Test"}).status_code == 401
    assert client.get(f"/api/v1/businesses/{uuid.uuid4()}").status_code == 401
