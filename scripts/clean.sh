#!/usr/bin/env bash
# ===========================================================================
# clean.sh — Script para limpiar archivos autogenerados y cachés
# ===========================================================================

set -euo pipefail

# ── Colores ────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${CYAN}${BOLD}🧹 Limpiando el repositorio...${RESET}"

# 1. Limpiar archivos precompilados de Python
echo -e "  ▸ Eliminando cachés de Python (__pycache__, *.pyc)..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# 2. Limpiar cachés de Pytest, Mypy y Ruff
echo -e "  ▸ Eliminando cachés de herramientas de testing y linting..."
rm -rf .pytest_cache/
rm -rf .mypy_cache/
rm -rf .ruff_cache/

# 3. Limpiar archivos de cobertura
echo -e "  ▸ Eliminando reportes de cobertura..."
rm -rf htmlcov/
rm -f .coverage

# 4. Limpiar entorno de pruebas de mutación (Mutmut)
echo -e "  ▸ Eliminando entorno de pruebas de mutación..."
rm -rf mutants/
rm -f .mutmut-cache

echo ""
echo -e "${GREEN}${BOLD}✨ ¡Limpieza completada con éxito! El repositorio está impecable.${RESET}"
