"""
Pruebas Metamórficas para el sistema de extracción de intenciones del Agente.

Estas pruebas evalúan que el LLM (o el FakeLLM en su defecto) cumple con
relaciones metamórficas esenciales en procesamiento de lenguaje natural:

1. MR-1 (Permutación): El orden en el que se dan los parámetros no debe alterar el resultado.
2. MR-2 (Ruido/Robustez): Añadir saludos, despedidas o texto irrelevante no debe alterar el resultado.
3. MR-3 (Invarianza de Case): Cambios en mayúsculas/minúsculas no deben afectar la extracción.
"""

import pytest

from app.agent_layer.agent import FakeLLMClient


@pytest.fixture
def parser() -> FakeLLMClient:
    return FakeLLMClient()


def test_mr1_order_permutation(parser: FakeLLMClient) -> None:
    """
    MR-1: Permutación del orden.
    Si proporcionamos los datos en distinto orden, la extracción debe ser idéntica.
    """
    # Prompt A: Orden natural
    prompt_a = [{"role": "user", "content": "Necesito un servicio api-backend con la imagen python:3.12 y el puerto 8000"}]

    # Prompt B: Orden invertido
    prompt_b = [{"role": "user", "content": "Con el puerto 8000 y la imagen python:3.12, necesito un servicio api-backend"}]

    result_a = parser._extract_params_from_history(prompt_a)
    result_b = parser._extract_params_from_history(prompt_b)

    assert result_a == result_b
    assert result_a == {"nombre": "api-backend", "imagen": "python:3.12", "puerto_interno": 8000}


def test_mr2_noise_invariance(parser: FakeLLMClient) -> None:
    """
    MR-2: Invarianza ante ruido (Robustez).
    Añadir texto introductorio, de cortesía o irrelevante no debe alterar la extracción.
    """
    base_prompt = [{"role": "user", "content": "Quiero desplegar mi-web con imagen nginx:latest en el puerto 80"}]

    noisy_prompt = [{"role": "user", "content": "Hola buenos dias equipo del SIC, por favor cuando tengais un hueco: Quiero desplegar mi-web con imagen nginx:latest en el puerto 80. Muchas gracias de antemano y un saludo cordial."}]

    result_base = parser._extract_params_from_history(base_prompt)
    result_noisy = parser._extract_params_from_history(noisy_prompt)

    assert result_base == result_noisy
    assert result_base == {"nombre": "mi-web", "imagen": "nginx:latest", "puerto_interno": 80}


def test_mr3_case_invariance(parser: FakeLLMClient) -> None:
    """
    MR-3: Invarianza de formato (Case).
    Usar mayúsculas o minúsculas en el texto (salvo para valores exactos) no debe afectar.
    """
    lower_prompt = [{"role": "user", "content": "quiero el servicio redis con imagen redis:7.0 en el puerto 6379"}]

    upper_prompt = [{"role": "user", "content": "QUIERO EL servicio redis CON IMAGEN redis:7.0 EN EL PUERTO 6379"}]

    result_lower = parser._extract_params_from_history(lower_prompt)
    result_upper = parser._extract_params_from_history(upper_prompt)

    assert result_lower == result_upper
    assert result_lower == {"nombre": "redis", "imagen": "redis:7.0", "puerto_interno": 6379}


def test_mr4_incremental_context(parser: FakeLLMClient) -> None:
    """
    MR-4: Composición incremental.
    Dar los datos en un solo mensaje debe ser equivalente a darlos en varios mensajes de historial.
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
    assert result_single == {"nombre": "app-test", "imagen": "node:18", "puerto_interno": 3000}
