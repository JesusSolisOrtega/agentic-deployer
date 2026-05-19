"""
Catálogo de herramientas MCP — funciones invocables por el Agente LLM.

Cada herramienta tiene:
  - La función Python que ejecuta la lógica.
  - Su definición en formato OpenAI Function Calling (TOOL_DEFINITIONS).
  - Un registro name→function para dispatch dinámico (TOOL_REGISTRY).
"""

from __future__ import annotations

import typing

import requests

BACKEND_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Herramientas
# ---------------------------------------------------------------------------

def calculate_optimal_resources(users: int) -> dict:
    """
    Calcula CPU y RAM recomendados según el número de usuarios esperados.

    Tiers:
      <= 0      -> 100m / 64Mi   (mínimo)
      1-100     -> 250m / 128Mi  (básico)
      101-1000  -> 500m / 256Mi  (estándar)
      1001-10K  -> 1    / 512Mi  (alto)
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
    nombre: str,
    imagen: str,
    puerto_interno: int,
    cpu: str = "250m",
    ram: str = "128Mi",
) -> dict:
    """
    Empaqueta los datos en un JSON válido y los envía al backend
    vía POST http://localhost:8000/mcp/intent.

    Returns:
        Respuesta del backend (id, status, message).

    Raises:
        requests.HTTPError: Si el backend rechaza la solicitud.
    """
    payload: dict[str, str | int] = {
        "nombre": nombre,
        "imagen": imagen,
        "puerto_interno": puerto_interno,
        "cpu": cpu,
        "ram": ram,
    }
    response = requests.post(
        f"{BACKEND_URL}/mcp/intent", json=payload, timeout=10,
    )
    response.raise_for_status()
    return dict(response.json())


# ---------------------------------------------------------------------------
# Definiciones de herramientas (formato OpenAI Function Calling)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_optimal_resources",
            "description": (
                "Calcula los recursos óptimos (CPU y RAM) para un despliegue "
                "según el número de usuarios esperados."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "integer",
                        "description": "Número estimado de usuarios concurrentes.",
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
                "Crea y envía una solicitud de despliegue al orquestador. "
                "Usar cuando se tienen todos los datos necesarios."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del servicio a desplegar.",
                    },
                    "imagen": {
                        "type": "string",
                        "description": "Imagen de contenedor (ej: nginx:1.25.3).",
                    },
                    "puerto_interno": {
                        "type": "integer",
                        "description": "Puerto expuesto por el contenedor.",
                    },
                    "cpu": {
                        "type": "string",
                        "description": "Request de CPU en notación K8s (ej: 250m).",
                    },
                    "ram": {
                        "type": "string",
                        "description": "Request de memoria (ej: 128Mi).",
                    },
                },
                "required": ["nombre", "imagen", "puerto_interno"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Registro de herramientas (dispatch dinámico name → function)
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict[str, typing.Callable[..., dict]] = {
    "calculate_optimal_resources": calculate_optimal_resources,
    "format_deployment_intent": format_deployment_intent,
}
