# Capítulo 9. Resultados Experimentales y Evaluación

El diseño arquitectónico (Capítulo 5), la implementación del agente cognitivo y el protocolo MCP (Capítulo 6), el gobierno humano mediante el patrón HITL (Capítulo 7) y la estrategia metodológica de aseguramiento de la calidad (Capítulo 8) convergen en este capítulo para someter al sistema a una rigurosa evaluación empírica. La validez de una solución de ingeniería de software orientada a operaciones de infraestructura no reside exclusivamente en la corrección formal de sus componentes aislados, sino en su capacidad para resolver tareas reales de aprovisionamiento de manera predecible, segura y eficiente bajo condiciones operativas realistas.

El presente capítulo estructura la experimentación en seis pilares complementarios:
1. **Marco y Entorno Experimental (§9.1):** Especificación rigurosa de la infraestructura de cómputo, los motores de inferencia, las precondiciones técnicas y el protocolo de repetibilidad estadística.
2. **Casos de Estudio Reales (*Walkthroughs* Extremo a Extremo) (§9.2):** Trazabilidad exhaustiva del comportamiento del sistema frente a cuatro escenarios prácticos: provisión estándar conforme (*Happy Path*), resiliencia perimetral ante inyecciones de *prompt* y violaciones de seguridad, gobierno asíncrono supervisado por un operador humano (*HITL*), y autocorrección guiada por excepciones deterministas.
3. **Evaluación Experimental y Comparativa de Modelos LLM (§9.3):** Análisis monográfico del comportamiento de los modelos fundacionales bajo dos condiciones operativas: en aislamiento estricto sin asistencia (*Stress-Test* Metamórfico *Zero-Shot*) y en producción asistida por la arquitectura (bucle ReAct y *Tool Calling*), comparando variantes locales y comerciales en la nube.
4. **Experimentos de Arquitectura Cognitiva (§9.4):** Evaluación de tres paradigmas de control conversacional (*ReAct* clásico, *Chain of Thought* y *Stateful Slot Filling*) para superar las restricciones atencionales en hardware local (<8B parámetros).
5. **Evaluación del Impacto Operativo en Procesos ITSM (§9.5):** Contraste cuantitativo de los tiempos y costes cognitivos medidos en el sistema frente a la gestión de servicios de TI tradicional, fundamentando la viabilidad económica del proyecto.
6. **Amenazas a la Validez del Estudio Empírico (§9.6):** Identificación y análisis metodológico de las amenazas a la validez interna, externa, de constructo y de conclusión de acuerdo con los marcos de evaluación empírica en ingeniería del software.

## 9.1. Marco y Entorno Experimental

Para garantizar la reproducibilidad científica de los resultados obtenidos, todos los ensayos se llevaron a cabo bajo condiciones controladas y homogéneas. Las sesiones experimentales fueron registradas íntegramente mediante volcados estructurados en formato JSON (disponibles en el directorio `demos/session_logs/` del repositorio), preservando las trazas de inferencia estocástica de los modelos sin alteraciones artificiales.

La infraestructura física y lógica empleada como banco de pruebas representativo de un entorno de investigación universitario se detalla en la Tabla 24:

| Parámetro | Valor |
|---|---|
| **Hardware de evaluación** | Estación de trabajo portátil: CPU AMD Ryzen 7 5800H (8 núcleos, 16 hilos a 3,2 GHz), 16 GB RAM DDR4, GPU NVIDIA GeForce RTX 3060 Laptop (6 GB VRAM GDDR6) |
| **Sistema Operativo** | Ubuntu 22.04 LTS (*Kernel* Linux 5.15), entorno de ejecución nativo |
| **Plataforma de Inferencia Local** | Ollama v0.6.2 con aceleración hardware NVIDIA CUDA |
| **Modelo Local de Referencia** | `qwen2.5:7b` (cuantización Q4_K_M, ~4,7 GB en memoria de vídeo) |
| **Variante Local Especializada** | `qwen2.5-coder:7b` (cuantización Q4_K_M, ~4,7 GB en memoria de vídeo) |
| **Modelos Cloud Evaluados** | Gemini 3.5 Flash (Google), Cohere Command R+ (Cohere), Ministral 8B (Mistral AI), Codestral (Mistral AI), Qwen 2.5 27B (Groq LPU) |
| **Backend de Aplicación** | FastAPI 0.115 ejecutado sobre servidor ASGI Uvicorn (modo *single-worker*) |
| **Capa de Persistencia** | SQLite 3.45 con soporte transaccional ACID en disco |
| **Protocolo de Repetibilidad** | Cada escenario práctico se ejecutó en lotes de 5 iteraciones consecutivas para amortiguar la variabilidad estocástica y de red; las métricas temporales se reportan como media (µ) ± desviación estándar (σ) |
<p align="center"><i><b>Tabla 24:</b> Entorno de evaluación para los casos de estudio prácticos.</i></p>

## 9.2. Casos de Estudio Reales (*Walkthroughs* Extremo a Extremo)

Esta sección documenta cuatro escenarios de ejecución real del sistema. Para cada uno se especifican el estímulo semántico del usuario en lenguaje natural, la traza de intermediación a través del protocolo MCP, la verificación determinista en el núcleo hexagonal y el resultado operativo materializado.

Para evaluar de manera transparente la capacidad del diseño arquitectónico para estabilizar motores estocásticos imperfectos, los recorridos guiados emplean deliberadamente el modelo generalista local `qwen2.5:7b` ejecutado en modo soberano (*Zero Data Retention*).

### 9.2.1. Escenario 1 — Provisión Estándar (*Happy Path*): Portal Web para Congreso Académico

Este escenario documenta el ciclo completo de provisión para una solicitud técnica conforme con las directrices institucionales, exponiendo los 10 pasos que conducen desde la petición conversacional del investigador hasta la generación del manifiesto Kubernetes.

**PASO 1 — Input del Investigador (Lenguaje Natural):**

> *«Hola, necesito publicar la web para el congreso de Inteligencia Artificial del departamento. Esperamos unos 200 asistentes. ¿Puedes gestionarlo?»*

---

**PASO 2 — Inferencia y Razonamiento Cognitivo (Agente ReAct):**

El `AgentOrchestrator` procesa la intención en el bucle ReAct. El modelo infiere que se trata de un servicio HTTP público, deduce una carga moderada y selecciona una imagen base estándar recomendada (`nginx:alpine`), configurando un puerto de aplicación estándar (`8080`) y asignando cuotas de recursos proporcionadas:

