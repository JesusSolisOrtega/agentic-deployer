# MVP Middleware Orquestador — Suite QA Profesional

## Pipeline CI local (`run_tests.sh`)

El script ejecuta 4 pasos secuenciales, fail-fast:

```
PASO 1/4 — Ruff (linter)            ✔ All checks passed
PASO 2/4 — mypy (tipado)            ✔ No issues found in 15 source files
PASO 3/4 — Playwright (E2E)         ✔ 1 passed
PASO 4/4 — Hypothesis (PBT+Coverage) ✔ 8 passed — 100.0% coverage
```

---

## Archivos creados / modificados

| Archivo | Descripción |
|---------|-------------|
| [pyproject.toml](file:///home/jesus/projects/TFM/pyproject.toml) | Config centralizada de pytest, coverage, ruff y mypy |
| [run_tests.sh](file:///home/jesus/projects/TFM/run_tests.sh) | Pipeline CI local (4 pasos, fail-fast, auto-start/stop uvicorn) |
| [test_use_cases.py](file:///home/jesus/projects/TFM/app/tests/test_use_cases.py) | Tests unitarios del caso de uso (4 tests) |
| [requirements.txt](file:///home/jesus/projects/TFM/requirements.txt) | Añadidos: pytest-cov, ruff, mypy, pytest-playwright |

Ficheros corregidos por ruff auto-fix:
| Archivo | Cambios |
|---------|---------|
| [models.py](file:///home/jesus/projects/TFM/app/domain/models.py) | `StrEnum` en lugar de `str, Enum`, `X \| None` en lugar de `Optional[X]`, imports ordenados |
| [main.py](file:///home/jesus/projects/TFM/app/infrastructure/main.py) | `raise ... from exc` (B904), imports ordenados |
| [test_security.py](file:///home/jesus/projects/TFM/app/tests/test_security.py) | Eliminado import no usado (`assume`), imports ordenados |

---

## Reporte de cobertura

```
Name                                    Stmts   Miss   Cover   Missing
----------------------------------------------------------------------
app/application/security_validator.py      12      0  100.0%
app/application/use_cases.py               12      0  100.0%
app/domain/exceptions.py                    4      0  100.0%
app/domain/models.py                       18      0  100.0%
----------------------------------------------------------------------
TOTAL                                      46      0  100.0%
```

> Reporte HTML en `htmlcov/index.html` — generado automáticamente por el pipeline.

---

## Configuración pyproject.toml

### pytest
- `testpaths`: `app/tests/` + `tests/`
- Auto-coverage con `--cov=app --cov-report=term-missing --cov-report=html`
- Marker `e2e` para separar tests que necesitan servidor

### coverage
- `fail_under = 90` — el pipeline falla si la cobertura baja del 90%
- Omite infraestructura, ports (ABC) y `__init__.py` del cálculo

### ruff
- Reglas: `E, W, F, I, UP, B, SIM, RUF`
- `isort` con `known-first-party = ["app"]`

### mypy
- `disallow_untyped_defs = true` para código de producción
- `ignore_missing_imports = true` para terceros sin stubs
- Override relajado para tests

---

## Cómo ejecutar

```bash
# Pipeline completo (4 pasos)
./run_tests.sh

# Solo linter
.venv/bin/ruff check app/

# Solo tipado
.venv/bin/mypy app/

# Solo tests con cobertura
.venv/bin/python -m pytest app/tests/ -v

# Solo E2E (requiere servidor corriendo)
.venv/bin/python -m pytest tests/test_ui.py -v --no-cov
```
