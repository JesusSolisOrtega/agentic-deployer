"""
Domain exceptions.

Semantic business errors that the application layer raises
and the infrastructure (API) translates to HTTP status codes.
"""


class SecurityViolationError(Exception):
    """Raised when a deployment intent violates security policies."""

    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__(f"Security violations: {', '.join(violations)}")
