"""
Suite de pruebas del Agente LLM y herramientas MCP.

Incluye:
  - Tests unitarios de calculate_optimal_resources (valores límite).
  - Tests de integración con Mock del LLM (simulación de tool calling).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from app.agent_layer.agent import AgentOrchestrator, AgentResponse, LLMClient, ToolCall
from app.agent_layer.mcp_server import (
    TOOL_REGISTRY as MCP_TOOL_REGISTRY,
)
from app.agent_layer.mcp_server import (
    _calculate_congress_resources,
    delete_university_service,
    deploy_congress_web,
    deploy_department_cms,
)
from app.agent_layer.tools import (
    TOOL_DEFINITIONS,
    TOOL_REGISTRY,
    calculate_optimal_resources,
)

# ===========================================================================
# TEST UNITARIO: calculate_optimal_resources
# ===========================================================================

class TestCalculateOptimalResources:
    """Verifica la función pura de cálculo de recursos en los límites."""

    @pytest.mark.parametrize(
        ("users", "expected_cpu", "expected_ram", "expected_tier"),
        [
            # Límite inferior: valores ≤ 0
            (-1, "100m", "64Mi", "mínimo"),
            (0, "100m", "64Mi", "mínimo"),
            # Tier básico: 1-100
            (1, "250m", "128Mi", "básico"),
            (100, "250m", "128Mi", "básico"),
            # Tier estándar: 101-1000
            (101, "500m", "256Mi", "estándar"),
            (1000, "500m", "256Mi", "estándar"),
            # Tier alto: 1001-10000
            (1001, "1", "512Mi", "alto"),
            (10000, "1", "512Mi", "alto"),
            # Tier enterprise: >10000
            (10001, "2", "1Gi", "enterprise"),
            (100000, "2", "1Gi", "enterprise"),
        ],
        ids=[
            "negativo", "cero",
            "minimo_basico", "maximo_basico",
            "minimo_estandar", "maximo_estandar",
            "minimo_alto", "maximo_alto",
            "minimo_enterprise", "gran_escala",
        ],
    )
    def test_boundary_values(
        self,
        users: int,
        expected_cpu: str,
        expected_ram: str,
        expected_tier: str,
    ) -> None:
        """Verifica que cada frontera devuelve el tier correcto."""
        result = calculate_optimal_resources(users)

        assert result["cpu"] == expected_cpu
        assert result["ram"] == expected_ram
        assert result["tier"] == expected_tier

    def test_return_type_is_dict_with_required_keys(self) -> None:
        """Verifica que siempre devuelve un dict con cpu, ram y tier."""
        result = calculate_optimal_resources(500)

        assert isinstance(result, dict)
        assert {"cpu", "ram", "tier"} <= set(result.keys())


# ===========================================================================
# TEST DE INTEGRACIÓN / MOCK: Simulación del flujo LLM → Tool Call
# ===========================================================================

class TestAgentOrchestrator:
    """
    Pruebas de integración que simulan una conversación completa.

    Se hace Mock del LLM para que devuelva directamente un Tool Call
    sin necesidad de API key. Valida que el orquestador:
      1. Captura la intención del LLM.
      2. Invoca la herramienta correcta.
      3. Devuelve al usuario el resultado formateado.
    """

    def _build_orchestrator(self, mock_llm: LLMClient) -> AgentOrchestrator:
        """Crea un orquestador con el mock LLM inyectado."""
        return AgentOrchestrator(
            llm=mock_llm,
            tool_registry=TOOL_REGISTRY,
            tool_definitions=TOOL_DEFINITIONS,
        )

    def test_llm_tool_call_triggers_deployment(self) -> None:
        """
        Simula que el LLM responde con un tool call a format_deployment_intent.
        Verifica que el backend recibe el JSON correcto y el usuario
        obtiene confirmación.
        """
        mock_llm = MagicMock(spec=LLMClient)

        # Respuesta 1: LLM decide desplegar (tool call)
        # Respuesta 2: LLM resume después del resultado de la herramienta
        mock_llm.chat.side_effect = [
            AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call_test_001",
                        name="format_deployment_intent",
                        arguments={
                            "nombre": "nginx-marketing",
                            "imagen": "nginx:1.25.3",
                            "puerto_interno": 8080,
                            "cpu": "250m",
                            "ram": "128Mi",
                        },
                    ),
                ],
            ),
            AgentResponse(
                content="✅ Solicitud enviada. ID: abc12345. Pendiente de aprobación.",
            ),
        ]

        # Mock de la petición HTTP al backend
        with patch("app.agent_layer.tools.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "id": "abc12345",
                "status": "PENDING_APPROVAL",
                "message": "Intención registrada.",
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            orchestrator = self._build_orchestrator(mock_llm)
            response, history = orchestrator.run(
                "Despliega nginx en el puerto 8080",
                [],
            )

        # ── Assertions ────────────────────────────────────────────────
        # 1. El backend recibió la petición
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        sent_json = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert sent_json["nombre"] == "nginx-marketing"
        assert sent_json["imagen"] == "nginx:1.25.3"
        assert sent_json["puerto_interno"] == 8080

        # 2. El usuario recibe confirmación
        assert "abc12345" in response

        # 3. El historial contiene el flujo completo
        roles = [m["role"] for m in history]
        assert roles == ["user", "assistant", "tool", "assistant"]

    def test_llm_resource_calculation_then_deploy(self) -> None:
        """
        Simula un flujo de 2 tool calls encadenados:
        1º calculate_optimal_resources → 2º format_deployment_intent.
        """
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.side_effect = [
            # Paso 1: LLM pide calcular recursos
            AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call_res",
                        name="calculate_optimal_resources",
                        arguments={"users": 500},
                    ),
                ],
            ),
            # Paso 2: Tras recibir recursos, LLM pide desplegar
            AgentResponse(
                content="Recursos calculados. Enviando solicitud…",
                tool_calls=[
                    ToolCall(
                        id="call_deploy",
                        name="format_deployment_intent",
                        arguments={
                            "nombre": "api-ventas",
                            "imagen": "python:3.12-slim",
                            "puerto_interno": 5000,
                            "cpu": "500m",
                            "ram": "256Mi",
                        },
                    ),
                ],
            ),
            # Paso 3: Resumen final
            AgentResponse(content="✅ Despliegue enviado a revisión."),
        ]

        with patch("app.agent_layer.tools.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "id": "xyz789",
                "status": "PENDING_APPROVAL",
                "message": "Intención registrada.",
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            orchestrator = self._build_orchestrator(mock_llm)
            _response, history = orchestrator.run(
                "Necesito desplegar api-ventas para 500 usuarios",
                [],
            )

        # calculate_optimal_resources se ejecutó (función pura, sin mock)
        tool_results = [
            m for m in history if m.get("role") == "tool"
        ]
        assert len(tool_results) == 2

        # Primer resultado: cálculo de recursos
        res_result = json.loads(tool_results[0]["content"])
        assert res_result["tier"] == "estándar"
        assert res_result["cpu"] == "500m"

        # Segundo resultado: despliegue
        deploy_result = json.loads(tool_results[1]["content"])
        assert deploy_result["id"] == "xyz789"

    def test_unknown_tool_returns_error(self) -> None:
        """Si el LLM invoca una herramienta inexistente, se maneja sin crash."""
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.side_effect = [
            AgentResponse(
                tool_calls=[
                    ToolCall(id="call_bad", name="herramienta_fantasma", arguments={}),
                ],
            ),
            AgentResponse(content="No pude ejecutar la herramienta."),
        ]

        orchestrator = self._build_orchestrator(mock_llm)
        _response, history = orchestrator.run("Haz algo raro", [])

        # El error queda registrado en el historial
        tool_msg = next(m for m in history if m.get("role") == "tool")
        result = json.loads(tool_msg["content"])
        assert "error" in result

    def test_tool_execution_exception_handled(self) -> None:
        """Si la herramienta lanza excepcion, se captura y se devuelve un dict con 'error'."""
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.return_value = AgentResponse(
            tool_calls=[ToolCall(id="1", name="failing_tool", arguments={})],
        )

        def _failing_tool():
            raise RuntimeError("Base de datos no disponible")

        orchestrator = AgentOrchestrator(
            llm=mock_llm,
            tool_registry={"failing_tool": _failing_tool},
            tool_definitions=[],
        )

        _response, history = orchestrator.run("Haz que falle", [])

        tool_msg = next(m for m in history if m.get("role") == "tool")
        result = json.loads(tool_msg["content"])
        assert "Base de datos no disponible" in result.get("error", "")

    def test_max_iterations_prevents_infinite_loop(self) -> None:
        """El orquestador se detiene tras max_iterations aunque el LLM siga pidiendo tools."""
        mock_llm = MagicMock(spec=LLMClient)
        # LLM siempre devuelve un tool call → bucle infinito potencial
        mock_llm.chat.return_value = AgentResponse(
            tool_calls=[
                ToolCall(
                    id="call_loop",
                    name="calculate_optimal_resources",
                    arguments={"users": 10},
                ),
            ],
        )

        orchestrator = self._build_orchestrator(mock_llm)
        response, history = orchestrator.run("loop", [], max_iterations=3)

        # Se detuvo y devolvió fallback
        assert "límite" in response.lower()
        # Exactamente 3 iteraciones de tool calls
        tool_msgs = [m for m in history if m.get("role") == "tool"]
        assert len(tool_msgs) == 3


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
        assert json.loads(result)["id"] == "abc123"

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
        assert json.loads(result)["id"] == "def456"

    def test_deploy_python_app_sends_correct_payload(self) -> None:
        from app.agent_layer.mcp_server import deploy_python_app
        with patch("app.agent_layer.mcp_server.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "id": "py789", "status": "PENDING_APPROVAL",
                "message": "OK",
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = deploy_python_app("api-test", "3.11")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["nombre"] == "api-test"
        assert sent["action"] == "CREATE"
        assert sent["imagen"] == "python:3.11-slim"
        assert sent["puerto_interno"] == 8000
        assert json.loads(result)["id"] == "py789"

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
        assert json.loads(result)["id"] == "ghi789"

    def test_tool_registry_has_all_tools(self) -> None:
        """El registry contiene las 3 herramientas del SIC."""
        assert "deploy_congress_web" in MCP_TOOL_REGISTRY
        assert "deploy_department_cms" in MCP_TOOL_REGISTRY
        assert "deploy_python_app" in MCP_TOOL_REGISTRY
        assert "delete_university_service" in MCP_TOOL_REGISTRY
