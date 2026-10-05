"""
Metamorphic Tests for the Agent's intent extraction system.

These tests evaluate that the LLM (or the FakeLLM in its absence) complies with
essential metamorphic relations in natural language processing:

1. MR-1 (Permutation): The order in which parameters are given should not alter the result.
2. MR-2 (Noise/Robustness): Adding greetings, farewells, or irrelevant text should not alter the result.
3. MR-3 (Case Invariance): Changes in uppercase/lowercase should not affect extraction.
"""

import os
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any

import pytest

from app.agent_layer.agent import FakeLLMClient, OllamaLLMClient, OpenAILLMClient
from app.agent_layer.tools import TOOL_DEFINITIONS


@pytest.fixture(scope="session", autouse=True)
def ensure_ollama_running():
    """
    Si se solicita ejecución real, comprueba si Ollama está corriendo.
    Si no lo está, levanta el demonio en background y lo cierra al terminar.
    """
    if os.getenv("RUN_REAL_LLM") != "true":
        yield
        return

    # Check if Ollama is already running
    url = "http://localhost:11434/api/tags"
    is_running = False
    try:
        urllib.request.urlopen(url, timeout=2)
        is_running = True
    except urllib.error.URLError:
        pass

    process = None
    if not is_running:
        print("\n[Metamorphic Tests] Iniciando demonio local de Ollama...")
        try:
            # Start Ollama daemon in background
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            pytest.fail("El ejecutable 'ollama' no está instalado o no se encuentra en el PATH.")

        # Wait for daemon to be ready (up to 15 seconds)
        ready = False
        for _ in range(15):
            time.sleep(1)
            try:
                urllib.request.urlopen(url, timeout=2)
                ready = True
                break
            except urllib.error.URLError:
                continue

        if not ready:
            if process:
                process.terminate()
            pytest.fail("No se pudo conectar a Ollama tras iniciar el demonio.")

    yield  # Run tests

    # Cleanup if we started the daemon
    if process:
        print("\n[Metamorphic Tests] Deteniendo demonio de Ollama...")
        process.terminate()
        process.wait()
def extract_params(client, messages: list[dict]) -> dict[str, Any]:
    """Extrae los parámetros usando el Fake o el modelo real."""
    if isinstance(client, FakeLLMClient):
        return client._extract_params_from_history(messages)

    # Si es Ollama o Gemini, llamamos al modelo y extraemos los argumentos del tool_call
    response = client.chat(messages, tools=TOOL_DEFINITIONS)
    for tc in response.tool_calls:
        if tc.name == "format_deployment_intent":
            return tc.arguments  # type: ignore
    return {}


