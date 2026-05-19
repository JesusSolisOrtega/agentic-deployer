"""
Servidor MCP -- herramientas del SIC universitario.

Expone 3 herramientas via el protocolo MCP (Model Context Protocol)
que envian peticiones POST a http://localhost:8000/mcp/intent.

Herramientas:
  - deploy_congress_web:       Web estatica para congreso (nginx:alpine).
  - deploy_department_cms:     WordPress para departamento.
  - delete_university_service: Baja de un servicio existente.

Ejecutar con:
    python -m app.agent_layer.mcp_server
"""

from __future__ import annotations

import typing

import requests

BACKEND_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _calculate_congress_resources(trafico_esperado: str) -> dict[str, str]:
    """Calcula CPU/RAM segun trafico esperado para un congreso."""
    trafico = trafico_esperado.lower()
    if any(k in trafico for k in ["alto", "high", ">500", "1000"]):
        return {"cpu": "1", "ram": "512Mi"}
    if any(k in trafico for k in ["medio", "medium", "200", "300", "400", "500"]):
        return {"cpu": "500m", "ram": "256Mi"}
    return {"cpu": "250m", "ram": "128Mi"}


def _send_intent(payload: dict) -> dict:
    """Envia la intencion al backend y devuelve la respuesta."""
    response = requests.post(
        f"{BACKEND_URL}/mcp/intent",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return dict(response.json())


# ---------------------------------------------------------------------------
# Herramientas MCP
# ---------------------------------------------------------------------------

def deploy_congress_web(
    nombre_proyecto: str,
    trafico_esperado: str = "bajo",
) -> dict:
    """
    Solicita el despliegue de una web estatica para un congreso academico.

    El SIC fuerza imagen nginx:alpine y puerto 8080.
    CPU y RAM se calculan segun el trafico esperado.

    Args:
        nombre_proyecto: Nombre del congreso (ej: 'congreso-ia-2025').
        trafico_esperado: Nivel de trafico: 'bajo', 'medio' o 'alto'.

    Returns:
        Respuesta del backend con id, status y mensaje.
    """
    resources = _calculate_congress_resources(trafico_esperado)
    payload = {
        "nombre": nombre_proyecto,
        "action": "CREATE",
        "imagen": "nginx:alpine",
        "puerto_interno": 8080,
        "cpu": resources["cpu"],
        "ram": resources["ram"],
    }
    return _send_intent(payload)


def deploy_department_cms(nombre_departamento: str) -> dict:
    """
    Solicita el despliegue de un WordPress para un departamento universitario.

    El SIC fuerza imagen wordpress:6.4, puerto 8080, 500m CPU y 1024Mi RAM.

    Args:
        nombre_departamento: Nombre del departamento (ej: 'informatica').

    Returns:
        Respuesta del backend con id, status y mensaje.
    """
    payload = {
        "nombre": f"cms-{nombre_departamento}",
        "action": "CREATE",
        "imagen": "wordpress:6.4",
        "puerto_interno": 8080,
        "cpu": "500m",
        "ram": "1024Mi",
    }
    return _send_intent(payload)


def delete_university_service(nombre_servicio: str) -> dict:
    """
    Solicita la baja de un servicio existente en el cluster.

    Args:
        nombre_servicio: Nombre del servicio a dar de baja.

    Returns:
        Respuesta del backend con id, status y mensaje.
    """
    payload = {
        "nombre": nombre_servicio,
        "action": "DELETE",
    }
    return _send_intent(payload)


# ---------------------------------------------------------------------------
# Definiciones de herramientas (formato OpenAI Function Calling)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "deploy_congress_web",
            "description": (
                "Solicita el despliegue de una web estatica para un congreso "
                "o evento academico. El SIC asigna imagen y recursos."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_proyecto": {
                        "type": "string",
                        "description": "Nombre del congreso o evento.",
                    },
                    "trafico_esperado": {
                        "type": "string",
                        "enum": ["bajo", "medio", "alto"],
                        "description": "Nivel de trafico esperado.",
                    },
                },
                "required": ["nombre_proyecto"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_department_cms",
            "description": (
                "Solicita el despliegue de un CMS WordPress para un "
                "departamento universitario."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_departamento": {
                        "type": "string",
                        "description": "Nombre del departamento.",
                    },
                },
                "required": ["nombre_departamento"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_university_service",
            "description": (
                "Solicita la baja de un servicio existente en el cluster "
                "universitario."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_servicio": {
                        "type": "string",
                        "description": "Nombre del servicio a dar de baja.",
                    },
                },
                "required": ["nombre_servicio"],
            },
        },
    },
]

TOOL_REGISTRY: dict[str, typing.Callable[..., dict]] = {
    "deploy_congress_web": deploy_congress_web,
    "deploy_department_cms": deploy_department_cms,
    "delete_university_service": delete_university_service,
}
