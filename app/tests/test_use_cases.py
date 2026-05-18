"""
Tests unitarios para ProcessDeploymentUseCase.

Verifica el flujo de orquestación: validación → persistencia en memoria.
Complementa los tests de hypothesis del validador cubriendo la capa
de aplicación.
"""

from __future__ import annotations

import pytest

from app.application.use_cases import ProcessDeploymentUseCase, deployment_store
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentIntent, DeploymentStatus


@pytest.fixture(autouse=True)
def _clean_store() -> None:  # type: ignore[misc]
    """Limpia el almacén en memoria antes de cada test."""
    deployment_store.clear()


class TestProcessDeploymentUseCase:
    """Tests del caso de uso principal."""

    def test_safe_intent_creates_pending_record(self) -> None:
        """Una intención segura se guarda con estado PENDING_APPROVAL."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            nombre="api-test",
            imagen="nginx:1.25.3",
            puerto_interno=8080,
            cpu="250m",
            ram="128Mi",
        )

        record = use_case.execute(intent)

        assert record.status == DeploymentStatus.PENDING_APPROVAL
        assert record.intent == intent
        assert record.result_url is None
        assert record.id in deployment_store

    def test_unsafe_port_rejects_intent(self) -> None:
        """Puerto < 1024 provoca SecurityViolationError y NO se guarda."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            nombre="hack-service",
            imagen="nginx:1.25.3",
            puerto_interno=80,
        )

        with pytest.raises(SecurityViolationError):
            use_case.execute(intent)

        # Verificar que NO se persistió
        assert len(deployment_store) == 0

    def test_latest_tag_rejects_intent(self) -> None:
        """Imagen con :latest provoca SecurityViolationError y NO se guarda."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            nombre="bad-image",
            imagen="nginx:latest",
            puerto_interno=8080,
        )

        with pytest.raises(SecurityViolationError):
            use_case.execute(intent)

        assert len(deployment_store) == 0

    def test_multiple_intents_get_unique_ids(self) -> None:
        """Cada intención registrada obtiene un ID único."""
        use_case = ProcessDeploymentUseCase()
        intent = DeploymentIntent(
            nombre="svc",
            imagen="python:3.12",
            puerto_interno=8080,
        )

        r1 = use_case.execute(intent)
        r2 = use_case.execute(intent)

        assert r1.id != r2.id
        assert len(deployment_store) == 2
