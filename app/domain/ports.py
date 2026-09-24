"""
Domain ports (interfaces).

Define the contracts that the infrastructure must implement.
The domain NEVER imports concrete implementations; only these ABCs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models import DeploymentIntent


class DeployPort(ABC):
    """
    Outbound port to execute a deployment on the cluster.

    Any adapter (fake, real OKD, EKS...) must implement this contract.
    """

    @abstractmethod
    def deploy(self, intent: DeploymentIntent) -> str:
        """
        Executes the deployment of the given intent.

        Args:
            intent: The validated and approved deployment intent.

        Returns:
            URL of the deployed service.

        Raises:
            RuntimeError: If the deployment fails.
        """
        ...
