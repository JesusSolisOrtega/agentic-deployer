"""
Validador de politicas de seguridad.

Logica pura (sin I/O, sin estado) -> ideal para Property-Based Testing.
"""

from __future__ import annotations

from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentAction, DeploymentIntent


class SecurityContextValidator:
    """
    Aplica politicas de seguridad sobre una intencion de despliegue.

    Reglas actuales (solo aplican a action=CREATE):
      1. El puerto interno debe ser >= 1024 (puertos privilegiados prohibidos).
      2. La imagen NO puede usar la etiqueta ':latest' (inmutabilidad de releases).

    Las acciones DELETE no requieren validacion de imagen/puerto.
    """

    def validate(self, intent: DeploymentIntent) -> None:
        """
        Valida la intencion contra todas las politicas.

        Args:
            intent: La intencion de despliegue a validar.

        Raises:
            SecurityViolationError: Si una o mas politicas se violan.
        """
        # DELETE no requiere validacion de imagen/puerto
        if intent.action == DeploymentAction.DELETE:
            return

        violations: list[str] = []

        if intent.puerto_interno is not None and intent.puerto_interno < 1024:
            violations.append(
                f"Puerto privilegiado no permitido: {intent.puerto_interno} < 1024"
            )

        if intent.imagen and ":latest" in intent.imagen:
            violations.append(
                f"Etiqueta ':latest' prohibida en imagen: {intent.imagen}"
            )

        if violations:
            raise SecurityViolationError(violations)
