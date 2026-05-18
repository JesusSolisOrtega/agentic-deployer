"""
Test E2E de la interfaz HITL usando Playwright.

Flujo:
  1. Crea un DeploymentIntent seguro vía POST /mcp/intent.
  2. Abre el panel HITL en un navegador headless.
  3. Espera a que la tabla cargue y hace clic en "Aprobar".
  4. Valida que el toast de éxito aparece en pantalla.

Requisitos:
  - El servidor FastAPI debe estar corriendo en http://localhost:8000
  - Ejecutar: pip install pytest-playwright && playwright install chromium
"""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------

SAFE_INTENT = {
    "nombre": "test-e2e-service",
    "imagen": "nginx:1.25.3",
    "puerto_interno": 8080,
    "cpu": "250m",
    "ram": "128Mi",
}

API_BASE = "http://localhost:8000"
FRONTEND_URL = f"{API_BASE}/frontend/index.html"


# ---------------------------------------------------------------------------
# Test E2E
# ---------------------------------------------------------------------------

@pytest.mark.e2e
class TestHITLPanel:
    """Tests end-to-end del panel Human-in-the-Loop."""

    def test_approve_deployment_shows_success_toast(self, page: Page) -> None:
        """
        Flujo completo: crear intención → abrir panel → aprobar → ver toast.
        """
        # ── 1. Crear un despliegue pendiente via la API ─────────────────
        response = page.request.post(
            f"{API_BASE}/mcp/intent",
            data=SAFE_INTENT,
        )
        assert response.ok, f"POST /mcp/intent falló: {response.status} — {response.text()}"
        intent_data = response.json()
        deployment_id = intent_data["id"]
        assert intent_data["status"] == "PENDING_APPROVAL"

        # ── 2. Abrir el panel HITL ──────────────────────────────────────
        page.goto(FRONTEND_URL)

        # ── 3. Esperar a que la tabla cargue con nuestro despliegue ─────
        #    Buscar la fila que contiene el ID del despliegue creado
        row = page.locator("tr", has_text=deployment_id)
        expect(row).to_be_visible(timeout=5000)

        # Verificar que el nombre del servicio aparece en la tabla
        expect(row.locator("td", has_text="test-e2e-service")).to_be_visible()

        # ── 4. Hacer clic en el botón "Aprobar" de esa fila ─────────────
        approve_btn = row.locator("button.btn--approve")
        expect(approve_btn).to_be_visible()
        approve_btn.click()

        # ── 5. Validar que el toast de éxito aparece ────────────────────
        toast = page.locator("#toast")
        expect(toast).to_have_class(re.compile(r"visible"), timeout=10000)

        # Verificar el texto del mensaje de éxito
        toast_message = page.locator("#toast-message")
        expect(toast_message).to_contain_text("Despliegue simulado con éxito")
