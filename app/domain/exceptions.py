"""
Excepciones de dominio.

Errores semánticos del negocio que la capa de aplicación lanza
y la infraestructura (API) traduce a códigos HTTP.
"""


class SecurityViolationError(Exception):
    """Se lanza cuando una intención de despliegue viola políticas de seguridad."""

    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__(f"Violaciones de seguridad: {', '.join(violations)}")
