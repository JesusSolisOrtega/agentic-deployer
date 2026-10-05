"""
LLM Agent Orchestrator.

Decouples the orchestration logic (tool-calling loop) from the concrete
LLM client, making it 100% testable with mocks.

Components:
  - ToolCall / AgentResponse: communication dataclasses.
  - LLMClient (ABC): interface that any provider must implement.
  - FakeLLMClient: simulation without API key for dev and demo.
  - OllamaLLMClient: native Ollama client (free, local, zero data retention).
  - OpenAILLMClient: OpenAI API client (also compatible with Ollama /v1).
  - AgentOrchestrator: ReAct (Reason + Act) loop that executes tools.

Provider selection (LLM_PROVIDER env var):
  - 'fake'   → FakeLLMClient (no API key required)
  - 'ollama' → OllamaLLMClient (requires local Ollama server)
  - 'openai' → OpenAILLMClient (requires OPENAI_API_KEY)
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
    """Represents a tool invocation requested by the LLM."""

    id: str
    name: str
    arguments: dict


@dataclass
class AgentResponse:
    """LLM Response: free text and/or tool calls."""

    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)


# ---------------------------------------------------------------------------
# LLM Client — Abstract Interface
# ---------------------------------------------------------------------------

class LLMClient(ABC):
    """
    Contract for any LLM client (OpenAI, LiteLLM, Ollama...).
    Receives messages + tools, returns an AgentResponse.
    """

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        ...


# ---------------------------------------------------------------------------
# Fake LLM — Rule-based simulation for demo
# ---------------------------------------------------------------------------

class FakeLLMClient(LLMClient):  # pragma: no cover
    """
    Mocked LLM client that uses pattern-matching to extract
    deployment parameters from the user's text.

    Perfect for local development and demos without an API key.
    """

    SYSTEM_PROMPT = (
        "You are a deployment assistant. You help teams "
        "request deployments in the OKD cluster easily."
    )

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        last = messages[-1]

        # ── After executing a tool -> summarize result ────
        if last.get("role") == "tool":
            return self._summarize_tool_result(last, messages)

        # ── User message -> extract parameters ────────────────────
        params = self._extract_params_from_history(messages)
        name = params.get("name")
        image = params.get("image")
        port = params.get("internal_port")
        users = params.get("users")

        # If there are users but we haven't calculated resources -> calculate
        if users and not self._has_resource_result(messages):
            return AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="calculate_optimal_resources",
                        arguments={"users": users},
                    ),
                ],
            )

        # If we have name + image + port -> deploy
        if name and image and port:
            cpu = params.get("cpu", "250m")
            ram = params.get("ram", "128Mi")
            return AgentResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="format_deployment_intent",
                        arguments={
                            "name": name,
                            "image": image,
                            "internal_port": port,
                            "cpu": cpu,
                            "ram": ram,
                        },
                    ),
                ],
            )

        # Missing data -> ask
        missing = []
        if not name:
            missing.append("the **name** of the service")
        if not image:
            missing.append("the container **image** (e.g. `nginx:1.25.3`)")
        if not port:
            missing.append("the internal **port**")

        return AgentResponse(
            content=(
                "I need some more information to prepare the deployment:\n"
                + "\n".join(f"- {m}" for m in missing)
                + "\n\nCould you provide them?"
            ),
        )

    # ── Private helpers ───────────────────────────────────────────────

    def _extract_params_from_history(self, messages: list[dict]) -> dict:
        """Extracts deployment parameters from all user messages."""
        all_text = " ".join(
            m.get("content", "")
            for m in messages
            if m.get("role") == "user" and m.get("content")
        ).lower()

        params: dict = {}

        # Image: word:tag or word/word:tag (exclude :latest-like that doesn't look like image)
        img_match = re.search(r"([\w\-]+(?:/[\w\-]+)?:[\w\.\-]+)", all_text)
        if img_match:
            params["image"] = img_match.group(1)

        # Port: number after "puerto" (we keep "puerto" since the UI is in Spanish)
        port_match = re.search(r"(?:puerto|port)\s+(\d+)", all_text)
        if port_match:
            params["internal_port"] = int(port_match.group(1))

        # Service name
        # Try explicit naming first
        name_match = re.search(r"(?:llamad[oa]|nombre de|nombre|name)[\s:\"']+([\w\-]+)", all_text)
        if not name_match:
            # Fallback to general verbs
            name_match = re.search(r"(?:servicio|desplegar|deploy)[\s:\"']+([\w\-]+)", all_text)

        if name_match:
            val = name_match.group(1)
            if val in ("un", "una", "el", "la", "a", "an", "the"):
                # fallback attempt, match after the stop word
                name_match2 = re.search(rf"{val}\s+([\w\-]+)", all_text[name_match.end(0)-len(val)-1:])
                if name_match2:
                    params["name"] = name_match2.group(1)
            else:
                params["name"] = val

        # Users
        users_match = re.search(r"(\d+)\s*usuarios", all_text)
        if users_match:
            params["users"] = int(users_match.group(1))

        # If resources are calculated, inject them
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
                    f"✅ **Request sent for review.**\n\n"
                    f"- **ID:** `{deploy_id}`\n"
                    f"- **Status:** Pending approval\n\n"
                    f"An IT technician will review it in the "
                    f"[HITL dashboard](http://localhost:8000/frontend/index.html)."
                ),
            )

        if tool_name == "calculate_optimal_resources":
            tier = result.get("tier", "")
            cpu = result.get("cpu", "")
            ram = result.get("ram", "")
            # Continue with deployment -> re-parse history
            params = self._extract_params_from_history(messages)
            name = params.get("name")
            image = params.get("image")
            port = params.get("internal_port")

            if name and image and port:
                return AgentResponse(
                    content=(
                        f"📊 For your volume of users I recommend tier "
                        f"**{tier}** ({cpu} CPU, {ram} RAM). Sending request..."
                    ),
                    tool_calls=[
                        ToolCall(
                            id=f"call_{uuid.uuid4().hex[:6]}",
                            name="format_deployment_intent",
                            arguments={
                                "name": name,
                                "image": image,
                                "internal_port": port,
                                "cpu": cpu,
                                "ram": ram,
                            },
                        ),
                    ],
                )

            return AgentResponse(
                content=(
                    f"📊 Recommended resources: **{tier}** ({cpu} CPU, {ram} RAM).\n"
                    f"Give me the service name, image, and port to continue."
                ),
            )

        return AgentResponse(content=f"Tool `{tool_name}` executed.")


# ---------------------------------------------------------------------------
# OpenAI LLM Client (compatible with Ollama / LiteLLM)
# ---------------------------------------------------------------------------

class OpenAILLMClient(LLMClient):  # pragma: no cover
    """
    Real LLM client using the OpenAI API.
    Compatible with local Ollama (http://localhost:11434/v1).
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

        import time
        if "gemini" in self.model.lower():
            # Evitar Rate Limit de 5 RPM en la cuota gratuita de Google AI Studio
            time.sleep(15)
        elif "llama" in self.model.lower() and "groq" in str(getattr(self.client, "base_url", "")):
            # Evitar Rate Limit de 30 RPM en la cuota gratuita de Groq
            time.sleep(2)
        elif "mistral.ai" in str(getattr(self.client, "base_url", "")):
            # Evitar Rate Limit estricto de la cuota gratuita de Mistral ("Le Free Tier")
            time.sleep(5)

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0].message

        agent_response = AgentResponse(content=choice.content)

        if choice.tool_calls:
            for tc in choice.tool_calls:
                # The LLM generates the arguments as a JSON string
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
# LiteLLM Client — Universal Interface
# ---------------------------------------------------------------------------

