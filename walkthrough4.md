# Agent Layer — LLM + MCP Tools + Chat

## Archivos creados

| Archivo | Descripción |
|---------|-------------|
| [tools.py](file:///home/jesus/projects/TFM/app/agent_layer/tools.py) | `calculate_optimal_resources` + `format_deployment_intent` + definiciones OpenAI |
| [agent.py](file:///home/jesus/projects/TFM/app/agent_layer/agent.py) | `LLMClient` (ABC), `FakeLLMClient` (demo), `AgentOrchestrator` (bucle ReAct) |
| [chat_app.py](file:///home/jesus/projects/TFM/app/agent_layer/chat_app.py) | Interfaz Streamlit para usuario no técnico |
| [test_agent.py](file:///home/jesus/projects/TFM/app/tests/test_agent.py) | 15 tests (11 unitarios + 4 integración con mock) |

## Tests — 23/23 ✅ — 98.2% cobertura

```
test_agent.py  — 11 boundary tests para calculate_optimal_resources
               — 4 tests de integración con Mock LLM:
                 • tool call → deployment (mock HTTP)
                 • chained: calculate_resources → deploy
                 • unknown tool → graceful error
                 • max_iterations → prevents infinite loop

test_security.py — 4 PBT con hypothesis
test_use_cases.py — 4 tests unitarios del caso de uso
```

## Comandos

```bash
# Instalar Streamlit
.venv/bin/pip install streamlit

# Ejecutar tests del agente
.venv/bin/python -m pytest app/tests/test_agent.py -v --no-cov

# Ejecutar TODOS los tests con cobertura
.venv/bin/python -m pytest app/tests/ -v

# Lanzar el chat (requiere backend en puerto 8000)
.venv/bin/uvicorn app.infrastructure.main:app --port 8000 &
.venv/bin/streamlit run app/agent_layer/chat_app.py
```