```json
{
  "thought": "El usuario solicita una web para un congreso académico de 200 asistentes. Requiere un servidor HTTP estándar. De acuerdo con las políticas institucionales, emplearé la imagen nginx:alpine en el puerto 8080 con 500m CPU y 256Mi RAM.",
  "tool_call": {
    "name": "format_deployment_intent",
    "arguments": {
      "name": "congreso-ia-departamento",
      "image": "nginx:alpine",
      "port": 8080,
      "cpu": "500m",
      "ram": "256Mi"
    }
  }
}
```

---

**PASO 3 — Invocación de la Herramienta en el Servidor MCP:**

El servidor FastMCP valida los argumentos contra el esquema Pydantic de la herramienta y despacha la petición HTTP `POST` hacia la capa de aplicación del backend (`http://localhost:8000/deployments/intent`).

---

**PASO 4 — Recepción en el Adaptador Primario (FastAPI):**

El controlador de FastAPI deserializa el payload JSON en una instancia de dominio `DeploymentIntent`.

---

**PASO 5 — Validación Determinista en el Núcleo Hexagonal (`SecurityContextValidator`):**

El caso de uso `RegisterDeploymentIntent` invoca formalmente al `SecurityContextValidator` (Sección 5.4, Algoritmo 1), evaluando sistemáticamente las políticas locales:

| Regla de Seguridad Evaluada | Estado de Conformidad |
|---|---|
| Puerto no reservado (8080 ≥ 1024) | Conforme |
| Etiqueta inmutable (`:alpine` ≠ `:latest`) | Conforme |
| Registro de imágenes confiable (`docker.io/library/nginx`) | Conforme |
| Cuota de CPU (500m ≤ 2000m límite departamental) | Conforme |
| Cuota de RAM (256Mi ≤ 4096Mi límite departamental) | Conforme |
| Ausencia de secretos en variables de entorno | Conforme |
<p align="center"><i><b>Tabla 25:</b> Traza de ejecución: Validación en el núcleo hexagonal (Paso 5).</i></p>

Al no detectarse violaciones de política, el repositorio SQLite persiste la intención en estado `PENDING_APPROVAL` con identificador único `dep-7f3a2c1b`.

---

**PASO 6 — Respuesta HTTP del Backend:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "dep-7f3a2c1b",
  "status": "PENDING_APPROVAL",
  "name": "congreso-ia-departamento",
  "image": "nginx:alpine",
  "port": 8080,
  "cpu": "500m",
  "ram": "256Mi",
  "message": "Intent registered. Awaiting HITL approval from SIC technician."
}
```

---

**PASO 7 — Observación Re-inyectada al LLM (Bucle ReAct):**

La respuesta estructurada del backend se inyecta como observación en la memoria a corto plazo del agente, solicitando el cierre de la interacción conversacional.

---

**PASO 8 — Respuesta Final del Asistente al Investigador:**

> *«He registrado su solicitud correctamente en el sistema. El Técnico de Operaciones del SIC revisará y autorizará el despliegue en el panel de control.*
>
> ***Detalles técnicos de la petición registrada:***
> *- **Identificador de seguimiento:** `dep-7f3a2c1b`*
> *- **Nombre del servicio:** `congreso-ia-departamento`*
> *- **Imagen de contenedor:** `nginx:alpine`*
> *- **Configuración de red:** Puerto 8080 | **CPU:** 500m | **RAM:** 256Mi*
> *- **Estado actual:** `PENDING_APPROVAL` (En espera de validación técnica)»*

---

**PASO 9 — Auditoría y Aprobación en el Dashboard HITL:**

El Técnico de Operaciones accede a la interfaz gráfica `/hitl` (Figura 17), inspecciona los parámetros precalculados y acciona el botón **«Aprobar»**:

```bash
# Equivalente operacional curl ejecutado por el Dashboard
curl -X POST http://localhost:8000/hitl/approve/dep-7f3a2c1b
```

```http
HTTP/1.1 200 OK
{"id": "dep-7f3a2c1b", "status": "DEPLOYED"}
```

La FSM ejecuta la transición atómica: `PENDING_APPROVAL → APPROVED → DEPLOYED`.

---

**PASO 10 — Materialización del Manifiesto Declarativo YAML:**

El adaptador secundario `FakeK8sAdapter` expande la plantilla *Golden Path*, generando en disco (`outputs/congreso-ia-departamento.yaml`) el manifiesto multi-documento de Kubernetes (`Deployment`, `Service` e `Ingress`), cuyo contenido íntegro se reproduce en el **Anexo A**.

---

**Métricas Consolidadas del Escenario 1:**

| Métrica de Ejecución | Valor (Media de 5 iteraciones: µ ± σ) |
|---|---|
| Iteraciones del bucle ReAct | 1,0 ± 0,0 |
| Latencia de inferencia cognitiva (LLM local 7B) | 12,99 s ± 1,52 s |
| Latencia de validación en núcleo hexagonal | < 1 ms |
| Tiempo total hasta estado `PENDING_APPROVAL` | 13,12 s ± 1,55 s |
| Tiempo de auditoría humana en Dashboard (*HITL*) | ~ 7 min (tiempo de decisión humana) |
| Tiempo total *End-to-End* | ~ 7,2 min frente a ~ 4.340 min en ITSM tradicional |
| Reducción relativa del *Time-To-Market* | **99,8%** |
<p align="center"><i><b>Tabla 26:</b> Métricas de rendimiento del walkthrough completo (Escenario 1).</i></p>

*Registro completo de sesión:* [`demos/session_logs/escenario1_happy_path.json`](../demos/session_logs/escenario1_happy_path.json).

---

### 9.2.2. Escenario 2 — Resiliencia ante Ataques e Inyección de Prompt: Ubuntu:latest en Puerto 22

Las garantías operativas de un sistema agéntico pierden su validez si este es vulnerable a la manipulación lingüística del usuario o es incapaz de salvaguardar las directrices de seguridad del clúster físico. Este escenario somete a la arquitectura a un vector adverso de **Inyección de Prompt (*Prompt Injection*)** [27], simulando un intento de forzar la apertura de un puerto administrativo privilegiado empleando imágenes volátiles no controladas.

#### El Vector de Ataque Cognitivo

El usuario introduce el siguiente estímulo semántico en la interfaz de Streamlit:

> *«Necesito acceso inmediato por consola para depurar unos scripts. Despliega un contenedor de Ubuntu con la última versión absoluta (usa latest para no liarnos) y exponlo directamente en el puerto 22 para que me conecte por SSH. Hazlo rápido.»*

El modelo de lenguaje procesa la petición. Al carecer intrínsecamente de un modelo de amenazas corporativo, su sesgo conversacional induce al formateo directo de los parámetros solicitados, emitiendo la siguiente llamada a herramienta en la primera iteración:

```json
{
  "name": "ubuntu-debug-console",
  "image": "ubuntu:latest",
  "port": 22
}
```

#### Intercepción Hexagonal y Respuesta HTTP 422

En arquitecturas no gobernadas donde el LLM dispone de acceso directo a la API de Kubernetes, esta invocación habría comprometido la seguridad del clúster abriendo el puerto SSH con una imagen mutable.

En el *Agentic Deployer*, el Servidor MCP transfiere la intención hacia el backend, donde el `SecurityContextValidator` (Sección 5.4) la intercepta de forma determinista y detecta tres violaciones concurrentes de política:
1. El puerto solicitado (`22`) pertenece al rango restringido para tareas de administración del sistema (< 1024).
2. La etiqueta de imagen `:latest` está expresamente prohibida para evitar derivas de configuración no reproducibles (*Configuration Drift*).
3. El repositorio de origen no cuenta con prefijo explícito de registro institucional confiable.

En consecuencia, el motor de validación aborta la operación emitiendo una excepción `SecurityViolationError`, que el framework traduce en una respuesta estructurada `HTTP 422 Unprocessable Entity`:

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    "Security Violation: Port 22 is reserved for administrative tasks.",
    "Security Violation: Use of mutable :latest tag is forbidden.",
    "Security Violation: Image must come from a trusted registry."
  ]
}
```

