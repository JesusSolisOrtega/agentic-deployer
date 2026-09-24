"""
Orquestador del Agente LLM.

Desacopla la lógica de orquestación (tool-calling loop) del cliente LLM
concreto, haciéndolo 100 % testeable con mocks.

Componentes:
  - ToolCall / AgentResponse: dataclasses de comunicación.
  - LLMClient (ABC): interfaz que cualquier proveedor debe implementar.
  - FakeLLMClient: simulación sin API key para desarrollo y demo.
  - AgentOrchestrator: bucle ReAct (Reason + Act) que ejecuta herramientas.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.agent_layer.tools import TOOL_DEFINITIONS, TOOL_REGISTRY

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ToolCall:
    """Representa una invocación de herramienta solicitada por el LLM."""

    id: str
    name: str
    arguments: dict


@dataclass
class AgentResponse:
    """Respuesta del LLM: texto libre y/o llamadas a herramientas."""

    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)


# ---------------------------------------------------------------------------
# LLM Client — Interfaz abstracta
# ---------------------------------------------------------------------------

class LLMClient(ABC):
    """
    Contrato para cualquier cliente LLM (OpenAI, LiteLLM, Ollama…).
    Recibe mensajes + herramientas, devuelve un AgentResponse.
    """

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        ...


# ---------------------------------------------------------------------------
# Fake LLM — Simulación basada en reglas para demo
# ---------------------------------------------------------------------------

class FakeLLMClient(LLMClient):  # pragma: no cover
    """
    Cliente LLM simulado que usa pattern-matching para extraer
    parámetros de despliegue del texto del usuario.

    Perfecto para desarrollo local y demos sin necesidad de API key.
    """

    SYSTEM_PROMPT = (
        "Eres un asistente de despliegues. Ayudas a los equipos "
        "a solicitar despliegues en el clúster OKD de forma sencilla."
    )

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        last = messages[-1]

        # ── Después de ejecutar una herramienta → resumir resultado ────
        if last.get("role") == "tool":
            return self._summarize_tool_result(last, messages)

        # ── Mensaje de usuario → extraer parámetros ────────────────────
        params = self._extract_params_from_history(messages)
        nombre = params.get("nombre")
        imagen = params.get("imagen")
        puerto = params.get("puerto_interno")
        usuarios = params.get("usuarios")

        # Si hay usuarios pero aún no calculamos recursos → calcular
        if usuarios and not self._has_resource_result(messages):
            return AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="calculate_optimal_resources",
                        arguments={"users": usuarios},
                    ),
                ],
            )

        # Si tenemos nombre + imagen + puerto → desplegar
        if nombre and imagen and puerto:
            cpu = params.get("cpu", "250m")
            ram = params.get("ram", "128Mi")
            return AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="format_deployment_intent",
                        arguments={
                            "nombre": nombre,
                            "imagen": imagen,
                            "puerto_interno": puerto,
                            "cpu": cpu,
                            "ram": ram,
                        },
                    ),
                ],
            )

        # Faltan datos → preguntar
        missing = []
        if not nombre:
            missing.append("el **nombre** del servicio")
        if not imagen:
            missing.append("la **imagen** de contenedor (ej: `nginx:1.25.3`)")
        if not puerto:
            missing.append("el **puerto** interno")

        return AgentResponse(
            content=(
                "Necesito algo más de información para preparar el despliegue:\n"
                + "\n".join(f"- {m}" for m in missing)
                + "\n\n¿Me los puedes proporcionar?"
            ),
        )

    # ── Helpers privados ───────────────────────────────────────────────

    def _extract_params_from_history(self, messages: list[dict]) -> dict:
        """Extrae parámetros de despliegue de todos los mensajes del usuario."""
        all_text = " ".join(
            m.get("content", "")
            for m in messages
            if m.get("role") == "user" and m.get("content")
        ).lower()

        params: dict = {}

        # Imagen: word:tag o word/word:tag (excluir :latest-like que no parezca imagen)
        img_match = re.search(r"([\w\-]+(?:/[\w\-]+)?:[\w\.\-]+)", all_text)
        if img_match:
            params["imagen"] = img_match.group(1)

        # Puerto: número después de "puerto"
        port_match = re.search(r"puerto\s+(\d+)", all_text)
        if port_match:
            params["puerto_interno"] = int(port_match.group(1))

        # Nombre del servicio
        name_match = re.search(
            r"(?:servicio|nombre|llamad[oa]|desplegar|deploy)\s+[\"']?([\w\-]+)",
            all_text,
        )
        if name_match:
            params["nombre"] = name_match.group(1)

        # Usuarios
        users_match = re.search(r"(\d+)\s*usuarios", all_text)
        if users_match:
            params["usuarios"] = int(users_match.group(1))

        # Si ya calculamos recursos, inyectarlos
        resources = self._get_resource_result(messages)
        if resources:
            params["cpu"] = resources.get("cpu", "250m")
            params["ram"] = resources.get("ram", "128Mi")

        return params

    def _has_resource_result(self, messages: list[dict]) -> bool:
        return any(
            m.get("role") == "tool" and m.get("name") == "calculate_optimal_resources"
            for m in messages
        )

    def _get_resource_result(self, messages: list[dict]) -> dict | None:
        for m in reversed(messages):
            if m.get("role") == "tool" and m.get("name") == "calculate_optimal_resources":
                return dict(json.loads(m["content"]))
        return None

    def _summarize_tool_result(
        self, tool_msg: dict, messages: list[dict],
    ) -> AgentResponse:
        tool_name = tool_msg.get("name", "")
        result = json.loads(tool_msg.get("content", "{}"))

        if tool_name == "format_deployment_intent":
            deploy_id = result.get("id", "???")
            return AgentResponse(
                content=(
                    f"✅ **Solicitud enviada a revisión.**\n\n"
                    f"- **ID:** `{deploy_id}`\n"
                    f"- **Estado:** Pendiente de aprobación\n\n"
                    f"Un técnico de operaciones la revisará en el "
                    f"[panel HITL](http://localhost:8000/frontend/index.html)."
                ),
            )

        if tool_name == "calculate_optimal_resources":
            tier = result.get("tier", "")
            cpu = result.get("cpu", "")
            ram = result.get("ram", "")
            # Continuar con el despliegue — re-analizar el historial
            params = self._extract_params_from_history(messages)
            nombre = params.get("nombre")
            imagen = params.get("imagen")
            puerto = params.get("puerto_interno")

            if nombre and imagen and puerto:
                return AgentResponse(
                    content=(
                        f"📊 Para tu volumen de usuarios recomiendo tier "
                        f"**{tier}** ({cpu} CPU, {ram} RAM). Enviando solicitud…"
                    ),
                    tool_calls=[
                        ToolCall(
                            id=f"call_{uuid.uuid4().hex[:6]}",
                            name="format_deployment_intent",
                            arguments={
                                "nombre": nombre,
                                "imagen": imagen,
                                "puerto_interno": puerto,
                                "cpu": cpu,
                                "ram": ram,
                            },
                        ),
                    ],
                )

            return AgentResponse(
                content=(
                    f"📊 Recursos recomendados: **{tier}** ({cpu} CPU, {ram} RAM).\n"
                    f"Dame el nombre del servicio, imagen y puerto para continuar."
                ),
            )

        return AgentResponse(content=f"Herramienta `{tool_name}` ejecutada.")


# ---------------------------------------------------------------------------
# OpenAI LLM Client (compatible con Ollama / LiteLLM)
# ---------------------------------------------------------------------------

class OpenAILLMClient(LLMClient):
    """
    Cliente LLM real usando la API de OpenAI.
    Compatible con Ollama local (http://localhost:11434/v1).
    """

    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        from openai import OpenAI

        self.model = model
        self.client = OpenAI(
            base_url=base_url or os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key=api_key or os.getenv("LLM_API_KEY", "ollama"),
        )

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        kwargs: dict = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0].message

        agent_response = AgentResponse(content=choice.content)

        if choice.tool_calls:
            for tc in choice.tool_calls:
                # El LLM genera los argumentos como un string JSON
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}

                agent_response.tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        return agent_response


# ---------------------------------------------------------------------------
# Orquestador del Agente (bucle ReAct)
# ---------------------------------------------------------------------------

class AgentOrchestrator:
    """
    Bucle ReAct: recibe un mensaje del usuario, interactúa con el LLM
    y ejecuta herramientas hasta obtener una respuesta final.

    Es 100 % agnóstico al proveedor de LLM gracias a la interfaz LLMClient.
    """

    def __init__(
        self,
        llm: LLMClient,
        tool_registry: dict | None = None,
        tool_definitions: list | None = None,
    ) -> None:
        self.llm = llm
        self.tool_registry = tool_registry or TOOL_REGISTRY
        self.tool_definitions = tool_definitions or TOOL_DEFINITIONS

    def run(
        self,
        user_message: str,
        history: list[dict],
        max_iterations: int = 5,
    ) -> tuple[str, list[dict]]:
        """
        Procesa un mensaje del usuario.

        Args:
            user_message: Texto del usuario.
            history: Historial de conversación (se muta in-place).
            max_iterations: Límite de iteraciones tool-calling.

        Returns:
            Tupla (respuesta_texto, historial_actualizado).
        """
        history.append({"role": "user", "content": user_message})

        for _ in range(max_iterations):
            response = self.llm.chat(history, self.tool_definitions)

            # Sin tool calls → respuesta final
            if not response.tool_calls:
                history.append({"role": "assistant", "content": response.content})
                return response.content or "", history

            # Registrar la respuesta del asistente con tool calls
            assistant_msg: dict = {
                "role": "assistant",
                "content": response.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in response.tool_calls
                ],
            }
            history.append(assistant_msg)

            # Ejecutar cada herramienta
            for tc in response.tool_calls:
                fn = self.tool_registry.get(tc.name)
                if fn is None:
                    result = {"error": f"Herramienta '{tc.name}' no encontrada"}
                else:
                    try:
                        result = fn(**tc.arguments)
                    except Exception as exc:
                        result = {"error": str(exc)}

                history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.name,
                    "content": json.dumps(result, ensure_ascii=False),
                })

        # Límite alcanzado
        fallback = "He alcanzado el límite de iteraciones. ¿Puedes reformular?"
        history.append({"role": "assistant", "content": fallback})
        return fallback, history
