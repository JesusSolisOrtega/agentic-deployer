"""
Chat interface -- Virtual Assistant of the IT Service (SIC).

Run with:
    streamlit run app/agent_layer/chat_app.py

Flow:
  1. The user describes what they need in natural language.
  2. The Agent parses and extracts parameters using the SIC system prompt.
  3. If data is missing, it asks in the chat.
  4. If it has everything, it invokes the corresponding MCP tool.
  5. Shows confirmation of sending to IT technician for review.
"""

from __future__ import annotations

import json
import os
import uuid

import streamlit as st

from app.agent_layer.agent import (
    AgentOrchestrator,
    AgentResponse,
    LLMClient,
    OpenAILLMClient,
    ToolCall,
)
from app.agent_layer.mcp_server import TOOL_DEFINITIONS, TOOL_REGISTRY

# ---------------------------------------------------------------------------
# SIC System Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "Eres el Asistente Virtual del SIC (Servicio de Informatica y Comunicaciones) "
    "de la Universidad. Atiendes solicitudes de PDI y PAS.\n\n"
    "REGLAS ESTRICTAS:\n"
    "1) NUNCA hables de Docker, puertos, CPU o RAM. Esos son detalles tecnicos internos.\n"
    "2) Si falta el nombre del proyecto o departamento, pidelo amablemente.\n"
    "3) Usa tus herramientas para solicitar el servicio y dile al usuario que "
    "un Tecnico del SIC debe validarlo antes de activarse.\n"
    "4) Si hay un error de seguridad, tranquiliza al usuario diciendo que el "
    "sistema ajustara la politica automaticamente.\n"
    "5) Se profesional pero cercano. Tutea al usuario."
)


# ---------------------------------------------------------------------------
# Fake LLM adapted to SIC (pattern matching for demo)
# ---------------------------------------------------------------------------

