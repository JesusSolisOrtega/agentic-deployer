"""
Domain models -- the truth of the business.

There are NO infrastructure dependencies here (neither FastAPI, nor DB).
Only Pydantic for structural validation and strict typing.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

class DeploymentAction(StrEnum):
    """Type of operation requested by the MCP agent."""

    CREATE = "CREATE"
    DELETE = "DELETE"


class DeploymentStatus(StrEnum):
    """Possible states of a deployment's lifecycle."""

    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"
    DELETED = "DELETED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Entities / Aggregates
# ---------------------------------------------------------------------------

class DeploymentIntent(BaseModel):
    """
    Deployment intent received from the MCP Agent.

    Represents *what* the agent wants to do (create or delete),
    before any security validation or human approval.

    For action=DELETE, image and internal_port are optional.
    """

    name: str = Field(
        ..., min_length=1, description="Name of the service",
    )
    action: DeploymentAction = Field(
        default=DeploymentAction.CREATE,
        description="Type of operation: CREATE or DELETE",
    )
    image: str | None = Field(
        default=None,
        description="Container image (required for CREATE)",
    )
    internal_port: int | None = Field(
        default=None, gt=0, le=65535,
        description="Port exposed by the container (required for CREATE)",
    )
    cpu: str = Field(
        default="250m",
        pattern=r"^\d+(m)?$",
        description="CPU request (K8s notation, e.g.: 250m or 1)",
    )
    ram: str = Field(
        default="128Mi",
        pattern=r"^\d+(Mi|Gi|Ti)$",
        description="Memory request (e.g.: 128Mi or 1Gi)",
    )
    storage: str | None = Field(
        default=None,
        pattern=r"^\d+(Mi|Gi|Ti)$",
        description="Persistent storage request (e.g.: 10Gi)",
    )
    env_vars: dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of container environment variables",
    )

    @model_validator(mode="after")
    def _validate_create_fields(self) -> DeploymentIntent:
        """If the action is CREATE, image and internal_port are mandatory."""
        if self.action == DeploymentAction.CREATE:
            if not self.image:
                msg = "The 'image' field is mandatory for action=CREATE"
                raise ValueError(msg)
            if self.internal_port is None:
                msg = "The 'internal_port' field is mandatory for action=CREATE"
                raise ValueError(msg)
        return self


class DeploymentRecord(BaseModel):
    """
    Persisted record in memory that wraps the original intent
    along with traceability metadata (id, status, result url).
    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    intent: DeploymentIntent
    status: DeploymentStatus = DeploymentStatus.PENDING_APPROVAL
    result_url: str | None = None
