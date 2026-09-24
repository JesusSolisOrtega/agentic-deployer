"""
Unit tests for ProcessDeploymentUseCase.

Verifies the orchestration flow: validation → memory persistence.
Complements the validator's hypothesis tests by covering the
application layer.
"""

from __future__ import annotations

import pytest

from app.application.use_cases import ProcessDeploymentUseCase, deployment_store
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentAction, DeploymentIntent, DeploymentStatus


@pytest.fixture(autouse=True)
def _clean_store() -> None:  # type: ignore[misc]
    """Cleans the in-memory store before each test."""
    deployment_store.clear()


class TestProcessDeploymentUseCase:
    """Main use case tests."""

    def test_safe_intent_creates_pending_record(self) -> None:
        """A safe intent is saved with PENDING_APPROVAL status."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            name="api-test",
            image="docker.io/library/nginx:1.25.3",
            internal_port=8080,
            cpu="250m",
            ram="128Mi",
        )

        record = use_case.execute(intent)

        assert record.status == DeploymentStatus.PENDING_APPROVAL
        assert record.intent == intent
        assert record.result_url is None
        assert record.id in deployment_store

    def test_unsafe_port_rejects_intent(self) -> None:
        """Port < 1024 raises SecurityViolationError and is NOT saved."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            name="hack-service",
            image="docker.io/library/nginx:1.25.3",
            internal_port=80,
        )

        with pytest.raises(SecurityViolationError):
            use_case.execute(intent)

        # Verify that it was NOT persisted
        assert len(deployment_store) == 0

    def test_latest_tag_rejects_intent(self) -> None:
        """Image with :latest raises SecurityViolationError and is NOT saved."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            name="bad-image",
            image="docker.io/library/nginx:latest",
            internal_port=8080,
        )

        with pytest.raises(SecurityViolationError):
            use_case.execute(intent)

        assert len(deployment_store) == 0

    def test_multiple_intents_get_unique_ids(self) -> None:
        """Each registered intent gets a unique ID."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            name="svc",
            image="docker.io/library/python:3.12",
            internal_port=8080,
        )

        r1 = use_case.execute(intent)
        r2 = use_case.execute(intent)

        assert r1.id != r2.id
        assert len(deployment_store) == 2

    def test_delete_intent_skips_validation(self) -> None:
        """A DELETE intent is saved without validating image or port."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            name="old-service",
            action=DeploymentAction.DELETE,
        )

        record = use_case.execute(intent)

        assert record.status == DeploymentStatus.PENDING_APPROVAL
        assert record.intent.action.value == "DELETE"
        assert record.id in deployment_store

    def test_create_intent_missing_image_raises_error(self) -> None:
        """Validation fails if action=CREATE but image is missing."""
        with pytest.raises(ValueError, match="The 'image' field is mandatory"):
            DeploymentIntent(
                name="test",
                action=DeploymentAction.CREATE,
                internal_port=8080,
            )

    def test_create_intent_missing_port_raises_error(self) -> None:
        """Validation fails if action=CREATE but port is missing."""
        with pytest.raises(ValueError, match="The 'internal_port' field is mandatory"):
            DeploymentIntent(
                name="test",
                action=DeploymentAction.CREATE,
                image="docker.io/library/nginx:1.25.3",
            )
