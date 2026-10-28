# Agentic Deployer: Orquestación de Infraestructura con IA Generativa

**Trabajo de Fin de Máster (TFM)**  
*Máster Universitario en Ingeniería del Software: Cloud, Datos y Gestión TI*  
*Escuela Internacional de Posgrado — Universidad de Sevilla*  
**Autor:** Jesús Solís Ortega | **Dirección:** Manuel Resinas Arias de Reyna  
**Convocatoria:** Noviembre 2026

Este repositorio contiene la prueba de concepto y el producto mínimo viable (MVP) del «Agentic Deployer», un sistema diseñado para gobernar el comportamiento estocástico de los Modelos de Lenguaje de Gran Escala (LLM) y utilizarlos como motores de provisión de infraestructura en entornos corporativos críticos.

## 🏗️ Arquitectura del Sistema

El proyecto demuestra que es posible delegar la abstracción de operaciones complejas a una Inteligencia Artificial sin comprometer la seguridad del centro de datos. Para ello, implementa tres patrones arquitectónicos fundamentales:

1. **Arquitectura Hexagonal (Ports and Adapters):** Aísla la lógica de negocio y las políticas de seguridad (`SecurityContextValidator`) del modelo de IA. La IA interactúa como un actor no privilegiado en la capa externa, sin acceso directo a Kubernetes.
2. **Model Context Protocol (MCP):** Define un contrato estándar para inyectar capacidades de despliegue en cualquier LLM (OpenAI, Ollama, Anthropic) vía `stdio`, aislando las credenciales y garantizando la Soberanía del Dato.
3. **Human-In-The-Loop (HITL):** Una máquina de estados finita (FSM) que garantiza que ninguna alteración de la infraestructura se ejecuta sin la aprobación asíncrona de un Ingeniero de Operaciones a través de un panel de control.

## 🚀 Instalación y Configuración

El sistema requiere **Python 3.11 o superior**.

### Instalación Manual Paso a Paso

```bash
# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias del proyecto
pip install -r requirements.txt

# 3. Configurar el motor de navegador para tests E2E
playwright install chromium

# 4. Inicializar variables de entorno a partir de la plantilla
cp .env.example .env
```

> **Alternativa automatizada:** Se provee el script `scripts/install.sh`, el cual automatiza los pasos anteriores e inicializa el modelo local de Ollama:
> ```bash
> chmod +x scripts/install.sh
> ./scripts/install.sh
> ```

## ⚙️ Ejecución del Proyecto

El sistema se compone de dos subsistemas desacoplados que deben ejecutarse de forma concurrente en terminales independientes con el entorno virtual activado (`source .venv/bin/activate`): el Backend de Operaciones (Hexagonal) y la Interfaz de Chat del Asistente.

### 1. Levantar el Backend (FastAPI + Panel HITL)

Expone la API REST, el contrato de herramientas MCP y sirve la interfaz estática para el Técnico de Operaciones:

```bash
uvicorn app.infrastructure.main:app --reload --port 8000
```