class SICFakeLLMClient(LLMClient):  # pragma: no cover
    """Mocked LLM with university IT rules."""

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AgentResponse:
        last = messages[-1]

        # After tool result -> summarize
        if last.get("role") == "tool":
            return self._after_tool(last)

        text = self._all_user_text(messages)

        # Detect decommissioning
        if any(k in text for k in ["baja", "borrar", "eliminar", "delete", "dar de baja"]):
            name = self._extract_service_name(text)
            if name:
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="delete_university_service",
                        arguments={"service_name": name},
                    )],
                )
            return AgentResponse(
                content="Para tramitar la baja, necesito el **nombre del servicio**. "
                "?Cual es?",
            )

        # Detect congress/event
        if any(k in text for k in ["congreso", "evento", "jornada", "conferencia", "web"]):
            name = self._extract_project_name(text)
            if name:
                traffic = "medium"
                if any(k in text for k in ["alto", "muchos", "1000", "grande"]):
                    traffic = "high"
                elif any(k in text for k in ["bajo", "pequeno", "pocos"]):
                    traffic = "low"
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="deploy_congress_web",
                        arguments={
                            "project_name": name,
                            "expected_traffic": traffic,
                        },
                    )],
                )
            return AgentResponse(
                content="Perfecto, puedo ayudarte con la web del congreso. "
                "?Como se llama el evento o proyecto?",
            )

        # Detect wordpress/department
        if any(k in text for k in ["wordpress", "departamento", "cms", "pagina departamento"]):
            name = self._extract_dept_name(text)
            if name:
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="deploy_department_cms",
                        arguments={"department_name": name},
                    )],
                )
            return AgentResponse(
                content="Puedo solicitar un WordPress para tu departamento. "
                "?Cual es el nombre del departamento?",
            )

        # Default
        return AgentResponse(
            content="Hola, soy el asistente del SIC. Puedo ayudarte con:\n\n"
            "- **Web para un congreso** o evento academico\n"
            "- **WordPress** para un departamento\n"
            "- **Dar de baja** un servicio existente\n\n"
            "?Que necesitas?",
        )

    # -- Helpers --

    def _all_user_text(self, messages: list[dict]) -> str:
        return " ".join(
            m.get("content", "") for m in messages
            if m.get("role") == "user" and m.get("content")
        ).lower()

    def _extract_project_name(self, text: str) -> str | None:
        import re
        m = re.search(
            r"(?:congreso|evento|jornada|proyecto|llamad[oa]|nombre)\s+[\"']?([\w\-]+)",
            text,
        )
        return m.group(1) if m else None

    def _extract_dept_name(self, text: str) -> str | None:
        import re
        m = re.search(
            r"(?:departamento|depto|dept)\s+(?:de\s+)?[\"']?([\w\-]+)", text,
        )
        return m.group(1) if m else None

    def _extract_service_name(self, text: str) -> str | None:
        import re
        m = re.search(
            r"(?:servicio|baja|borrar|eliminar)\s+[\"']?([\w\-]+)", text,
        )
        return m.group(1) if m else None

    def _after_tool(self, tool_msg: dict) -> AgentResponse:
        tool_name = tool_msg.get("name", "")
        result = json.loads(tool_msg.get("content", "{}"))
        deploy_id = result.get("id", "???")

        if "delete" in tool_name:
            return AgentResponse(
                content=(
                    f"He registrado la solicitud de baja.\n\n"
                    f"- **ID:** `{deploy_id}`\n"
                    f"- **Estado:** Pendiente de aprobacion\n\n"
                    f"Un tecnico del SIC revisara la solicitud en breve."
                ),
            )

        return AgentResponse(
            content=(
                f"Tu solicitud ha sido enviada correctamente.\n\n"
                f"- **ID:** `{deploy_id}`\n"
                f"- **Estado:** Pendiente de aprobacion\n\n"
                f"Un tecnico del SIC debe validarla antes de que se active. "
                f"Te notificaremos cuando este disponible."
            ),
        )


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="SIC -- Asistente de Servicios",
    page_icon="🏛️",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .suggestion-btn {
        display: inline-block; padding: 8px 16px; margin: 4px;
        border-radius: 20px; font-size: 13px; cursor: pointer;
        background: #222632; border: 1px solid #2e3348; color: #e4e6ef;
        transition: all 0.2s ease;
    }
    .suggestion-btn:hover { border-color: #6c63ff; background: #2a2f3e; }
</style>
""", unsafe_allow_html=True)

# -- Session state --
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]
if "agent" not in st.session_state:
    provider = os.getenv("LLM_PROVIDER", "fake").lower()

    llm: LLMClient
    if provider == "ollama":
        llm = OpenAILLMClient(model="llama3.1", base_url="http://localhost:11434/v1", api_key="ollama")
    elif provider == "openai":
        llm = OpenAILLMClient(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY", ""))
    else:
        llm = SICFakeLLMClient()

    st.session_state.agent = AgentOrchestrator(
        llm=llm,
        tool_registry=TOOL_REGISTRY,
        tool_definitions=TOOL_DEFINITIONS,
    )

# -- Header --
st.markdown("### 🏛️ Asistente del SIC -- Universidad")
st.caption("Servicio de Informatica y Comunicaciones")

# -- Suggestion buttons --
cols = st.columns(3)
suggestions = [
    ("🌐 Web para Congreso", "Necesito una web para un congreso de investigacion"),
    ("📝 WordPress Departamento", "Necesito un WordPress para mi departamento"),
    ("🗑️ Dar de baja servicio", "Quiero dar de baja un servicio"),
]
for col, (label, prompt) in zip(cols, suggestions, strict=True):
    if col.button(label, use_container_width=True):
        st.session_state.pending_prompt = prompt

# -- Chat history --
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -- Input --
user_input = st.chat_input("Escribe tu solicitud...")

# Handle suggestion button click
if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt
    del st.session_state.pending_prompt

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Procesando solicitud..."):
            try:
                response_text, st.session_state.history = st.session_state.agent.run(
                    user_message=user_input,
                    history=st.session_state.history,
                )
            except Exception as exc:
                response_text = (
                    f"Lo siento, ha habido un problema tecnico: `{exc}`\n\n"
                    "Asegurate de que el backend del SIC esta operativo."
                )
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
