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
      2. La imagen NO puede usar la etiqueta ':latest' (inmutabilidad).
      3. La imagen debe provenir de un registro confiable (Whitelist).
      4. Las cuotas de Hardware no pueden exceder 4 Cores o 8 GiB.
      5. Las variables de entorno no pueden contener secretos en texto plano.
    """

    ALLOWED_REGISTRIES = ("docker.io/", "quay.io/", "harbor.universidad.edu/")
    MAX_CPU_MILLICORES = 4000  # 4 Cores
    MAX_RAM_MI = 8192          # 8 GiB
    FORBIDDEN_ENV_KEYS = ("password", "secret", "token", "key", "credential")

    def _parse_cpu(self, cpu_str: str) -> int:
        if cpu_str.endswith("m"):
            return int(cpu_str[:-1])
        return int(cpu_str) * 1000

    def _parse_ram(self, ram_str: str) -> int:
        if ram_str.endswith("Mi"):
            return int(ram_str[:-2])
        if ram_str.endswith("Gi"):
            return int(ram_str[:-2]) * 1024
        if ram_str.endswith("Ti"):
            return int(ram_str[:-2]) * 1024 * 1024
        return 0

    def validate(self, intent: DeploymentIntent) -> None:
        """
        Valida la intencion contra todas las politicas.
        """
        if intent.action == DeploymentAction.DELETE:
            return

        violations: list[str] = []

        if intent.puerto_interno is not None and intent.puerto_interno < 1024:
            violations.append(f"Puerto privilegiado no permitido: {intent.puerto_interno} < 1024")

        if intent.imagen:
            if ":latest" in intent.imagen:
                violations.append(f"Etiqueta ':latest' prohibida en imagen: {intent.imagen}")

            if not any(intent.imagen.startswith(reg) for reg in self.ALLOWED_REGISTRIES):
                violations.append(f"Registro no confiable. Imagen debe empezar por {self.ALLOWED_REGISTRIES}")

        try:
            cpu_m = self._parse_cpu(intent.cpu)
            if cpu_m > self.MAX_CPU_MILLICORES:
                violations.append(f"Cuota CPU excedida: {intent.cpu} > {self.MAX_CPU_MILLICORES}m")
        except ValueError:
            pass

        try:
            ram_mi = self._parse_ram(intent.ram)
            if ram_mi > self.MAX_RAM_MI:
                violations.append(f"Cuota RAM excedida: {intent.ram} > {self.MAX_RAM_MI}Mi")
        except ValueError:
            pass

        for key in intent.env_vars:
            if any(forbidden in key.lower() for forbidden in self.FORBIDDEN_ENV_KEYS):
                violations.append(f"Posible secreto en texto plano en variable: {key}")

        if violations:
            raise SecurityViolationError(violations)
