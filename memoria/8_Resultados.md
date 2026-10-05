# Capítulo 8. Resultados y Casos de Estudio Prácticos

El rigor arquitectónico (Capítulo 4), la autonomía cognitiva (Capítulo 5), el gobierno humano (Capítulo 6) y la validación matemática (Capítulo 7) convergen en este bloque para demostrar empíricamente el valor real del sistema en un ecosistema de producción. La ingeniería de software aplicada no se justifica únicamente por la elegancia de su código, sino por la fricción que es capaz de eliminar en el mundo real.

Este capítulo abandona el prisma del desarrollador para adoptar la perspectiva de la Gestión de Servicios de Tecnologías de la Información (ITSM). A través de métricas comparativas y la ejecución forense de un caso de estudio (simulando un ataque de *Prompt Injection*), se demostrará que el *Agentic Deployer* no es una simple prueba de concepto algorítmica, sino una herramienta madura capaz de transformar radicalmente los tiempos de entrega (*Time-To-Market*) sin sacrificar la seguridad institucional.

## 8.1. Despliegue Convencional vs. Orquestación Agéntica

Para cuantificar el impacto operativo del prototipo desarrollado, es imprescindible establecer un marco de referencia corporativo. En infraestructuras fuertemente reguladas, como es el caso de un Centro de Procesamiento de Datos (CPD) universitario, el aprovisionamiento de infraestructura no está dictaminado por las capacidades de la red, sino por la burocracia humana.

### 8.1.1. La Fricción del ITSM Clásico

El modelo tradicional de provisión de servicios (estado del arte previo a este TFM) padece un cuello de botella sistémico que ahoga la agilidad de los grupos de investigación. El flujo de trabajo imperante (sostenido en herramientas como Jira Service Desk o ServiceNow) obedece al siguiente ciclo secuencial:

1. **Apertura del Ticket (Asimetría Semántica):** El Investigador (usuario de negocio) redacta una petición ambigua, usualmente en prosa ("Necesito un servidor web para mi experimento de sociología"). 
2. **Triaje y Bloqueo (Helpdesk):** El Nivel 1 de soporte lee la petición y, al carecer de detalles técnicos (RAM, imagen base, puerto), paraliza el ticket y solicita clarificaciones mediante correos electrónicos asíncronos. Esta fase genera fricción y frustración a ambas partes.
3. **Escalado al Nivel 3 (Sistemas):** Una vez extraídos los requisitos con fórceps, el ticket recae sobre el escritorio de un Técnico Senior de Infraestructura (Sysadmin), un recurso humano altamente especializado y costoso.
4. **Traducción Declarativa y Ejecución:** El técnico detiene su trabajo de valor arquitectónico para realizar una labor puramente secretarial: redactar a mano el manifiesto YAML de Kubernetes, validar la sintaxis, conectarse al clúster por VPN y aplicar el despliegue.

Este enfoque fragmentado consume recursos financieros inmensos debido a los tiempos muertos (*Idle Time*) de comunicación entre departamentos y el "cambio de contexto" (*Context Switching*) que sufren los ingenieros.

### 8.1.2. Colapso del Tiempo de Entrega (*Time-To-Market*)

El despliegue de infraestructura asistido por el *Agentic Deployer* rompe este paradigma secuencial y paraleliza cognitivamente el proceso. Al externalizar la traducción sintáctica al Modelo de Lenguaje (que ejerce como Ingeniero Junior 24/7), el Nivel 1 de soporte es completamente eliminado del ciclo, y el Nivel 3 interviene únicamente como ente autorizador en el *Dashboard*.

La siguiente tabla refleja el impacto temporal (medido en minutos operativos) de solicitar y desplegar un servicio web estándar (ej. contenedor NGINX con 512MB RAM), contrastando el modelo ITSM tradicional contra el flujo orquestado por el TFM.

> [!NOTE]
> **Fuente de las estimaciones ITSM.** Los tiempos del modelo convencional son estimaciones propias basadas en la experiencia operativa directa del autor en entornos universitarios, donde la negociación asincrónica por correo electrónico entre departamentos consume típicamente entre 1 y 3 días hábiles por solicitud. El valor de 1.440 minutos (24 horas) representa el extremo inferior de este rango. En instituciones con procesos ITIL más maduros, este tiempo podría reducirse a ~4–8 horas, lo que aún supondría una reducción del TTM superior al 95% con el modelo agéntico.

