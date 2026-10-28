# Capítulo 10. Conclusiones, Limitaciones y Trabajo Futuro

La integración de modelos de lenguaje de gran escala (LLM, *Large Language Models*) en la automatización de operaciones de infraestructura (*Platform Engineering*) exige salvaguardas arquitectónicas estrictas que mitiguen su inherente naturaleza estocástica. El presente Trabajo de Fin de Máster ha abordado este desafío mediante el diseño, implementación y evaluación de una arquitectura desacoplada orientada a garantizar la validación determinista de invariantes, la trazabilidad transaccional y el gobierno mediante supervisión humana en el ciclo de aprovisionamiento de servicios.

A continuación, se exponen las conclusiones fundamentales derivadas de la validación empírica del sistema, las limitaciones inherentes al alcance del prototipo desarrollado y la hoja de ruta estratégica para su evolución futura.

## 10.1. Conclusiones

La conceptualización, el desarrollo y la evaluación empírica del sistema *Agentic Deployer* han validado la viabilidad técnica de intermediar peticiones de infraestructura en lenguaje natural mediante agentes inteligentes, siempre que su actuación quede estrictamente confinada dentro de un perímetro arquitectónico determinista. Las conclusiones fundamentales derivadas de esta investigación se articulan en los siguientes ejes:

### 10.1.1. Matriz de Cumplimiento y Trazabilidad de Objetivos

Para certificar formalmente la correspondencia entre los compromisos técnicos iniciales y los resultados alcanzados, la Tabla 36 sintetiza la matriz de trazabilidad biunívoca entre los cinco objetivos específicos (*O*₁ a *O*₅) definidos en la Sección 1.3.2, los requisitos funcionales y no funcionales asociados, los componentes de software materializados y la evidencia empírica que valida su cumplimiento:

| Objetivo Específico | Requisitos Vinculados | Artefactos e Implementación | Evidencia Empírica de Validación | Grado de Consecución |
|---|---|---|---|:---:|
| ***O*₁: Núcleo Hexagonal Desacoplado (*Ports & Adapters*)** | RNF-02, RNF-04 | Dominio inmutable Pydantic, casos de uso puros y validador `SecurityContextValidator` (Cap. 5, §5.1-5.4). | Aislamiento verificado ante inyección de parámetros no conformes (§9.2.2) y 100% de cobertura en tests unitarios. | **100% (Completado)** |
| ***O*₂: Servidor de Herramientas Estándar (MCP)** | RF-03, RNF-01 | Servidor FastMCP autónomo sobre canal `stdio` exponiendo el catálogo del SIC (Cap. 6, §6.1). | Certificación de interoperabilidad externa mediante **MCP Inspector** oficial y desacoplamiento verificado de APIs propietarias (§9.1, §10.1.3). | **100% (Completado)** |
| ***O*₃: Orquestador Agéntico ReAct con *Feedback Loop*** | RF-02, RNF-04 | Orquestador cognitivo `AgentOrchestrator` con bucle de razonamiento ReAct y patrón *Stateful Slot Filling* (Cap. 6, §6.2). | Convergencia en 1,0 iteraciones con `qwen2.5-coder:7b` (§9.3) y resolución del límite atencional con 100% de éxito (§9.4). | **100% (Completado)** |
| ***O*₄: Rutas Doradas (*Golden Paths*) Declarativas** | RF-01, RF-03 | Plantillas de Kubernetes pre-auditadas (`Deployment`, `Service`, `Ingress`) y adaptador `FakeK8sAdapter` (Cap. 5, §5.4.3; Anexo A). | Generación determinista libre de alucinaciones en los 4 casos de estudio prácticos (§9.2) y validación sintáctica de manifiestos. | **100% (Completado)** |
| ***O*₅: Gobernanza de Seguridad *Human-In-The-Loop* (HITL)** | RF-04, RF-05, RNF-03 | Máquina de Estados Finita (FSM), persistencia SQLite ACID y consola web de operaciones en Streamlit (Cap. 7, §7.1-7.3). | Cero ejecuciones no autorizadas; reducción del 98,5% en el *Time-To-Market* y del 76,7% en tiempo de gestión activa del técnico (§9.5). | **100% (Completado)** |
<p align="center"><i><b>Tabla 36:</b> Matriz de trazabilidad y grado de cumplimiento de los objetivos específicos del proyecto.</i></p>

