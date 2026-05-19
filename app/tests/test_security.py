"""
Property-Based Testing para SecurityContextValidator.

Usa `hypothesis` para generar intenciones de despliegue aleatorias y
verificar que el validador SIEMPRE detecta violaciones de seguridad
cuando existen puertos privilegiados o etiquetas :latest.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.application.security_validator import SecurityContextValidator
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentAction, DeploymentIntent

# ---------------------------------------------------------------------------
# Estrategias de generacion
# ---------------------------------------------------------------------------

# Generador de nombres validos (1-30 chars alfanumericos con guiones)
valid_name = st.from_regex(r"[a-z][a-z0-9\-]{0,29}", fullmatch=True)

# Generador de requests CPU estilo K8s (ej: "100m", "500m", "1")
valid_cpu = st.sampled_from(["100m", "250m", "500m", "1", "2"])

# Generador de requests RAM estilo K8s (ej: "64Mi", "128Mi", "256Mi")
valid_ram = st.sampled_from(["64Mi", "128Mi", "256Mi", "512Mi", "1Gi"])

# Generador de imagenes seguras (sin :latest)
safe_image = st.from_regex(r"[a-z]{3,15}:[0-9]+\.[0-9]+(\.[0-9]+)?", fullmatch=True)

# Generador de imagenes inseguras (siempre contiene :latest)
unsafe_latest_image = st.from_regex(r"[a-z]{3,15}:latest", fullmatch=True)

# Generador de puertos seguros (>= 1024)
safe_port = st.integers(min_value=1024, max_value=65535)

# Generador de puertos inseguros (< 1024, > 0)
unsafe_port = st.integers(min_value=1, max_value=1023)


# ---------------------------------------------------------------------------
# Estrategia compuesta: DeploymentIntent como diccionario
# ---------------------------------------------------------------------------

@st.composite
def deployment_intent_dict(
    draw: st.DrawFn,
    *,
    force_unsafe_port: bool = False,
    force_latest_image: bool = False,
) -> dict:
    """
    Genera un diccionario que representa un DeploymentIntent (action=CREATE).

    Permite forzar condiciones inseguras para probar que el validador
    las detecta de forma determinista.
    """
    nombre = draw(valid_name)
    imagen = draw(unsafe_latest_image if force_latest_image else safe_image)
    puerto = draw(unsafe_port if force_unsafe_port else safe_port)
    cpu = draw(valid_cpu)
    ram = draw(valid_ram)

    return {
        "nombre": nombre,
        "action": "CREATE",
        "imagen": imagen,
        "puerto_interno": puerto,
        "cpu": cpu,
        "ram": ram,
    }


# ---------------------------------------------------------------------------
# Instancia del validador bajo test
# ---------------------------------------------------------------------------

validator = SecurityContextValidator()


# ---------------------------------------------------------------------------
# Propiedades
# ---------------------------------------------------------------------------

class TestSecurityContextValidator:
    """Propiedades que deben cumplirse PARA TODO input generado."""

    @given(data=deployment_intent_dict(force_unsafe_port=True, force_latest_image=False))
    @settings(max_examples=100)
    def test_privileged_port_always_raises(self, data: dict) -> None:
        """
        PROPIEDAD: Si el puerto es < 1024, el validador SIEMPRE lanza
        SecurityViolationError con un mensaje sobre el puerto.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        assert any("Puerto privilegiado" in v for v in exc_info.value.violations)

    @given(data=deployment_intent_dict(force_unsafe_port=False, force_latest_image=True))
    @settings(max_examples=100)
    def test_latest_tag_always_raises(self, data: dict) -> None:
        """
        PROPIEDAD: Si la imagen contiene ':latest', el validador SIEMPRE
        lanza SecurityViolationError con un mensaje sobre la etiqueta.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        assert any(":latest" in v for v in exc_info.value.violations)

    @given(data=deployment_intent_dict(force_unsafe_port=True, force_latest_image=True))
    @settings(max_examples=100)
    def test_both_violations_detected_simultaneously(self, data: dict) -> None:
        """
        PROPIEDAD: Si AMBAS condiciones inseguras estan presentes,
        el validador detecta las DOS en una sola pasada.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        violations = exc_info.value.violations
        assert len(violations) == 2
        assert any("Puerto privilegiado" in v for v in violations)
        assert any(":latest" in v for v in violations)

    @given(data=deployment_intent_dict(force_unsafe_port=False, force_latest_image=False))
    @settings(max_examples=100)
    def test_safe_intent_never_raises(self, data: dict) -> None:
        """
        PROPIEDAD: Si el puerto es >= 1024 y la imagen NO contiene ':latest',
        el validador NUNCA lanza excepcion.
        """
        intent = DeploymentIntent(**data)

        # No debe lanzar ninguna excepcion
        validator.validate(intent)

    @given(nombre=valid_name)
    @settings(max_examples=50)
    def test_delete_action_always_passes(self, nombre: str) -> None:
        """
        PROPIEDAD: Las acciones DELETE NUNCA lanzan excepcion
        independientemente de los demas campos.
        """
        intent = DeploymentIntent(nombre=nombre, action=DeploymentAction.DELETE)
        # No debe lanzar ninguna excepcion
        validator.validate(intent)
