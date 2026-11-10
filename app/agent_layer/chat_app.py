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
import re
import sys
import uuid
from pathlib import Path

# Ensure project root is in sys.path when launched via 'streamlit run'
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
import streamlit as st

from app.agent_layer.agent import (
    AgentOrchestrator,
    AgentResponse,
    LLMClient,
    OllamaLLMClient,
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
    "3) Cuando uses una herramienta de despliegue o baja, indica SIEMPRE de forma clara el "
    "identificador generado (ej. **ID:** `abc12345`) y recuerda al usuario que un Técnico del SIC debe validarlo.\n"
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

        user_msgs = [m for m in messages if m.get("role") == "user" and m.get("content")]
        if not user_msgs:
            return AgentResponse(content="Hola, ¿en qué puedo ayudarte?")

        current_text = user_msgs[-1]["content"].lower()
        all_text = " ".join(m["content"] for m in user_msgs).lower()
        last_assistant_msg = next(
            (m["content"].lower() for m in reversed(messages) if m.get("role") == "assistant" and m.get("content")),
            "",
        )

        # 1. Detect status query (ONLY if the current user message explicitly asks for it)
        if any(k in current_text for k in ["estado", "status", "consultar", "cómo va", "como va"]):
            import re
            m = re.search(r"([a-f0-9]{8}|dep-[a-f0-9]{7,8})", current_text)
            if m:
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="get_deployment_status",
                        arguments={"deployment_id": m.group(1)},
                    )],
                )
            return AgentResponse(
                content="Para consultar el estado de una solicitud, por favor indícame su **ID** (ejemplo: `consultar estado a1b2c3d4`).",
            )

        # 2. Detect decommissioning
        is_delete = any(k in current_text for k in ["baja", "borrar", "eliminar", "delete", "dar de baja"])
        waiting_delete_name = "nombre del servicio" in last_assistant_msg

        if is_delete or waiting_delete_name:
            name = self._extract_service_name(current_text)
            if not name and waiting_delete_name:
                name = self._extract_service_name(all_text) or self._extract_quoted_or_word(current_text, [r"([\w\-]+)"])
            if name:
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="delete_university_service",
                        arguments={"service_name": name},
                    )],
                )
            return AgentResponse(
                content="Para tramitar la baja, necesito el **nombre del servicio** a retirar. ¿Cuál es el nombre del servicio?",
            )

        # 3. Detect congress/event
        is_congress = any(k in current_text for k in ["congreso", "evento", "jornada", "conferencia"])
        waiting_congress_name = "llama el evento" in last_assistant_msg

        if is_congress or waiting_congress_name:
            name = self._extract_project_name(current_text)
            if not name and waiting_congress_name:
                name = self._extract_project_name(all_text) or self._extract_quoted_or_word(current_text, [r"([\w\-]+)"])
            if name:
                traffic = "medium"
                if any(k in current_text or k in all_text for k in ["alto", "muchos", "1000", "grande"]):
                    traffic = "high"
                elif any(k in current_text or k in all_text for k in ["bajo", "pequeno", "pequeño", "pocos"]):
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
                content="Perfecto, puedo tramitar el despliegue de la web del congreso. ¿Cómo se llama el evento o proyecto?",
            )

        # 4. Detect wordpress/department
        is_cms = any(k in current_text for k in ["wordpress", "cms", "pagina departamento"])
        waiting_cms_name = "nombre del departamento" in last_assistant_msg

        if is_cms or waiting_cms_name:
            name = self._extract_dept_name(current_text)
            if not name and waiting_cms_name:
                name = self._extract_dept_name(all_text) or self._extract_quoted_or_word(current_text, [r"([\w\-]+)"])
            if name:
                return AgentResponse(
                    tool_calls=[ToolCall(
                        id=f"call_{uuid.uuid4().hex[:6]}",
                        name="deploy_department_cms",
                        arguments={"department_name": name},
                    )],
                )
            return AgentResponse(
                content="Puedo solicitar un WordPress institucional para tu departamento. ¿Cuál es el nombre del departamento?",
            )

        # 5. Detect generic python application
        if any(k in current_text for k in ["python", "fastapi", "api", "backend"]):
            name = self._extract_quoted_or_word(
                current_text,
                [r"(?:app|api|aplicacion|proyecto|servicio)\s+(?:de\s+|para\s+|del\s+)?[\"']?([\w\-]+)"],
            ) or "api-investigacion"
            return AgentResponse(
                tool_calls=[ToolCall(
                    id=f"call_{uuid.uuid4().hex[:6]}",
                    name="deploy_python_app",
                    arguments={"project_name": name, "python_version": "3.12"},
                )],
            )

        # 6. Detect database
        if any(k in current_text for k in ["base de datos", "bbdd", "database", "postgres", "postgresql", "mysql", "redis"]):
            db = "postgres"
            if "mysql" in current_text:
                db = "mysql"
            elif "redis" in current_text:
                db = "redis"
            return AgentResponse(
                tool_calls=[ToolCall(
                    id=f"call_{uuid.uuid4().hex[:6]}",
                    name="deploy_database",
                    arguments={
                        "db_type": db,
                        "version": "15" if db == "postgres" else "8.0" if db == "mysql" else "7.0",
                        "storage_gb": 10,
                    },
                )],
            )

        # 7. Detect generic static website
        if any(k in current_text for k in ["web estatica", "estática", "html", "landing"]):
            name = self._extract_quoted_or_word(
                current_text,
                [r"(?:web|sitio|pagina|portal)\s+(?:de\s+|para\s+|del\s+)?[\"']?([\w\-]+)"],
            ) or "web-institucional"
            return AgentResponse(
                tool_calls=[ToolCall(
                    id=f"call_{uuid.uuid4().hex[:6]}",
                    name="deploy_static_website",
                    arguments={"project_name": name, "domain": f"{name}.us.es"},
                )],
            )

        # 8. Greetings / help
        if any(k in current_text for k in ["hola", "buenos dias", "buenas", "ayuda", "que puedes hacer", "gracias"]):
            return AgentResponse(
                content="¡Hola! Soy el asistente virtual del SIC. Puedo ayudarte con las siguientes gestiones:\n\n"
                "- **Web para congreso o evento académico**\n"
                "- **WordPress institucional para tu departamento**\n"
                "- **Despliegue de API o aplicación en Python**\n"
                "- **Base de datos gestionada** (PostgreSQL, MySQL o Redis)\n"
                "- **Baja de servicios existentes**\n"
                "- **Consulta del estado de solicitudes** (indicando su ID)\n\n"
                "¿Qué necesitas tramitar hoy?",
            )

        # Default fallback
        return AgentResponse(
            content="Hola, soy el asistente del SIC. Puedo ayudarte a tramitar:\n\n"
            "- **Web para congreso o evento académico** (ej. *'Web para congreso IA-2025'*)\n"
            "- **WordPress institucional para departamento** (ej. *'WordPress para informática'*)\n"
            "- **API o aplicación Python** (ej. *'Desplegar API Python para notas'*)\n"
            "- **Base de datos gestionada** (PostgreSQL, MySQL o Redis con volumen persistente)\n"
            "- **Baja o desmantelamiento de servicios** (ej. *'Dar de baja servicio web-antigua'*)\n"
            "- **Consulta de estado** de solicitudes anteriores indicando el ID\n\n"
            "¿Qué servicio necesitas gestionar?",
        )

    # -- Helpers --

    def _all_user_text(self, messages: list[dict]) -> str:
        # pyrefly: ignore [no-any-return-implicit]
        return " ".join(
            m.get("content", "") for m in messages
            if m.get("role") == "user" and m.get("content")
        ).lower()

    def _extract_quoted_or_word(self, text: str, patterns: list[str]) -> str | None:
        import re
        m_quote = re.search(r"['\"]([\w\-]+)['\"]", text)
        if m_quote:
            return m_quote.group(1)
        for pattern in patterns:
            m = re.search(pattern, text)
            if m:
                val = m.group(1).lower()
                if val not in ("de", "para", "un", "una", "el", "la", "los", "las", "mi", "mis", "servicio", "investigacion"):
                    return val
        return None

    def _extract_project_name(self, text: str) -> str | None:
        return self._extract_quoted_or_word(
            text,
            [
                r"(?:congreso|evento|jornada|proyecto|llamad[oa]|nombre)\s+(?:de\s+|para\s+|del\s+)?[\"']?([\w\-]+)",
            ],
        )

    def _extract_dept_name(self, text: str) -> str | None:
        return self._extract_quoted_or_word(
            text,
            [
                r"(?:departamento|depto|dept)\s+(?:de\s+)?[\"']?([\w\-]+)",
            ],
        )

    def _extract_service_name(self, text: str) -> str | None:
        return self._extract_quoted_or_word(
            text,
            [
                r"(?:servicio)\s+[\"']?([\w\-]+)",
                r"(?:baja|borrar|eliminar)\s+(?:de\s+|del\s+|el\s+)?(?:servicio\s+)?[\"']?([\w\-]+)",
            ],
        )

    def _after_tool(self, tool_msg: dict) -> AgentResponse:
        tool_name = tool_msg.get("name", "")
        result = json.loads(tool_msg.get("content", "{}"))

        if "error" in result:
            return AgentResponse(
                content=(
                    f"⚠️ **La solicitud no pudo procesarse debido a una restricción de seguridad o técnica:**\n\n"
                    f"`{result['error']}`\n\n"
                    "Por favor, verifica los parámetros o contacta con el soporte técnico del SIC."
                ),
            )

        if tool_name == "get_deployment_status":
            return AgentResponse(
                content=(
                    f"📊 **Estado del Despliegue `{result.get('id', '')}`:**\n\n"
                    f"- **Servicio:** `{result.get('name', 'N/D')}`\n"
                    f"- **Estado actual:** `{result.get('status', 'DESCONOCIDO')}`\n"
                    f"- **Imagen:** `{result.get('image', 'N/D')}`\n"
                    f"- **Puerto interno:** `{result.get('port', 'N/D')}`\n"
                    f"- **Detalle:** {result.get('message', '')}"
                ),
            )

        deploy_id = result.get("id", "???")

        if "delete" in tool_name:
            return AgentResponse(
                content=(
                    f"He registrado la solicitud de baja en el clúster.\n\n"
                    f"- **ID de Solicitud:** `{deploy_id}`\n"
                    f"- **Estado:** `PENDING_APPROVAL` (Pendiente de aprobación técnica)\n\n"
                    f"Un técnico del SIC revisará la solicitud antes de desmantelar el pod. "
                    f"Puedes seguir la resolución en tiempo real desde el panel inferior 'Mis Solicitudes Pendientes'."
                ),
            )

        return AgentResponse(
            content=(
                f"Tu solicitud de despliegue ha sido registrada correctamente.\n\n"
                f"- **ID de Solicitud:** `{deploy_id}`\n"
                f"- **Estado:** `PENDING_APPROVAL` (Pendiente de validación)\n\n"
                f"Un técnico del SIC validará la intención en la consola de supervisión antes de aplicarla en OpenShift. "
                f"Puedes consultar el estado en tiempo real en el panel inferior 'Mis Solicitudes Pendientes' pulsando '🔄 Actualizar'."
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
# pending_deployments: list of {id, name} for deployments awaiting HITL decision
if "pending_deployments" not in st.session_state:
    st.session_state.pending_deployments = []
if "agent" not in st.session_state:
    provider = os.getenv("LLM_PROVIDER", "fake").lower()

    llm: LLMClient
    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        llm = OllamaLLMClient(model=model, host=host)
    elif provider == "openai":
        llm = OpenAILLMClient(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY", ""))
    elif provider == "gemini":
        llm = OpenAILLMClient(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=os.getenv("GEMINI_API_KEY", ""),
        )
    else:
        llm = SICFakeLLMClient()

    st.session_state.agent = AgentOrchestrator(
        llm=llm,
        tool_registry=TOOL_REGISTRY,
        tool_definitions=TOOL_DEFINITIONS,
    )

# -- Header --
provider_label = {
    "ollama": f"🤖 LLM Soberano · Ollama ({os.getenv('OLLAMA_MODEL', 'qwen2.5:7b')})",
    "openai": f"🌐 OpenAI · {os.getenv('OPENAI_MODEL', 'GPT-4o-mini')}",
    "gemini": f"✨ Google Gemini · {os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')}",
    "fake": "⚡ Orquestador SIC · Motor ReAct Local",
}.get(os.getenv("LLM_PROVIDER", "fake").lower(), "⚡ Orquestador SIC")

st.markdown("### 🏛️ Asistente del SIC — Universidad")
st.caption(f"Servicio de Informática y Comunicaciones · {provider_label}")

# -- Suggestion buttons --
cols = st.columns(3)
suggestions = [
    ("🌐 Web para Congreso", "Necesito una web para el congreso 'congreso-ia-2025' con tráfico medio"),
    ("📝 WordPress Departamento", "Necesito un WordPress para el departamento de informatica"),
    ("🗑️ Dar de baja servicio", "Quiero dar de baja el servicio web-antigua"),
]
for col, (label, prompt) in zip(cols, suggestions, strict=True):
    if col.button(label, use_container_width=True):
        st.session_state.pending_prompt = prompt

st.caption("💡 *Sugerencias rápidas para demo. También puedes pedir en lenguaje natural bases de datos, APIs en Python o consultar estados.*")

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
                    f"Lo siento, ha habido un problema técnico: `{exc}`\n\n"
                    "Asegúrate de que el backend del SIC está operativo."
                )
        st.markdown(response_text)

    # -- Extract deployment ID directly from tool results in conversation history --
    for msg in reversed(st.session_state.history):
        if msg.get("role") == "tool":
            try:
                tool_data = json.loads(msg.get("content", "{}"))
                _dep_id = tool_data.get("id")
                _status = tool_data.get("status", "")
                if _dep_id and "PENDING" in _status.upper():
                    if not any(d["id"] == _dep_id for d in st.session_state.pending_deployments):
                        st.session_state.pending_deployments.append({"id": _dep_id, "name": _dep_id})
                    break
            except Exception:
                pass

    # Fallback: search in natural language response text
    if not st.session_state.pending_deployments:
        _id_match = re.search(r"(?:ID(?: de Solicitud)?:\*\*\s*`?)([a-f0-9]{8})`?", response_text, re.IGNORECASE)
        if not _id_match:
            _id_match = re.search(r"\b([a-f0-9]{8}|dep-[a-f0-9]{7,8})\b", response_text)
        if _id_match:
            _dep_id = _id_match.group(1) if _id_match.lastindex else _id_match.group(0)
            if not any(d["id"] == _dep_id for d in st.session_state.pending_deployments):
                st.session_state.pending_deployments.append({"id": _dep_id, "name": _dep_id})

    st.session_state.messages.append({"role": "assistant", "content": response_text})


# ---------------------------------------------------------------------------
# Researcher notification panel — HITL status feedback
# ---------------------------------------------------------------------------

_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

_STATUS_ICONS = {
    "PENDING_APPROVAL": "⏳",
    "APPROVED": "🔄",
    "DEPLOYED": "✅",
    "REJECTED": "❌",
    "FAILED": "🚨",
}
_STATUS_COLORS = {
    "PENDING_APPROVAL": "#f0ad4e",
    "APPROVED": "#5bc0de",
    "DEPLOYED": "#5cb85c",
    "REJECTED": "#d9534f",
    "FAILED": "#d9534f",
}

if st.session_state.pending_deployments:
    st.divider()
    st.markdown("#### 📬 Mis Solicitudes Pendientes")
    st.caption("Pulsa '🔄 Actualizar' para consultar si el técnico del SIC ha tomado una decisión.")

    _resolved = []
    for _dep in st.session_state.pending_deployments:
        with st.container():
            _col1, _col2 = st.columns([4, 1])
            with _col1:
                st.markdown(f"**ID:** `{_dep['id']}`")
            with _col2:
                if st.button("🔄 Actualizar", key=f"status_{_dep['id']}"):
                    try:
                        _resp = requests.get(
                            f"{_BACKEND_URL}/hitl/status/{_dep['id']}",
                            timeout=5,
                        )
                        if _resp.status_code == 200:
                            _data = _resp.json()
                            _s = _data["status"]
                            _icon = _STATUS_ICONS.get(_s, "❓")
                            _color = _STATUS_COLORS.get(_s, "#aaa")
                            _msg = _data["message"]
                            st.markdown(
                                f"<div style='padding:8px;border-radius:6px;"
                                f"border-left:4px solid {_color};background:#1e2130'>"
                                f"<b>{_icon} {_s}</b><br><small>{_msg}</small></div>",
                                unsafe_allow_html=True,
                            )
                            # Remove from pending list if terminal state
                            if _s in ("DEPLOYED", "REJECTED", "FAILED"):
                                _resolved.append(_dep["id"])
                                _notification = {
                                    "DEPLOYED": f"✅ Tu servicio `{_dep['id']}` ha sido **desplegado exitosamente**.",
                                    "REJECTED": f"❌ Tu solicitud `{_dep['id']}` fue **rechazada** por el técnico. Contacta con el SIC.",
                                    "FAILED": f"🚨 El despliegue `{_dep['id']}` encontró un error técnico. El equipo SIC ha sido notificado.",
                                }[_s]
                                st.session_state.messages.append(
                                    {"role": "assistant", "content": _notification}
                                )
                        else:
                            st.warning(f"No se encontró el deployment `{_dep['id']}`")
                    except requests.exceptions.ConnectionError:
                        st.error("No se puede conectar con el backend del SIC. ¿Está en marcha?")

    # Remove resolved deployments from tracking list
    st.session_state.pending_deployments = [
        d for d in st.session_state.pending_deployments if d["id"] not in _resolved
    ]
