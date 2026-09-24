"""
Modelos de dominio -- la verdad del negocio.

Aqui NO hay dependencias de infraestructura (ni FastAPI, ni DB).
Solo Pydantic para validacion estructural y tipado estricto.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

class DeploymentAction(StrEnum):
    """Tipo de operacion solicitada por el agente MCP."""

    CREATE = "CREATE"
    DELETE = "DELETE"


class DeploymentStatus(StrEnum):
    """Estados posibles del ciclo de vida de un despliegue."""

    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"
    DELETED = "DELETED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Entidades / Agregados
# ---------------------------------------------------------------------------

class DeploymentIntent(BaseModel):
    """
    Intencion de despliegue recibida desde el Agente MCP.

    Representa *que* quiere hacer el agente (crear o borrar),
    antes de cualquier validacion de seguridad o aprobacion humana.

    Para action=DELETE, imagen y puerto_interno son opcionales.
    """

    nombre: str = Field(
        ..., min_length=1, description="Nombre del servicio",
    )
    action: DeploymentAction = Field(
        default=DeploymentAction.CREATE,
        description="Tipo de operacion: CREATE o DELETE",
    )
    imagen: str | None = Field(
        default=None,
        description="Imagen de contenedor (requerida para CREATE)",
    )
    puerto_interno: int | None = Field(
        default=None, gt=0, le=65535,
        description="Puerto expuesto por el contenedor (requerido para CREATE)",
    )
    cpu: str = Field(
        default="250m",
        pattern=r"^\d+(m)?$",
        description="Request de CPU (notacion K8s, ej: 250m o 1)",
    )
    ram: str = Field(
        default="128Mi",
        pattern=r"^\d+(Mi|Gi|Ti)$",
        description="Request de memoria (ej: 128Mi o 1Gi)",
    )
    env_vars: dict[str, str] = Field(
        default_factory=dict,
        description="Diccionario de variables de entorno del contenedor",
    )

    @model_validator(mode="after")
    def _validate_create_fields(self) -> DeploymentIntent:
        """Si la accion es CREATE, imagen y puerto son obligatorios."""
        if self.action == DeploymentAction.CREATE:
            if not self.imagen:
                msg = "El campo 'imagen' es obligatorio para action=CREATE"
                raise ValueError(msg)
            if self.puerto_interno is None:
                msg = "El campo 'puerto_interno' es obligatorio para action=CREATE"
                raise ValueError(msg)
        return self


class DeploymentRecord(BaseModel):
    """
    Registro persistido en memoria que envuelve la intencion original
    junto con metadatos de trazabilidad (id, estado, url resultado).
    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    intent: DeploymentIntent
    status: DeploymentStatus = DeploymentStatus.PENDING_APPROVAL
    result_url: str | None = None
