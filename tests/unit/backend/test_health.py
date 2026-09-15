from unittest.mock import MagicMock

import pytest
from app.api.deps import get_db
from app.main import app
from fastapi.testclient import TestClient


def override_get_db():
    mock_db = MagicMock()
    mock_db.execute.return_value.scalar.return_value = 1
    yield mock_db

@pytest.fixture(autouse=True)
def setup_health_db_override():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["status"] == "ok"

def test_health_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"data": {"status": "alive"}}

def test_health_ready():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ready", "database": "connected"}}
