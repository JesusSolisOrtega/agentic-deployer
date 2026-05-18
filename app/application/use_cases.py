"""
Caso de uso principal: procesar una intención de despliegue.

Orquesta la validación de seguridad y el almacenamiento en memoria.
NO conoce la infraestructura (solo depende del dominio).
"""

from __future__ import annotations

from app.application.security_validator import SecurityContextValidator
from app.domain.models import DeploymentIntent, DeploymentRecord

# ---------------------------------------------------------------------------
# Almacén en memoria (estado global del prototipo)
# ---------------------------------------------------------------------------
# dict[id → DeploymentRecord]
deployment_store: dict[str, DeploymentRecord] = {}


class ProcessDeploymentUseCase:
    """
    Recibe una intención del Agente MCP, la valida contra políticas
    de seguridad y la persiste en memoria con estado PENDING_APPROVAL
    para que un humano la apruebe vía HITL.
    """

    def __init__(self) -> None:
        self._validator = SecurityContextValidator()

    def execute(self, intent: DeploymentIntent) -> DeploymentRecord:
        """
        Procesa la intención de despliegue.

        Args:
            intent: Intención recibida del agente MCP.

        Returns:
            El registro de despliegue creado (estado PENDING_APPROVAL).

        Raises:
            SecurityViolationError: Si la intención viola políticas de seguridad.
        """
        # 1. Validar políticas de seguridad
        self._validator.validate(intent)

        # 2. Crear registro y persistir en memoria
        record = DeploymentRecord(intent=intent)
        deployment_store[record.id] = record

        return record
