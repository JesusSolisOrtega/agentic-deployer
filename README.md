# Agentic Deployer: Plataforma Interna de Despliegue (IDP) en OpenShift Gobernada por Agentes IA y Protocolo MCP

**Trabajo de Fin de Máster (TFM)**  
*Máster Universitario en Ingeniería del Software: Cloud, Datos y Gestión TI*  
*Escuela Internacional de Posgrado — Universidad de Sevilla*  
**Autor:** Jesús Solís Ortega | **Tutor:** Dr. Manuel Resinas Arias de Reyna  
**Convocatoria:** Curso Académico 2025/2026  

---

Este repositorio contiene la implementación de referencia del **Agentic Deployer**, una Plataforma Interna de Despliegue (*Internal Developer Platform*, IDP) que delega la interpretación y provisión de infraestructura a agentes fundamentados en Modelos de Lenguaje de Gran Escala (LLM). El sistema gobierna el comportamiento estocástico de la Inteligencia Artificial mediante contratos declarativos bajo el estándar **Model Context Protocol (MCP)**, una arquitectura desacoplada de Puertos y Adaptadores (Hexagonal) y una máquina de estados finita con intervención humana obligatoria (**Human-In-The-Loop**, HITL).

---

## 🏗️ Arquitectura y Estructura del Repositorio

El diseño desacopla de forma estricta el razonamiento de la IA de la ejecución privilegiada en el clúster de contenedores, garantizando que el modelo cognitivo nunca acceda directamente a las credenciales del centro de datos ni a la API de Kubernetes/OpenShift.

```text
agentic-deployer/
├── app/
│   ├── domain/               # Capa Núcleo: Modelos puros (DeploymentIntent) y contratos de puertos (DeployPort)
│   │   ├── exceptions.py     # Excepciones de dominio y violaciones de seguridad
│   │   ├── models.py         # Entidades inmutables y máquina de estados (FSM: PENDING, DEPLOYED, REJECTED)
│   │   └── ports.py          # Interfaces abstractas (DeployPort, DeploymentRepositoryPort)
│   ├── application/          # Capa de Lógica de Aplicación
│   │   ├── security_validator.py # Validación determinista de políticas de seguridad corporativas
│   │   └── use_cases.py      # Casos de uso de procesamiento, aprobación y rechazo de solicitudes
│   ├── infrastructure/       # Capa de Adaptadores de Entrada/Salida
│   │   ├── fake_k8s_adapter.py # Adaptador de pruebas que emula despliegues y genera manifiestos YAML
│   │   ├── main.py           # Servidor REST FastAPI, middleware CORS y despacho de eventos HITL
│   │   └── repository.py     # Adaptador de persistencia SQLite (agentic_deployer.db)
│   ├── agent_layer/          # Capa Cognitiva y Orquestación Agéntica
│   │   ├── agent.py          # Motor ReAct con soporte multi-proveedor (Ollama, Gemini, OpenAI)
│   │   ├── chat_app.py       # Interfaz conversacional para investigadores (Streamlit)
│   │   ├── mcp_server.py     # Servidor MCP stdio con catálogo de herramientas de infraestructura
│   │   └── tools.py          # Definición de herramientas del agente y adaptación a SDKs
│   ├── frontend/             # Dashboard web para el Operador de Infraestructura HITL (HTML5/CSS3/JS)
│   │   ├── index.html        # Vista operativa de solicitudes pendientes y auditoría
│   │   ├── styles.css        # Hoja de estilos responsiva con tablas adaptadas
│   │   └── app.js            # Lógica de consumo de API REST y transiciones de estado
│   └── tests/                # Suite de pruebas automatizadas (unitarias, integración, PBT, mutación)
├── demos/                    # Evidencia empírica de pruebas y transcripciones de ejecución real
│   ├── session_logs/         # Trazas JSON de conversaciones reales con Ollama (Capítulo 8 de la memoria)
│   └── README.md             # Documentación de escenarios de demostración
├── memoria/                  # Documentación académica completa y memoria técnica oficial
│   ├── 00_Portada.md ... 11_Bibliografia.md # Capítulos en Markdown (renderizables en GitHub)
│   ├── Anexo_A_YAML.md ... Anexo_C_Manual.md # Anexos formales del TFM
│   └── TFM_JesusSolisOrtega_DEFINITIVO.pdf # Documento final consolidado con portada vectorial
├── scripts/                  # Scripts de utilidad para desarrollo, calidad y reproducibilidad
│   ├── install.sh            # Inicialización automática del entorno virtual y dependencias
│   ├── run_tests.sh          # Pipeline completo de aseguramiento de la calidad (QA)
│   ├── run_tests_only.sh     # Ejecución rápida de la suite de pruebas Pytest
│   ├── clean.sh              # Limpieza de cachés, mutantes y residuos de ejecución
│   ├── locustfile.py         # Pruebas de estrés y evaluación de latencia de la API
│   ├── compare_models.py     # Evaluación comparativa multi-modelo
│   └── generate_demos.py     # Generación automatizada de sesiones de evidencia empírica
├── requirements.txt          # Dependencias de producción y calidad fijadas
├── pyproject.toml            # Configuración de herramientas de análisis y testing
└── .env.example              # Plantilla de variables de entorno del sistema
```

