"""
Servidor MCP -- herramientas del SIC universitario.

Implementado con el SDK oficial de MCP v2 (MCPServer).
Expone herramientas via el protocolo Model Context Protocol (MCP)
que envian peticiones POST a http://localhost:8000/mcp/intent.

Herramientas:
  - deploy_congress_web:       Web estatica para congreso (nginx:alpine).
  - deploy_department_cms:     WordPress para departamento.
  - delete_university_service: Baja de un servicio existente.

Modos de ejecucion:
  - stdio (Claude Desktop):  python -m app.agent_layer.mcp_server
  - SSE (web):               python -m app.agent_layer.mcp_server --sse
  - Importable:               from app.agent_layer.mcp_server import mcp_server
"""

from __future__ import annotations

import json
import sys
import typing

import requests
from mcp.server.mcpserver import MCPServer

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

BACKEND_URL = "http://localhost:8000"

# ---------------------------------------------------------------------------
# Servidor MCP
# ---------------------------------------------------------------------------

mcp_server = MCPServer(
    name="agentic-deployer",
    instructions=(
        "Servidor MCP del SIC (Servicio de Informatica y Comunicaciones) "
        "de la Universidad. Proporciona herramientas para solicitar despliegues "
        "y bajas de servicios en el cluster Kubernetes. Todas las solicitudes "
        "quedan pendientes de aprobacion por un tecnico del SIC."
    ),
)


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
# Herramientas MCP (registradas con el SDK oficial)
# ---------------------------------------------------------------------------

@mcp_server.tool()
def deploy_congress_web(
    nombre_proyecto: str,
    trafico_esperado: str = "bajo",
) -> str:
    """Solicita el despliegue de una web estatica para un congreso academico.

    El SIC fuerza imagen nginx:alpine y puerto 8080.
    CPU y RAM se calculan segun el trafico esperado.

    Args:
        nombre_proyecto: Nombre del congreso (ej: 'congreso-ia-2025').
        trafico_esperado: Nivel de trafico: 'bajo', 'medio' o 'alto'.
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
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def deploy_department_cms(nombre_departamento: str) -> str:
    """Solicita el despliegue de un WordPress para un departamento universitario.

    El SIC fuerza imagen wordpress:6.4, puerto 8080, 500m CPU y 1024Mi RAM.

    Args:
        nombre_departamento: Nombre del departamento (ej: 'informatica').
    """
    payload = {
        "nombre": f"cms-{nombre_departamento}",
        "action": "CREATE",
        "imagen": "wordpress:6.4",
        "puerto_interno": 8080,
        "cpu": "500m",
        "ram": "1024Mi",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def deploy_python_app(nombre_proyecto: str, version_python: str = "3.12") -> str:
    """Solicita el despliegue de una aplicacion Python generica.

    Args:
        nombre_proyecto: Nombre del proyecto (ej: 'api-notas').
        version_python: Version de Python a utilizar (ej: '3.11', '3.12').
    """
    payload = {
        "nombre": nombre_proyecto,
        "action": "CREATE",
        "imagen": f"python:{version_python}-slim",
        "puerto_interno": 8000,
        "cpu": "250m",
        "ram": "256Mi",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


@mcp_server.tool()
def delete_university_service(nombre_servicio: str) -> str:
    """Solicita la baja de un servicio existente en el cluster.

    Args:
        nombre_servicio: Nombre del servicio a dar de baja.
    """
    payload = {
        "nombre": nombre_servicio,
        "action": "DELETE",
    }
    result = _send_intent(payload)
    return json.dumps(result, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Registros compatibles con AgentOrchestrator y tests existentes
# ---------------------------------------------------------------------------
# El AgentOrchestrator usa TOOL_REGISTRY (name -> callable) y
# TOOL_DEFINITIONS (formato OpenAI) para el dispatch. Mantenemos
# ambos para compatibilidad, generando TOOL_DEFINITIONS a partir
# del schema que el SDK de MCP ya genera automaticamente.

TOOL_REGISTRY: dict[str, typing.Callable[..., typing.Any]] = {
    "deploy_congress_web": lambda **kwargs: json.loads(deploy_congress_web(**kwargs)),
    "deploy_department_cms": lambda **kwargs: json.loads(deploy_department_cms(**kwargs)),
    "deploy_python_app": lambda **kwargs: json.loads(deploy_python_app(**kwargs)),
    "delete_university_service": lambda **kwargs: json.loads(delete_university_service(**kwargs)),
}

# Definiciones en formato OpenAI Function Calling (para el AgentOrchestrator)
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
            "name": "deploy_python_app",
            "description": (
                "Solicita el despliegue de una aplicacion Python generica."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_proyecto": {
                        "type": "string",
                        "description": "Nombre del proyecto.",
                    },
                    "version_python": {
                        "type": "string",
                        "description": "Version de Python a utilizar (ej: 3.11, 3.12).",
                        "default": "3.12",
                    },
                },
                "required": ["nombre_proyecto"],
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


# ---------------------------------------------------------------------------
# Punto de entrada: ejecutar el servidor MCP
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    transport: typing.Literal["stdio", "sse", "streamable-http"] = "stdio"
    if "--sse" in sys.argv:
        transport = "sse"
    elif "--http" in sys.argv:
        transport = "streamable-http"

    print(f"Iniciando servidor MCP '{mcp_server.name}' con transporte: {transport}")
    mcp_server.run(transport=transport)
