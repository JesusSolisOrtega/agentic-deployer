"""
Security policy validator.

Pure logic (no I/O, no state) -> ideal for Property-Based Testing.
"""

from __future__ import annotations

from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentAction, DeploymentIntent


class SecurityContextValidator:
    """
    Applies security policies to a deployment intent.

    Current rules (only apply to action=CREATE):
      1. Internal port must be >= 1024 (privileged ports prohibited).
      2. The image CANNOT use the ':latest' tag (immutability).
      3. The image must come from a trusted registry (Whitelist).
      4. Hardware quotas cannot exceed 4 Cores or 8 GiB.
      5. Environment variables cannot contain plaintext secrets.
      6. Databases must have explicit storage defined.
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
        Validates the intent against all policies.
        """
        if intent.action == DeploymentAction.DELETE:
            return

        violations: list[str] = []

        if intent.internal_port is not None and intent.internal_port < 1024:
            violations.append(f"Privileged port not allowed: {intent.internal_port} < 1024")

        if intent.image:
            if ":latest" in intent.image:
                violations.append(f"':latest' tag prohibited in image: {intent.image}")

            if not any(intent.image.startswith(reg) for reg in self.ALLOWED_REGISTRIES):
                violations.append(f"Untrusted registry. Image must start with {self.ALLOWED_REGISTRIES}")

            if any(db in intent.image.lower() for db in ["postgres", "mysql", "redis", "mongo"]) and not getattr(intent, "storage", None):
                violations.append("Databases require explicit storage (e.g. storage='10Gi')")

        cpu_m = self._parse_cpu(intent.cpu)
        if cpu_m > self.MAX_CPU_MILLICORES:
            violations.append(f"CPU quota exceeded: {intent.cpu} > {self.MAX_CPU_MILLICORES}m")

        ram_mi = self._parse_ram(intent.ram)
        if ram_mi > self.MAX_RAM_MI:
            violations.append(f"RAM quota exceeded: {intent.ram} > {self.MAX_RAM_MI}Mi")

        for key in intent.env_vars:
            if any(forbidden in key.lower() for forbidden in self.FORBIDDEN_ENV_KEYS):
                violations.append(f"Potential plaintext secret in variable: {key}")

        if violations:
            raise SecurityViolationError(violations)
