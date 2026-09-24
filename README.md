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
En una terminal separada, levanta la interfaz conversacional para que el Investigador solicite infraestructura en lenguaje natural. 
*(Nota: Requiere tener exportada la variable `OPENAI_API_KEY` o configurar Ollama localmente).*
```bash
streamlit run app/agent_layer/chat_app.py
```

## 🧪 Aseguramiento de Calidad Avanzado (QA)

Para garantizar la estabilidad del sistema frente al ruido inyectado por la IA, este TFM implementa un *Pipeline* de pruebas agresivo y multicapa, superando la cobertura clásica:

- **Testing Unitario y de Integración:** Validación matemática del Dominio.
- **Pruebas Basadas en Propiedades (Hypothesis):** Fuzzing de entropía masiva contra el validador de seguridad.
- **Mutation Testing (Mutmut):** Generación de clones maliciosos para auditar la solidez de las propias pruebas.
- **Pruebas Metamórficas:** Evaluación del LLM ante ruido léxico, faltas de ortografía e inversión sintáctica.
- **Testing E2E (Playwright) y Carga (Locust):** Auditoría del flujo HITL y rendimiento de la API.

### Ejecución de la Suite de Pruebas

```bash
# Ejecutar toda la batería estática, de propiedades y metamórfica:
python -m pytest app/tests/ -v

# Ejecutar las pruebas E2E de interfaz (requiere que FastAPI esté corriendo en el puerto 8000):
python -m pytest tests/test_ui.py -v

# Ejecutar auditoría de Mutantes en todo el sistema:
mutmut run
```

## 📄 Memoria del Proyecto

Toda la fundamentación teórica, diagramas arquitectónicos, decisiones de diseño y análisis de resultados se encuentran documentados en los archivos Markdown dentro del directorio `/memoria`. Se proveen scripts (como `combinar_tfm_y_toc.py`) para compilar un documento único listo para su exportación a PDF.