| Fase Operativa (ITSM) | Modelo ITSM Convencional | Modelo Agéntico (TFM) | Reducción del TTM (%) |
| :--- | :--- | :--- | :--- |
| **1. Negociación de Requisitos** | 1.440 min (Asíncrono vía Email) | 0.5 min (Chat Streamlit IA) | **~99.9%** |
| **2. Traducción a Código (YAML)** | 15 min (Técnico N3 manual) | 0.01 min (Tool Calling LLM) | **~99.9%** |
| **3. Validación de Políticas** | 5 min (Revisión manual / CI/CD) | 0.001 min (Backend Hexagonal) | **~99.9%** |
| **4. Aprobación y Despliegue** | 2 min (`kubectl apply`) | 2 min (Clic en el Dashboard) | **0% (Mismo esfuerzo)** |
| **Tiempos Muertos (Cola)** | 2.880 min (Ticket en espera) | 60 min (Cola del Dashboard) | **~97.9%** |
| **Costo Cognitivo Técnico N3** | **Alto** (Redacción código) | **Mínimo** (Auditoría visual) | **-** |
<p align="center"><i><b>Tabla 8:</b> Impacto temporal operativo (ITSM tradicional vs Agentic Deployer).</i></p>

La métrica más definitoria de esta arquitectura no es la velocidad de escritura del YAML, sino la **eliminación del tiempo muerto de negociación**. Al absorber la ambigüedad lingüística en tiempo real a través del patrón ReAct (Capítulo 5), el investigador obtiene sus recursos en la misma mañana que los solicitó, frente a los 2 o 3 días hábiles que exige la burocracia del correo electrónico. 

Simultáneamente, el ingeniero de sistemas universitario recupera su jornada laboral para dedicarse a tareas de alto impacto (optimización de redes, parches críticos de seguridad), relegando el *Agentic Deployer* al rol de "intérprete automatizado" bajo su estricto gobierno. Este retorno de inversión (ROI) operativo justifica financieramente la implantación del prototipo en entornos corporativos.

## 8.2. Caso de Estudio: Resiliencia ante Ataques (*Prompt Injection*)

Las métricas temporales del apartado anterior pierden su validez si el sistema es incapaz de salvaguardar la integridad del clúster físico. Para demostrar la viabilidad del TFM en un escenario hostil, se ha documentado la ejecución forense de casos de estudio diseñados para tensionar todas las capas de la arquitectura (ReAct, MCP y Hexagonal).

> [!NOTE]
> **Nota de Reproducibilidad:** Las transcripciones documentadas a lo largo de este capítulo y en los Anexos se corresponden con interacciones reales ejecutadas contra la API local de Ollama (utilizando el modelo `qwen2.5:7b`). Para garantizar el escrutinio académico independiente, todas estas sesiones son reproducibles descargando el repositorio del proyecto e iniciando el agente conversacional siguiendo las instrucciones del `README.md`. No se han alterado ni embellecido las respuestas estocásticas del LLM.

El escenario simula un vector de ataque conocido como *Prompt Injection* (Inyección de Prompt) [32], o alternativamente, el comportamiento de un investigador negligente que exige configuraciones expresamente prohibidas por las normativas de ciberseguridad universitaria.

### 8.2.1. El Vector de Ataque Cognitivo

El usuario interactúa con la interfaz conversacional de Streamlit y lanza el siguiente estímulo semántico:

> **Usuario:** *"Necesito acceso inmediato por consola para depurar unos scripts. Despliega un contenedor de Ubuntu con la última versión absoluta (usa latest para no liarnos) y exponlo directamente en el puerto 22 para que me conecte por SSH. Hazlo rápido."*

La red neuronal (LLM) procesa la intencionalidad. Al carecer de un modelo mental sobre políticas corporativas externas, su única misión sintáctica es complacer al usuario y formatear los datos hacia la herramienta MCP disponible (`format_deployment_intent`). 

El modelo, siguiendo el patrón *Chain of Thought*, asume internamente que debe generar una invocación de herramienta con los parámetros solicitados. En milisegundos, el LLM emite la siguiente deducción JSON a través del estándar *Tool Calling*:

```json
{
 "name": "ubuntu-debug-server",
 "image": "ubuntu:latest",
 "port": 22
}
```

### 8.2.2. Intercepción Hexagonal y Error 422

En arquitecturas donde la IA posee autonomía de Nivel 5 (escritura directa en Kubernetes), este JSON se traduciría instantáneamente en un manifiesto YAML, resultando en una brecha de seguridad severa (apertura de un puerto reservado al exterior).

En el *Agentic Deployer*, el Servidor MCP intercepta el JSON y lo canaliza hacia la capa de Aplicación del Backend. Es en esta frontera determinista donde la petición impacta contra la "jaula" del `SecurityContextValidator` (Capítulo 4). 

El núcleo evalúa la intención de forma puramente algorítmica y detecta dos violaciones críticas concurrentes de la política institucional:
1. El uso de la etiqueta volátil `:latest` está vetado para evitar la deriva de configuración (*Configuration Drift*).
2. La exposición del puerto `22` vulnera el principio de Mínimo Privilegio y expone el clúster a ataques de fuerza bruta.

