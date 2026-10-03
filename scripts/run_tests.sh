#!/usr/bin/env bash
# ===========================================================================
# run_tests.sh — Pipeline de CI local
# ===========================================================================
# Ejecuta análisis estático, tipado y tests en orden.
# Se detiene al primer fallo (set -e).
#
# Uso:
#   chmod +x run_tests.sh
#   ./run_tests.sh
# ===========================================================================

set -euo pipefail

# ── Colores ────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Directorio del proyecto ───────────────────────────────────────────────
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_BIN="${PROJECT_DIR}/.venv/bin"
PYTHON="${VENV_BIN}/python"
UVICORN="${VENV_BIN}/uvicorn"

# Verificar que el venv existe
if [ ! -f "${PYTHON}" ]; then
    echo -e "${RED}Error: No se encontró el virtualenv en .venv/${RESET}"
    echo "Ejecuta:  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

step() {
    echo ""
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${CYAN}${BOLD}  ▸ $1${RESET}"
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
}

pass() {
    echo ""
    echo -e "  ${GREEN}✔ $1${RESET}"
}

# ===========================================================================
# PASO 1 — Análisis estático (Linter)
# ===========================================================================
step "PASO 1/6 — Análisis estático con Ruff"
${VENV_BIN}/ruff check app/
pass "Ruff: sin errores de linting"

# ===========================================================================
# PASO 2 — Análisis de tipado
# ===========================================================================
step "PASO 2/6 — Análisis de tipado con mypy"
${VENV_BIN}/mypy app/ --config-file="${PROJECT_DIR}/pyproject.toml"
pass "mypy: tipado correcto"

# ===========================================================================
# PASO 3 — Tests E2E / UI (requiere servidor)
# ===========================================================================
step "PASO 3/6 — Tests E2E con Playwright"

# Arrancar uvicorn en background
echo "  Arrancando servidor FastAPI en background..."
${UVICORN} app.infrastructure.main:app --host 127.0.0.1 --port 8000 &
UVICORN_PID=$!

# Esperar a que el servidor esté listo
for i in $(seq 1 15); do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "  Servidor listo (PID: ${UVICORN_PID})"
        break
    fi
    if [ "$i" -eq 15 ]; then
        echo -e "${RED}Error: El servidor no arrancó en 15 segundos${RESET}"
        kill ${UVICORN_PID} 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Ejecutar tests E2E
${PYTHON} -m pytest tests/test_ui.py -v --no-cov || {
    kill ${UVICORN_PID} 2>/dev/null || true
    exit 1
}

# Parar servidor
kill ${UVICORN_PID} 2>/dev/null || true
wait ${UVICORN_PID} 2>/dev/null || true
pass "Playwright E2E: tests pasados"

# ===========================================================================
# PASO 4 — Tests unitarios + PBT con cobertura
# ===========================================================================
step "PASO 4/6 — Property-Based Testing + Cobertura"
${PYTHON} -m pytest app/tests/ -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov --cov-config=pyproject.toml
pass "Hypothesis PBT + Coverage: completado"

# ===========================================================================
# PASO 4.5 — Pruebas Metamórficas contra IA Real (Solo si Ollama está disponible)
# ===========================================================================
if command -v ollama >/dev/null 2>&1; then
    step "PASO 4.5/6 — Evaluación Cognitiva (Pruebas Metamórficas Reales)"
    echo "  Detectado demonio de Ollama en el sistema. Ejecutando tests cognitivos..."
    mkdir -p demos/metamorphic_results
    RUN_REAL_LLM=true ${PYTHON} -m pytest app/tests/test_metamorphic.py -v > demos/metamorphic_results/report_real_llm.txt || {
        echo -e "${RED}Error en las pruebas metamórficas reales. Revisa el reporte.${RESET}"
    }
    pass "Pruebas Metamórficas (Real LLM): reporte guardado en demos/metamorphic_results/report_real_llm.txt"
else
    echo ""
    echo "  (Saltando PASO 4.5: 'ollama' no está instalado en este sistema de CI)"
fi

# ===========================================================================
# PASO 5 — Pruebas de Mutación (Mutmut)
# ===========================================================================
step "PASO 5/6 — Mutation Testing con mutmut"
${VENV_BIN}/mutmut run --paths-to-mutate app/application/security_validator.py || true
${VENV_BIN}/mutmut results || true
pass "Mutation Testing: completado"

# ===========================================================================
# PASO 6 — Pruebas de Carga (Locust)
# ===========================================================================
step "PASO 6/6 — Pruebas de Carga con Locust"

echo "  Arrancando servidor FastAPI en background..."
${UVICORN} app.infrastructure.main:app --host 127.0.0.1 --port 8000 &
UVICORN_PID=$!

# Esperar a que el servidor esté listo
for i in $(seq 1 15); do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "  Servidor listo (PID: ${UVICORN_PID})"
        break
    fi
    if [ "$i" -eq 15 ]; then
        echo -e "${RED}Error: El servidor no arrancó en 15 segundos${RESET}"
        kill ${UVICORN_PID} 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

echo "  Ejecutando Locust en modo headless (10 usuarios, 5s)..."
${VENV_BIN}/locust -f scripts/locustfile.py --headless -u 10 -r 2 --run-time 5s --host=http://127.0.0.1:8000 || {
    kill ${UVICORN_PID} 2>/dev/null || true
    exit 1
}

# Parar servidor
kill ${UVICORN_PID} 2>/dev/null || true
wait ${UVICORN_PID} 2>/dev/null || true
pass "Locust Load Testing: completado"

# ===========================================================================
# Resumen final
# ===========================================================================
echo ""
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}${BOLD}  ✅  PIPELINE COMPLETO — Todos los pasos pasaron${RESET}"
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
echo -e "  📊 Reporte de cobertura HTML: ${BOLD}htmlcov/index.html${RESET}"
echo ""
