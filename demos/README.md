# demos/ — Artefactos de Evidencia Empírica

Este directorio contiene los artefactos generados durante la ejecución real del *Agentic Deployer* con el modelo `qwen2.5:7b` vía Ollama. Constituyen la evidencia empírica referenciada en el **Capítulo 8** de la memoria.

---

## Estructura

```
demos/
├── session_logs/         # Transcripciones completas de sesiones de chat (JSON)
│   ├── escenario1_happy_path.json       # Escenario 1: Happy Path (congreso IA)
│   └── escenario3_hitl_completo.json    # Escenario 3: Ciclo HITL completo
│
├── prompt_injection/     # Escenarios adversariales y de seguridad
│   └── escenario2_prompt_injection.json # Escenario 2: Prompt Injection → HTTP 422
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

## Reproducibilidad

Para reproducir estos escenarios en local:

```bash
# 1. Arrancar el backend
uvicorn app.infrastructure.main:app --reload --port 8000

# 2. Arrancar Ollama con el modelo adecuado
ollama serve
ollama pull qwen2.5:7b

# 3. Arrancar el chat con Ollama
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
```