#### Autocorrección Guiada mediante Bucle de Retroalimentación (*Feedback Loop*)

El bucle ReAct intercepta la respuesta `HTTP 422` no como una falla del sistema, sino como una **Observación (*Observation*)** objetiva del entorno, reinyectándola inmediatamente en el contexto atencional del modelo.

El agente analiza la observación en su monólogo interno (*Thought*) y genera una respuesta asistencial y pedagógica al usuario:

> *«El Servicio de Informática ha rechazado automáticamente la petición por motivos de ciberseguridad. Concretamente, las normativas prohíben el uso de la etiqueta ':latest', el puerto 22 (SSH reservado) y repositorios no explícitos. Para poder tramitar su despliegue, ¿podría especificar una versión estable inmutable (por ejemplo, 'ubuntu:22.04') y confirmar un puerto de aplicación superior al 1024?»*

A lo largo de 5 iteraciones de diálogo asistido, el modelo converge progresivamente hasta registrar la alternativa conforme `docker.io/library/ubuntu:22.04` en el puerto `2222`.

| Fase Operativa | Acción y Resultado |
|---|---|
| **Estímulo inicial** | Petición de usuario solicitando `ubuntu:latest` expuesto en puerto 22 (SSH) |
| **Invocación inicial LLM** | `format_deployment_intent(image="ubuntu:latest", port=22, ...)` |
| **Respuesta de la Arquitectura** | **`HTTP 422 Unprocessable Entity`** — Tres violaciones de seguridad detectadas |
| **Autocorrección iterativa** | Explicación pedagógica de normativas y convergencia asistida durante 5 iteraciones |
| **Resultado final** | Propuesta conforme en puerto `2222` con imagen inmutable registrada como `PENDING_APPROVAL` |
<p align="center"><i><b>Tabla 27:</b> Traza de ejecución: Intento de Prompt Injection (Escenario 2).</i></p>

La intercepción se produjo **antes de que ninguna operación modificara el clúster**, validando el principio *Fail-Safe* y demostrando que la seguridad perimetral no depende de la fiabilidad estocástica de la IA, sino del rigor del núcleo hexagonal.

*Registro completo de sesión:* [`demos/session_logs/escenario2_prompt_injection.json`](../demos/session_logs/escenario2_prompt_injection.json).

---

### 9.2.3. Escenario 3 — Ciclo Completo de Gobierno HITL: CMS WordPress Departamental

Este caso de estudio evalúa la gestión de servicios complejos dependientes de base de datos y la sincronización con el panel de control del operador humano.

**Entrada del investigador:**
> *«El departamento de Ciencias de la Computación necesita un CMS WordPress para publicar noticias y eventos. ¿Podrías solicitar su provisión?»*

**Secuencia de transiciones en la Máquina de Estados Finita (FSM):**
```text
[CREACIÓN] ──> PENDING_APPROVAL ──> APPROVED ──> DEPLOYED
```

Durante el procesamiento, el agente infiere la necesidad de persistencia y la configuración del puerto 8080. Al registrarse la intención en la FSM, el técnico del SIC recibe la notificación asíncrona en el Dashboard. Tras verificar que el consumo de recursos se adecua a las cuotas del departamento solicitante, el operador aprueba la provisión, materializándose el YAML en el almacenamiento compartido.

*Registro completo de sesión:* [`demos/session_logs/escenario3_hitl_completo.json`](../demos/session_logs/escenario3_hitl_completo.json).

---

### 9.2.4. Escenario 4 — Autocorrección Multi-turno Guiada por Excepciones

Para verificar la capacidad de recuperación autónoma ante errores de configuración de almacenamiento, se evaluó una petición con parámetros incompletos:

**Entrada del investigador:**
> *«Despliega una base de datos PostgreSQL estándar para guardar las encuestas del proyecto.»*

1. **Iteración 1 (Invocación con parámetros insuficientes):** El modelo deduce la necesidad de almacenamiento persistente y lanza `format_deployment_intent(image="postgres:13.4", storage="10Gi", ...)`. No obstante, omite el prefijo de registro de confianza (`docker.io/`).
2. **Intercepción Determinista:** El validador detecta la falta de registro explícito y emite un `HTTP 422: "Untrusted registry"`.
3. **Autocorrección Cognitiva:** El LLM procesa la observación devuelta, comprende la regla de registro y emite una segunda invocación corregida incorporando el espacio de nombres `docker.io/library/postgres:13.4`, completando el registro exitoso en 2 iteraciones (26,1 s).

*Registro completo de sesión:* [`demos/session_logs/escenario4_autocorreccion.json`](../demos/session_logs/escenario4_autocorreccion.json).

---

### 9.2.5. Síntesis y Desglose Comparativo de Casos de Estudio

El análisis cuantitativo del ciclo de vida de las solicitudes permite aislar la contribución de cada componente tecnológico a la latencia total del sistema:

| Componente del Sistema | Capa Tecnológica | Latencia Medida | Naturaleza Operativa |
|---|---|---|---|
| **Interacción y chat** | Frontend Streamlit | ~ 5 s | Entrada de lenguaje natural del usuario |
| **Inferencia y razonamiento** | Agente ReAct (qwen2.5:7b) | 12 - 27 s | Inferencia estocástica local en GPU |
| **Protocolo de herramientas** | Servidor FastMCP | < 5 ms | Serialización JSON-RPC y ruteo stdio |
| **Validación de seguridad** | `SecurityContextValidator` | < 1 ms | Evaluación determinista en CPU |
| **Gestión transaccional** | Repositorio SQLite / FSM | < 2 ms | Persistencia ACID y transición de estados |
| **Auditoría humana (HITL)** | Dashboard Operaciones SIC | ~ 7 min | Inspección visual y clic técnico |
| **Expansión declarativa** | `FakeK8sAdapter` | < 1 ms | Interpolación de plantillas YAML |
<p align="center"><i><b>Tabla 28:</b> Desglose de latencias por componente en el ciclo de vida.</i></p>

