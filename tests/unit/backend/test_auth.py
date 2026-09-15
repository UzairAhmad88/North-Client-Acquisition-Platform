import sys
from pathlib import Path

import pytest

# Ensure root path is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.api.deps import get_db
from app.core.security import hash_password, normalize_email, verify_password
from app.main import app
from app.models.base import Base
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
    app.dependency_overrides.pop(get_db, None)


client = TestClient(app)


def test_password_hashing_and_verification():
    raw_password = "SecurePassword123!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_email_normalization():
    assert normalize_email("  User@Example.COM ") == "user@example.com"


def test_register_user_success():
    payload = {
        "email": "Operator@Uzaii.Com",
        "password": "Password123!",
        "full_name": "Uzaii Operator",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]

    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "operator@uzaii.com"
    assert data["user"]["full_name"] == "Uzaii Operator"
    assert "password" not in data["user"]
    assert "password_hash" not in data["user"]
    assert data["token"]["access_token"] is not None


def test_register_duplicate_email_fails():
    payload = {
        "email": "duplicate@uzaii.com",
        "password": "Password123!",
        "full_name": "First User",
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    err_data = res2.json()
    assert err_data["error"]["code"] == "DUPLICATE_ACCOUNT"


def test_login_success_and_protected_me_endpoint():
    # Register user first
    reg_payload = {
        "email": "login_test@uzaii.com",
        "password": "SecretPassword123!",
        "full_name": "Login User",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_payload = {
        "email": "LOGIN_TEST@UZAII.COM",
        "password": "SecretPassword123!",
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token = login_res.json()["data"]["token"]["access_token"]

    # Access protected /auth/me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    user_data = me_res.json()["data"]
    assert user_data["email"] == "login_test@uzaii.com"
    assert "password_hash" not in user_data


def test_login_invalid_credentials():
    login_payload = {
        "email": "nonexistent@uzaii.com",
        "password": "WrongPassword",
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "AUTH_REQUIRED"


def test_protected_route_unauthenticated_fails():
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "AUTH_REQUIRED"


def test_protected_route_inactive_account_blocked():
    # Create user directly and mark inactive
    db = TestingSessionLocal()
    hashed = hash_password("Password123!")
    user = User(
        email="inactive@uzaii.com",
        password_hash=hashed,
        full_name="Inactive User",
        is_active=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    # Attempt login
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "inactive@uzaii.com", "password": "Password123!"},
    )
    assert login_res.status_code == 403
    assert login_res.json()["error"]["code"] == "FORBIDDEN"
