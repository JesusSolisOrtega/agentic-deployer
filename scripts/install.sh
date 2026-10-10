#!/bin/bash
set -e

echo "=========================================="
echo " Instalador del Agentic Deployer (TFM)"
echo "=========================================="

# Comprobar versión de Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 no está instalado."
    exit 1
fi

# 1. Crear entorno virtual
if [ ! -d ".venv" ]; then
    echo ">> Creando entorno virtual de Python en .venv..."
    python3 -m venv .venv
else
    echo ">> El entorno virtual .venv ya existe."
fi

# 2. Activar e instalar dependencias
echo ">> Instalando dependencias de Python (requirements.txt)..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Navegadores Playwright
echo ">> Instalando navegadores para Playwright (Tests E2E)..."
playwright install chromium

# 4. Configurar variables de entorno
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo ">> Creando archivo .env por defecto a partir de .env.example..."
        cp .env.example .env
    fi
fi

# 5. Configuración de Ollama y Modelos
echo ">> Comprobando instalación de Ollama..."
if ! command -v ollama &> /dev/null; then
    echo ">> Ollama no encontrado. Descargando e instalando (puede solicitar contraseña de sudo)..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo ">> Ollama ya está instalado."
fi

echo ">> Comprobando si el servicio de Ollama está corriendo..."
OLLAMA_STARTED_BY_US=0
if ! curl -s http://localhost:11434/api/version > /dev/null; then
    echo ">> Arrancando servicio Ollama en segundo plano para descargar el modelo..."
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    OLLAMA_STARTED_BY_US=1
    sleep 3 # Tiempo de gracia para que levante el socket
else
    echo ">> El servicio Ollama ya está activo."
fi

echo ">> Descargando modelo LLM (qwen2.5-coder:7b). Esto puede tardar varios minutos..."
ollama pull qwen2.5-coder:7b

if [ "$OLLAMA_STARTED_BY_US" -eq 1 ]; then
    echo ">> Deteniendo servicio Ollama temporal..."
    kill $OLLAMA_PID
fi

echo ""
echo "========================================================"
echo " Instalación completa del ecosistema finalizada con éxito."
echo "========================================================"
echo ""
echo "🚀 Para arrancar el proyecto:"
echo ""
echo " 1️⃣  Activa el entorno virtual:"
echo "    source .venv/bin/activate"
echo ""
echo " 2️⃣  Abre una terminal y levanta el servicio IA:"
echo "    ollama serve"
echo ""
echo " 3️⃣  Abre otra terminal y levanta el Backend (FastAPI):"
echo "    source .venv/bin/activate"
echo "    uvicorn app.infrastructure.main:app --reload --port 8000"
echo ""
echo " 4️⃣  Abre una tercera terminal y levanta la Interfaz (Streamlit):"
echo "    source .venv/bin/activate"
echo "    LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5-coder:7b streamlit run app/agent_layer/chat_app.py"
echo "========================================================"