@pytest.fixture
def parser():
    if os.getenv("RUN_REAL_LLM") == "true":
        provider = os.getenv("LLM_PROVIDER", "ollama")
        if provider == "gemini":
            return OpenAILLMClient(
                model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=os.getenv("GEMINI_API_KEY", "")
            )
        elif provider == "groq":
            return OpenAILLMClient(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                base_url="https://api.groq.com/openai/v1",
                api_key=os.getenv("GROQ_API_KEY", "")
            )
        elif provider == "mistral":
            return OpenAILLMClient(
                model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
                base_url="https://api.mistral.ai/v1",
                api_key=os.getenv("MISTRAL_API_KEY", "")
            )
        elif provider == "cohere":
            from app.agent_layer.agent import LiteLLMClient
            return LiteLLMClient(
                model=os.getenv("COHERE_MODEL", "cohere/command-r-plus-08-2024")
            )
        # Usado para las ejecuciones documentadas en el Capítulo 7
        return OllamaLLMClient(model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"))
    return FakeLLMClient()


def test_mr1_order_permutation(parser: FakeLLMClient) -> None:
    """
    MR-1: Order permutation.
    If we provide data in a different order, the extraction must be identical.
    """
    # Prompt A: Natural order
    prompt_a = [{"role": "user", "content": "Necesito un servicio llamado api-backend con la imagen python:3.12 y el puerto 8000"}]

    # Prompt B: Reversed order
    prompt_b = [{"role": "user", "content": "Con el puerto 8000 y la imagen python:3.12, necesito un servicio llamado api-backend"}]

    result_a = extract_params(parser, prompt_a)
    result_b = extract_params(parser, prompt_b)

    # Las heurísticas del LLM real a veces deducen CPU/RAM por defecto si no se lo damos.
    # Así que verificamos que, como mínimo, los obligatorios coinciden.
    assert result_a.get("name") == result_b.get("name") == "api-backend"
    assert result_a.get("image") == result_b.get("image") == "python:3.12"
    assert int(result_a.get("internal_port", 0)) == int(result_b.get("internal_port", 0)) == 8000


def test_mr2_noise_invariance(parser: FakeLLMClient) -> None:
    """
    MR-2: Noise invariance (Robustness).
    Adding introductory, courtesy, or irrelevant text must not alter extraction.
    """
    base_prompt = [{"role": "user", "content": "Quiero desplegar mi-web con imagen nginx:latest en el puerto 80"}]

    noisy_prompt = [{"role": "user", "content": "Hola buenos dias equipo del SIC, por favor cuando tengais un hueco: Quiero desplegar mi-web con imagen nginx:latest en el puerto 80. Muchas gracias de antemano y un saludo cordial."}]

    result_base = extract_params(parser, base_prompt)
    result_noisy = extract_params(parser, noisy_prompt)

    assert result_base.get("name") == result_noisy.get("name") == "mi-web"
    assert result_base.get("image") == result_noisy.get("image") == "nginx:latest"
    assert int(result_base.get("internal_port", 0)) == int(result_noisy.get("internal_port", 0)) == 80


def test_mr3_case_invariance(parser: FakeLLMClient) -> None:
    """
    MR-3: Case invariance.
    Using uppercase or lowercase in the text (except for exact values) must not affect.
    """
    lower_prompt = [{"role": "user", "content": "quiero el servicio redis con imagen redis:7.0 en el puerto 6379"}]

    upper_prompt = [{"role": "user", "content": "QUIERO EL servicio redis CON IMAGEN redis:7.0 EN EL PUERTO 6379"}]

    result_lower = extract_params(parser, lower_prompt)
    result_upper = extract_params(parser, upper_prompt)

    assert result_lower.get("name") == result_upper.get("name") == "redis"
    assert result_lower.get("image") == result_upper.get("image") == "redis:7.0"
    assert int(result_lower.get("internal_port", 0)) == int(result_upper.get("internal_port", 0)) == 6379


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

    result_single = extract_params(parser, single_message)
    result_incremental = extract_params(parser, incremental_messages)

    assert result_single.get("name") == result_incremental.get("name") == "app-test"
    assert result_single.get("image") == result_incremental.get("image") == "node:18"
    assert int(result_single.get("internal_port", 0)) == int(result_incremental.get("internal_port", 0)) == 3000


def test_mr5_paraphrasing(parser: FakeLLMClient) -> None:
    """
    MR-5: Paraphrasing.
    Using synonymous verbs or different grammatical structures should yield the same parameters.
    """
    base_prompt = [{"role": "user", "content": "Necesito que levantes un wordpress:6.0 en el puerto 80 llamado blog"}]
    paraphrase_prompt = [{"role": "user", "content": "Por favor, crea un servicio que responda al nombre de blog, utilizando para ello la imagen de contenedor wordpress:6.0 y publicándolo internamente a través del puerto 80."}]

    result_base = extract_params(parser, base_prompt)
    result_para = extract_params(parser, paraphrase_prompt)

    assert result_base.get("name") == result_para.get("name") == "blog"
    assert result_base.get("image") == result_para.get("image") == "wordpress:6.0"
    assert int(result_base.get("internal_port", 0)) == int(result_para.get("internal_port", 0)) == 80


def test_mr6_language_invariance(parser: FakeLLMClient) -> None:
    """
    MR-6: Language invariance.
    Providing the request in a different language (e.g., English) should yield the same extraction,
    demonstrating the LLM's cross-lingual semantic understanding.
    """
    spanish_prompt = [{"role": "user", "content": "Despliega una base de datos postgres:14 en el puerto 5432 con el nombre db-prod"}]
    english_prompt = [{"role": "user", "content": "Deploy a postgres:14 database on port 5432 with the name db-prod"}]

    result_es = extract_params(parser, spanish_prompt)
    result_en = extract_params(parser, english_prompt)

    assert result_es.get("name") == result_en.get("name") == "db-prod"
    assert result_es.get("image") == result_en.get("image") == "postgres:14"
    assert int(result_es.get("internal_port", 0)) == int(result_en.get("internal_port", 0)) == 5432
