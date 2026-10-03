"""
MCP Tools Catalog — functions callable by the LLM Agent.

Each tool has:
  - The Python function that executes the logic.
  - Its definition in OpenAI Function Calling format (TOOL_DEFINITIONS).
  - A name->function registry for dynamic dispatch (TOOL_REGISTRY).
"""

from __future__ import annotations

import typing

import requests

BACKEND_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def calculate_optimal_resources(users: int) -> dict:
    """
    Calculates recommended CPU and RAM based on expected users.

    Tiers:
      <= 0      -> 100m / 64Mi   (minimum)
      1-100     -> 250m / 128Mi  (basic)
      101-1000  -> 500m / 256Mi  (standard)
      1001-10K  -> 1    / 512Mi  (high)
      >10K      -> 2    / 1Gi    (enterprise)
    """
    if users <= 0:
        return {"cpu": "100m", "ram": "64Mi", "tier": "mínimo"}
    if users <= 100:
        return {"cpu": "250m", "ram": "128Mi", "tier": "básico"}
    if users <= 1000:
        return {"cpu": "500m", "ram": "256Mi", "tier": "estándar"}
    if users <= 10000:
        return {"cpu": "1", "ram": "512Mi", "tier": "alto"}
    return {"cpu": "2", "ram": "1Gi", "tier": "enterprise"}


def format_deployment_intent(
    name: str,
    image: str,
    internal_port: int,
    cpu: str = "250m",
    ram: str = "128Mi",
    storage: str | None = None,
) -> dict:
    """
    Packages the data into a valid JSON and sends it to the backend
    via POST http://localhost:8000/mcp/intent.

    Returns:
        Backend response (id, status, message).

    Raises:
        requests.HTTPError: If the backend rejects the request.
    """
    payload: dict[str, str | int] = {
        "name": name,
        "image": image,
        "internal_port": internal_port,
        "cpu": cpu,
        "ram": ram,
    }
    if storage:
        payload["storage"] = storage
    response = requests.post(
        f"{BACKEND_URL}/mcp/intent", json=payload, timeout=10,
    )
    if response.status_code == 422:
        return dict(response.json())
    response.raise_for_status()
    return dict(response.json())


# ---------------------------------------------------------------------------
# Tool Definitions (OpenAI Function Calling format)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_optimal_resources",
            "description": (
                "Calculates optimal resources (CPU and RAM) for a deployment "
                "based on the expected number of users."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "integer",
                        "description": "Estimated number of concurrent users.",
                    },
                },
                "required": ["users"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "format_deployment_intent",
            "description": (
                "Creates and sends a deployment request to the orchestrator. "
                "Use when all necessary data is available."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the service to deploy.",
                    },
                    "image": {
                        "type": "string",
                        "description": "Container image (e.g. nginx:1.25.3).",
                    },
                    "internal_port": {
                        "type": "integer",
                        "description": "Port exposed by the container.",
                    },
                    "cpu": {
                        "type": "string",
                        "description": "CPU request in K8s notation (e.g. 250m).",
                    },
                    "ram": {
                        "type": "string",
                        "description": "Memory request (e.g. 128Mi).",
                    },
                    "storage": {
                        "type": "string",
                        "description": "Persistent storage request (e.g. 10Gi). Required for databases.",
                    },
                },
                "required": ["name", "image", "internal_port"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Tool Registry (dynamic dispatch name -> function)
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict[str, typing.Callable[..., dict]] = {
    "calculate_optimal_resources": calculate_optimal_resources,
    "format_deployment_intent": format_deployment_intent,
}
