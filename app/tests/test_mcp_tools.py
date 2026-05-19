"""
Tests para las herramientas del servidor MCP del SIC.

Valida:
  - Calculo de recursos para congresos (limites de trafico).
  - Formato correcto del JSON enviado al backend.
  - Acciones CREATE/DELETE correctas.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.agent_layer.mcp_server import (
    TOOL_REGISTRY,
    _calculate_congress_resources,
    delete_university_service,
    deploy_congress_web,
    deploy_department_cms,
)

# ===========================================================================
# TEST UNITARIO: _calculate_congress_resources
# ===========================================================================

class TestCalculateCongressResources:
    """Verifica el calculo de recursos segun trafico."""

    @pytest.mark.parametrize(
        ("trafico", "expected_cpu", "expected_ram"),
        [
            ("bajo", "250m", "128Mi"),
            ("medio", "500m", "256Mi"),
            ("alto", "1", "512Mi"),
            ("high", "1", "512Mi"),
            ("unknown", "250m", "128Mi"),
            (">500 usuarios", "1", "512Mi"),
        ],
        ids=["bajo", "medio", "alto", "high_en", "desconocido", "numerico"],
    )
    def test_traffic_tiers(
        self, trafico: str, expected_cpu: str, expected_ram: str,
    ) -> None:
        result = _calculate_congress_resources(trafico)
        assert result["cpu"] == expected_cpu
        assert result["ram"] == expected_ram


# ===========================================================================
# TESTS DE INTEGRACION: MCP Tools con Mock HTTP
# ===========================================================================

class TestMCPTools:
    """Verifica que cada tool envia el JSON correcto al backend."""

    def test_deploy_congress_web_sends_correct_payload(self) -> None:
        with patch("app.agent_layer.mcp_server.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "id": "abc123", "status": "PENDING_APPROVAL",
                "message": "OK",
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = deploy_congress_web("congreso-ia-2025", "alto")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["nombre"] == "congreso-ia-2025"
        assert sent["action"] == "CREATE"
        assert sent["imagen"] == "nginx:alpine"
        assert sent["puerto_interno"] == 8080
        assert sent["cpu"] == "1"
        assert result["id"] == "abc123"

    def test_deploy_department_cms_sends_correct_payload(self) -> None:
        with patch("app.agent_layer.mcp_server.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "id": "def456", "status": "PENDING_APPROVAL",
                "message": "OK",
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = deploy_department_cms("informatica")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["nombre"] == "cms-informatica"
        assert sent["action"] == "CREATE"
        assert sent["imagen"] == "wordpress:6.4"
        assert sent["cpu"] == "500m"
        assert sent["ram"] == "1024Mi"
        assert result["id"] == "def456"

    def test_delete_university_service_sends_delete_action(self) -> None:
        with patch("app.agent_layer.mcp_server.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "id": "ghi789", "status": "PENDING_APPROVAL",
                "message": "OK",
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = delete_university_service("servicio-viejo")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["nombre"] == "servicio-viejo"
        assert sent["action"] == "DELETE"
        assert "imagen" not in sent
        assert result["id"] == "ghi789"

    def test_tool_registry_has_all_tools(self) -> None:
        """El registry contiene las 3 herramientas del SIC."""
        assert "deploy_congress_web" in TOOL_REGISTRY
        assert "deploy_department_cms" in TOOL_REGISTRY
        assert "delete_university_service" in TOOL_REGISTRY
