# Agentic Deployer: Orquestación de Infraestructura con IA Generativa

**Trabajo de Fin de Máster (TFM)**

Este repositorio contiene la prueba de concepto y el producto mínimo viable (MVP) del "Agentic Deployer", un sistema diseñado para gobernar el comportamiento estocástico de los Modelos de Lenguaje Grandes (LLM) y utilizarlos como motores de provisión de infraestructura en entornos corporativos críticos.

## 🏗️ Arquitectura del Sistema

El proyecto demuestra que es posible delegar la abstracción de operaciones complejas a una Inteligencia Artificial sin comprometer la seguridad del centro de datos. Para ello, implementa tres patrones arquitectónicos fundamentales:

1. **Arquitectura Hexagonal (Ports and Adapters):** Aísla la lógica de negocio y las políticas de seguridad (`SecurityContextValidator`) del modelo de IA. La IA interactúa como un actor no privilegiado en la capa externa, sin acceso directo a Kubernetes.
2. **Model Context Protocol (MCP):** Define un contrato estándar para inyectar capacidades de despliegue en cualquier LLM (OpenAI, Ollama, Anthropic) vía `stdio`, aislando las credenciales y garantizando la Soberanía del Dato.
3. **Human-In-The-Loop (HITL):** Una máquina de estados finita (FSM) que garantiza que ninguna alteración de la infraestructura se ejecuta sin la aprobación asíncrona de un Ingeniero de Operaciones a través de un panel de control.

## 🚀 Instalación y Configuración

El sistema requiere **Python 3.11 o superior**.

```bash
# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias del proyecto
pip install -r requirements.txt

# 3. Configurar navegadores para los tests E2E
playwright install chromium
```

## ⚙️ Ejecución del Proyecto

El sistema se divide en dos grandes bloques de ejecución paralelos: el Backend de Operaciones (Hexagonal) y la Interfaz Cognitiva del Usuario.

### 1. Levantar el Backend (FastAPI + Panel HITL)
Este servidor expone el contrato de herramientas MCP y sirve la interfaz estática para el Técnico de Operaciones.
```bash
uvicorn app.infrastructure.main:app --reload --port 8000
```
- **Panel de Aprobación (HITL):** [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html)

### 2. Levantar el Agente LLM (Chat UI)

El sistema soporta **tres modos de proveedor LLM** seleccionables vía variable de entorno:

**Modo recomendado — Ollama (gratuito, local, Zero Data Retention):**
```bash
# 1. Instalar Ollama: https://ollama.com
ollama serve                        # Iniciar servidor (otra terminal)
ollama pull qwen2.5:7b              # Descargar modelo (~4.7 GB)

# 2. Lanzar el chat con Ollama
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
```

**Modo OpenAI:**
```bash
OPENAI_API_KEY=sk-... LLM_PROVIDER=openai streamlit run app/agent_layer/chat_app.py
```

**Modo Demo (sin IA, para pruebas rápidas):**
```bash
streamlit run app/agent_layer/chat_app.py   # LLM_PROVIDER=fake por defecto
```

> Ver [`.env.example`](.env.example) para la lista completa de variables de configuración.

## 🧪 Aseguramiento de Calidad Avanzado (QA)

Para garantizar la estabilidad del sistema frente al ruido inyectado por la IA, este TFM implementa un *Pipeline* de pruebas agresivo y multicapa, superando la cobertura clásica:

- **Testing Unitario y de Integración:** Validación matemática del Dominio.
- **Pruebas Basadas en Propiedades (Hypothesis):** Fuzzing de entropía masiva contra el validador de seguridad.
- **Mutation Testing (Mutmut):** Generación de clones maliciosos para auditar la solidez de las propias pruebas.
- **Pruebas Metamórficas:** Evaluación del LLM ante ruido léxico, faltas de ortografía e inversión sintáctica.
- **Testing E2E (Playwright) y Carga (Locust):** Auditoría del flujo HITL y rendimiento de la API.

### Ejecución de la Suite de Pruebas

Para mayor comodidad y rigor, el proyecto incluye un script de *pipeline* continuo (`scripts/run_tests.sh`) que ejecuta de forma desatendida y secuencial todas las capas de calidad: linters, análisis de tipos, pruebas de interfaz (E2E), pruebas estocásticas y de propiedades, inyección de mutantes lógicos (mutmut) y pruebas de carga (Locust).

```bash
# Otorgar permisos y ejecutar el pipeline completo (recomendado):
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

Alternativamente, se pueden ejecutar bloques aislados:
```bash
python -m pytest app/tests/ -v      # Dominio y PBT
python -m pytest tests/test_ui.py -v # E2E Interfaz (requiere FastAPI activo)
mutmut run                          # Auditoría de mutantes
```

## 📄 Memoria del Proyecto

Toda la fundamentación teórica, diagramas arquitectónicos, decisiones de diseño y análisis de resultados se encuentran documentados en los archivos Markdown dentro del directorio `/memoria`. Se proveen scripts (como `scripts/combinar_tfm_y_toc.py`) para compilar un documento único listo para su exportación a PDF.

## 🔌 Integración con Clientes MCP Externos

Una de las propiedades clave del *Agentic Deployer* es que su servidor MCP es **agnóstico al cliente**. Al implementar el estándar [Model Context Protocol](https://github.com/modelcontextprotocol/specification) sobre transporte `stdio`, cualquier cliente compatible puede descubrir e invocar las herramientas del Servicio de Informática sin modificar una sola línea del servidor.

### Validación Oficial con MCP Inspector

El [MCP Inspector](https://github.com/modelcontextprotocol/inspector) es la herramienta oficial de Anthropic para validar servidores MCP. Permite explorar el catálogo de herramientas e invocarlas visualmente desde el navegador:

```bash
# Sin instalación permanente (requiere Node.js)
npx @modelcontextprotocol/inspector \
  .venv/bin/python app/agent_layer/mcp_server.py
```

Al ejecutarlo, se abre `http://localhost:5173` con:
- Lista de todas las herramientas expuestas (`tools/list`)
- Formulario para invocar `deploy_congress_web`, `deploy_python_app`, etc.
- Respuesta JSON en tiempo real


