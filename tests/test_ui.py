"""
E2E Test of the HITL interface using Playwright.

Flow:
  1. Creates a safe DeploymentIntent via POST /mcp/intent.
  2. Opens the HITL panel in a headless browser.
  3. Waits for the table to load and clicks "Approve".
  4. Validates that the success toast appears on screen.

Requirements:
  - The FastAPI server must be running at http://localhost:8000
  - Run: pip install pytest-playwright && playwright install chromium
"""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Test data
# ---------------------------------------------------------------------------

SAFE_INTENT = {
    "name": "test-e2e-service",
    "image": "docker.io/library/nginx:1.25.3",
    "internal_port": 8080,
    "cpu": "250m",
    "ram": "128Mi",
}

API_BASE = "http://localhost:8000"
FRONTEND_URL = f"{API_BASE}/frontend/index.html"


# ---------------------------------------------------------------------------
# E2E Test
# ---------------------------------------------------------------------------

@pytest.mark.e2e
class TestHITLPanel:
    """End-to-end tests for the Human-in-the-Loop panel."""

    def test_approve_deployment_shows_success_toast(self, page: Page) -> None:
        """
        Complete flow: create intent → open panel → approve → see toast.
        """
        # ── 1. Create a pending deployment via API ────────────────────────
        response = page.request.post(
            f"{API_BASE}/mcp/intent",
            data=SAFE_INTENT,
        )
        assert response.ok, f"POST /mcp/intent failed: {response.status} — {response.text()}"
        intent_data = response.json()
        deployment_id = intent_data["id"]
        assert intent_data["status"] == "PENDING_APPROVAL"

        # ── 2. Open the HITL panel ─────────────────────────────────────────
        page.goto(FRONTEND_URL)

        # ── 3. Wait for the table to load with our deployment ──────────────
        #    Search for the row containing the created deployment ID
        row = page.locator("tr", has_text=deployment_id)
        expect(row).to_be_visible(timeout=5000)

        # Verify that the service name appears in the table
        expect(row.locator("td", has_text="test-e2e-service")).to_be_visible()

        # ── 4. Click the "Aprobar" button in that row ───────────────────────
        approve_btn = row.locator("button.btn--approve")
        expect(approve_btn).to_be_visible()
        approve_btn.click()

        # ── 5. Validate that the success toast appears ───────────────────────
        toast = page.locator("#toast")
        expect(toast).to_have_class(re.compile(r"visible"), timeout=10000)

        # Verify the text of the success message (this is still in Spanish in the UI)
        toast_message = page.locator("#toast-message")
        expect(toast_message).to_contain_text("Despliegue simulado con éxito")
