"""
Tests for the researcher-facing GET /hitl/status/{id} endpoint.

Verifies:
- Returns 404 for unknown deployment IDs.
- Returns correct status and message for each FSM state
  (PENDING_APPROVAL, DEPLOYED, REJECTED).
- Status message is human-readable (not raw enum value).
"""

from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.main import app, repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean_store() -> None:
    """Cleans the SQLite store before each test."""
    with sqlite3.connect(repository.db_path) as conn:
        conn.execute("DELETE FROM deployments")


def _create_pending(name: str = "test-service") -> str:
    """Helper: POST a valid intent and return the deployment ID."""
    response = client.post(
        "/mcp/intent",
        json={
            "name": name,
            "action": "CREATE",
            "image": "docker.io/library/nginx:1.25.3",
            "internal_port": 8080,
            "cpu": "250m",
            "ram": "128Mi",
        },
    )
    assert response.status_code == 201, response.text
    return str(response.json()["id"])


class TestStatusEndpoint:
    """Tests for GET /hitl/status/{deployment_id}."""

    def test_unknown_id_returns_404(self) -> None:
        """Unknown deployment ID should return HTTP 404."""
        response = client.get("/hitl/status/dep-nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_pending_approval_returns_correct_status(self) -> None:
        """A freshly created intent should be PENDING_APPROVAL."""
        dep_id = _create_pending()

        response = client.get(f"/hitl/status/{dep_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == dep_id
        assert data["status"] == "PENDING_APPROVAL"
        assert data["message"]  # non-empty human-readable message
        assert "queued" in data["message"].lower() or "awaiting" in data["message"].lower()

    def test_deployed_status_after_approval(self) -> None:
        """After approval, status endpoint should reflect DEPLOYED."""
        dep_id = _create_pending()

        # Approve via HITL endpoint
        approve_resp = client.post(f"/hitl/approve/{dep_id}")
        assert approve_resp.status_code == 200

        response = client.get(f"/hitl/status/{dep_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "DEPLOYED"
        assert "deployed" in data["message"].lower() or "success" in data["message"].lower()

    def test_rejected_status_after_rejection(self) -> None:
        """After rejection, status endpoint should reflect REJECTED."""
        dep_id = _create_pending()

        # Reject via HITL endpoint
        reject_resp = client.post(f"/hitl/reject/{dep_id}")
        assert reject_resp.status_code == 200

        response = client.get(f"/hitl/status/{dep_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "REJECTED"
        assert "rejected" in data["message"].lower()

    def test_response_includes_deployment_metadata(self) -> None:
        """Status response must include name, image and port fields."""
        dep_id = _create_pending(name="metadata-check")

        response = client.get(f"/hitl/status/{dep_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "metadata-check"
        assert "nginx" in data["image"]
        assert data["port"] == 8080

    def test_status_endpoint_does_not_mutate_state(self) -> None:
        """Calling GET /hitl/status must not change the FSM state."""
        dep_id = _create_pending()

        # Call status multiple times
        for _ in range(3):
            resp = client.get(f"/hitl/status/{dep_id}")
            assert resp.status_code == 200
            assert resp.json()["status"] == "PENDING_APPROVAL"
