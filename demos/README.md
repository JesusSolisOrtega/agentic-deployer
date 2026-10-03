# demos/ — Artefactos de Evidencia Empírica

Este directorio contiene los artefactos generados durante la ejecución real del *Agentic Deployer* con el modelo `qwen2.5:7b` vía Ollama. Constituyen la evidencia empírica referenciada en el **Capítulo 8** de la memoria.

---

## Estructura

```
demos/
├── session_logs/         # Transcripciones completas de sesiones de chat (JSON)
│   ├── escenario1_happy_path.json       # Escenario 1: Happy Path (congreso IA)
│   ├── escenario2_prompt_injection.json # Escenario 2: Prompt Injection → HTTP 422
│   ├── escenario3_hitl_completo.json    # Escenario 3: Ciclo HITL completo
│   └── escenario4_autocorreccion.json   # Escenario 4: Autocorrección del LLM
│
└── outputs/              # Manifiestos YAML generados por FakeK8sAdapter
    └── dep-7f3a2c1b_congreso-ia-departamento.yaml
```

## Escenarios

| # | Escenario | Resultado | Referencia en Memoria |
|---|---|---|---|
| 1 | Happy Path — Portal web congreso IA | `PENDING_APPROVAL` → `DEPLOYED` | Cap. 8.3.1 |
| 2 | Prompt Injection — Ubuntu:latest puerto 22 | `HTTP 422` → Autocorrección LLM | Cap. 8.2 / 8.3.2 |
| 3 | Ciclo HITL completo — CMS WordPress | Aprobación en Dashboard | Cap. 8.3.3 |
| 4 | Autocorrección Multiturno (BBDD sin disco) | `HTTP 422` → Reintento con storage | Cap. 8.3.5 |

## Reproducibilidad

Para garantizar el rigor académico y demostrar que los logs no han sido generados a mano, se provee un script de evaluación automatizada. Este script recrea los prompts de la memoria contra la API de Ollama y el backend FastAPI, documentando la conversación en formato JSON.

### Ejecución Automática (Recomendada)

```bash
# 1. Arrancar el backend (requerido para que el LLM pruebe las herramientas)
uvicorn app.infrastructure.main:app --port 8000 &

# 2. Asegurarse de tener Ollama corriendo con el modelo
ollama serve &
ollama pull qwen2.5:7b

# 3. Lanzar el script de reproducibilidad
PYTHONPATH=. python3 scripts/generate_demos.py
```

### Ejecución Manual (Frontend)
También se puede reproducir interactivamente levantando la interfaz:
```bash
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
```