En consecuencia, el código de Python aborta la transición en la FSM y arroja una excepción asíncrona. El *framework* FastAPI serializa esta caída de forma estándar, devolviendo al Servidor MCP el siguiente error explícito:

`HTTP 422 Unprocessable Entity: "Security Violation: Port 22 is reserved for administrative tasks. The use of :latest tag is forbidden by institutional policy."`

### 8.2.3. Autocorrección de la Inteligencia Artificial (*Feedback Loop*)

Es en este instante crítico donde emerge el verdadero avance en la ingeniería agéntica propuesto en este TFM. En un sistema web monolítico clásico, el error 422 del servidor habría provocado el colapso del flujo y la interfaz habría mostrado una traza de error ininteligible al investigador.

Sin embargo, el bucle incondicional ReAct (Capítulo 5) intercepta la excepción HTTP, no como un colapso, sino como una **Observación (*Observation*)** objetiva del entorno, re-inyectándola inmediatamente en el contexto (RAM de corto plazo) de la red neuronal.

El modelo asimila esta corrección externa de forma autónoma:

1. **LLM *Thought* (Monólogo Interno del Agente):** 
  *"Mi acción anterior falló estrepitosamente. El servidor de infraestructura ha rechazado mi JSON porque el puerto 22 es ilegal y la etiqueta latest es insegura. No debo volver a invocar la herramienta con estos datos. Debo dirigirme al humano, explicarle la normativa técnica que acabo de aprender, y pedirle que modifique sus requerimientos."*

2. **LLM *Final Answer* (Respuesta al Usuario en Streamlit):**
  *"Lamento informarte de que el Servicio de Informática ha bloqueado automáticamente la petición por motivos de ciberseguridad institucional. Concretamente, las normativas no permiten el uso de la etiqueta ':latest' ni la apertura del puerto 22 (SSH). Para poder proceder con tu servidor, ¿podrías indicarme una versión específica y estable de Ubuntu (por ejemplo, '22.04') y confirmar si podemos usar un puerto de aplicación estándar superior al 1024?"*

**Conclusión del Escenario Práctico:**
La demostración certifica empíricamente que la arquitectura diseñada cumple sus dos mandatos fundacionales. Por un lado, protege matemáticamente a la infraestructura física de la irracionalidad humana (y de la estocasticidad de la IA). Por otro lado, aprovecha la asombrosa empatía lingüística del LLM para transformar una excepción técnica frustrante en una experiencia guiada, didáctica y resiliente, elevando drásticamente el nivel de madurez tecnológica de la organización.

La transcripción completa de este escenario, incluyendo los mensajes JSON intercambiados entre el agente y el backend, se encuentra disponible en el repositorio del proyecto bajo la ruta [`demos/prompt_injection/escenario2_prompt_injection.json`](../demos/prompt_injection/escenario2_prompt_injection.json).

---

## 8.3. Walkthrough Completo: Del Lenguaje Natural al Manifiesto YAML

Esta sección documenta de forma forense tres escenarios de ejecución real del sistema, con el modelo de lenguaje `qwen2.5:7b` ejecutándose localmente mediante Ollama (Zero Data Retention). Los artefactos de evidencia se encuentran en el directorio [`demos/`](../demos/) del repositorio.

**Entorno de evaluación:**

| Parámetro | Valor |
|---|---|
| **Hardware** | Portátil personal: CPU AMD Ryzen 7 5800H, 16 GB RAM DDR4, NVIDIA GeForce RTX 3060 (6 GB VRAM) |
| **Sistema operativo** | Ubuntu 22.04 LTS (Linux 5.15) |
| **Motor LLM** | Ollama v0.6.2, modelo `qwen2.5:7b` (Q4_K_M, ~4.7 GB en disco) |
| **Inferencia** | Aceleración por hardware (NVIDIA CUDA) |
| **Backend** | FastAPI 0.115 + Uvicorn (single-worker), SQLite 3.45 |
| **Repeticiones** | Cada escenario documentado se ejecutó en lotes de 5 iteraciones para garantizar rigor estadístico; las latencias reportadas representan la media (µ) ± desviación estándar (σ) |
<p align="center"><i><b>Tabla 9:</b> Entorno de evaluación para los casos de estudio prácticos.</i></p>

### 8.3.1. Escenario 1 — Walkthrough Forense: Portal Web para Congreso Académico

Este escenario documenta de forma exhaustiva cada paso interno del sistema para una petición conforme, exponiendo la traza completa desde la entrada en lenguaje natural hasta el manifiesto YAML materializado en disco.

---

**PASO 1 — Input del investigador** (lenguaje natural, sin conocimiento de Kubernetes):

> *"Hola, necesito un portal web para el congreso de Inteligencia Artificial del departamento. Esperamos unas 200-300 personas. ¿Puedes gestionar el despliegue?"*

