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
            "mínimo_básico", "máximo_básico",
            "mínimo_estándar", "máximo_estándar",
            "mínimo_alto", "máximo_alto",
            "mínimo_enterprise", "gran_escala",
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