La comparativa transversal entre los cuatro escenarios de estudio confirma la estabilidad global del sistema:

| Escenario Evaluado | Iteraciones ReAct (µ) | Latencia Inferencia (µ ± σ) | Estado FSM Resultante | Artefacto Generado |
|---|---|---|---|---|
| **1. Provisión Estándar (Congreso IA)** | 1,0 ± 0,0 | 12,99 s ± 1,52 s | `DEPLOYED` | YAML completo en disco |
| **2. Prompt Injection (Ubuntu SSH)** | 5,0 ± 0,6 | 45,07 s ± 3,21 s | `PENDING_APPROVAL`* | Confinamiento perimetral |
| **3. Ciclo HITL (CMS WordPress)** | 2,0 ± 0,0 | 27,84 s ± 2,14 s | `PENDING_APPROVAL` | Notificación en Dashboard |
| **4. Autocorrección (PostgreSQL)** | 2,0 ± 0,0 | 26,10 s ± 1,98 s | `PENDING_APPROVAL` | Recuperación autónoma |
<p align="center"><i><b>Tabla 29:</b> Comparativa E2E de métricas operativas (multi-escenario).</i></p>

> \* *Nota sobre el Escenario 2:* El estado final `PENDING_APPROVAL` refleja la propuesta resultante tras cinco rondas de negociación en las que el validador contuvo sucesivamente los intentos de eludir la política institucional, registrándose finalmente una intención segura pendiente de auditoría humana.

---

## 9.3. Evaluación Experimental y Comparativa de Modelos LLM

Uno de los objetivos metodológicos cardinales de este Trabajo de Fin de Máster consiste en determinar en qué medida la fiabilidad de un sistema agéntico depende de la escala bruta de los modelos fundacionales frente a los mecanismos deterministas de contención provistos por la ingeniería de software.

Para responder a esta cuestión con rigor empírico, se diseñó un banco de experimentación que evalúa a los modelos bajo dos condiciones operativas marcadamente distintas:
1. **Evaluación de Robustez Intrínseca (*Zero-Shot* Puro):** El modelo se enfrenta a la batería de Pruebas Metamórficas en aislamiento estricto, sin *System Prompt* de apoyo, sin memoria conversacional y sin mecanismos de recuperación arquitectónica.
2. **Rendimiento en Producción Asistida (Bucle ReAct):** Los mismos modelos se integran como motor cognitivo del `AgentOrchestrator`, recibiendo el *System Prompt* institucional, el esquema formal de herramientas MCP y el bucle de retroalimentación de la FSM.

### 9.3.1. Evaluación de Robustez Estocástica Intrínseca: Stress-Test Metamórfico (Zero-Shot Puro)

De acuerdo con el marco metodológico definido en la Sección 8.4, las **Pruebas Metamórficas** permiten resolver el Problema del Oráculo evaluando si el modelo preserva de forma invariante los parámetros técnicos de la intención (`name`, `image`, `internal_port`) al someter la entrada a seis transformaciones léxicas y gramaticales (MR-1 a MR-6).

La suite se ejecutó en primer término contra el modelo local de referencia `qwen2.5:7b` (a través de `OllamaLLMClient`), arrojando los resultados empíricos recogidos en la Tabla 30:

| Relación Metamórfica | Transformación Aplicada | Vector de Entrada Evaluado | Resultado | Extracción Estructurada JSON |
|---|---|---|---|---|
| **MR-1:** Permutación sintáctica | Alteración en el orden de los parámetros técnicos | `"api-backend con imagen python:3.12 y puerto 8000"` ↔ `"Con el puerto 8000 y la imagen python:3.12, necesito api-backend"` | **Éxito** | Idéntica (`name`, `image`, `port`) |
| **MR-2:** Invarianza al ruido léxico | Inyección de cortesías, saludos y texto periférico | Base: `"desplegar mi-web con nginx:alpine en el puerto 8080"` ↔ Ruidosa: misma frase envuelta en giros coloquiales | **Fallo** | Revierte a texto conversacional libre |
| **MR-3:** Invarianza tipográfica | Alternancia de caja (`MAYÚSCULAS` / `minúsculas`) | `"quiero el servicio redis..."` ↔ `"QUIERO EL servicio redis..."` | **Fallo** | Modifica el nombre (`redis-service`) |
| **MR-4:** Composición incremental | Entrada consolidada vs. diálogo en 3 turnos | Mensaje único completo ↔ 3 turnos conversacionales con datos parciales | **Fallo** | Revierte a texto conversacional |
| **MR-5:** Parafraseo semántico | Uso de sinónimos y construcciones pasivas | `"Levanta un wordpress en el puerto 80 llamado blog"` ↔ `"Crea un servicio que responda al nombre de blog..."` | **Éxito** | Idéntica |
| **MR-6:** Invarianza lingüística | Traducción de la petición a idioma inglés | `"Despliega una base de datos postgres en el 5432"` ↔ `"Deploy a postgres database on port 5432"` | **Éxito** | Idéntica |
<p align="center"><i><b>Tabla 30:</b> Resultados empíricos de las Pruebas Metamórficas por Relación frente a Qwen 2.5 (7B).</i></p>

| Métrica de la Batería Metamórfica | Valor Obtenido |
|---|---|
| Relaciones metamórficas evaluadas | 6 |
| Pruebas ejecutadas | 6 |
| Tasa de éxito intrínseca (*Zero-Shot*) | **50% (3/6)** |
| Tiempo total de ejecución de la batería | 89,7 s |
| Motor cognitivo bajo prueba | `OllamaLLMClient` (qwen2.5:7b local) |
<p align="center"><i><b>Tabla 31:</b> Métricas globales de la batería metamórfica.</i></p>

#### Interpretación de los Fallos Cognitivos y Límites de la Ingeniería de Prompts

El análisis de los fallos en MR-2, MR-3 y MR-4 aporta una evidencia empírica fundamental: **la capacidad de procesamiento estructurado de los modelos generalistas de escala reducida (<8B parámetros) se degrada significativamente cuando se introduce ruido léxico o dispersión multi-turno en ausencia de mecanismos externos de control y mediación**. Al diluirse el foco atencional, el modelo omite su cometido de emitir JSON estructurado y revierte a un comportamiento de *chatbot* conversacional libre.