### 10.1.2. Síntesis de Contribuciones Tangibles de Ingeniería

Como resultado del desarrollo y validación experimental del sistema, el presente Trabajo de Fin de Máster aporta a la comunidad académica y profesional los siguientes activos y contribuciones metodológicas:

1. **Arquitectura de Perímetro Determinista para Agentes de Infraestructura:** Especificación y validación de un patrón arquitectónico hexagonal que desacopla estrictamente el razonamiento probabilístico de los modelos de lenguaje respecto a la capa de ejecución física, confinando el estocasticismo mediante validadores de invariantes en el núcleo.
2. **Servidor FastMCP Autónomo e Interoperable para Operaciones de TI:** Implementación de referencia de un servidor compatible con el estándar abierto *Model Context Protocol* (MCP) que expone operaciones de infraestructura de un CPD universitario (`deploy_congress_web`, `deploy_department_cms`, `deploy_python_app`, `deploy_static_website`, `deploy_database`), validado externamente mediante la herramienta oficial *MCP Inspector*.
3. **Patrón de Desacoplamiento de Estado Conversacional (*Stateful Slot Filling*):** Demostración empírica de una técnica de ingeniería que segrega la extracción semántica puntual del seguimiento transaccional del diálogo mediante una FSM determinista, elevando la fiabilidad de modelos locales de 7B parámetros del 0% al 100% en flujos multi-turno complejos.
4. **Marco de Aseguramiento de Calidad Híbrido para Sistemas con IA:** Metodología integral de verificación que trasciende la cobertura tradicional de código mediante la combinación sinérgica de *Property-Based Testing* (Hypothesis), Pruebas Metamórficas y *Mutation Testing* (Mutmut), identificando fallas de resiliencia lógica que pasan desapercibidas ante suites unitarias convencionales.
5. **Catálogo de Evaluación Empírica Multi-Modelo y Reproducible:** Banco de pruebas sistemático y conjunto de trazas experimentales sobre 8 familias de modelos neuronales (locales en Ollama, LPUs en Groq y comerciales en la nube), estableciendo directrices empíricas para la adopción de agentes soberanos (*Zero Data Retention*) en el sector público.

### 10.1.3. Superación del Acoplamiento a Proveedores Propietarios (*Vendor Lock-In*) mediante MCP

La adopción estratégica del protocolo **Model Context Protocol (MCP)** [13] para aislar el catálogo de operaciones del Servicio de Informática y Comunicaciones (SIC) ha permitido desacoplar formalmente la especificación de herramientas respecto a las interfaces de programación de aplicaciones (APIs) propietarias de los proveedores de IA. Se ha verificado empíricamente la factibilidad de estructurar un catálogo de capacidades operativas interoperable y modular. El servidor FastMCP desarrollado expone contratos dinámicos autogenerados mediante introspección estática de tipos, garantizando compatibilidad con cualquier motor cognitivo compatible con el estándar.

Este desacoplamiento se constató empíricamente en dos ámbitos complementarios:
1. **Sustitución transparente del motor de inferencia:** La implementación del cliente nativo `OllamaLLMClient` (Sección 6.2.1) permitió reemplazar el modelo comercial de OpenAI por un modelo de código abierto ejecutado en infraestructura local (`qwen2.5:7b`), sin requerir modificaciones en la lógica de dominio hexagonal ni en las definiciones de herramientas del servidor MCP.
2. **Interoperabilidad externa certificada:** La conformidad del servidor se evaluó formalmente mediante la herramienta de inspección oficial del protocolo (**MCP Inspector**). Ejecutándose de forma independiente a la interfaz gráfica Streamlit, la herramienta descubrió (`tools/list`) e invocó exitosamente las capacidades del catálogo del SIC a través del canal de comunicación estándar (`stdio`), confirmando que el servidor constituye un activo reutilizable por clientes y herramientas de auditoría externas.