---

## 🚀 Instalación y Preparación del Entorno

El sistema requiere **Python 3.11 o superior** y un sistema operativo tipo UNIX (GNU/Linux o macOS; compatible con Windows mediante WSL2).

### Opción A. Instalación Rápida Automatizada (Recomendada)

Se proporciona un script que configura el entorno virtual, instala dependencias, provisiona los navegadores headless para pruebas E2E y genera el archivo `.env`:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Opción B. Instalación Manual Paso a Paso

```bash
# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias del proyecto
pip install --upgrade pip
pip install -r requirements.txt

# 3. Provisionar navegadores para pruebas de interfaz E2E (Playwright)
playwright install chromium

# 4. Crear archivo de variables de entorno a partir de la plantilla
cp .env.example .env
```

---

## ⚙️ Ejecución de los Subsistemas

El sistema consta de dos procesos desacoplados que deben ejecutarse concurrentemente en terminales independientes con el entorno virtual activo (`source .venv/bin/activate`).

### 1. Backend de Operaciones y Middleware HITL (FastAPI)

Expone la API REST, orquesta el validador de políticas y sirve la interfaz web de supervisión:

```bash
uvicorn app.infrastructure.main:app --host 0.0.0.0 --port 8000 --reload
```

* **Panel de Control de Operaciones (HITL):** [http://localhost:8000/](http://localhost:8000/) *(redirección automática hacia `/frontend/`)*
* **Documentación Interactiva (Swagger / OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Endpoint de trazabilidad de solicitudes:** `GET http://localhost:8000/hitl/status/{deployment_id}`

### 2. Interfaz Conversacional del Asistente (Streamlit)

La interfaz de chat asiste a los usuarios en la formulación de sus peticiones mediante razonamiento ReAct:

#### Modo On-Premise / Soberanía del Dato (Ollama — Recomendado)
Permite inferencia local sin fuga de información a nubes de terceros (Zero Data Retention). El modelo base oficial evaluado en la investigación es `qwen2.5:7b` (compatible también con `qwen2.5-coder:7b`):

```bash
# En una terminal auxiliar, iniciar Ollama y descargar el modelo:
ollama serve
ollama pull qwen2.5:7b

# Iniciar la interfaz conectada al modelo local:
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
```

> **Servidores remotos con GPU:** Si el SIC aloja Ollama en un servidor corporativo centralizado, basta con configurar la variable `OLLAMA_HOST=http://<ip-o-dominio-gpu>:11434` en el archivo `.env`.

#### Modo Demostración Rápida (Determinista, sin consumo de GPU ni API Keys)
```bash
streamlit run app/agent_layer/chat_app.py   # Utiliza LLM_PROVIDER=fake por defecto
```

#### Modo Modelos Comerciales (OpenAI / Gemini)
```bash
OPENAI_API_KEY=sk-... LLM_PROVIDER=openai streamlit run app/agent_layer/chat_app.py
```

* **Punto de acceso al Chat:** [http://localhost:8501](http://localhost:8501)

---

## 🔄 Flujo de Operación Human-In-The-Loop (HITL)

1. **Petición en Lenguaje Natural:** El usuario introduce en el chat ([http://localhost:8501](http://localhost:8501)) una petición libre, por ejemplo:  
   *«Necesito desplegar el portal web para el congreso de IA del departamento.»*
2. **Razonamiento Agéntico y Validación:** El agente deduce parámetros de cómputo, imagen y puertos, invocando la herramienta MCP correspondiente. Si el despliegue vulnera alguna política (p. ej. puerto privilegiado `< 1024` o tag `:latest`), el validador emite una alerta determinista y el agente negocia parámetros seguros.
3. **Registro en Cuarentena:** Se genera un registro con identificador único (ej. `120a9ea1`) en estado `PENDING_APPROVAL`.
4. **Supervisión Humana:** El operador del SIC accede al Dashboard ([http://localhost:8000/](http://localhost:8000/)), examina la tarjeta técnica y valida las cuotas.
5. **Decisión:**
   * **Aprobar:** La máquina de estados transiciona a `DEPLOYED`, invocando el adaptador de despliegue y guardando la auditoría.
   * **Rechazar:** La máquina transiciona a `REJECTED`, notificando la causa y cancelando la provisión.
6. **Consulta Asíncrona:** El usuario puede pulsar **«Actualizar»** en el chat o preguntar *«¿Cuál es el estado de mi solicitud 120a9ea1?»* para conocer la resolución en tiempo real.

---

## 🛠️ Guía de Personalización y Extensión para el SIC

Esta sección detalla los puntos de extensión previstos para que el equipo de sistemas del Servicio de Informática y Comunicaciones (SIC) adapte la plataforma a la infraestructura corporativa de la Universidad de Sevilla mediante una rama propia de trabajo.

### 1. Estrategia de Ramificación Recomendada (Git Branching)

Para preservar la base canónica del TFM y versionar de forma limpia las adaptaciones institucionales:

```bash
git checkout -b corp/sic-deploy
```

### 2. Conexión a Clúster OpenShift Real (`app/infrastructure/`)

El sistema utiliza el patrón Hexagonal. Para desplegar contenedores reales sobre Red Hat OpenShift o Kubernetes en lugar de emularlos:

1. Crear un adaptador concreto que implemente el contrato [`DeployPort`](file:///home/jesus/projects/TFM/app/domain/ports.py):
   ```python
   # app/infrastructure/openshift_adapter.py
   from app.domain.ports import DeployPort
   from app.domain.models import DeploymentIntent, DeploymentAction
   from kubernetes import client, config

   class OpenshiftK8sAdapter(DeployPort):
       def __init__(self, kubeconfig_path: str = None, namespace: str = "idp-workloads"):
           self.namespace = namespace
           if kubeconfig_path:
               config.load_kube_config(config_file=kubeconfig_path)
           else:
               config.load_incluster_config()
           self.apps_api = client.AppsV1Api()
           self.core_api = client.CoreV1Api()

       def deploy(self, intent: DeploymentIntent) -> str:
           if intent.action == DeploymentAction.DELETE:
               self.apps_api.delete_namespaced_deployment(name=intent.name, namespace=self.namespace)
               return f"Recurso {intent.name} eliminado."
           
           # Generar y aplicar Deployment / Service / Route de OpenShift
           # ...
           return f"https://{intent.name}.apps.openshift.us.es"
   ```

2. Inyectar el nuevo adaptador en [`app/infrastructure/main.py`](file:///home/jesus/projects/TFM/app/infrastructure/main.py):
   ```python
   # app/infrastructure/main.py (línea ~58)
   from app.infrastructure.openshift_adapter import OpenshiftK8sAdapter

   # Sustituir FakeK8sAdapter por el adaptador real:
   k8s_adapter = OpenshiftK8sAdapter(namespace="sic-idp-apps")
   ```

### 3. Ajuste de Políticas de Seguridad Institucionales

Las restricciones operativas se configuran en [`app/application/security_validator.py`](file:///home/jesus/projects/TFM/app/application/security_validator.py):

* **Registros de Contenedores Confiables (`ALLOWED_REGISTRIES`):**  
  Añadir los registros internos del SIC o corporativos:
  ```python
  ALLOWED_REGISTRIES = (
      "docker.io/library/",
      "quay.io/",
      "registry.redhat.io/",
      "harbor.sic.us.es/",
  )
  ```
* **Cuotas de Recursos Departamentales:**  
  Modificar `MAX_CPU_MILLICORES` (por defecto 4 Cores) y `MAX_RAM_MI` (por defecto 8 GiB) de acuerdo con los límites de cuota de los proyectos de OpenShift.
* **Control de Secretos:**  
  Ampliar la lista `FORBIDDEN_ENV_KEYS` para forzar el uso de `Secrets` / `ConfigMaps` en lugar de variables de entorno directas.

### 4. Ampliación del Catálogo de Herramientas MCP (`mcp_server.py`)

Para exponer nuevos servicios institucionales (p. ej. portal institucional Drupal, instancia MariaDB departamental o gestor de tareas Celery):

1. Definir la nueva herramienta en [`app/agent_layer/mcp_server.py`](file:///home/jesus/projects/TFM/app/agent_layer/mcp_server.py) bajo los decoradores `@server.list_tools()` y `@server.call_tool()`.
2. Asignar parámetros declarativos seguros (imágenes auditadas, puertos $\ge 1024$, variables no sensibles).
3. El agente descubrirá dinámicamente la herramienta en la fase de inicialización sin requerir cambios en el núcleo del orquestador.

### 5. Persistencia en Base de Datos de Producción

En el prototipo se emplea SQLite (`SQLiteDeploymentRepository`). Para producción, basta con crear una clase que implemente [`DeploymentRepositoryPort`](file:///home/jesus/projects/TFM/app/domain/ports.py) conectada a un servidor PostgreSQL corporativo y reemplazar la instancia en `app/infrastructure/main.py`.

---

## 🧪 Aseguramiento de la Calidad (QA) y Reproducibilidad

El repositorio implementa una estrategia de verificación formal y multicapa orientada a garantizar la robustez del sistema frente al estocasticismo del LLM:

* **Pruebas Basadas en Propiedades (*Property-Based Testing* con Hypothesis):** Fuzzing sistemático sobre el validador de seguridad con miles de combinaciones generadas pseudo-aleatoriamente.
* **Testing de Mutación (*Mutation Testing* con Mutmut):** Introducción de mutantes lógicos en `SecurityContextValidator` para auditar la efectividad de la suite de tests.
* **Testing Metamórfico:** Evaluación empírica de robustez del LLM ante perturbaciones semánticas, inyección de ruido léxico y variaciones de temperatura.
* **Testing E2E de Flujo Completo (Playwright):** Automatización del ciclo interactivo navegando el dashboard HITL y comprobando la persistencia.
* **Evaluación de Rendimiento y Carga (Locust):** Simulación de concurrencia y auditoría de tiempos de respuesta en la API de intermediación.

### Ejecución de Pruebas

```bash
# 1. Ejecución rápida de la suite de tests (65 tests en ~3.5 s):
./scripts/run_tests_only.sh

# 2. Ejecución integral del pipeline de calidad (Linters, Tipos, Tests, Mutmut, Locust):
./scripts/run_tests.sh

# 3. Reproducción de las sesiones empíricas documentadas en el Capítulo 8:
PYTHONPATH=. python3 scripts/generate_demos.py

# 4. Evaluación comparativa entre familias de modelos (Qwen, Llama, Mistral):
PYTHONPATH=. python3 scripts/compare_models.py
```

Para depurar y resetear los entornos de pruebas y reportes generados:
```bash
./scripts/clean.sh
```

---

## 🔌 Validación Oficial con MCP Inspector

El servidor MCP es interoperable con cualquier cliente estándar. Se puede inspeccionar visualmente su esquema declarativo e invocar herramientas en tiempo real usando la herramienta oficial de la especificación:

```bash
# Requiere Node.js / npx
npx @modelcontextprotocol/inspector .venv/bin/python app/agent_layer/mcp_server.py
```

Al iniciarse, abrirá el navegador en `http://localhost:5173`, permitiendo auditar las firmas JSON Schema de `deploy_congress_web`, `deploy_python_app`, `deploy_wordpress`, etc.

---

## 📄 Memoria del Trabajo de Fin de Máster

La documentación formal completa del proyecto se encuentra disponible en el directorio [`memoria/`](memoria/):

* **Capítulos del Documento:** Redactados en Markdown independiente con numeración canónica (`00_Portada.md` a `11_Bibliografia.md` y `Anexo_A` a `Anexo_C`), optimizados para su renderizado y lectura directa en GitHub.
* **PDF Definitivo Oficial:** Documento consolidado (161 páginas) ensamblado con la cubierta vectorial oficial de la Universidad de Sevilla:  
  👉 **[`memoria/TFM_JesusSolisOrtega_DEFINITIVO.pdf`](memoria/TFM_JesusSolisOrtega_DEFINITIVO.pdf)**

---

## ⚖️ Licencia y Régimen de Explotación

Copyright (C) 2026 Jesús Solís Ortega.

* **Software y Código Fuente:** Publicado bajo los términos de la **GNU Affero General Public License v3.0 (GNU AGPLv3)**. Consulta el archivo [`LICENSE`](LICENSE) para acceder al texto íntegro de la licencia.
  * *Uso Abierto y Académico:* Se autoriza la copia, ejecución, inspección y modificación del software para fines personales, educativos, de investigación y proyectos sin ánimo de lucro, con la obligación recíproca de compartir las modificaciones y el código fuente derivado bajo esta misma licencia si se ofrece el software a través de una red telemática (Sección 13).
  * *Licenciamiento Comercial y Consultoría:* Si representa a una entidad u organización que desea integrar, desplegar u operar esta plataforma en entornos corporativos privativos sin acogerse a las obligaciones de la licencia AGPLv3, o precisa soporte de arquitectura y adaptación a medida para OpenShift/Kubernetes, contacte directamente con el autor:  
    📫 **Jesús Solís Ortega** — [jesussolisortega@gmail.com](mailto:jesussolisortega@gmail.com)

* **Memoria Técnica y Documentación:** La memoria académica del Trabajo de Fin de Máster y sus especificaciones formales se distribuyen bajo licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.