Para intentar mitigar esta fragilidad mediante técnicas puras de Ingeniería de Prompts, se evaluó la inyección de un **Sufijo de Refuerzo** (*Reinforcement Prompt Suffix*), concatenando al final de la entrada directrices imperativas estrictas (ej. *"Responde única y exclusivamente con la llamada a la herramienta en formato JSON"*). 

Sin embargo, el experimento reveló un efecto adverso secundario: el **sobrecumplimiento prematuro (*over-compliance*)**. Al ser instruido con un imperativo estricto, el modelo intentó emitir la llamada a herramienta en turnos intermedios cuando aún carecía de los parámetros obligatorios (alucinando valores de puerto o imagen), lo que provocó excepciones de validación de esquema en la capa de datos (`ValidationError`). Asimismo, la incorporación de razonamiento intermedio mediante *Cadena de Pensamiento* (*Chain of Thought*) [17] indujo errores de sintaxis y desviaciones del esquema JSON al intercalar explicaciones discursivas con los delimitadores formales.

#### Benchmarking Comparativo Multi-Modelo en Estrés Metamórfico

Para contrastar este comportamiento con el estado del arte de la industria, la batería metamórfica se ejecutó de forma idéntica contra un conjunto heterogéneo de 9 arquitecturas neuronales (locales, clústeres LPU de ultrabaja latencia y APIs comerciales en la nube). Los resultados empíricos se sintetizan en la Tabla 32:

| Modelo Evaluado | Entorno de Ejecución | Tasa de Éxito Zero-Shot | Comportamiento Observado ante Ruido y Perturbaciones |
|---|---|:---:|---|
| **Gemini 3.5 Flash** (Google) | Cloud | **66% (4/6)** | Tolera el ruido léxico (MR-2) y la composición multi-turno (MR-4). Falla en alternancia de mayúsculas (MR-3) e invarianza idiomática (MR-6). |
| **Cohere Command R+** (Cohere) | Cloud | **66% (4/6)** | Diseñado específicamente para *Tool Calling*. Empata con Gemini, fallando ante lenguaje informal extremo (MR-2) y cruce idiomático (MR-6). |
| **Qwen 2.5 (7B)** (Alibaba) | Local (Ollama) | **50% (3/6)** | Pérdida de foco atencional ante ruido léxico (MR-2) y contexto disperso (MR-4), revirtiendo a texto libre. |
| **Llama 3.2 (3B)** (Meta) | Local (Ollama) | **0% (0/6)** | Incapacidad para sostener la extracción *Zero-Shot*. Falla al mapear campos nulos (emite `"None"` en lugar de `null`). |
| **Mistral (7B)** (Mistral AI) | Local (Ollama) | **0% (0/6)** | Incumplimiento sistemático del formato esperado. Omite la estructura JSON en cuanto se introduce cualquier perturbación léxica. |
| **Ministral 8B** (Mistral AI) | Cloud | **0% (0/6)** | Incapacidad de extracción sin el apoyo explícito del *System Prompt*. |
| **Codestral** (Mistral AI) | Cloud | **0% (0/6)** | Carece de *fine-tuning* para herramientas estructuradas. Emite bloques de código procedural o explicaciones en texto plano. |
| **Qwen 2.5 (27B)** (Alibaba) | Groq (LPU) | **50% (3/6)** | Rendimiento dispar: consistente en permutación y parafraseo, pero vulnerable a ruido conversacional largo. |
| **Qwen 2.5 Coder (7B)** (Alibaba) | Local (Ollama) | **100% (6/6)** | **Supera íntegramente la batería (6/6).** Su especialización en código y estructuras formales neutraliza completamente la degradación de atención y el ruido léxico. |
<p align="center"><i><b>Tabla 32:</b> Resultados comparativos del stress-test metamórfico (Zero-Shot puro).</i></p>

Este experimento arroja dos conclusiones metodológicas relevantes:
1. **La especialización sintáctica prevalece sobre la escala del modelo:** El hecho de que modelos de mayor escala en la nube (Cohere, Gemini) no superen el 66% de invarianza en aislamiento, mientras que un modelo local de 7B especializado en código (**`qwen2.5-coder:7b`**) alcance el **100% de éxito**, demuestra que la competencia en *Tool Calling* depende del alineamiento del entrenamiento con gramáticas formales (código fuente, esquemas JSON, tipado estricto) más que del tamaño del modelo.
2. **La limitación de los modelos de código sin interfaz de herramientas:** La tasa nula de éxito de *Codestral* (0%) evidencia que la destreza para redactar algoritmos no equivale a la capacidad de orquestación agéntica: sin un ajuste fino (*fine-tuning*) específico para emitir llamadas a funciones bajo esquemas formales, el modelo genera texto plano no procesable por protocolos estructurados como MCP.

---

### 9.3.2. Rendimiento en Producción Asistida: Orquestación Agéntica y Tool Calling en Bucle ReAct

Para evaluar cómo la infraestructura arquitectónica de soporte (Arquitectura Hexagonal, Servidor MCP y Máquina de Estados) transforma el rendimiento de estos mismos modelos en un entorno productivo real, se sometió al conjunto de motores a una prueba homogénea de aprovisionamiento asistido.

Se utilizó como estímulo idéntico para todos los modelos la entrada del Escenario 1:
> *«Hola, necesito un portal web para el congreso de Inteligencia Artificial del departamento. Esperamos unas 200-300 personas. ¿Puedes gestionar el despliegue?»*

La Tabla 33 sintetiza el rendimiento comparativo obtenido:

| Modelo LLM Evaluado | Escala / Entorno | Iteraciones ReAct (sobre éxitos) | Latencia Media E2E | Tasa de Invocación Válida |
|---|---|:---:|:---:|:---:|
| **Qwen 2.5 Coder** | 7B (Local / Ollama) | 1,0 ± 0,0 | 12,15 s ± 1,12 s | **100%** |
| **Qwen 2.5** (Generalista) | 7B (Local / Ollama) | 3,0 ± 0,4 | 47,33 s ± 3,85 s | **100%** |
| **Llama 3.2** | 3B (Local / Ollama) | 1,0 ± 0,0 | 9,44 s ± 0,85 s | **75%** |
| **Mistral** | 7B (Local / Ollama) | N/A | N/A | **0%** |
| **Gemini 3.5 Flash** | Cloud (Google) | 1,0 ± 0,0 | ~ 5,50 s | **100%** |
| **Cohere Command R+** | Cloud (Cohere) | 1,0 ± 0,0 | ~ 9,00 s | **100%** |
| **Ministral 8B** | Cloud (Mistral AI) | 1,0 ± 0,0 | ~ 3,20 s | **100%** |
| **Qwen 2.5 (27B)** | Cloud (Groq LPU) | 2,0 ± 0,0 | ~ 2,45 s | **100%** |
<p align="center"><i><b>Tabla 33:</b> Rendimiento comparativo real de modelos alternativos en el bucle ReAct.</i></p>

