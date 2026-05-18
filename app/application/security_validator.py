"""
Validador de políticas de seguridad.

Lógica pura (sin I/O, sin estado) → ideal para Property-Based Testing.
"""

from __future__ import annotations

from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentIntent


class SecurityContextValidator:
    """
    Aplica políticas de seguridad sobre una intención de despliegue.

    Reglas actuales:
      1. El puerto interno debe ser >= 1024 (puertos privilegiados prohibidos).
      2. La imagen NO puede usar la etiqueta ':latest' (inmutabilidad de releases).
    """

    def validate(self, intent: DeploymentIntent) -> None:
        """
        Valida la intención contra todas las políticas.

        Args:
            intent: La intención de despliegue a validar.

        Raises:
            SecurityViolationError: Si una o más políticas se violan.
        """
        violations: list[str] = []

        if intent.puerto_interno < 1024:
            violations.append(
                f"Puerto privilegiado no permitido: {intent.puerto_interno} < 1024"
            )

        if ":latest" in intent.imagen:
            violations.append(
                f"Etiqueta ':latest' prohibida en imagen: {intent.imagen}"
            )

        if violations:
            raise SecurityViolationError(violations)