class LiteLLMClient(LLMClient):  # pragma: no cover
    """
    Client using litellm to support any provider (Cohere, Anthropic, etc).
    """

    def __init__(
        self,
        model: str,
    ):
        self.model = model

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        import litellm

        kwargs: dict = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        import time
        if "command-r" in self.model.lower():
            time.sleep(2) # rate limit prevention

        response = litellm.completion(**kwargs)
        choice = response.choices[0].message

        agent_response = AgentResponse(content=choice.content)

        if choice.tool_calls:
            for tc in choice.tool_calls:
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
# Ollama LLM Client — Native SDK (free, local, zero data retention)
# ---------------------------------------------------------------------------

class OllamaLLMClient(LLMClient):  # pragma: no cover
    """
    Native Ollama client using the official `ollama` Python SDK.

    Recommended for institutional environments (universities, public sector)
    where data sovereignty (Zero Data Retention) is mandatory.

    Requires a running Ollama server:
        ollama serve                    # Start server
        ollama pull qwen2.5:14b         # Download model (recommended)
        ollama pull llama3.1            # Alternative with tool_calls support

    Recommended models with native tool_calls support by tier:
        - [Basic]        qwen2.5:7b    (8 GB VRAM, good for testing/MVP)
        - [Intermediate] qwen2.5:14b   (16 GB VRAM, optimal balance of speed & reliability)
        - [Enterprise]   qwen2.5:32b   (24 GB VRAM, high reliability, production-grade)
        - [Enterprise]   llama3.1:70b  (48 GB VRAM, maximum reasoning capacity)

    NOT recommended (tested but prone to cognitive collapse in ReAct loops):
        - llama3.1:8b   (Frequent JSON schema violations under stress)
        - mistral:7b    (Attention dilution in multi-turn conversations)
    """

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
    ) -> None:
        try:
            import ollama as _ollama
            self._ollama = _ollama
        except ImportError as exc:
            raise ImportError(
                "The 'ollama' package is required. Install it with: "
                "pip install ollama"
            ) from exc

        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        """
        Sends messages to Ollama and returns an AgentResponse.

        Converts OpenAI-format tool definitions to Ollama-compatible format
        and maps the response back to the common AgentResponse dataclass.
        """
        client = self._ollama.Client(host=self.host)

        # Ollama accepts OpenAI-compatible tool definitions directly
        kwargs: dict = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = client.chat(**kwargs)
        message = response.message

        agent_response = AgentResponse(content=message.content or None)

        # Map Ollama tool calls → ToolCall dataclass
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = dict(tc.function.arguments) if tc.function.arguments else {}
                except (TypeError, AttributeError):
                    args = {}

                agent_response.tool_calls.append(
                    ToolCall(
                        id=f"ollama_{uuid.uuid4().hex[:8]}",
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        return agent_response


# ---------------------------------------------------------------------------
# Agent Orchestrator (ReAct loop)
# ---------------------------------------------------------------------------

class AgentOrchestrator:
    """
    ReAct loop: receives a user message, interacts with the LLM
    and executes tools until a final response is obtained.

    It is 100% LLM provider agnostic thanks to the LLMClient interface.
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
        Processes a user message.

        Args:
            user_message: User text.
            history: Conversation history (mutated in-place).
            max_iterations: Tool-calling iterations limit.

        Returns:
            Tuple (text_response, updated_history).
        """
        import copy
        import os

        history.append({"role": "user", "content": user_message})

        for _ in range(max_iterations):
            # Evaluate reinforcement suffix
            use_suffix = os.getenv("USE_REINFORCEMENT_SUFFIX", "false").lower() == "true"
            chat_history = history

            if use_suffix:
                # We copy the history to avoid modifying the real conversation state
                chat_history = copy.deepcopy(history)
                # Find the last user message and append the suffix
                for msg in reversed(chat_history):
                    if msg["role"] == "user":
                        msg["content"] += (
                            "\n\n[SYSTEM DIRECTIVE: 1) First, explicitly list the parameters you have gathered so far (Project Name, Docker Image, Port). "
                            "2) If any is missing, you MUST NOT invoke the tool; just ask the user for it. "
                            "3) ONLY if you have gathered all three parameters, invoke the tool.]"
                        )
                        break

            response = self.llm.chat(chat_history, self.tool_definitions)

            # No tool calls -> final response
            if not response.tool_calls:
                history.append({"role": "assistant", "content": response.content})
                return response.content or "", history

            # Register the assistant's response with tool calls
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

            # Execute each tool
            for tc in response.tool_calls:
                fn = self.tool_registry.get(tc.name)
                if fn is None:
                    result = {"error": f"Tool '{tc.name}' not found"}
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

        # Limit reached
        fallback = "Iteration limit reached. Could you rephrase?"
        history.append({"role": "assistant", "content": fallback})
        return fallback, history
