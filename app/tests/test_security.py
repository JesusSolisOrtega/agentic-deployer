"""
Property-Based Testing for SecurityContextValidator.

Uses `hypothesis` to generate random deployment intents and
verify that the validator ALWAYS detects security violations
when privileged ports or :latest tags are present.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.application.security_validator import SecurityContextValidator
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentAction, DeploymentIntent

# ---------------------------------------------------------------------------
# Generation strategies
# ---------------------------------------------------------------------------

# Generator for valid names (1-30 alphanumeric chars with hyphens)
valid_name = st.from_regex(r"[a-z][a-z0-9\-]{0,29}", fullmatch=True)

# Generator for K8s-style CPU requests (e.g. "100m", "500m", "1")
valid_cpu = st.sampled_from(["100m", "250m", "500m", "1", "2"])

# Generator for K8s-style RAM requests (e.g. "64Mi", "128Mi", "256Mi")
valid_ram = st.sampled_from(["64Mi", "128Mi", "256Mi", "512Mi", "1Gi"])

# Generator for safe images (allowed registry, no :latest)
safe_image = st.from_regex(r"(docker\.io/|harbor\.universidad\.edu/)[a-z]{3,10}:[0-9]+\.[0-9]+", fullmatch=True)

# Generator for unsafe images (always contains :latest)
unsafe_latest_image = st.from_regex(r"(docker\.io/|harbor\.universidad\.edu/)[a-z]{3,10}:latest", fullmatch=True)

# Generator for safe ports (>= 1024)
safe_port = st.integers(min_value=1024, max_value=65535)

# Generator for unsafe ports (< 1024, > 0)
unsafe_port = st.integers(min_value=1, max_value=1023)


# ---------------------------------------------------------------------------
# Composite strategy: DeploymentIntent as dictionary
# ---------------------------------------------------------------------------

@st.composite
def deployment_intent_dict(
    draw: st.DrawFn,
    *,
    force_unsafe_port: bool = False,
    force_latest_image: bool = False,
) -> dict:
    """
    Generates a dictionary representing a DeploymentIntent (action=CREATE).

    Allows forcing unsafe conditions to prove the validator
    detects them deterministically.
    """
    name = draw(valid_name)
    image = draw(unsafe_latest_image if force_latest_image else safe_image)
    port = draw(unsafe_port if force_unsafe_port else safe_port)
    cpu = draw(valid_cpu)
    ram = draw(valid_ram)
    env: dict[str, str] = {}

    return {
        "name": name,
        "action": "CREATE",
        "image": image,
        "internal_port": port,
        "cpu": cpu,
        "ram": ram,
        "env_vars": env,
    }


# ---------------------------------------------------------------------------
# Validator instance under test
# ---------------------------------------------------------------------------

validator = SecurityContextValidator()


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------

class TestSecurityContextValidator:
    """Properties that must hold true FOR ALL generated inputs."""

    @given(data=deployment_intent_dict(force_unsafe_port=True, force_latest_image=False))
    @settings(max_examples=100)
    def test_privileged_port_always_raises(self, data: dict) -> None:
        """
        PROPERTY: If the port is < 1024, the validator ALWAYS raises
        SecurityViolationError with a message about the port.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        assert any("Privileged port" in v for v in exc_info.value.violations)

    @given(data=deployment_intent_dict(force_unsafe_port=False, force_latest_image=True))
    @settings(max_examples=100)
    def test_latest_tag_always_raises(self, data: dict) -> None:
        """
        PROPERTY: If the image contains ':latest', the validator ALWAYS
        raises SecurityViolationError with a message about the tag.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        assert any(":latest" in v for v in exc_info.value.violations)

    @given(data=deployment_intent_dict(force_unsafe_port=True, force_latest_image=True))
    @settings(max_examples=100)
    def test_both_violations_detected_simultaneously(self, data: dict) -> None:
        """
        PROPERTY: If BOTH unsafe conditions are present,
        the validator detects BOTH in a single pass.
        """
        intent = DeploymentIntent(**data)

        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)

        violations = exc_info.value.violations
        assert len(violations) == 2
        assert any("Privileged port" in v for v in violations)
        assert any(":latest" in v for v in violations)

    @given(data=deployment_intent_dict(force_unsafe_port=False, force_latest_image=False))
    @settings(max_examples=100)
    def test_safe_intent_never_raises(self, data: dict) -> None:
        """
        PROPERTY: If the port is >= 1024 and the image DOES NOT contain ':latest',
        the validator NEVER raises an exception.
        """
        intent = DeploymentIntent(**data)

        # Should not raise any exception
        validator.validate(intent)

    @given(
        name=valid_name,
        image=unsafe_latest_image | st.none(),
        port=unsafe_port | st.none()
    )
    @settings(max_examples=50)
    def test_delete_action_always_passes(
        self, name: str, image: str | None, port: int | None
    ) -> None:
        """
        PROPERTY: DELETE actions NEVER raise an exception
        regardless of other fields (even if invalid).
        """
        intent = DeploymentIntent(
            name=name,
            action=DeploymentAction.DELETE,
            image=image,
            internal_port=port
        )
        # Should not raise any exception
        validator.validate(intent)

    @given(data=deployment_intent_dict())
    @settings(max_examples=50)
    def test_untrusted_registry_always_raises(self, data: dict) -> None:
        """PROPERTY: Images outside the whitelist are always rejected."""
        data["image"] = "hacker.io/miner:1.0"
        intent = DeploymentIntent(**data)
        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)
        assert any("Untrusted registry" in v for v in exc_info.value.violations)

    @given(data=deployment_intent_dict())
    @settings(max_examples=50)
    def test_hardware_quotas_always_raises(self, data: dict) -> None:
        """PROPERTY: Exceeding 4 cores or 8Gi RAM always raises violation."""
        data["cpu"] = "5"      # Equivalent to 5000m > 4000m
        data["ram"] = "10Gi"   # Equivalent to 10240Mi > 8192Mi
        intent = DeploymentIntent(**data)
        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)
        violations = exc_info.value.violations
        assert any("CPU quota exceeded" in v for v in violations)
        assert any("RAM quota exceeded" in v for v in violations)

    @given(data=deployment_intent_dict())
    @settings(max_examples=50)
    def test_secrets_in_env_always_raises(self, data: dict) -> None:
        """PROPERTY: Detecting words like 'password' or 'secret' in env_vars dictionary raises violation."""
        data["env_vars"] = {"DB_PASSWORD": "supersecret", "API_KEY": "123"}
        intent = DeploymentIntent(**data)
        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)
        violations = exc_info.value.violations
        assert any("Potential plaintext secret" in v for v in violations)

    def test_database_without_storage_raises(self) -> None:
        """PROPERTY: Databases without explicit storage raise violation."""
        intent = DeploymentIntent(
            name="mydb",
            action=DeploymentAction.CREATE,
            image="docker.io/postgres:14.0",
            internal_port=5432
        )
        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)
        assert any("Databases require explicit storage" in v for v in exc_info.value.violations)

    def test_ram_tib_parsing(self) -> None:
        """Test parsing of TiB RAM and invalid RAM fallback to 0."""
        # 1Ti is 1048576 Mi, which is > MAX_RAM_MI (8192)
        intent = DeploymentIntent(
            name="huge-app",
            action=DeploymentAction.CREATE,
            image="docker.io/app:1.0",
            internal_port=8080,
            ram="1Ti"
        )
        with pytest.raises(SecurityViolationError) as exc_info:
            validator.validate(intent)
        assert any("RAM quota exceeded" in v for v in exc_info.value.violations)


