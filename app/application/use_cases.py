"""
Main use case: process a deployment intent.

Orchestrates security validation and memory storage.
Does NOT know infrastructure (depends only on domain).
"""

from __future__ import annotations

from app.application.security_validator import SecurityContextValidator
from app.domain.models import DeploymentIntent, DeploymentRecord

# ---------------------------------------------------------------------------
# In-memory store (global state of the prototype)
# ---------------------------------------------------------------------------
# dict[id → DeploymentRecord]
deployment_store: dict[str, DeploymentRecord] = {}


class ProcessDeploymentUseCase:
    """
    Receives an intent from the MCP Agent, validates it against security
    policies, and persists it in memory with status PENDING_APPROVAL
    so that a human can approve it via HITL.
    """

    def __init__(self) -> None:
        self._validator = SecurityContextValidator()

    def execute(self, intent: DeploymentIntent) -> DeploymentRecord:
        """
        Processes the deployment intent.

        Args:
            intent: Intent received from the MCP agent.

        Returns:
            The created deployment record (status PENDING_APPROVAL).

        Raises:
            SecurityViolationError: If the intent violates security policies.
        """
        # 1. Validate security policies
        self._validator.validate(intent)

        # 2. Create record and persist in memory
        record = DeploymentRecord(intent=intent)
        deployment_store[record.id] = record

        return record
