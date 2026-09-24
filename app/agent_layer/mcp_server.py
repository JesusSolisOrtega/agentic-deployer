"""
MCP Server -- University IT Service (SIC) tools.

Implemented with the official MCP v2 SDK (MCPServer).
Exposes tools via the Model Context Protocol (MCP)
that send POST requests to http://localhost:8000/mcp/intent.

Tools:
  - deploy_congress_web:       Static web for congress (nginx:alpine).
  - deploy_department_cms:     WordPress for department.
  - delete_university_service: Decommission an existing service.

Execution modes:
  - stdio (Claude Desktop):  python -m app.agent_layer.mcp_server
  - SSE (web):               python -m app.agent_layer.mcp_server --sse
  - Importable:              from app.agent_layer.mcp_server import mcp_server
"""

from __future__ import annotations

import json
import sys
import typing

import requests
from mcp.server.mcpserver import MCPServer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BACKEND_URL = "http://localhost:8000"

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp_server = MCPServer(
    name="agentic-deployer",
    instructions=(
        "MCP Server for the University IT Service (SIC). "
        "Provides tools to request deployments and decommissioning of services "
        "in the Kubernetes cluster. All requests are pending approval by an IT technician."
    ),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _calculate_congress_resources(expected_traffic: str) -> dict[str, str]:
    """Calculates CPU/RAM based on expected traffic for a congress."""
    traffic = expected_traffic.lower()
    if any(k in traffic for k in ["alto", "high", ">500", "1000"]):
        return {"cpu": "1", "ram": "512Mi"}
    if any(k in traffic for k in ["medio", "medium", "200", "300", "400", "500"]):
        return {"cpu": "500m", "ram": "256Mi"}
    return {"cpu": "250m", "ram": "128Mi"}


def _send_intent(payload: dict) -> dict:
    """Sends the intent to the backend and returns the response."""
    response = requests.post(
        f"{BACKEND_URL}/mcp/intent",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return dict(response.json())


# ---------------------------------------------------------------------------
# MCP Tools (registered with the official SDK)
# ---------------------------------------------------------------------------

@mcp_server.tool()
def deploy_congress_web(
    project_name: str,
    expected_traffic: str = "low",
) -> str:
    """Requests the deployment of a static web for an academic congress.

    IT enforces nginx:alpine image and port 8080.
    CPU and RAM are calculated based on expected traffic.

    Args:
        project_name: Name of the congress (e.g. 'ai-congress-2025').
        expected_traffic: Traffic level: 'low', 'medium', or 'high'.
    """
    resources = _calculate_congress_resources(expected_traffic)
    payload = {
        "name": project_name,
        "action": "CREATE",
        "image": "nginx:alpine",
        "internal_port": 8080,
        "cpu": resources["cpu"],
        "ram": resources["ram"],
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def deploy_department_cms(department_name: str) -> str:
    """Requests the deployment of a WordPress for a university department.

    IT enforces wordpress:6.4 image, port 8080, 500m CPU and 1024Mi RAM.

    Args:
        department_name: Name of the department (e.g. 'computer-science').
    """
    payload = {
        "name": f"cms-{department_name}",
        "action": "CREATE",
        "image": "wordpress:6.4",
        "internal_port": 8080,
        "cpu": "500m",
        "ram": "1024Mi",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def deploy_python_app(project_name: str, python_version: str = "3.12") -> str:
    """Requests the deployment of a generic Python application.

    Args:
        project_name: Name of the project (e.g. 'grades-api').
        python_version: Python version to use (e.g. '3.11', '3.12').
    """
    payload = {
        "name": project_name,
        "action": "CREATE",
        "image": f"python:{python_version}-slim",
        "internal_port": 8000,
        "cpu": "250m",
        "ram": "256Mi",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def delete_university_service(service_name: str) -> str:
    """Requests the decommissioning of an existing service in the cluster.

    Args:
        service_name: Name of the service to decommission.
    """
    payload = {
        "name": service_name,
        "action": "DELETE",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Registries compatible with AgentOrchestrator and existing tests
# ---------------------------------------------------------------------------
# The AgentOrchestrator uses TOOL_REGISTRY (name -> callable) and
# TOOL_DEFINITIONS (OpenAI format) for dispatch. We maintain both for
# compatibility, generating TOOL_DEFINITIONS from the schema that the
# MCP SDK automatically generates.

TOOL_REGISTRY: dict[str, typing.Callable[..., typing.Any]] = {
    "deploy_congress_web": lambda **kwargs: json.loads(deploy_congress_web(**kwargs)),
    "deploy_department_cms": lambda **kwargs: json.loads(deploy_department_cms(**kwargs)),
    "deploy_python_app": lambda **kwargs: json.loads(deploy_python_app(**kwargs)),
    "delete_university_service": lambda **kwargs: json.loads(delete_university_service(**kwargs)),
}

# Definitions in OpenAI Function Calling format (for AgentOrchestrator)
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "deploy_congress_web",
            "description": (
                "Requests the deployment of a static web for a congress "
                "or academic event. IT assigns image and resources."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the congress or event.",
                    },
                    "expected_traffic": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Expected traffic level.",
                    },
                },
                "required": ["project_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_department_cms",
            "description": (
                "Requests the deployment of a WordPress CMS for a university department."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "department_name": {
                        "type": "string",
                        "description": "Name of the department.",
                    },
                },
                "required": ["department_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_python_app",
            "description": (
                "Requests the deployment of a generic Python application."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project.",
                    },
                    "python_version": {
                        "type": "string",
                        "description": "Python version to use (e.g. 3.11, 3.12).",
                        "default": "3.12",
                    },
                },
                "required": ["project_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_university_service",
            "description": (
                "Requests the decommissioning of an existing service in the university cluster."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to decommission.",
                    },
                },
                "required": ["service_name"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Entry point: run the MCP server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    transport: typing.Literal["stdio", "sse", "streamable-http"] = "stdio"
    if "--sse" in sys.argv:
        transport = "sse"
    elif "--http" in sys.argv:
        transport = "streamable-http"

    print(f"Starting MCP server '{mcp_server.name}' with transport: {transport}")
    mcp_server.run(transport=transport)