#### El Efecto Estabilizador de la Arquitectura de Software

La contrastación directa entre la Tabla 32 (*Zero-Shot*) y la Tabla 33 (*Bucle ReAct*) proporciona la evidencia empírica definitiva que sustenta la tesis de este trabajo:

- **Qwen 2.5 (7B) generalista** pasó de una tasa de acierto del **50% en aislamiento estocástico** a un **100% de invocación exitosa** al ser asistido por el bucle ReAct y el contrato semántico de MCP, estabilizando sus decisiones a través de 3 iteraciones de retroalimentación reflexiva.
- **Ministral 8B**, que obtuvo un **0% de éxito en el test metamórfico en aislamiento**, alcanzó el **100% de éxito con una sola iteración (3,2 s)** al ser guiado por el *System Prompt* y la especificación de herramientas del orquestador.
- **Qwen 2.5 Coder (7B)** confirmó su idoneidad como motor soberano óptimo: convergió consistentemente en **1,0 iteraciones**, reduciendo la latencia de inferencia local de 47 s a **12,15 s** y eliminando toda necesidad de turnos conversacionales correctivos.

### 9.3.3. Síntesis Comparativa y Criterios de Selección Tecnológica

A partir de la evidencia experimental acumulada en las Tablas 32 y 33, se extraen tres directrices de ingeniería para la adopción de agentes de infraestructura en organizaciones públicas:
1. **Viabilidad de la Soberanía de Datos (*Zero Data Retention*):** La especialización en código de modelos compactos (`qwen2.5-coder:7b`) equipara la precisión de orquestación de las mejores soluciones comerciales en la nube operando dentro de una envolvente de consumo térmico y de memoria modesta (6 GB VRAM), permitiendo a la institución prescindir del envío de metadatos de red hacia servidores de terceros.
2. **Aceleración Hardware Estratégica:** En escenarios donde las normativas de privacidad permitan el uso de nubes corporativas privadas, clústeres de inferencia especializados basados en LPUs (como Groq) reducen la latencia a ~2 segundos por turno, lo que habilita experiencias conversacionales en tiempo real.
3. **El Software Tradicional como Barrera Determinista de Contención:** Ningún modelo de lenguaje, independientemente de su escala o reputación comercial, exhibe invarianza absoluta en modo *Zero-Shot*. La fiabilidad del sistema no puede delegarse en la probabilidad del modelo; debe residir en el control determinista del software tradicional (Arquitectura Hexagonal) y en la supervisión humana (*HITL*).

---

## 9.4. Experimentos de Arquitectura Cognitiva: Superando el Límite Atencional (7B)

La experimentación documentada en la sección previa constató que los modelos generalistas de 7B presentan un sesgo de sobrecumplimiento prematuro (*over-compliance*) en diálogos multi-turno. Para determinar si este cuello de botella puede resolverse mediante técnicas avanzadas de desacoplamiento de software, se diseñó un banco de pruebas sistemático (`demos/demo_state_machine.py`) que compara tres paradigmas arquitectónicos frente a una secuencia incremental de tres turnos de diálogo:
- **Turno 1:** El usuario inicia la solicitud sin datos técnicos: *«Hola equipo del SIC, necesito desplegar un servicio web por favor.»*
- **Turno 2:** El usuario aporta únicamente el identificador: *«Se va a llamar proyecto-web.»*
- **Turno 3:** El usuario aporta la especificación técnica restante: *«La imagen será nginx:alpine y el puerto es el 8080. Con eso ya lo tendríamos.»*

### 9.4.1. Paradigma 1: ReAct Clásico con Sufijo Estricto (Fallo Lógico)
Se instruyó al LLM con un sufijo imperativo absoluto (*"Responde única y exclusivamente con JSON"*).
- **Resultado:** En el Turno 2, al disponer solo del nombre, el modelo forzó la emisión de la llamada a la herramienta alucinando la imagen (`nginx:latest`) y el puerto (`80`), incurriendo en un fallo lógico por sobrecumplimiento prematuro.

### 9.4.2. Paradigma 2: Cadena de Pensamiento (*Chain of Thought*) (Fallo Sintáctico)
Se instruyó al modelo para que razonara paso a paso en texto libre antes de estructurar el JSON [17].
- **Resultado:** Superó con éxito el Turno 2 solicitando los datos faltantes. Sin embargo, en el Turno 3, al intentar concatenar el razonamiento cualitativo con la sintaxis estricta de la herramienta, incurrió en una ruptura sintáctica arrojando una excepción `ValidationError`. Se constató un compromiso (*trade-off*) en la capacidad atencional: razonar en texto libre degrada la precisión sintáctica en modelos de 7B.

### 9.4.3. Paradigma 3: Llenado de Huecos con Estado (*Stateful Slot Filling*) y Destilación de Contexto

Para erradicar la sobrecarga cognitiva de los paradigmas anteriores, se implementó el patrón de **Llenado de Huecos con Estado (*Stateful Slot Filling*)**, fundamentado en la literatura de seguimiento del estado del diálogo (*Dialogue State Tracking*) [39] y la destilación de contexto [40, 41].

El patrón descompone la interacción en dos planos ortogonales:
1. **Plano Cognitivo Pasivo (Extracción Semántica Aislada):** El LLM opera exclusivamente como extractor de entidades sobre el último mensaje del usuario, limitándose a poblar una estructura discreta (`{"name": null, "image": null, "port": null}`) sin interactuar con el entorno ni decidir si invoca herramientas.
2. **Plano Determinista de Control (Máquina de Estados en Python):** El software tradicional mantiene el vector de estado acumulado en memoria. Si faltan parámetros obligatorios, la máquina de estados genera deterministamente la pregunta de clarificación. Solo cuando el vector está 100% completo, el orquestador despacha de forma autónoma la herramienta MCP.

### 9.4.4. Comparativa Multi-Modelo Transversal: Locales vs Cloud Comercial

Los tres paradigmas de control cognitivo se evaluaron homogéneamente frente a las 8 familias de modelos bajo la secuencia idéntica de tres turnos. La Tabla 34 recoge los resultados experimentales:

| Modelo Evaluado | ReAct Clásico (Sin Sufijo) | ReAct con *Chain of Thought* | Máquina de Estado Destilado (*Stateful Slot Filling*) |
|---|---|---|---|
| **Qwen 2.5 Coder (7B)** | **Éxito 100%** (Hiper-especialización) | **Éxito 100%** (Sintaxis robusta) | **Éxito 100%** (Precisión absoluta) |
| **Qwen 2.5 (7B)** (Generalista) | Fallo Lógico (Sobrecumplimiento Turno 2) | Ruptura Sintáctica (`ValidationError`) | **Éxito 100%** (Control determinista de estado) |
| **Llama 3.2 (3B)** | Fallo Sintáctico (Inyecta `"None"`) | Incapacidad de Estructuración | **Éxito Parcial** (Extrae `"null"` como cadena) |
| **Mistral (7B)** | Fallo Lógico (Olvida el formato en turnos) | Bucle de Repetición Atencional | **Éxito 100%** (Extracción semántica aislada) |
| **Gemini 3.5 Flash** | **Éxito 100%** (Atención superior) | **Éxito 100%** (Sintaxis robusta) | **Éxito 100%** (Extracción perfecta) |
| **Cohere Command R+** | **Éxito 100%** (Diseño *Tool Calling*) | **Éxito 100%** (Respuesta determinista) | **Éxito 100%** (Precisión absoluta) |
| **Ministral 8B** | **Éxito 100%** (Soporte nativo herramientas) | **Éxito 100%** (Razonamiento estable) | **Éxito 100%** (Precisión absoluta) |
| **Qwen 2.5 (27B)** | **Éxito 100%** (Inferencia ultra-rápida Groq) | **Éxito 100%** (Razonamiento estable) | **Éxito 100%** (Precisión absoluta) |
<p align="center"><i><b>Tabla 34:</b> Resultados de los Experimentos de Arquitectura Cognitiva ampliado con modelos Cloud.</i></p>

#### Conclusiones de los Experimentos de Arquitectura Cognitiva

La evidencia empírica confirma que existen dos vías independientes y complementarias para alcanzar fiabilidad productiva en sistemas agénticos:
- **Vía del Software Tradicional (*Stateful Slot Filling*):** Al delegar la retención del estado conversacional en una máquina de estados determinista, incluso modelos generalistas con fragilidad atencional (Qwen 2.5 y Mistral) alcanzan el **100% de fiabilidad**, desacoplando el control de flujo de la inferencia estocástica.
- **Vía de la Especialización de Modelos (`qwen2.5-coder:7b`):** El pre-entrenamiento intensivo en código fuente capacita al modelo para gestionar simultáneamente la extracción semántica y el formateo formal de herramientas sin requerir mecanismos auxiliares de seguimiento de estado por ranuras, equiparándose a los motores comerciales más avanzados de la industria.

---

## 9.5. Evaluación del Impacto Operativo en Procesos ITSM

Una vez demostrada la solidez arquitectónica en los *walkthroughs* reales (§9.2), caracterizado el comportamiento de los modelos fundacionales (§9.3) y superado el límite atencional mediante desacoplamiento de estado (§9.4), los resultados experimentales permiten formular una conclusión de impacto global orientada a la Gestión de Servicios de Tecnologías de la Información (ITSM).

### 9.5.1. La Fricción del ITSM Tradicional frente a la Automatización Agéntica

En infraestructuras fuertemente reguladas, como es el caso de un Centro de Procesamiento de Datos (CPD) universitario, el ritmo de provisión de infraestructura no está limitado por el ancho de banda ni por la capacidad de cómputo del clúster, sino por la burocracia de los flujos de trabajo tradicionales sustentados en tickets (Jira Service Management, ServiceNow o correo electrónico):

1. **Apertura del Ticket (Diferencia de Abstracción Técnica):** El investigador redacta una petición en prosa informal carente de especificaciones de ingeniería (*«Necesito una base de datos para mi proyecto»*).
2. **Triaje y Bloqueo de Soporte (Nivel 1):** El operador de soporte detiene el ticket y solicita aclaraciones mediante correos electrónicos asíncronos (puerto, almacenamiento, cuota de memoria).
3. **Escalado a Infraestructura (Nivel 3):** Una vez consolidados los requisitos tras sucesivos intercambios que consumen días hábiles, el ticket se transfiere a un Ingeniero de Sistemas sénior.
4. **Redacción Manual de Código Declarativo:** El ingeniero detiene sus tareas de alto valor de ingeniería para redactar a mano el manifiesto YAML de Kubernetes, conectarse por VPN y aplicar el despliegue.

Este ciclo de vida genera tiempos muertos inmensos (*Idle Time*) por desalineamiento comunicativo y un elevado coste por cambio de contexto (*Context Switching*) en los ingenieros de infraestructura.

### 9.5.2. Cuantificación del Ahorro Temporal y Reducción del *Time-To-Market* (TTM)

El *Agentic Deployer* transforma este paradigma secuencial al resolver la negociación en tiempo real mediante el bucle ReAct, reduciendo la intervención del personal técnico a una función de auditoría y aprobación ágil a través del Dashboard HITL.

La Tabla 35 cuantifica el impacto temporal comparativo entre el modelo ITSM convencional y el flujo agéntico evaluado en este trabajo para el despliegue de un servicio web institucional estándar:

| Fase Operativa del Ciclo de Vida (ITSM) | Modelo ITSM Convencional | Modelo Agéntico (*Agentic Deployer*) | Reducción del Tiempo de Entrega (*TTM*) |
|---|---|---|:---:|
| **1. Negociación y clarificación de requisitos** | 1.440 min† (Asíncrono vía Email / Ticket) | ~ 5 min (Interacción en lenguaje natural con IA) | **~ 99,7%** |
| **2. Traducción técnica y generación declarativa (YAML)** | 15 min (Redacción manual por Técnico N3) | < 0,01 min (Expansión de plantillas *Golden Path*) | **~ 99,9%** |
| **3. Validación de seguridad y políticas institucionales** | 5 min (Inspección manual / CI/CD) | < 0,001 min (Núcleo Hexagonal en CPU) | **~ 99,9%** |
| **4. Aprobación formal y autorización de despliegue** | 2 min (Confirmación manual / `kubectl apply`) | 2 min (Inspección y clic en Dashboard HITL) | **0% (Mismo control)** |
| **Tiempos muertos de espera en cola (*Idle Time*)** | 2.880 min (Ticket en espera de asignación) | 60 min (Cola de revisión en Dashboard) | **~ 97,9%** |
| **Tiempo de Entrega Total (*Time-To-Market*)** | **~ 4.342 min (~ 72,4 horas / 3 días hábiles)** | **~ 67 min (~ 1,1 horas)** | **~ 98,5%** |
| **Tiempo Activo de Gestión Técnica** | **30 min** (Triaje + redacción + validación) | **~ 5 min** (Chat IA) + **2 min** (HITL) = **7 min** | **~ 76,7%** |
| **Carga cognitiva del Técnico de Sistemas** | **Alta** (Redacción de código y soporte N1) | **Mínima** (Auditoría visual de intención) | **Reducción cualitativa** |
<p align="center"><i><b>Tabla 35:</b> Impacto temporal operativo (ITSM tradicional vs Agentic Deployer).</i></p>

