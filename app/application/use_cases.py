"""
Main use case: process a deployment intent.

Orchestrates security validation and memory storage.
Does NOT know infrastructure (depends only on domain).
"""

from __future__ import annotations

from app.application.security_validator import SecurityContextValidator
from app.domain.models import DeploymentIntent, DeploymentRecord
from app.domain.ports import DeploymentRepositoryPort


class ProcessDeploymentUseCase:
    """
    Receives an intent from the MCP Agent, validates it against security
    policies, and persists it in memory with status PENDING_APPROVAL
    so that a human can approve it via HITL.
    """

    def __init__(self, repository: DeploymentRepositoryPort) -> None:
        self._validator = SecurityContextValidator()
        self._repository = repository

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

        # 2. Create record and persist via repository
        record = DeploymentRecord(intent=intent)
        self._repository.save(record)

        return record
