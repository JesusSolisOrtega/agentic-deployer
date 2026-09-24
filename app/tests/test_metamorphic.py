"""
Metamorphic Tests for the Agent's intent extraction system.

These tests evaluate that the LLM (or the FakeLLM in its absence) complies with
essential metamorphic relations in natural language processing:

1. MR-1 (Permutation): The order in which parameters are given should not alter the result.
2. MR-2 (Noise/Robustness): Adding greetings, farewells, or irrelevant text should not alter the result.
3. MR-3 (Case Invariance): Changes in uppercase/lowercase should not affect extraction.
"""

import pytest

from app.agent_layer.agent import FakeLLMClient


@pytest.fixture
def parser() -> FakeLLMClient:
    return FakeLLMClient()


def test_mr1_order_permutation(parser: FakeLLMClient) -> None:
    """
    MR-1: Order permutation.
    If we provide data in a different order, the extraction must be identical.
    """
    # Prompt A: Natural order
    prompt_a = [{"role": "user", "content": "Necesito un servicio api-backend con la imagen python:3.12 y el puerto 8000"}]

    # Prompt B: Reversed order
    prompt_b = [{"role": "user", "content": "Con el puerto 8000 y la imagen python:3.12, necesito un servicio api-backend"}]

    result_a = parser._extract_params_from_history(prompt_a)
    result_b = parser._extract_params_from_history(prompt_b)

    assert result_a == result_b
    assert result_a == {"name": "api-backend", "image": "python:3.12", "internal_port": 8000}


def test_mr2_noise_invariance(parser: FakeLLMClient) -> None:
    """
    MR-2: Noise invariance (Robustness).
    Adding introductory, courtesy, or irrelevant text must not alter extraction.
    """
    base_prompt = [{"role": "user", "content": "Quiero desplegar mi-web con imagen nginx:latest en el puerto 80"}]

    noisy_prompt = [{"role": "user", "content": "Hola buenos dias equipo del SIC, por favor cuando tengais un hueco: Quiero desplegar mi-web con imagen nginx:latest en el puerto 80. Muchas gracias de antemano y un saludo cordial."}]

    result_base = parser._extract_params_from_history(base_prompt)
    result_noisy = parser._extract_params_from_history(noisy_prompt)

    assert result_base == result_noisy
    assert result_base == {"name": "mi-web", "image": "nginx:latest", "internal_port": 80}


def test_mr3_case_invariance(parser: FakeLLMClient) -> None:
    """
    MR-3: Case invariance.
    Using uppercase or lowercase in the text (except for exact values) must not affect.
    """
    lower_prompt = [{"role": "user", "content": "quiero el servicio redis con imagen redis:7.0 en el puerto 6379"}]

    upper_prompt = [{"role": "user", "content": "QUIERO EL servicio redis CON IMAGEN redis:7.0 EN EL PUERTO 6379"}]

    result_lower = parser._extract_params_from_history(lower_prompt)
    result_upper = parser._extract_params_from_history(upper_prompt)

    assert result_lower == result_upper
    assert result_lower == {"name": "redis", "image": "redis:7.0", "internal_port": 6379}


def test_mr4_incremental_context(parser: FakeLLMClient) -> None:
    """
    MR-4: Incremental composition.
    Providing data in a single message must be equivalent to providing it in multiple history messages.
    """
    single_message = [
        {"role": "user", "content": "desplegar app-test con imagen node:18 y puerto 3000"}
    ]

    incremental_messages = [
        {"role": "user", "content": "quiero desplegar app-test"},
        {"role": "assistant", "content": "¿Qué imagen y puerto?"},
        {"role": "user", "content": "la imagen es node:18"},
        {"role": "assistant", "content": "¿Y el puerto?"},
        {"role": "user", "content": "puerto 3000"}
    ]

    result_single = parser._extract_params_from_history(single_message)
    result_incremental = parser._extract_params_from_history(incremental_messages)

    assert result_single == result_incremental
    assert result_single == {"name": "app-test", "image": "node:18", "internal_port": 3000}
