from app.core.exceptions import AppError, NotFoundError
from app.main import app
from fastapi import APIRouter
from fastapi.testclient import TestClient

dummy_router = APIRouter()

@dummy_router.get("/test/custom-error")
def trigger_custom_error():
    raise NotFoundError("Specific item was not found")

@dummy_router.get("/test/app-error")
def trigger_app_error():
    raise AppError(code="OUTREACH_BLOCKED", message="Sending is disabled", status_code=400)

app.include_router(dummy_router)
client = TestClient(app)

def test_app_error_format():
    response = client.get("/test/app-error")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "OUTREACH_BLOCKED"
    assert data["error"]["message"] == "Sending is disabled"
    assert "request_id" in data["error"]
    assert data["error"]["request_id"] is not None

def test_not_found_error_format():
    response = client.get("/test/custom-error")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert data["error"]["message"] == "Specific item was not found"

def test_404_route_error_format():
    response = client.get("/non-existent-route-xyz")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
