import uuid

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_request_id_generated():
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    # Verify valid UUID structure
    val = response.headers["X-Request-ID"]
    uuid.UUID(val)

def test_request_id_preserved_when_supplied():
    custom_id = "test-custom-request-id-12345"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id
