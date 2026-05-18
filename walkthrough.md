# MVP Middleware Orquestador — HITL + MCP

## Estructura generada

```
TFM/
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py                          # Re-export de conveniencia
    ├── domain/
    │   ├── __init__.py
    │   ├── models.py                    # DeploymentIntent, DeploymentRecord, DeploymentStatus
    │   ├── ports.py                     # DeployPort (ABC)
    │   └── exceptions.py               # SecurityViolationError
    ├── application/
    │   ├── __init__.py
    │   ├── security_validator.py        # SecurityContextValidator (lógica pura)
    │   └── use_cases.py                 # ProcessDeploymentUseCase + deployment_store
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── fake_k8s_adapter.py          # FakeK8sAdapter (implementa DeployPort)
    │   └── main.py                      # FastAPI app + 3 endpoints
    └── tests/
        ├── __init__.py
        └── test_security.py             # PBT con hypothesis (4 propiedades)
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/mcp/intent` | Recibe intención del Agente MCP → valida → guarda con estado `PENDING_APPROVAL` |
| `GET` | `/hitl/pending` | Lista despliegues pendientes de aprobación humana |
| `POST` | `/hitl/approve/{id}` | Aprueba un despliegue → ejecuta FakeK8sAdapter → devuelve URL |
| `GET` | `/health` | Health check |

## Tests ejecutados

**4/4 Property-Based Tests pasaron** (100 ejemplos aleatorios cada uno):

1. `test_privileged_port_always_raises` — Puerto < 1024 siempre lanza error
2. `test_latest_tag_always_raises` — Imagen con `:latest` siempre lanza error
3. `test_both_violations_detected_simultaneously` — Ambas violaciones detectadas en una pasada
4. `test_safe_intent_never_raises` — Intent seguro nunca lanza excepción

## Verificación E2E

Flujo completo probado con curl:

1. ✅ `POST /mcp/intent` → devuelve `id` + estado `PENDING_APPROVAL`
2. ✅ `GET /hitl/pending` → lista el despliegue pendiente
3. ✅ `POST /hitl/approve/{id}` → estado cambia a `DEPLOYED` + URL generada
4. ✅ Validación de seguridad rechaza puerto 80 (< 1024) con HTTP 422
5. ✅ Validación de seguridad rechaza imagen `nginx:latest` con HTTP 422

## Cómo ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Arrancar servidor
uvicorn app.infrastructure.main:app --reload --port 8000

# Ejecutar tests
pytest app/tests/test_security.py -v

# Swagger UI automático
# → http://localhost:8000/docs
```
