"""
LLM Agent and MCP tools test suite.

Includes:
  - Unit tests for calculate_optimal_resources (boundary values).
  - Integration tests with LLM Mock (tool calling simulation).
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
# UNIT TEST: calculate_optimal_resources
# ===========================================================================

class TestCalculateOptimalResources:
    """Verifies the pure function for resource calculation at boundaries."""

    @pytest.mark.parametrize(
        ("users", "expected_cpu", "expected_ram", "expected_tier"),
        [
            # Lower bound: values ≤ 0
            (-1, "100m", "64Mi", "mínimo"),
            (0, "100m", "64Mi", "mínimo"),
            # Basic tier: 1-100
            (1, "250m", "128Mi", "básico"),
            (100, "250m", "128Mi", "básico"),
            # Standard tier: 101-1000
            (101, "500m", "256Mi", "estándar"),
            (1000, "500m", "256Mi", "estándar"),
            # High tier: 1001-10000
            (1001, "1", "512Mi", "alto"),
            (10000, "1", "512Mi", "alto"),
            # Enterprise tier: >10000
            (10001, "2", "1Gi", "enterprise"),
            (100000, "2", "1Gi", "enterprise"),
        ],
        ids=[
            "negative", "zero",
            "min_basic", "max_basic",
            "min_standard", "max_standard",
            "min_high", "max_high",
            "min_enterprise", "large_scale",
        ],
    )
    def test_boundary_values(
        self,
        users: int,
        expected_cpu: str,
        expected_ram: str,
        expected_tier: str,
    ) -> None:
        """Verifies that each boundary returns the correct tier."""
        result = calculate_optimal_resources(users)

        assert result["cpu"] == expected_cpu
        assert result["ram"] == expected_ram
        assert result["tier"] == expected_tier

    def test_return_type_is_dict_with_required_keys(self) -> None:
        """Verifies that it always returns a dict with cpu, ram and tier."""
        result = calculate_optimal_resources(500)

        assert isinstance(result, dict)
        assert {"cpu", "ram", "tier"} <= set(result.keys())


# ===========================================================================
# INTEGRATION / MOCK TEST: LLM Flow Simulation → Tool Call
# ===========================================================================

class TestAgentOrchestrator:
    """
    Integration tests simulating a complete conversation.

    Mocks the LLM so it returns a Tool Call directly
    without needing an API key. Validates that the orchestrator:
      1. Captures the LLM intent.
      2. Invokes the correct tool.
      3. Returns the formatted result to the user.
    """

    def _build_orchestrator(self, mock_llm: LLMClient) -> AgentOrchestrator:
        """Creates an orchestrator with the injected mock LLM."""
        return AgentOrchestrator(
            llm=mock_llm,
            tool_registry=TOOL_REGISTRY,
            tool_definitions=TOOL_DEFINITIONS,
        )

    def test_llm_tool_call_triggers_deployment(self) -> None:
        """
        Simulates the LLM responding with a tool call to format_deployment_intent.
        Verifies that the backend receives the correct JSON and the user
        gets confirmation.
        """
        mock_llm = MagicMock(spec=LLMClient)

        # Response 1: LLM decides to deploy (tool call)
        # Response 2: LLM summarizes after tool result
        mock_llm.chat.side_effect = [
            AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call_test_001",
                        name="format_deployment_intent",
                        arguments={
                            "name": "nginx-marketing",
                            "image": "nginx:1.25.3",
                            "internal_port": 8080,
                            "cpu": "250m",
                            "ram": "128Mi",
                        },
                    ),
                ],
            ),
            AgentResponse(
                content="✅ Request sent. ID: abc12345. Pending approval.",
            ),
        ]

        # Mock the HTTP request to the backend
        with patch("app.agent_layer.tools.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "id": "abc12345",
                "status": "PENDING_APPROVAL",
                "message": "Intent registered.",
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            orchestrator = self._build_orchestrator(mock_llm)
            response, history = orchestrator.run(
                "Deploy nginx on port 8080",
                [],
            )

        # ── Assertions ────────────────────────────────────────────────
        # 1. The backend received the request
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        sent_json = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert sent_json["name"] == "nginx-marketing"
        assert sent_json["image"] == "nginx:1.25.3"
        assert sent_json["internal_port"] == 8080

        # 2. The user receives confirmation
        assert "abc12345" in response

        # 3. The history contains the full flow
        roles = [m["role"] for m in history]
        assert roles == ["user", "assistant", "tool", "assistant"]

    def test_llm_resource_calculation_then_deploy(self) -> None:
        """
        Simulates a flow of 2 chained tool calls:
        1st calculate_optimal_resources → 2nd format_deployment_intent.
        """
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.side_effect = [
            # Step 1: LLM asks to calculate resources
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
            # Step 2: After receiving resources, LLM asks to deploy
            AgentResponse(
                content="Resources calculated. Sending request...",
                tool_calls=[
                    ToolCall(
                        id="call_deploy",
                        name="format_deployment_intent",
                        arguments={
                            "name": "sales-api",
                            "image": "python:3.12-slim",
                            "internal_port": 5000,
                            "cpu": "500m",
                            "ram": "256Mi",
                        },
                    ),
                ],
            ),
            # Step 3: Final summary
            AgentResponse(content="✅ Deployment sent for review."),
        ]

        with patch("app.agent_layer.tools.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "id": "xyz789",
                "status": "PENDING_APPROVAL",
                "message": "Intent registered.",
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            orchestrator = self._build_orchestrator(mock_llm)
            _response, history = orchestrator.run(
                "I need to deploy sales-api for 500 users",
                [],
            )

        # calculate_optimal_resources was executed (pure function, no mock)
        tool_results = [
            m for m in history if m.get("role") == "tool"
        ]
        assert len(tool_results) == 2

        # First result: resource calculation
        res_result = json.loads(tool_results[0]["content"])
        assert res_result["tier"] == "estándar"
        assert res_result["cpu"] == "500m"

        # Second result: deployment
        deploy_result = json.loads(tool_results[1]["content"])
        assert deploy_result["id"] == "xyz789"

    def test_unknown_tool_returns_error(self) -> None:
        """If the LLM invokes a non-existent tool, it handles without crash."""
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.side_effect = [
            AgentResponse(
                tool_calls=[
                    ToolCall(id="call_bad", name="ghost_tool", arguments={}),
                ],
            ),
            AgentResponse(content="Could not execute the tool."),
        ]

        orchestrator = self._build_orchestrator(mock_llm)
        _response, history = orchestrator.run("Do something weird", [])

        # The error is logged in the history
        tool_msg = next(m for m in history if m.get("role") == "tool")
        result = json.loads(tool_msg["content"])
        assert "error" in result

    def test_tool_execution_exception_handled(self) -> None:
        """If the tool raises an exception, it is caught and returns a dict with 'error'."""
        mock_llm = MagicMock(spec=LLMClient)
        mock_llm.chat.return_value = AgentResponse(
            tool_calls=[ToolCall(id="1", name="failing_tool", arguments={})],
        )

        def _failing_tool():
            raise RuntimeError("Database not available")

        orchestrator = AgentOrchestrator(
            llm=mock_llm,
            tool_registry={"failing_tool": _failing_tool},
            tool_definitions=[],
        )

        _response, history = orchestrator.run("Make it fail", [])

        tool_msg = next(m for m in history if m.get("role") == "tool")
        result = json.loads(tool_msg["content"])
        assert "Database not available" in result.get("error", "")

    def test_max_iterations_prevents_infinite_loop(self) -> None:
        """The orchestrator stops after max_iterations even if LLM keeps asking for tools."""
        mock_llm = MagicMock(spec=LLMClient)
        # LLM always returns a tool call → potential infinite loop
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

        # Stopped and returned fallback
        assert "limit" in response.lower()
        # Exactly 3 iterations of tool calls
        tool_msgs = [m for m in history if m.get("role") == "tool"]
        assert len(tool_msgs) == 3


# ===========================================================================
# UNIT TEST: _calculate_congress_resources
# ===========================================================================

class TestCalculateCongressResources:
    """Verifies the resource calculation based on traffic."""

    @pytest.mark.parametrize(
        ("traffic", "expected_cpu", "expected_ram"),
        [
            ("bajo", "250m", "128Mi"),
            ("medio", "500m", "256Mi"),
            ("alto", "1", "512Mi"),
            ("high", "1", "512Mi"),
            ("unknown", "250m", "128Mi"),
            (">500 usuarios", "1", "512Mi"),
        ],
        ids=["low", "medium", "high", "high_en", "unknown", "numeric"],
    )
    def test_traffic_tiers(
        self, traffic: str, expected_cpu: str, expected_ram: str,
    ) -> None:
        result = _calculate_congress_resources(traffic)
        assert result["cpu"] == expected_cpu
        assert result["ram"] == expected_ram


# ===========================================================================
# INTEGRATION TESTS: MCP Tools with HTTP Mock
# ===========================================================================

class TestMCPTools:
    """Verifies that each tool sends the correct JSON to the backend."""

    def test_deploy_congress_web_sends_correct_payload(self) -> None:
        with patch("app.agent_layer.mcp_server.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "id": "abc123", "status": "PENDING_APPROVAL",
                "message": "OK",
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = deploy_congress_web("ai-congress-2025", "alto")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["name"] == "ai-congress-2025"
        assert sent["action"] == "CREATE"
        assert sent["image"] == "nginx:alpine"
        assert sent["internal_port"] == 8080
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

            result = deploy_department_cms("computer-science")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["name"] == "cms-computer-science"
        assert sent["action"] == "CREATE"
        assert sent["image"] == "wordpress:6.4"
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
        assert sent["name"] == "api-test"
        assert sent["action"] == "CREATE"
        assert sent["image"] == "python:3.11-slim"
        assert sent["internal_port"] == 8000
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

            result = delete_university_service("old-service")

        sent = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert sent["name"] == "old-service"
        assert sent["action"] == "DELETE"
        assert "image" not in sent
        assert json.loads(result)["id"] == "ghi789"

    def test_tool_registry_has_all_tools(self) -> None:
        """The registry contains the 4 SIC tools."""
        assert "deploy_congress_web" in MCP_TOOL_REGISTRY
        assert "deploy_department_cms" in MCP_TOOL_REGISTRY
        assert "deploy_python_app" in MCP_TOOL_REGISTRY
        assert "delete_university_service" in MCP_TOOL_REGISTRY
