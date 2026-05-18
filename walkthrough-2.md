# MVP Middleware Orquestador — HITL + MCP

## Estructura final

```
TFM/
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py                          # Re-export de conveniencia
│   ├── domain/
│   │   ├── models.py                    # DeploymentIntent, DeploymentRecord, DeploymentStatus
│   │   ├── ports.py                     # DeployPort (ABC)
│   │   └── exceptions.py               # SecurityViolationError
│   ├── application/
│   │   ├── security_validator.py        # SecurityContextValidator (lógica pura)
│   │   └── use_cases.py                 # ProcessDeploymentUseCase + deployment_store
│   ├── infrastructure/
│   │   ├── fake_k8s_adapter.py          # FakeK8sAdapter (implementa DeployPort)
│   │   └── main.py                      # FastAPI app + CORS + static files + 3 endpoints
│   ├── frontend/
│   │   └── index.html                   # Panel HITL (dark dashboard, Vanilla JS)
│   └── tests/
│       └── test_security.py             # PBT con hypothesis (4 propiedades)
└── tests/
    └── test_ui.py                       # E2E con Playwright
```

---

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/mcp/intent` | Recibe intención del Agente MCP → valida → `PENDING_APPROVAL` |
| `GET` | `/hitl/pending` | Lista despliegues pendientes de aprobación |
| `POST` | `/hitl/approve/{id}` | Aprueba → ejecuta FakeK8sAdapter → `DEPLOYED` |
| `GET` | `/frontend/index.html` | Panel HITL (servido como estático) |
| `GET` | `/health` | Health check |

---

## Tests — Todos en verde ✅

### Property-Based Testing (hypothesis) — 4/4

```
app/tests/test_security.py::test_privileged_port_always_raises    PASSED
app/tests/test_security.py::test_latest_tag_always_raises         PASSED
app/tests/test_security.py::test_both_violations_detected         PASSED
app/tests/test_security.py::test_safe_intent_never_raises         PASSED
```

### E2E con Playwright — 1/1

```
tests/test_ui.py::test_approve_deployment_shows_success_toast[chromium]  PASSED
```

El test E2E ejecuta el flujo completo:
1. POST `/mcp/intent` (crea despliegue seguro)
2. Abre el panel HITL en Chromium headless
3. Espera la tabla, clic en "Aprobar"
4. Valida que aparece el toast *"Despliegue simulado con éxito"*

---

## Frontend HITL

Panel de operaciones dark-themed con:
- **Stats bar** (pendientes / aprobados / estado API)
- **Tabla** con filas animadas (fade-in)
- **Badges** de estado (Pendiente / Desplegado)
- **Botón Aprobar** con spinner de loading
- **Toast notification** con animación slide-up

---

## Instrucciones Mutmut (Mutation Testing)

### Paso 1 — Instalar mutmut

```bash
.venv/bin/pip install mutmut
```

### Paso 2 — Ejecutar mutación sobre el validador

```bash
.venv/bin/mutmut run \
  --paths-to-mutate=app/application/security_validator.py \
  --tests-dir=app/tests/ \
  --runner=".venv/bin/python -m pytest app/tests/test_security.py -x -q"
```

### Paso 3 — Generar reporte HTML

```bash
.venv/bin/mutmut html
```

> El reporte se genera en `html/index.html`. Ábrelo en el navegador para ver qué mutantes fueron killed/survived.

---

## Cómo ejecutar

```bash
# Instalar dependencias
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install pytest-playwright && .venv/bin/playwright install chromium

# Arrancar servidor
.venv/bin/uvicorn app.infrastructure.main:app --reload --port 8000

# Tests de seguridad (PBT)
.venv/bin/python -m pytest app/tests/test_security.py -v

# Test E2E (requiere servidor corriendo)
.venv/bin/python -m pytest tests/test_ui.py -v

# Panel HITL
# → http://localhost:8000/frontend/index.html

# Swagger UI
# → http://localhost:8000/docs
```