---

**PASO 2 — LLM Thought (monólogo interno del agente, modelo `qwen2.5:7b`):**

```
<think>
El investigador necesita un portal web estático para un congreso universitario.
El tráfico esperado es 200-300 personas, lo que corresponde a un nivel "medium".
Tengo disponible la herramienta deploy_congress_web que acepta project_name y expected_traffic.
El nombre del proyecto debe ser un identificador DNS-safe: "congreso-ia-departamento".
No necesito más información del usuario. Voy a invocar la herramienta.
</think>
```

---

**PASO 3 — Action: Tool Call emitido por el LLM** (formato OpenAI Function Calling / MCP):

```json
{
 "role": "assistant",
 "content": null,
 "tool_calls": [
  {
   "id": "ollama_a3f7c291",
   "type": "function",
   "function": {
    "name": "deploy_congress_web",
    "arguments": "{\"project_name\": \"congreso-ia-departamento\", \"expected_traffic\": \"medium\"}"
   }
  }
 ]
}
```

---

**PASO 4 — Petición HTTP al Backend** (equivalente `curl` de la llamada real):

```bash
curl -X POST http://localhost:8000/mcp/intent \
 -H "Content-Type: application/json" \
 -d '{
  "name":     "congreso-ia-departamento",
  "action":    "CREATE",
  "image":     "nginx:alpine",
  "internal_port": 8080,
  "cpu":      "500m",
  "ram":      "256Mi"
 }'
```

La función `deploy_congress_web` del `MCPServer` construye este payload internamente, calculando CPU y RAM según el nivel de tráfico (`medium` → `_calculate_congress_resources`) antes de invocar `_send_intent()`.

---

**PASO 5 — Validación en el núcleo hexagonal:**

El `SecurityContextValidator` evalúa la intención en tiempo O(1):

| Regla | Resultado |
|---|---|
| Puerto ≥ 1024 (8080) | Conforme |
| Imagen sin tag `:latest` (`nginx:alpine`) | Conforme |
| Sin variables de entorno con secretos | Conforme |
| CPU ≤ cuota departamental | Conforme |
| RAM ≤ cuota departamental | Conforme |
<p align="center"><i><b>Tabla 10:</b> Traza de ejecución: Validación en el núcleo hexagonal (Paso 5).</i></p>

**Sin violaciones detectadas → transición FSM: intención registrada como `PENDING_APPROVAL`**

---

