"""Smoke test for the FastAPI health endpoint (no DB dependency)."""

from app.main import app
from fastapi.testclient import TestClient


def test_health_returns_ok() -> None:
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