### 10.1.4. La Arquitectura Hexagonal como Perímetro Determinista de Contención

Uno de los hallazgos centrales de este trabajo radica en la eficacia demostrada por la Arquitectura Hexagonal (*Ports and Adapters*) [19] para confinar y neutralizar las anomalías estocásticas y alucinaciones de los modelos de lenguaje. Al exigir que toda propuesta de inferencia atraviese los contratos de un modelo de dominio inmutable y fuertemente tipado (`Pydantic`) evaluado por un validador determinista (`SecurityContextValidator`), la estocasticidad del modelo queda interceptada antes de alcanzar los adaptadores de infraestructura física.

El sistema asume metodológicamente la falibilidad del LLM: intercepta las propuestas no conformes y reinyecta las excepciones estructuradas en el contexto conversacional (*Feedback Loop*), habilitando una autocorrección asistida y pedagógica. El caso de estudio de inyección de instrucciones adversarias documentado en la Sección 9.2.2 demuestra que peticiones que vulneran las normativas de seguridad (uso de la etiqueta volátil `ubuntu:latest` en el puerto administrativo privilegiado `22`) son bloqueadas en el núcleo de la aplicación emitiendo un código de estado `HTTP 422 Unprocessable Entity`, guiando la convergencia hacia parámetros conformes en iteraciones sucesivas sin comprometer el entorno físico.

### 10.1.5. La Necesidad del Patrón *Human-In-The-Loop* (HITL) en Infraestructuras Críticas

Frente a las posturas que postulan la conveniencia de una autonomía algorítmica total (Nivel 5), este trabajo concluye que en infraestructuras institucionales la supervisión humana representa una salvaguarda ineludible de cumplimiento, responsabilidad legal y gobernanza de TI. La implementación de la Máquina de Estados Finita (FSM) y del panel de control asíncrono demostró que el patrón HITL no introduce fricciones operativas indeseadas, sino que articula una segregación efectiva de roles:
- El modelo de lenguaje asume la extracción de intenciones y la clarificación de parámetros técnicos en lenguaje natural.
- El técnico especialista audita, verifica y autoriza formalmente la orden en la consola de operaciones.
- El investigador solicitante monitoriza en tiempo real el ciclo de vida de su petición a través de la interfaz conversacional.

La reducción empírica del tiempo de entrega demostrada —disminuyendo el tiempo activo de gestión técnica especializada de 30 minutos a 7 minutos (ahorro del 76,7%) y el tiempo total de entrega (*Time-To-Market*) de ~4.342 minutos en el flujo convencional a ~67 minutos en el flujo asistido (reducción del 98,5%, Sección 9.5)— ratifica que el control humano y la eficiencia operativa son plenamente convergentes cuando la automatización cognitiva absorbe la burocracia de triaje.

### 10.1.6. Redefinición del Aseguramiento de la Calidad (QA) frente a la Falacia de Cobertura

Las técnicas convencionales de aseguramiento de calidad basadas en pruebas unitarias deterministas resultan insuficientes para certificar sistemas gobernados por componentes probabilísticos. La integración de *Property-Based Testing* (Hypothesis) [37] y de Pruebas Metamórficas [38] ha permitido validar que el agente preserva la invarianza semántica y la estructura formal de salida frente a transformaciones lingüísticas, sintácticas y tipográficas complejas.

Asimismo, la aplicación de pruebas de mutación (*Mutation Testing* con Mutmut) evidenció que una alta cobertura de líneas no garantiza resiliencia lógica. La evaluación inicial reveló **30 mutantes supervivientes** en funciones de normalización de recursos (`_parse_cpu`, `_parse_ram`), pese a que la cobertura de código reportaba un 100% en dichos bloques. Este hallazgo guio la refactorización sistemática de los algoritmos de análisis sintáctico y la incorporación de aserciones de invariantes, validando el análisis de mutaciones como una práctica indispensable para auditar software de infraestructura gobernado por IA.

### 10.1.7. Viabilidad y Estabilización de Modelos de Escala Reducida (7B)

