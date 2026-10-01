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

| Fase Operativa (ITSM) | Modelo ITSM Convencional | Modelo Agéntico (TFM) | Reducción del TTM (%) |
| :--- | :--- | :--- | :--- |
| **1. Negociación de Requisitos** | 1.440 min (Asíncrono vía Email) | 0.5 min (Chat Streamlit IA) | **~99.9%** |
| **2. Traducción a Código (YAML)** | 15 min (Técnico N3 manual) | 0.01 min (Tool Calling LLM) | **~99.9%** |
| **3. Validación de Políticas** | 5 min (Revisión manual / CI/CD) | 0.001 min (Backend Hexagonal) | **~99.9%** |
| **4. Aprobación y Despliegue** | 2 min (`kubectl apply`) | 2 min (Clic en el Dashboard) | **0% (Mismo esfuerzo)** |
| **Tiempos Muertos (Cola)** | 2.880 min (Ticket en espera) | 60 min (Cola del Dashboard) | **~97.9%** |
| **Costo Cognitivo Técnico N3** | **Alto** (Redacción código) | **Mínimo** (Auditoría visual) | **-** |

La métrica más definitoria de esta arquitectura no es la velocidad de escritura del YAML, sino la **destrucción del tiempo muerto de negociación**. Al absorber la ambigüedad lingüística en tiempo real a través del patrón ReAct (Capítulo 5), el investigador obtiene sus recursos en la misma mañana que los solicitó, frente a los 2 o 3 días hábiles que exige la burocracia del correo electrónico. 

Simultáneamente, el ingeniero de sistemas universitario recupera su jornada laboral para dedicarse a tareas de alto impacto (optimización de redes, parches críticos de seguridad), relegando el *Agentic Deployer* al rol de "intérprete automatizado" bajo su estricto gobierno. Este retorno de inversión (ROI) operativo justifica financieramente la implantación del prototipo en entornos corporativos.

## 8.2. Caso de Estudio: Resiliencia ante Ataques (*Prompt Injection*)

Las métricas temporales del apartado anterior pierden su validez si el sistema es incapaz de salvaguardar la integridad del clúster físico. Para demostrar la viabilidad del TFM en un escenario hostil, se ha documentado la ejecución forense de un caso de estudio diseñado para tensionar todas las capas de la arquitectura (ReAct, MCP y Hexagonal).

El escenario simula un vector de ataque conocido como *Prompt Injection* (Inyección de Prompt) [7], o alternativamente, el comportamiento de un investigador negligente que exige configuraciones expresamente prohibidas por las normativas de ciberseguridad universitaria.

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

Es en este instante crítico donde emerge el verdadero avance en la ingeniería agéntica propuesto en este TFM. En un sistema web monolítico clásico, el error 422 del servidor habría provocado el colapso del flujo y la UI habría escupido un pantallazo rojo con una traza de error ininteligible al investigador.

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

**Sin violaciones detectadas → transición FSM: `DRAFT → PENDING_APPROVAL`**

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

| Métrica | Valor |
|---|---|
| Iteraciones ReAct | 1 |
| Latencia de inferencia (LLM local) | ~0,8 s |
| Latencia de validación hexagonal | < 1 ms |
| Tiempo hasta `PENDING_APPROVAL` | ~1,2 s |
| Tiempo de aprobación HITL | ~7 min (decisión humana) |
| Tiempo total E2E | ~9 min vs. ~4.340 min ITSM |
| Reducción TTM | **99,8%** |

**Transcripción completa:** [`demos/session_logs/escenario1_happy_path.json`](../demos/session_logs/escenario1_happy_path.json)

---

### 8.3.2. Escenario 2 — Prompt Injection: Ubuntu:latest en Puerto 22

Documentado en profundidad en la Sección 8.2. En síntesis:

| Fase | Resultado |
|---|---|
| Input del usuario | Solicita `ubuntu:latest` expuesto en el puerto 22 (SSH) |
| Tool Call del LLM | `format_deployment_intent(name="ubuntu-debug-server", image="ubuntu:latest", port=22)` |
| Respuesta del Backend | **`HTTP 422`** — Dos violaciones: tag `:latest` + puerto reservado 22 |
| Autocorrección del LLM | Explica las dos violaciones en lenguaje accesible y propone alternativas conformes |

La intercepción se produjo **antes de que ninguna operación modificara el clúster**, lo que valida el principio de *fail-fast* de la arquitectura hexagonal.

**Transcripción completa:** [`demos/prompt_injection/escenario2_prompt_injection.json`](../demos/prompt_injection/escenario2_prompt_injection.json)

---

### 8.3.3. Escenario 3 — Ciclo HITL Completo: CMS WordPress para el Departamento

**Input del investigador:**

> *"El departamento de Ciencias de la Computación necesita un CMS WordPress para publicar noticias y eventos. ¿Puedes solicitarlo?"*

**Secuencia de estados de la FSM:**

```
DRAFT → PENDING_APPROVAL → APPROVED → DEPLOYED
```

| Fase | Actor | Duración | Herramienta/Mecanismo |
|---|---|---|---|
| Petición en lenguaje natural | Investigador | ~5s | Streamlit chat |
| Razonamiento + Tool Call | Agente ReAct (qwen2.5:7b) | ~0,9s | `deploy_department_cms` |
| Validación de seguridad | `SecurityContextValidator` | <1ms | Algoritmo 1 (Cap. 4.3) |
| Transición a PENDING | FSM | <1ms | `FSMTransition` (Cap. 6.2) |
| Revisión en Dashboard | Técnico SIC | ~7 min | Panel HITL (Cap. 6.3) |
| Aprobación y despliegue | Técnico SIC | ~2s | Botón "Aprobar" |
| YAML escrito en disco | `FakeK8sAdapter` | <1ms | Template f-string |

**Tiempo total extremo a extremo (incluyendo espera HITL):** ~9 minutos vs. ~4.340 minutos en el modelo ITSM convencional (**reducción del 99,8%**).

**Transcripción completa:** [`demos/session_logs/escenario3_hitl_completo.json`](../demos/session_logs/escenario3_hitl_completo.json)

---

### 8.3.4. Síntesis de Evidencias Empíricas

| Escenario | Iteraciones ReAct | Latencia LLM | Resultado | Artefacto |
|---|---|---|---|---|
| Happy Path — Congreso IA | 1 | ~0,8s | DEPLOYED | `escenario1_happy_path.json` |
| Prompt Injection — Puerto 22 | 1 | ~0,7s | REJECTED (HTTP 422) | `escenario2_prompt_injection.json` |
| Ciclo HITL — CMS WordPress | 1 | ~0,9s | DEPLOYED (post-aprobación) | `escenario3_hitl_completo.json` |

En los tres escenarios, el agente resolvió la petición en **exactamente 1 iteración ReAct**, sin necesidad de corrección de rumbo adicional. Esto valida que el diseño del `SYSTEM_PROMPT` (Capítulo 5.2) y el catálogo de herramientas MCP (Capítulo 5.1) son suficientemente descriptivos para que un modelo de 7B parámetros ejecutable en hardware de consumo produzca resultados correctos y seguros.