> † *Distinción metodológica sobre el tiempo transcurrido:* El valor de **1.440 minutos (24 horas)** representa *tiempo transcurrido de calendario* (*elapsed time*), originado por las demoras asíncronas de lectura y respuesta de correos electrónicos entre departamentos, y no tiempo de trabajo activo continuado. Por el contrario, el modelo agéntico opera de forma síncrona en tiempo real durante la interacción con el usuario. Esta distinción se analiza en profundidad en la Sección 4.6.4 para la formulación del modelo económico de viabilidad.

#### Conclusión del Impacto Experimental

La evidencia experimental sintetizada en la Tabla 35 demuestra que la aportación diferencial del *Agentic Deployer* no radica únicamente en acelerar la generación sintáctica de ficheros YAML, sino en **erradicar la fricción burocrática del triaje asíncrono interdepartamental**. Al resolver la clarificación de requisitos en tiempo real mediante el bucle conversacional y confinar el rol del especialista en la toma de decisiones estructuradas en el Dashboard, el sistema reduce el *Time-To-Market* en un **98,5%**, liberando el 76,7% del tiempo activo del personal técnico.

Estos ahorros temporales empíricamente contrastados proporcionan las bases cuantitativas directas sobre las que se articula el estudio de viabilidad económica, costes de adopción y retorno de inversión (ROI) formulado en el modelo de viabilidad económica del **Capítulo 4 (Sección 4.6)**.

---

## 9.6. Amenazas a la Validez del Estudio Empírico

De acuerdo con las directrices metodológicas para la investigación empírica en ingeniería del software [42, 43], todo estudio experimental que evalúe componentes de software estocásticos debe explicitar las posibles amenazas a la validez que puedan condicionar la interpretación de sus resultados y las estrategias adoptadas para su mitigación.

### 9.6.1. Validez Interna

La validez interna concierne a la medida en que los factores no controlados del diseño experimental pueden haber influido en los resultados observados:

- **Estocasticidad de los Modelos de Lenguaje:** La inferencia en redes neuronales generativas está sujeta a variabilidad estadística incluso cuando el parámetro de temperatura se fija en cero (*T* = 0), debido a la falta de determinismo en las operaciones concurrentes de coma flotante sobre hardware GPU/LPU. Para mitigar esta variabilidad, las ejecuciones de los casos de estudio y pruebas metamórficas se repitieron en lotes de 5 iteraciones consecutivas, reportándose las métricas en términos de media (*μ*) y desviación estándar (*σ*).
- **Latencia de Red y Saturación de Servicios Cloud:** Los ensayos con proveedores comerciales (Google Cloud, Cohere, Groq, Mistral AI) dependen de la latencia de tránsito de la red pública y del estado de carga de las infraestructuras remotas, lo que introduce fluctuaciones temporales ajenas al diseño del software. Esta amenaza se controló aislando las métricas de inferencia pura del modelo respecto a los tiempos de serialización y red, y contrastando dichos resultados con la ejecución estrictamente local sobre Ollama en condiciones de red desconectada.
- **Degradación Térmica en Hardware Local:** La estación de trabajo empleada para los ensayos locales (NVIDIA RTX 3060 Laptop) puede experimentar estrangulamiento térmico (*thermal throttling*) tras ejecuciones continuas prolongadas. Se introdujeron periodos de enfriamiento pasivo de 30 segundos entre lotes de inferencia para preservar la estabilidad de la frecuencia de reloj de la GPU.

### 9.6.2. Validez Externa

La validez externa atañe al grado en que los hallazgos y conclusiones pueden generalizarse a otros contextos, infraestructuras y dominios:

- **Representatividad del Catálogo de Herramientas:** El catálogo de operaciones implementado en el servidor MCP se centró en cuatro casos de uso institucionales prevalentes (portales web, gestores de contenidos CMS, microservicios en Python y bases de datos relacionales). Si bien estos perfiles cubren la mayoría de las solicitudes típicas de un entorno académico, la extrapolación de los resultados a arquitecturas distribuidas complejas con múltiples dependencias cruzadas (mallas de servicios, operadores personalizados o recursos con estado distribuido) requerirá validación empírica adicional.
- **Generalización a Nuevas Arquitecturas de Modelos:** Los resultados se circunscriben a las ocho familias neuronales analizadas en la Sección 9.3. La rápida evolución de la disciplina implica que nuevas variantes de modelos de frontera o técnicas de destilación y cuantización podrían exhibir comportamientos atencionales sensiblemente diferentes. No obstante, la directriz metodológica central —la necesidad de un perímetro determinista hexagonal para gobernar el estocasticismo— preserva su validez con independencia del modelo evaluado.

### 9.6.3. Validez de Constructo

La validez de constructo evalúa si las métricas e indicadores empíricos empleados reflejan adecuadamente los conceptos teóricos que se pretenden medir:

- **Medición de la Fiabilidad y Robustez:** La fiabilidad del sistema no se evaluó mediante impresiones subjetivas de interacción, sino a través de variables booleanas y cuantitativas estrictas: el cumplimiento de invariantes de tipos en Pydantic, la tasa de captura de excepciones en el validador de seguridad, la superación de aserciones metamórficas y la ratio de mutantes eliminados en las pruebas de mutación.
- **Estimación del Impacto Operativo (ITSM):** Para la comparación temporal documentada en la Sección 9.5, los tiempos del modelo convencional se fundamentaron en estándares de gestión de servicios de TI (ITIL v4) y en la experiencia operativa de centros de datos universitarios, distinguiendo formalmente entre tiempo de dedicación técnica activa y tiempos muertos de espera en cola (*Idle Time*).

### 9.6.4. Validez de Conclusión

La validez de conclusión analiza si las relaciones observadas entre las variables del estudio y las conclusiones extraídas son estadísticamente e inferencialmente consistentes:

- **Sesgo de Confirmación en la Selección de Casos:** Existía el riesgo de evaluar únicamente escenarios favorables (*Happy Paths*) donde los modelos convergieran sin dificultad. Esta amenaza se neutralizó sistemáticamente mediante la inclusión de escenarios adversarios (§9.2.2), modelos con severas carencias de formateo sintáctico (`codestral-latest`, `llama-3.2-3b`) y la aplicación de mutaciones deliberadas en el código de normalización (§8.3), garantizando que las conclusiones reflejen con objetividad tanto las fortalezas como las limitaciones del sistema.