- **Panel de Aprobación (HITL):** [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html)
- **Documentación Interactiva (Swagger/OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Levantar el Agente LLM (Chat UI con Streamlit)

La interfaz conversacional se ejecuta sobre Streamlit y escucha en el puerto `8501`:

**Modo Recomendado — Ollama (local, privado, Zero Data Retention):**
```bash
# En una terminal auxiliar, iniciar el servicio local y descargar el modelo:
ollama serve
ollama pull qwen2.5-coder:7b

# Lanzar el chat conectado a Ollama:
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5-coder:7b streamlit run app/agent_layer/chat_app.py
```

**Modo Demo (Determinista, sin dependencias de GPU ni API Keys externas):**
```bash
streamlit run app/agent_layer/chat_app.py   # LLM_PROVIDER=fake por defecto
```

**Modo OpenAI / Modelos Comerciales:**
```bash
OPENAI_API_KEY=sk-... LLM_PROVIDER=openai streamlit run app/agent_layer/chat_app.py
```

> La aplicación estará accesible en: [http://localhost:8501](http://localhost:8501)

### 3. Flujo de Operación Manual Completo (HITL)

Para verificar el ciclo de vida completo de una solicitud de infraestructura:

1. **Interacción Conversacional:** Acceder a [http://localhost:8501](http://localhost:8501). Introducir una solicitud en lenguaje natural (ejemplo: *"Necesito desplegar la web para el congreso de Inteligencia Artificial del departamento"* o hacer clic en los botones de plantilla sugeridos).
2. **Razonamiento y Validación:** El agente analiza el requerimiento, deduce los parámetros (CPU, RAM, imagen de contenedor), valida las políticas de seguridad y ejecuta la herramienta MCP correspondiente, registrando la intención en el backend en estado `PENDING`.
3. **Revisión Técnica:** Acceder al Panel de Operaciones en [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html). En la bandeja de entrada aparecerá la tarjeta de despliegue con el desglose técnico y las validaciones superadas.
4. **Decisión Humana:** El operador hace clic en **«Aprobar»** (o **«Rechazar»**). La máquina de estados transiciona a `DEPLOYED`, ejecutando la provisión y registrando la auditoría de la operación.

## 🧪 Aseguramiento de Calidad Avanzado (QA)

Para verificar el comportamiento determinista del sistema frente a la naturaleza estocástica de los modelos de lenguaje, el proyecto implementa un pipeline de pruebas multicapa que complementa la cobertura de código convencional con técnicas avanzadas de verificación:

- **Testing Unitario y de Integración:** Validación exhaustiva de invariantes de dominio y contratos de puertos hexagonales.
- **Pruebas Basadas en Propiedades (*Property-Based Testing* con Hypothesis):** Fuzzing generativo sobre el validador de políticas de seguridad (`SecurityContextValidator`).
- **Mutation Testing (Mutmut):** Inyección sistemática de mutantes sintácticos para evaluar la capacidad de detección de la suite de pruebas.
- **Pruebas Metamórficas:** Evaluación de robustez del LLM ante perturbaciones semánticas, ruido léxico y reordenaciones sintácticas.
- **Testing E2E (Playwright) y Evaluación de Carga (Locust):** Verificación del flujo asíncrono HITL y auditoría de latencia de la API.

### Ejecución de la Suite de Pruebas

El repositorio incluye un script de ejecución integral (`scripts/run_tests.sh`) que ejecuta de forma desatendida y secuencial todas las capas de calidad: linters, análisis de tipos, pruebas de interfaz (E2E), pruebas estocásticas y de propiedades, mutación lógica (mutmut) y pruebas de carga (Locust).

```bash
# Otorgar permisos y ejecutar el pipeline completo:
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

Alternativamente, se pueden ejecutar bloques aislados:
```bash
python -m pytest app/tests/ -v                                        # Dominio, PBT y metamórficos
python -m pytest tests/test_ui.py -v                                  # E2E Interfaz (requiere FastAPI activo)
mutmut run --paths-to-mutate app/application/security_validator.py     # Auditoría de mutantes sobre el validador
```

Para restablecer el repositorio y eliminar cachés de pruebas y reportes generados:
```bash
chmod +x scripts/clean.sh
./scripts/clean.sh
```

## 📄 Memoria del Proyecto y Flujo de Compilación

La memoria académica completa, diagramas arquitectónicos (C4 y UML), especificaciones formales y análisis de resultados experimentales se encuentran redactados en el directorio [`/memoria`](memoria/). La estructura capitular sigue la plantilla oficial del grupo de investigación **Diverso Lab** (Universidad de Sevilla).

Se provee un conjunto de herramientas en [`scripts/`](scripts/) para la consolidación, verificación y ensamblado del documento final:

```bash
# 1. Validar y reordenar citas bibliográficas según el estándar IEEE (1..45 secuencial)
python scripts/reordenar_citas.py

# 2. Generar el documento consolidado preliminar
python scripts/combinar_tfm_y_toc.py

# 3. Exportar TFM_Completo.md a PDF desde Typora (guardar como TFM_Completo.pdf)

# 4. Inyectar números de página físicos en los índices con alineación tabular formal (flexbox dot-leaders)
python scripts/actualizar_indices_con_paginas.py

# 5. Ensamblar el PDF definitivo sustituyendo la portada por la cubierta institucional vectorial
python scripts/ensamblar_pdf_definitivo.py
```

> **Nota:** La compilación de la portada institucional y el ensamblado de PDFs requieren `weasyprint`, `poppler-utils` (`pdftotext`, `pdfunite`) y `ghostscript` instalados en el sistema anfitrión.

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