La experimentación con modelos fundacionales ejecutados en local demostró que los modelos generalistas de 7B parámetros presentan limitaciones atencionales al gestionar flujos multi-turno mediante arquitecturas puramente reactivas, mostrando inconsistencias en el seguimiento de esquemas JSON estructurados a medida que se incrementa el historial conversacional.

No obstante, al incorporar el patrón arquitectónico de **Llenado de Huecos con Estado (*Stateful Slot Filling*)** (Sección 9.4.3) —en el cual el modelo opera exclusivamente como extractor semántico desacoplado en cada turno individual y una máquina de estados determinista en Python retiene el vector de parámetros acumulados—, **estos mismos modelos alcanzan una fiabilidad del 100% sin requerir incremento en el volumen de parámetros ni costosos procesos de reentrenamiento**. Esta segregación entre extracción semántica y control transaccional confirma la viabilidad de desplegar sistemas agénticos sobre hardware estándar de consumo moderado.

### 10.1.8. Hallazgos Transversales de la Evaluación Multi-Modelo

La batería experimental sistemática desarrollada frente a 9 arquitecturas neuronales heterogéneas (locales cuantizados en Ollama, unidades LPU en Groq y APIs comerciales en la nube) arroja cuatro directrices de ingeniería transferibles:

1. **Alineamiento de dominio frente a volumen de parámetros:** La destreza para emitir llamadas a funciones estructuradas (*Tool Calling*) depende del alineamiento específico del entrenamiento con gramáticas formales y tipado estricto más que de la escala bruta de parámetros. Modelos de alta capacidad algorítmica general (como `codestral-latest`) obtuvieron un 0% de éxito en modo *Zero-Shot* al emitir texto libre o código procedural no estructurado. En contraste, modelos compactos especializados en código (`qwen2.5-coder:7b`) lograron un 100% de éxito metamórfico en modo soberano.
2. **Complementariedad entre inferencia probabilística y control determinista:** Ningún modelo de lenguaje generalista operando en aislamiento estricto superó el 66% de invarianza semántica ante perturbaciones léxicas y cruce idiomático. Sin embargo, al integrarse en el bucle ReAct coordinado por la Arquitectura Hexagonal y la FSM, la tasa de éxito convergió al 100%. La robustez de un sistema agéntico reside en la solidez del perímetro de software que lo envuelve y no en la infalibilidad del modelo de lenguaje.
3. **Aislamiento tecnológico frente a la obsolescencia:** La interoperabilidad provista por el protocolo MCP y el adaptador `OpenAILLMClient` garantiza que las organizaciones puedan adoptar inicialmente motores locales soberanos a coste cero y migrar progresivamente hacia aceleradores dedicados o modelos de frontera comerciales sin modificar el código de negocio ni los contratos de herramientas.
4. **Soberanía del dato y gobernanza institucional:** Si bien los proveedores en la nube ofrecen tiempos de respuesta reducidos, su adopción introduce dependencias externas, límites de tasa (`HTTP 429 Rate Limit Exceeded`) y transferencias de metadatos sensibles. Para administraciones públicas y entornos con alta exigencia regulatoria, el despliegue local de modelos especializados bajo el principio de Soberanía del Dato (*Zero Data Retention*) constituye una alternativa técnica plenamente viable y económicamente sostenible.

### 10.1.9. Síntesis Comparativa de Modelos Evaluados

Como consolidación de la experimentación desarrollada en el Capítulo 9 (**Tablas 30, 31 y 32** en evaluación metamórfica *Zero-Shot*, y **Tablas 33 y 34** en orquestación ReAct y arquitectura cognitiva), en la **Tabla 37** se sintetiza y clasifica a los motores cognitivos según su idoneidad técnica para la orquestación agéntica institucional:

| Motor / Modelo | Ámbito de Ejecución | Nivel de Idoneidad | Comportamiento Observado y Respaldo Empírico |
|---|---|---|---|
| **`qwen2.5-coder:7b`** (Alibaba / Ollama) | Local | **Alta (Soberana - Código)** | Máxima fiabilidad. 100% de éxito en stress metamórfico (*Tabla 32*) y convergencia en 1,0 iteraciones (*Tabla 33*). La especialización en código suple las restricciones de hardware. |
| **`qwen2.5:7b`** (Alibaba / Ollama) | Local | **Media-Alta (Soberana - Generalista)** | Fiabilidad moderada en aislamiento (50% metamórfico, *Tabla 32*). Requiere soporte de la máquina de estados para evitar inconsistencias en diálogos extensos. |
| **`gemini-3.5-flash`** (Google Cloud) | Cloud | **Alta (Comercial)** | Modelo en la nube más consistente en extracción estructurada (66% metamórfico, *Tabla 32*). Sujeto a cuotas externas y políticas de retención comercial. |
| **`command-r-plus`** (Cohere Cloud) | Cloud | **Alta (Comercial)** | Diseñado específicamente para invocación de herramientas (66% metamórfico, *Tabla 32*); muestra vulnerabilidad ante giros coloquiales extremos. |
| **`ministral-8b-latest`** (Mistral AI) | Cloud | **Media (Comercial)** | Desempeño óptimo bajo tutela de la FSM (*Tabla 33*), pero vulnerable en modo *Zero-Shot* no asistido (0% metamórfico, *Tabla 32*). |
| **`codestral-latest`** (Mistral AI) | Cloud | **Inadecuado para Tool Calling** | No apto para orquestación: carece de ajuste para emitir invocaciones formales bajo esquemas JSON, emitiendo texto plano explicativo (0% metamórfico, *Tabla 32*). |
<p align="center"><i><b>Tabla 37:</b> Clasificación y respaldo empírico de idoneidad de motores cognitivos para orquestación agéntica institucional.</i></p>

**Conclusiones Clave de la Evaluación Comparativa:**
1. **La especialización sintáctica prevalece sobre la escala:** La especialización sobre gramáticas formales y contratos de interfaz es más crítica que el volumen de parámetros, posibilitando despliegues institucionales confiables bajo el principio de **Zero Data Retention** en hardware asequible.
2. **Invarianza y contención determinista:** La incapacidad de los modelos comerciales de alcanzar un 100% de invarianza en solitario ante ruido lingüístico confirma que la fiabilidad productiva debe descansar en las defensas deterministas del software tradicional.
3. **Perspectivas de adopción en plataformas comerciales:** Modelos comerciales de referencia sujetos a tarificación por consumo (tales como **GPT-4o [44]** o **Claude 3.5 Sonnet [45]**) disponen de optimizaciones avanzadas de fabricante para protocolos agénticos y MCP, garantizando una alternativa complementaria en entornos donde la política de privacidad autorice el uso de nubes externas.

---

## 10.2. Limitaciones del Prototipo

En concordancia con el principio de honestidad y rigor científico, a continuación se detallan las limitaciones técnicas inherentes al prototipo de investigación, identificando las fronteras operativas del sistema frente a un despliegue de producción maduro:

### 10.2.1. Adaptador de Infraestructura Simulado (`FakeK8sAdapter`)

La materialización de las configuraciones declarativas se efectúa mediante generación y volcado de archivos YAML en el sistema de almacenamiento local, y no a través de una conexión interactiva con la API de Kubernetes. Si bien la validez sintáctica de los manifiestos generados está certificada (Anexo A), esta simulación excluye la validación de condiciones dinámicas del clúster físico:
- **Validación de cuotas dinámicas:** El *Control Plane* de Kubernetes podría denegar la creación si el espacio de nombres (*namespace*) excede cuotas globales concurrentes.
- **Conflictos de concurrencia e identificadores:** La duplicidad de nombres de servicio generaría códigos de error `HTTP 409 Conflict` en el servidor de API de Kubernetes, no contemplados en el arnés simulado.
- **Dependencias de controladores externos:** La emisión de certificados TLS a través de `cert-manager` requiere la presencia física del operador en el clúster; en su ausencia, los recursos `Ingress` permanecerían en estado pendiente indefinidamente.

### 10.2.2. Ausencia de Mecanismos de Autenticación y Autorización Perimetral

