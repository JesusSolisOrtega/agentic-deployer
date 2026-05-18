"""
Puertos (interfaces) del dominio.

Definen los contratos que la infraestructura debe implementar.
El dominio NUNCA importa implementaciones concretas; solo estos ABCs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models import DeploymentIntent


class DeployPort(ABC):
    """
    Puerto de salida para ejecutar un despliegue en el clúster.

    Cualquier adaptador (fake, OKD real, EKS…) debe implementar este contrato.
    """

    @abstractmethod
    def deploy(self, intent: DeploymentIntent) -> str:
        """
        Ejecuta el despliegue de la intención dada.

        Args:
            intent: La intención de despliegue validada y aprobada.

        Returns:
            URL del servicio desplegado.

        Raises:
            RuntimeError: Si el despliegue falla.
        """
        ...