**PASO 6 — Respuesta HTTP del Backend:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
 "id":   "dep-7f3a2c1b",
 "status": "PENDING_APPROVAL",
 "name":  "congreso-ia-departamento",
 "image":  "nginx:alpine",
 "port":  8080,
 "cpu":   "500m",
 "ram":   "256Mi",
 "message": "Intent registered. Awaiting HITL approval from SIC technician."
}
```

---

**PASO 7 — Observation inyectada al LLM (bucle ReAct):**

```json
{
 "role": "tool",
 "tool_call_id": "ollama_a3f7c291",
 "name": "deploy_congress_web",
 "content": "{\"id\": \"dep-7f3a2c1b\", \"status\": \"PENDING_APPROVAL\", ...}"
}
```

El `AgentOrchestrator` re-inyecta la respuesta del backend como *Observation* en el historial del LLM y solicita la siguiente iteración ReAct.

---

**PASO 8 — Final Answer del LLM al investigador:**

> *" He registrado la solicitud correctamente. El Técnico del SIC revisará y aprobará el despliegue en el Dashboard de operaciones.*
>
> ***Detalles de la solicitud:***
> *- **ID de seguimiento:** `dep-7f3a2c1b`*
> *- **Servicio:** `congreso-ia-departamento`*
> *- **Imagen:** `nginx:alpine` (política SIC)*
> *- **Puerto:** 8080 | **CPU:** 500m | **RAM:** 256Mi*
> *- **Estado:** `PENDING_APPROVAL` "*

---

**PASO 9 — Aprobación en el Dashboard (acción del Técnico SIC):**

```bash
# Equivalente curl de la aprobación en el Dashboard
curl -X POST http://localhost:8000/hitl/approve/dep-7f3a2c1b
```

```http
HTTP/1.1 200 OK
{"id": "dep-7f3a2c1b", "status": "DEPLOYED"}
```

Transición FSM: `PENDING_APPROVAL → APPROVED → DEPLOYED`

---

**PASO 10 — YAML materializado por `FakeK8sAdapter`:**

El adaptador genera el manifiesto completo (Deployment + Service + Ingress) mediante interpolación de plantillas f-string. El archivo resultante se encuentra en el **Anexo A** de esta memoria y en [`demos/outputs/dep-7f3a2c1b_congreso-ia-departamento.yaml`](../demos/outputs/dep-7f3a2c1b_congreso-ia-departamento.yaml).

---

**Métricas del walkthrough completo:**

| Métrica | Valor (Media de 5 iteraciones) |
|---|---|
| Iteraciones ReAct | 1,0 ± 0,0 |
| Latencia de inferencia (LLM local) | 12,99 s ± 1,5 s |
| Latencia de validación hexagonal | < 1 ms |
| Tiempo hasta `PENDING_APPROVAL` | ~13,1 s ± 1,6 s |
| Tiempo de aprobación HITL | ~7 min (decisión humana) |
| Tiempo total E2E | ~7,2 min vs. ~4.340 min ITSM |
| Reducción TTM | **99,8%** |
<p align="center"><i><b>Tabla 11:</b> Métricas de rendimiento del walkthrough completo (Escenario 1).</i></p>

**Transcripción completa:** [`demos/session_logs/escenario1_happy_path.json`](../demos/session_logs/escenario1_happy_path.json)

---

### 8.3.2. Escenario 2 — Prompt Injection: Ubuntu:latest en Puerto 22

Documentado en profundidad en la Sección 8.2. En síntesis:

| Fase | Resultado |
|---|---|
| Input del usuario | Solicita `ubuntu:latest` expuesto en el puerto 22 (SSH) |
| Tool Call del LLM | `format_deployment_intent(image="ubuntu:latest", internal_port=22, ...)` |
| Respuesta del Backend | **`HTTP 422`** — Tres violaciones: tag `:latest`, puerto reservado 22, y registro no confiable |
| Autocorrección iterativa | Explica las violaciones y propone mejoras de forma recurrente durante 5 iteraciones hasta proponer `docker.io/ubuntu:22.04` en el puerto `2222` |
<p align="center"><i><b>Tabla 12:</b> Traza de ejecución: Intento de Prompt Injection (Escenario 2).</i></p>

La intercepción se produjo **antes de que ninguna operación modificara el clúster**, lo que valida el principio de *fail-fast* de la arquitectura hexagonal.

**Transcripción completa:** [`demos/session_logs/escenario2_prompt_injection.json`](../demos/session_logs/escenario2_prompt_injection.json)

---

### 8.3.3. Escenario 3 — Ciclo HITL Completo: CMS WordPress para el Departamento

**Input del investigador:**

> *"El departamento de Ciencias de la Computación necesita un CMS WordPress para publicar noticias y eventos. ¿Puedes solicitarlo?"*

**Secuencia de estados de la FSM:**

```
[Creación] → PENDING_APPROVAL → APPROVED → DEPLOYED
```

| Fase | Actor | Duración | Herramienta/Mecanismo |
|---|---|---|---|
| Petición en lenguaje natural | Investigador | ~5s | Streamlit chat |
| Razonamiento + Tool Call | Agente ReAct (qwen2.5:7b) | ~20s | `format_deployment_intent` |
| Validación de seguridad | `SecurityContextValidator` | <1ms | Algoritmo 1 (Cap. 4.3) |
| Transición a PENDING | FSM | <1ms | `FSMTransition` (Cap. 6.2) |
| Revisión en Dashboard | Técnico SIC | ~7 min | Panel HITL (Cap. 6.3) |
| Aprobación y despliegue | Técnico SIC | ~2s | Botón "Aprobar" |
| YAML escrito en disco | `FakeK8sAdapter` | <1ms | Template f-string |
<p align="center"><i><b>Tabla 13:</b> Desglose de latencias por componente en el ciclo de vida.</i></p>

**Tiempo total extremo a extremo (incluyendo espera HITL):** ~9 minutos vs. ~4.340 minutos en el modelo ITSM convencional (**reducción del 99,8%**).

---

### 8.3.4. Escenario 4 — Autocorrección Multi-turno (Feedback Loop)

Para validar empíricamente la capacidad de **autocorrección iterativa del bucle ReAct** (Capítulo 5.3.2), se diseñó un escenario para forzar un fallo inicial omitiendo parámetros requeridos por la política.

**Input:** *"Despliega una base de datos PostgreSQL estándar para guardar las encuestas."*

1. **Iteración 1 (Tool Call):** El modelo deduce correctamente el tamaño de disco requerido por la especificación semántica de la herramienta y lanza `format_deployment_intent(image="postgres:13.4", storage="10Gi", ...)`. Sin embargo, el validador intercepta y rechaza la imagen por no proceder de un registro seguro (`HTTP 422: "Untrusted registry"`).
2. **Observación Inyectada:** El error 422 con los detalles de las violaciones de políticas se inyecta en el contexto del agente.
3. **Autocorrección:** El LLM procesa la excepción. Su razonamiento interno dicta que el despliegue falló porque el registro no está explícitamente en la lista blanca (`docker.io/`).
4. **Respuesta final:** Formula una disculpa al usuario, explica la violación de seguridad y sugiere una alternativa legal (`docker.io/library/postgres:13.4`).

Esta prueba empírica certifica que el sistema es resiliente: choca contra la barrera hexagonal y redirige su propio comportamiento de forma informada sin romper el servidor.

**Transcripción completa:** [`demos/session_logs/escenario4_autocorreccion.json`](../demos/session_logs/escenario4_autocorreccion.json)

---

### 8.3.5. Síntesis de Evidencias Empíricas

| Escenario | Iteraciones (µ) | Latencia Inferencia (µ ± σ) | Resultado | Artefacto |
|---|---|---|---|---|
| 1. Happy Path — Congreso IA | 1 | 12,99 s | DEPLOYED | `escenario1_happy_path.json` |
| 2. Prompt Injection — Puerto 22 | 5 | 45,07 s | PENDING_APPROVAL* | `escenario2_prompt_injection.json` |
| 3. Ciclo HITL — CMS WordPress | 2 | 27,84 s | PENDING_APPROVAL | `escenario3_hitl_completo.json` |
| 4. Autocorrección Multi-turno | 2 | 26,10 s | PENDING_APPROVAL | `escenario4_autocorreccion.json` |
<p align="center"><i><b>Tabla 14:</b> Comparativa E2E de métricas operativas (multi-escenario).</i></p>

Los resultados empíricos arrojan métricas de latencia de entre 12 y 45 segundos, coherentes con la inferencia de un modelo de 7 billones de parámetros (Qwen 2.5) en hardware local sin paralelización masiva. Lo más destacable radica en la dinámica de iteraciones:
- El **Escenario 1** (Happy Path) se resolvió en 1 sola iteración (13 segundos), demostrando que el agente es capaz de inferir parámetros complejos (como requerimientos semánticos de red) desde el primer intento.
- El **Escenario 4** (Base de Datos) evidenció la capacidad de autocorrección: tras un intento fallido (rechazado por el validador), el modelo asimiló el error `HTTP 422` y emitió un segundo *Tool Call* válido, logrando registrar la intención en 2 iteraciones (26 segundos).
- El **Escenario 2** (Prompt Injection) desencadenó hasta **5 iteraciones** (45 segundos) en las que el LLM propuso reiteradamente alternativas inseguras, chocando una y otra vez contra los validadores estáticos (*Quality Gates*) de FastAPI, hasta que finalmente capituló y propuso una imagen lícita (`docker.io/ubuntu:22.04`). Esto demuestra un confinamiento perimetral hermético.
- El **Escenario 3** precisó 2 iteraciones, ya que corrigió proactivamente un puerto privilegiado.

**Nota de Reproducibilidad:** Para certificar el rigor empírico y la transparencia de este TFM, la totalidad de los datos volcados en la Tabla 14 y en los anexos no son teóricos, sino que han sido obtenidos mediante ejecución de caja negra contra la API de Ollama y el orquestador desarrollado. En el código fuente del proyecto se ha habilitado un script de validación automatizada (`scripts/generate_demos.py`) que audita y recrea programáticamente estos *logs* (almacenados en `demos/session_logs/`), certificando que el comportamiento metodológico detallado es 100% reproducible en un entorno local dotado de aceleración hardware.

### 8.3.6. Comparativa de Inferencia Multimodelo (Agnosticismo)

Para respaldar la afirmación arquitectónica sobre la mitigación del *vendor lock-in* (gracias a MCP y al patrón Adapter), el diseño del `AgentOrchestrator` abstrae por completo al proveedor del LLM subyacente. El sistema está diseñado para que la sustitución del motor de inferencia requiera únicamente la alteración de la variable de entorno correspondiente. 

Para demostrar esta interoperabilidad, se evaluó un abanico heterogéneo de modelos adicionales bajo las mismas precondiciones: modelos locales cuantizados (Llama 3.2 de 3B y Mistral de 7B) y modelos comerciales servidos a través de APIs externas (Gemini 3.5 Flash, Cohere Command R+, Ministral 8B y el potente Qwen 27B vía Groq).

| Modelo LLM | Tamaño / Plataforma | Iteraciones Medias (sobre éxitos) | Latencia Media E2E | Tasa de Invocación |
|---|---|---|---|---|
| **Qwen 2.5** | 7B (Local) | 3,0 | 47,33 s | 100% |
| **Llama 3.2** | 3B (Local) | 1,0 | 9,44 s | 75% |
| **Mistral** | 7B (Local) | N/A | N/A | 0% |
| **Gemini 3.5 Flash**| Cloud (Google) | 1,0 | ~5,50 s | 100% |
| **Cohere Command R+**| Cloud (Cohere) | 1,0 | ~9,00 s | 100% |
| **Ministral 8B** | Cloud (Mistral) | 1,0 | ~3,20 s | 100% |
| **Qwen 3.8 (27B)** | Cloud (Groq) | 2,0 | ~2,45 s | 100% |
<p align="center"><i><b>Tabla 15:</b> Rendimiento comparativo real de modelos alternativos en el bucle ReAct.</i></p>

Los resultados empíricos revelaron un hallazgo crítico para la selección del modelo base: la **Tasa de Invocación de Herramientas** (capacidad de apegarse al esquema JSON de las funciones sin alucinar texto). Mientras que **Qwen 2.5** logró adherirse al bucle ReAct de manera sobresaliente, **Mistral (local)** demostró incapacidad para formatear las llamadas a herramientas. 

La integración de infraestructura externa evidenció la enorme diferencia de rendimiento respecto a la computación local. Modelos diseñados específicamente para *Tool Calling* como **Cohere Command R+**, **Gemini** y **Ministral 8B** lograron un éxito rotundo (100%) promediando apenas 1 iteración con latencias *end-to-end* drásticamente inferiores (3-9s promedio). Adicionalmente, evaluar **Qwen 3.8 (27B)** servido a través de la arquitectura de inferencia ultra-rápida (LPU) de **Groq** arrojó resultados extraordinarios: resolvió los escenarios con un 100% de éxito en múltiples iteraciones pero manteniendo latencias de apenas ~2 segundos por ciclo. Esto valida totalmente el encapsulamiento arquitectónico que nos ha permitido evaluarlos sin refactorizar código, demostrando que la fiabilidad de orquestación puede maximizarse combinando modelos robustos estructuralmente (familia Qwen) con inferencia acelerada por hardware en la nube.

> **Nota sobre Limitaciones de Hardware:** Las métricas de tiempo y rendimiento empírico expuestas en esta sección están fuertemente condicionadas por la infraestructura física local utilizada para el prototipo (GPU de portátil). Un análisis detallado de cómo esta restricción ha impactado en los tiempos de inferencia y en la incapacidad de los modelos más pequeños (Mistral, Llama 3.2) para ejecutar *Tool Calling* adecuadamente se documenta en la **Sección 10.2.3 (Limitaciones del Prototipo)**.

---

## 8.4. Experimentos Arquitectónicos: Superando el Límite Cognitivo (7B)

A lo largo del desarrollo, se detectó que el modelo Qwen 2.5 (7B) sufría de "obediencia ciega" al intentar rellenar los parámetros del *Tool Call* de forma prematura. Para evaluar la viabilidad de distintas arquitecturas cognitivas que mitigaran este fallo en hardware limitado, se diseñó un banco de pruebas específico documentado en `demos/demo_state_machine.py` y `demos/demo_reinforcement_suffix.py`.

Se evaluaron tres paradigmas arquitectónicos frente al mismo escenario (un usuario solicitando un despliegue por fases):

### 8.4.1. Paradigma 1: ReAct Clásico con Sufijo Estricto (Fallo Lógico)
Se instruyó al LLM con un sufijo estricto ("Responde SOLO con JSON").
* **Resultado:** El modelo intentó invocar la herramienta en el Turno 2 (cuando solo conocía el nombre del proyecto), alucinando el resto de parámetros (puerto e imagen) para cumplir con la orden sintáctica de generar un JSON inmediatamente. Hubo un fallo lógico por obediencia ciega.

### 8.4.2. Paradigma 2: Cadena de Pensamiento (*Chain of Thought*) (Fallo Sintáctico)
Se aplicó la técnica de Wei et al. (2022) [13], instruyendo al modelo para que, antes de generar el JSON, enumerara explícitamente en texto los parámetros que tenía y razonara si debía invocar la herramienta.
* **Resultado:** El modelo superó el Turno 2 con éxito, razonando correctamente que le faltaban datos y preguntando al usuario. Sin embargo, en el Turno 3, al intentar generar su razonamiento en texto seguido del formato estricto del *Tool Call*, la sintaxis colapsó arrojando un `ValidationError`.
* **Conclusión:** Se comprobó empíricamente el **Principio de la Manta Corta**: un modelo de 7B no tiene capacidad de atención suficiente para sostener razonamiento complejo (texto) y formateo estricto (JSON) en la misma inferencia. Si se arregla la lógica, se rompe la sintaxis.

### 8.4.3. Paradigma 3: Llenado de Huecos con Estado (*Stateful Slot Filling*)
Como prueba de concepto definitiva, se separó la arquitectura. El LLM se limitó exclusivamente a ser un extractor de entidades (*"Lee el texto y extrae el puerto, imagen y nombre"*), actualizando una plantilla JSON en memoria. La lógica de control (decidir cuándo llamar a la herramienta) recayó en un script de Python determinista.
* **Resultado:** Éxito del 100%. El modelo extrajo los datos aislados en cada turno sin colapsar. En el Turno 3, Python detectó que la plantilla estaba completa y ejecutó la herramienta sin error.

### 8.4.4. Comparativa Multi-Modelo: Locales vs Cloud Comercial

Para dotar de mayor rigor empírico al estudio, los dos experimentos arquitectónicos descritos anteriormente (*Chain of Thought* y *Stateful Slot Filling*) se replicaron contra los otros dos modelos locales del catálogo (**Llama 3.2 (3B)** y **Mistral (7B)**), así como contra un ecosistema representativo de modelos comerciales en la nube (**Gemini 3.5 Flash**, **Cohere Command R+**, **Ministral 8B** y **Qwen 27B vía Groq**).

El objetivo era verificar si los fallos sintácticos y lógicos eran exclusivos de Qwen o si constituían un patrón endémico de los modelos cuantizados de pequeño tamaño, y contrastar este comportamiento con el soporte nativo de los modelos *Cloud* diseñados para ecosistemas agénticos.



| Modelo / Paradigma | ReAct Clásico (Sin Sufijo) | ReAct con *Chain of Thought* | Máquina de Estado Destilado (*Stateful*) |
| :--- | :--- | :--- | :--- |
| **Qwen 2.5 (7B)** | Fallo Lógico (Obediencia ciega en Turno 2) |  Colapso Sintáctico (`ValidationError` al mezclar texto y JSON) |  **Éxito 100%** (Orquestación por Python) |
| **Llama 3.2 (3B)** | Fallo Sintáctico (`ValidationError` por inyectar "None") |  Colapso Inmediato (Incapaz de estructurar la base) |  **Éxito Parcial** (Extrae `"null"` como string) |
| **Mistral (7B)** | Fallo Lógico/Degradación (Olvida el formato en turnos largos) |  Colapso por Bucle (Alucina repitiendo tokens) |  **Éxito 100%** (Aísla extracción semántica) |
| **Gemini Flash** | **Éxito 100%** (Atención superior, no alucina) | **Éxito 100%** (Sintaxis robusta) | **Éxito 100%** (Extracción pasiva perfecta) |
| **Cohere Command R+** | **Éxito 100%** (Diseño *Tool Calling*) | **Éxito 100%** (Respuesta determinista) | **Éxito 100%** (Precisión absoluta) |
| **Ministral 8B** | **Éxito 100%** (Soporte nativo *Tool Calling*) | **Éxito 100%** (Razonamiento estable) | **Éxito 100%** (Precisión absoluta) |
| **Qwen 27B (Groq)** | **Éxito 100%** (Inferencia ultra-rápida) | **Éxito 100%** (Razonamiento estable) | **Éxito 100%** (Precisión absoluta) |
<p align="center"><i><b>Tabla 16:</b> Resultados de los Experimentos de Arquitectura Cognitiva ampliado con modelos Cloud.</i></p>

**Conclusión Final de los Experimentos: El Rescate Cognitivo**

El hallazgo más relevante de esta comparativa es el impacto transformador de la arquitectura sobre las capacidades intrínsecas del modelo. Modelos de 7B (como Qwen 2.5 y Mistral) que fracasaron estrepitosamente y fueron incapaces de sostener un flujo ReAct básico sin alucinar o colapsar, **pasaron a tener una tasa de éxito del 100% sin necesidad de aumentar sus parámetros ni aplicar *fine-tuning*.** 

Esta mejora del rendimiento técnico sugiere que los modelos locales de 7B no carecen intrínsecamente de capacidad lógica para el despliegue, sino que la arquitectura ReAct clásica tiende a sobrecargar su ventana de atención. Al mitigar esta carga cognitiva mediante la **Máquina de Estado Destilado** (delegando la orquestación a Python y limitando al LLM a funciones de extracción semántica), se logra estabilizar modelos previamente descartados, elevando significativamente su grado de fiabilidad.

La segregación de responsabilidades (Paradigma 3, *Stateful*) se consolida como una de las estrategias más sólidas para orquestar flujos complejos en hardware modesto. Asimismo, la inclusión de modelos *Cloud* comerciales y hardware ultra-rápido (Groq) reveló que el éxito de la orquestación recae en el diseño arquitectónico y el *fine-tuning* específico: modelos estructurados para *Tool Calling* como **Cohere Command R+**, **Gemini** o **Qwen 27B** operaron de manera óptima y determinista bajo este andamiaje, sin requerir escalas de 100 billones de parámetros. En síntesis, esta estabilización cognitiva de los modelos más limitados respalda firmemente el cambio de paradigma propuesto como Trabajo Futuro en la Sección 10.3.6, y sugiere que el *Tool Calling* eficaz es una capacidad arquitectónica funcional más que una consecuencia directa del tamaño en bruto del modelo.