Los puntos de acceso expuestos por el backend de aplicación (`/mcp/intent`, `/hitl/approve`, `/hitl/status`) **carecen de mecanismos de autenticación y autorización criptográfica** (OAuth2, OpenID Connect, JWT o API Keys). En el prototipo de laboratorio, cualquier proceso con acceso a la red local puede consultar o autorizar intenciones de despliegue. En un entorno institucional real, esta carencia constituye una vulnerabilidad crítica que requeriría la integración obligatoria con el directorio corporativo (LDAP/Keycloak) y la implementación de un modelo de control de acceso basado en roles (RBAC).

### 10.2.3. Resiliencia frente a Vectores Complejos de Inyección de Prompt

Si bien el sistema intercepta con éxito inyecciones de instrucciones directas mediante el validador determinista (Sección 9.2.2), el diseño actual no incorpora contramedidas específicas frente a vectores adversarios avanzados documentados en la literatura:
- **Inyecciones indirectas de instrucciones:** Incorporación de fragmentos adversarios en fuentes documentales externas que el modelo pudiera consumir inadvertidamente.
- **Evasión acumulativa mediante diálogo multi-turno (*Context Jailbreaking*):** Manipulación deliberada de la ventana de contexto a lo largo de turnos iterativos para diluir la efectividad de las directrices de seguridad del *System Prompt*.

### 10.2.4. Cobertura Acotada del Catálogo de Herramientas y Operaciones de Ciclo de Vida

El servidor MCP implementa un catálogo orientado al aprovisionamiento inicial de servicios estándar (`deploy_congress_web`, `deploy_department_cms`, `deploy_python_app`, `deploy_static_website`, `deploy_database`, `get_deployment_status` y `delete_university_service`). No obstante, quedan fuera del alcance del prototipo operaciones complejas de administración continuada del ciclo de vida, tales como el escalado dinámico de réplicas, la gestión de secretos cifrados (`Secrets`), la rotación de certificados o la monitorización interactiva de registros de ejecución (*logs*).

### 10.2.5. Concurrencia y Escalabilidad en la Capa de Aplicación

El backend FastAPI opera en modo síncrono sobre un único proceso servidor ASGI (Uvicorn). En un escenario de alta concurrencia con múltiples operadores y peticiones simultáneas, la arquitectura actual presentaría cuellos de botella por saturación de hilos. Si bien la capa de persistencia en SQLite resuelve las condiciones de carrera locales mediante bloqueos transaccionales a nivel de fichero, un entorno productivo requiere motores de bases de datos relacionales cliente-servidor distribuidos.

### 10.2.6. Inmutabilidad Previa en el Canal de Supervisión Humana (HITL)

En la interfaz actual del panel HITL, la potestad del técnico de operaciones es de naturaleza estrictamente binaria (Aprobar o Rechazar). Si una propuesta presenta parámetros razonables pero una reserva de memoria ligeramente sobredimensionada, el operador no dispone de mecanismos para editar directamente los campos de la intención antes de confirmar el despliegue (*Pre-Deployment Mutability*), viéndose forzado a rechazar la petición e iniciar un nuevo ciclo de clarificación.

### 10.2.7. Evaluación de Usabilidad Acotada y Validación con Usuarios Finales

Las métricas de eficiencia operativa analizadas en el Capítulo 9 corresponden a trazas de ejecución en entornos de ensayo controlados. El sistema no ha sido sometido a ensayos de usabilidad formalizados (tales como la metodología *System Usability Scale*, SUS) con investigadores o personal administrativo real ajeno al desarrollo. La interacción de perfiles sin competencias técnicas frente a la interfaz conversacional podría revelar barreras lingüísticas o expectativas de interacción no identificadas en la evaluación de laboratorio.

### 10.2.8. Condicionantes Hardware y Restricciones de Cuantización

Los ensayos locales se ejecutaron sobre una estación de trabajo equipada con una GPU de 6 GB de memoria de vídeo (VRAM), lo que limitó la experimentación a modelos de tamaño reducido (<8B parámetros) con formatos de cuantización a 4 bits (Q4_K_M). Aunque `qwen2.5-coder:7b` demostró un comportamiento adecuado y estable en las pruebas, la evaluación de arquitecturas de mayor escala (14B o 32B parámetros) en hardware de cómputo institucional con mayor capacidad de memoria permitiría contrastar posibles mejoras en latencia y comprensión contextual.

