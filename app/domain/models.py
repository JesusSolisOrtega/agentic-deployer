"""
Modelos de dominio — la verdad del negocio.

Aquí NO hay dependencias de infraestructura (ni FastAPI, ni DB).
Solo Pydantic para validación estructural y tipado estricto.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

class DeploymentStatus(StrEnum):
    """Estados posibles del ciclo de vida de un despliegue."""
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Entidades / Agregados
# ---------------------------------------------------------------------------

class DeploymentIntent(BaseModel):
    """
    Intención de despliegue recibida desde el Agente MCP.

    Representa *qué* quiere desplegar el agente, antes de cualquier
    validación de seguridad o aprobación humana.
    """
    nombre: str = Field(..., min_length=1, description="Nombre del servicio a desplegar")
    imagen: str = Field(..., min_length=1, description="Imagen de contenedor (ej: nginx:1.25)")
    puerto_interno: int = Field(..., gt=0, le=65535, description="Puerto expuesto por el contenedor")
    cpu: str = Field(default="250m", description="Request de CPU (notación K8s, ej: 250m)")
    ram: str = Field(default="128Mi", description="Request de memoria (ej: 128Mi)")


class DeploymentRecord(BaseModel):
    """
    Registro persistido en memoria que envuelve la intención original
    junto con metadatos de trazabilidad (id, estado, url resultado).
    """
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    intent: DeploymentIntent
    status: DeploymentStatus = DeploymentStatus.PENDING_APPROVAL
    result_url: str | None = None
