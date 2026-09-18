import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"
    assert "environment" in data
    assert "timestamp" in data


def test_chat_endpoint_returns_501(client: TestClient) -> None:
    response = client.post("/api/v1/chat", json={"message": "What is the return policy?"})
    assert response.status_code == 501
    data = response.json()
    assert data["error"]["status_code"] == 501
    assert "not yet implemented" in data["error"]["message"].lower()


def test_chat_validation_error(client: TestClient) -> None:
    # Empty message should fail Pydantic validation (min_length=1)
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_documents_list_returns_501(client: TestClient) -> None:
    response = client.get("/api/v1/documents")
    assert response.status_code == 501