### 10.2.9. Disonancia Lingüística en Tareas de Razonamiento Estructurado

El prototipo se evaluó forzando la interacción íntegramente en lengua española (instrucciones del sistema, entradas de usuario y descripciones semánticas de herramientas). Dado que los modelos fundacionales han sido pre-entrenados mayoritariamente sobre corpus en idioma inglés, su capacidad de razonamiento formal y adherencia a contratos sintácticos estrictos experimenta una degradación apreciable en idiomas secundarios. Parte de las desviaciones de formato registradas en modelos generalistas de 7B se atribuyen a este desalineamiento representacional.

---

## 10.3. Trabajo Futuro

Para abordar las limitaciones identificadas y guiar la transición del prototipo hacia un entorno productivo en centros de datos universitarios, se definen las siguientes líneas prioritarias de evolución técnica estructuradas en dos horizontes complementarios:

### 10.3.1. Evolución hacia Producción Institucional (Corto Plazo)

El horizonte inmediato se enfoca en dotar a la plataforma de ejecución física, concurrencia y seguridad perimetral sobre infraestructura institucional:

- **Adaptador Físico de Kubernetes (`RealK8sAdapter`) y Almacenamiento:** Sustituir el adaptador simulado por un adaptador secundario conectado al *Control Plane* de Kubernetes mediante la librería oficial `kubernetes-client`, despachando llamadas autenticadas al API-server tras la aprobación HITL. Asimismo, se incorporará soporte declarativo para `PersistentVolumeClaim` (PVC), posibilitando la provisión de bases de datos con persistencia en disco real.
- **Persistencia Distribuida y Concurrencia (PostgreSQL):** Migración del repositorio SQLite embebido hacia un motor relacional cliente-servidor (PostgreSQL). La abstracción del patrón *Repository* de la Arquitectura Hexagonal permite esta sustitución sin alterar el dominio, habilitando despliegues del backend en alta disponibilidad con múltiples trabajadores Uvicorn/Gunicorn.
- **Control de Acceso Basado en Roles (RBAC) y Autenticación:** Incorporar autenticación perimetral basada en OAuth2 y OpenID Connect con tokens JWT, federada con el directorio institucional (Keycloak, LDAP). Se discriminarán perfiles de investigador frente a operadores del SIC autorizados para aprobar despliegues en el panel de control.
- **Edición Asistida en el Flujo HITL:** Permitir que el operador técnico ajuste parámetros de la intención (como cuotas de CPU o puertos) directamente en la consola antes de confirmar el despliegue, evitando reiniciar la interacción ante discrepancias menores.

### 10.3.2. Integración en Plataformas y Gobernanza Declarativa (Medio Plazo)

El horizonte a medio plazo persigue integrar el sistema en los flujos modernos de entrega continua e ingeniería de plataformas:

- **Adopción del Paradigma GitOps (ArgoCD / Flux):** Depositar los manifiestos generados en un repositorio Git versionado en lugar de aplicarlos directamente (*Push Model*), delegando la sincronización en controladores de reconciliación declarativa como ArgoCD o Flux para garantizar auditoría y recuperación ante desastres.
- **Observabilidad en Tiempo Real (Prometheus y Grafana):** Dotar al agente de herramientas MCP de telemetría operativa para consultar la carga real y cuotas del clúster antes de formular una propuesta de despliegue, asistiendo al operador en la toma de decisiones.
- **Gobernanza Declarativa (*Policy-as-Code*):** Externalizar las políticas del validador de seguridad hacia motores declarativos estándar como Open Policy Agent (OPA) [46] o Kyverno [47], permitiendo al equipo de ciberseguridad actualizar normativas de forma desacoplada del ciclo de vida del backend.
- **Desacoplamiento del Estado Conversacional (*Stateful Slot Filling*):** Consolidar la arquitectura de extracción desacoplada de entidades para eliminar el historial acumulativo de la ventana de contexto del LLM, erradicando el riesgo de degradación atencional documentado en este trabajo.
