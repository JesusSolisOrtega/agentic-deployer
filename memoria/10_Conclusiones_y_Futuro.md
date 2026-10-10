# Capítulo 10. Conclusiones, Limitaciones y Trabajo Futuro

La convergencia entre la Inteligencia Artificial Generativa y la automatización de la infraestructura operativa (*Platform Engineering*) representa uno de los vectores de innovación más significativos de la década. Este Trabajo de Fin de Máster nació con la ambición de gobernar dicha intersección, transformando el comportamiento impredecible de los Modelos de Lenguaje en una herramienta corporativa determinista, segura y auditable.

A continuación, se exponen las conclusiones derivadas de la validación empírica del sistema, las limitaciones inherentes al alcance del prototipo y la hoja de ruta estratégica para su evolución futura.

## 10.1. Conclusiones

La conceptualización, desarrollo y sometimiento a pruebas de estrés del *Agentic Deployer* ha demostrado de manera concluyente la viabilidad técnica de delegar la provisión de infraestructura a agentes autónomos, siempre y cuando se encuentren bajo un control arquitectónico estricto. Las conclusiones fundamentales derivadas de este trabajo de investigación se articulan en cinco puntos:

### 10.1.1. Superación del *Vendor Lock-In* mediante MCP

La decisión arquitectónica de aislar el catálogo de operaciones del Servicio de Informática (SIC) utilizando el **Model Context Protocol (MCP)** [10] se ha revelado como el mayor acierto estratégico del proyecto. Se ha demostrado empíricamente que es posible construir herramientas de automatización complejas sin escribir una sola línea de código acoplada a las APIs nativas de OpenAI, Google o Anthropic. El servidor MCP desarrollado actúa como un activo tecnológico universal; su capacidad para inyectar *JSON Schemas* dinámicamente mediante la introspección de funciones Python asegura que el código universitario heredará compatibilidad nativa con cualquier evolución futura de los Modelos de Lenguaje.

Este desacoplamiento estratégico se validó materialmente en dos frentes. En primer lugar, con la implementación del `OllamaLLMClient` nativo (sección 5.2.1), que sustituyó la dependencia en la API de OpenAI por un modelo ejecutado localmente (`qwen2.5:7b`), sin modificar una sola línea de la lógica de negocio hexagonal ni del servidor MCP. En segundo lugar, mediante la validación del servidor con el **MCP Inspector** — la herramienta de certificación oficial de Anthropic — que, ejecutándose de forma completamente independiente al cliente Streamlit del proyecto, fue capaz de descubrir (`tools/list`) e invocar todas las herramientas del catálogo del SIC mediante el protocolo `stdio` estándar. Esta doble evidencia certifica que el servidor MCP del proyecto es un activo interoperable: consumible indistintamente por el agente propio, por herramientas de auditoría externas y por clientes de terceros (documentado en el README del repositorio mediante el MCP Inspector oficial).

### 10.1.2. La Arquitectura Hexagonal como Mecanismo de Contención Cognitiva

Uno de los mayores hallazgos de este trabajo es la refutación práctica del mito de la "Inteligencia Artificial incontrolable" en entornos de operaciones. La adopción del patrón *Ports and Adapters* (Arquitectura Hexagonal) [16] ha demostrado ser un mecanismo de contención eficaz contra las "alucinaciones" del LLM.

Al forzar a la IA a cruzar la frontera de un Dominio inmutable fuertemente tipado (`Pydantic`) y regido por un validador determinista (`SecurityContextValidator`), la estocasticidad queda fuertemente mitigada antes de alcanzar la capa de infraestructura. El sistema no confía en la precisión del LLM; asume que este fallará, intercepta sus errores y los retroalimenta (*Feedback Loop*), creando un mecanismo iterativo de corrección automática. El escenario de *Prompt Injection* documentado en la sección 8.2 certifica que ni siquiera una instrucción deliberadamente maliciosa (`ubuntu:latest`, puerto `22`) consigue atravesar la barrera hexagonal: el sistema la intercepta, devuelve un `HTTP 422`, y el agente se autocorrige en la siguiente iteración ReAct.

### 10.1.3. La Ineludibilidad del Patrón *Human-In-The-Loop*

En contraste con la corriente de mercado que persigue la autonomía algorítmica total (Nivel 5), este TFM concluye que en infraestructuras críticas institucionales, el humano es un componente crítico y necesario. La implementación de la Máquina de Estados Finita (FSM) y el *Dashboard* asíncrono demostró que la barrera humana (HITL) no erosiona la eficiencia del sistema, sino que la maximiza bajo un modelo de **Asimetría de Contexto Triangular**: el agente LLM asume el esfuerzo cognitivo de generar manifiestos válidos y seguros, el técnico SIC ejerce la soberanía legal con un solo clic, y el investigador recibe una notificación del resultado directamente en la interfaz conversacional (sección 6.4).

La reducción del tiempo de entrega demostrada —de ~4.340 minutos (ITSM clásico) a ~9 minutos (ciclo E2E con HITL)— certifica que la supervisión humana y la eficiencia extrema no son objetivos mutuamente excluyentes cuando el agente abstrae correctamente la carga cognitiva.

### 10.1.4. Redefinición del Aseguramiento de Calidad (QA) y los Falsos Positivos de Cobertura

Las metodologías de *testing* convencionales son insuficientes para sistemas estocásticos. El TFM ha validado que auditar IAs generativas requiere paradigmas avanzados. La integración de *Property-Based Testing* (Hypothesis) [32] y Pruebas Metamórficas [33] ha demostrado que el agente extrae entidades matemáticas correctas a partir de texto con alto ruido sintáctico.

De igual trascendencia ha sido el descubrimiento derivado del *Mutation Testing* (Mutmut): se ha evidenciado que una alta cobertura de líneas no garantiza la resiliencia lógica. La auditoría inicial detectó **30 mutantes supervivientes** en los parsers de recursos auxiliares (`_parse_cpu`, `_parse_ram`), brechas que las métricas clásicas reportaban como "cubiertas". Este hallazgo permitió refactorizar el código, eliminar lógica muerta y neutralizar dichos mutantes antes de la entrega final, resolviendo la deuda técnica. Esto constituye una contribución metodológica por sí misma, demostrando la superioridad epistémica del *Mutation Testing* como herramienta de mejora continua para sistemas de infraestructura crítica.

### 10.1.5. La Interfaz Conversacional como Democratizador de la Infraestructura

La evaluación empírica de los tres escenarios (Cap. 8.3) ha confirmado la hipótesis central del proyecto: es posible que un investigador sin formación en Kubernetes gestione el despliegue de servicios productivos mediante lenguaje natural. Frases como *"necesito un portal web para el congreso de IA del departamento, esperamos 200-300 personas"* son suficientes para que el sistema genere un manifiesto Kubernetes completo y válido (Deployment + Service + Ingress, véase Anexo A), atraviese la validación de seguridad hexagonal y notifique al técnico SIC para su aprobación en cuestión de segundos.

En síntesis, este Trabajo de Fin de Máster aporta una **arquitectura de referencia replicable**, demostrando que la Inteligencia Artificial no viene a reemplazar al ingeniero de infraestructuras, sino a abstraer la aridez del código declarativo bajo una capa de razonamiento lingüístico natural, preservando íntegra la cadena de responsabilidad humana.

### 10.1.6. Garantía de Persistencia (Transacciones ACID)

El desarrollo del MVP ha resuelto con éxito el desafío de la persistencia de estado en sistemas agénticos. Mediante la implementación del patrón de repositorio (`SQLiteDeploymentRepository`), el sistema ha abandonado el almacenamiento volátil en memoria para garantizar que el historial de intenciones y aprobaciones (la Máquina de Estados) sobreviva a reinicios del servidor. Esta inyección de dependencias consolida el diseño hexagonal y certifica que el prototipo es robusto y ACID-compliant frente a fallos de infraestructura.

### 10.1.7. La Estabilización Cognitiva en Hardware Modesto (7B)

La conclusión más reveladora sobre el uso empírico de LLMs locales es el impacto directo de la arquitectura sobre las capacidades intrínsecas del modelo. Durante las pruebas (documentadas en la sección 8.4), modelos de 7B (Qwen 2.5 y Mistral) presentaron severas limitaciones al intentar orquestar flujos conversacionales mediante la arquitectura clásica (ReAct o *Chain of Thought*), colapsando frecuentemente por dilución de atención y emitiendo JSONs inválidos.

Sin embargo, al transicionar hacia una arquitectura de Máquina de Estado Destilado —donde el LLM actúa únicamente como extractor semántico pasivo y Python asume el control del flujo determinista—, **estos mismos modelos alcanzaron niveles de éxito cercanos al 100% sin necesidad de aumentar sus parámetros ni aplicar *fine-tuning***. Este hallazgo sugiere que los modelos locales de 7B no carecen de la capacidad lógica necesaria, sino que las arquitecturas agénticas tradicionales sobrecargan su capacidad cognitiva. Aliviar esta carga permite "rescatar" modelos que de otro modo serían descartados por su tasa de error, habilitando una IA corporativa mucho más predecible sobre hardware de consumo estándar.

### 10.1.8. Viabilidad Híbrida y las Limitaciones Cognitivas del Cloud

La validación empírica final, incorporando ecosistemas en la nube como **Google Gemini 3.5 Flash** y proveedores de alta velocidad (LPUs) como **Groq**, arrojó resultados determinantes sobre el uso de infraestructura externa. Si bien los modelos comerciales alcanzan el éxito en escenarios interactivos relajados, las pruebas de estrés metamórfico revelaron ciertas limitaciones estructurales del paradigma "Cloud-First":

1. **La influencia del tamaño de parámetros y la especialización:** Durante los experimentos se testearon modelos especializados en código fuente (`codestral-latest` de Mistral). Paradójicamente, no lograron superar ninguna de las pruebas de alto estrés (0/6). A pesar de su inmensa pericia en programación, al carecer de un *fine-tuning* estricto y nativo para *Tool Calling*, estos modelos tienden a ignorar el esquema JSON y retornan respuestas conversacionales, dificultando su compatibilidad con estándares modernos de orquestación como MCP (*Model Context Protocol*).
2. **La eficacia de los modelos locales (*Edge*) con soporte nativo:** En contraposición a los modelos masivos, el modelo de reducidas dimensiones `ministral-8b-latest` logró superar los casos prácticos con alta precisión. Esto evidencia que la idoneidad de un modelo para actuar como núcleo de un agente no reside exclusivamente en su tamaño, sino en su entrenamiento explícito para interpretar catálogos de herramientas, validando que el *Edge AI* (IA local) puede llegar a soportar cargas de orquestación.
3. **La estocasticidad latente (Gemini):** Incluso Gemini 3.5 Flash, diseñado específicamente para este fin, evidenció una **Tasa de Éxito del 66%**, fallando al procesar la invarianza a mayúsculas (MR-3) y el cruce lingüístico (MR-6) al emitir estructuras JSON inválidas bajo estrés.
4. **El riesgo de fragmentación y gobernanza (*Rate Limits*):** La adopción comercial implica dependencia de la infraestructura de terceros. Ecosistemas como Groq pueden retirar modelos sin previo aviso (p. ej., `llama-3.1-8b-instant`), mientras que las políticas de uso gratuito estandarizadas devuelven errores recurrentes `HTTP 429 Rate Limit Exceeded`, exigiendo implementar rutinas de retardo asíncrono para mantener la estabilidad.

Esto indica empíricamente que la adopción de ecosistemas *cloud* gigantescos no es una solución exenta de riesgos frente a las "alucinaciones" estocásticas. Las redes neuronales profundas siguen beneficiándose sustancialmente de mecanismos deterministas de contención como el que ofrece la Arquitectura Hexagonal y la Máquina de Estados Finita. Adicionalmente, el requerimiento de cuotas y la volatilidad de los proveedores evidencia que la nube traslada parte del riesgo desde la inteligencia del agente hacia la gobernanza de la infraestructura.

### 10.1.9. Resumen Comparativo de Modelos Evaluados

Como consolidación de los experimentos realizados durante el desarrollo del *Agentic Deployer*, la siguiente tabla clasifica los modelos de lenguaje según su viabilidad para actuar como motores cognitivos en arquitecturas de agentes autónomos (con soporte estricto para *Tool Calling* y JSON):

| Proveedor | Modelo | Modalidad | Capa Gratuita | Viabilidad / Adecuación al Proyecto | Observaciones Empíricas |
|---|---|---|---|---|---|
| **Ollama** | `qwen2.5-coder:7b` | Local | Sí (Hardware propio) | **Excelente (Soberanía)** | Superó el stress-test metamórfico con un 100% de éxito. Su hiper-especialización en código y *Tool Calling* elimina las alucinaciones estructurales, validando que la especialización del modelo compensa las limitaciones de hardware. |
| **Ollama** | `qwen2.5:7b` | Local | Sí (Hardware propio) | **Alta (Soberanía)** | Sorprendente resiliencia (50% en metamórficos). Capaz de solventar casos prácticos iterando. Proyecta un rendimiento excelente para despliegues locales (Zero Data Retention) al escalar a modelos superiores (32B/72B) con hardware dedicado. |
| **Google** | `gemini-3.5-flash` | Cloud | Sí (15 RPM) | **Alta** | El más resiliente a nivel estructural. Tasa de éxito del 66% (4/6) en el riguroso stress-test metamórfico (Zero-Shot). |
| **Mistral** | `ministral-8b-latest`| Cloud | Sí | **Alta** | Excelente rendimiento en casos prácticos con System Prompt (Máquina de Estados), pero colapsa (0/6) en el stress-test metamórfico puro. |
| **Mistral** | `codestral-latest` | Cloud | Sí | **Nula** | Pese a su especialización en código, carece de *fine-tuning* para herramientas estructuradas (responde con texto libre). |
| **Cohere** | `command-r-plus` | Cloud | Sí (1k rpm) | **Alta** | Modelo construido para *Tool Calling*. Empata con Gemini en resiliencia metamórfica (66%), colapsando bajo entropía coloquial. |
| **Groq** | `Qwen 3.8 (27B)` | Cloud (LPU) | Sí (30 RPM / 1K TPM) | **Alta** | Rendimiento y velocidad excelentes, pero el límite de tokens (*Rate Limit*) bloquea su uso ininterrumpido. |
| **Mistral** | `mistral-small-latest` | Cloud | Limitada (429) | **Media** | Adecuado técnicamente, pero la estricta gobernanza de "Le Free Tier" (Error 429) bloquea su uso práctico continuado. |

**El Mejor Rendimiento Empírico y la Promesa Local:**
La experimentación ha revelado una dualidad interesante en la nube: por un lado, **`gemini-3.5-flash`** y **`cohere-command-r-plus`** demostraron ser campeones de la resiliencia estructural en modelos generalistas (empatando al 66% en el stress-test aislado). Que ni siquiera un modelo corporativo ultra-especializado en *Tool Calling* como Cohere logre el 100% en solitario (al confundirse con ruido coloquial) justifica la pertinencia de nuestra Arquitectura Hexagonal. Por otro lado, precisamente gracias al apoyo de esta arquitectura y sus barreras de contención, modelos más compactos como **`ministral-8b-latest`** logran ofrecer un rendimiento funcional altamente satisfactorio en casos prácticos convencionales, mitigando sus evidentes debilidades en entornos no guiados (*zero-shot*). 

Sin embargo, el hallazgo empírico definitivo que consolida este trabajo de investigación corresponde a la variante especializada **`qwen2.5-coder:7b`**. Pese a ejecutarse en hardware de consumo estándar (8GB VRAM), este modelo se ha consolidado como el motor cognitivo más fiable de todo el catálogo evaluado: demostró una precisión milimétrica en la simulación de escenarios realistas *End-to-End* (promediando 1,0 iteraciones) y ha sido el único modelo capaz de superar con un **100% de éxito** la batería inicial de pruebas metamórficas, batiendo incluso a los modelos comerciales masivos de la nube. Este resultado valida de manera concluyente la hipótesis de que la optimización del corpus de entrenamiento (código, JSON, YAML) es un factor más determinante para el *Tool Calling* que el recuento bruto de parámetros. En consecuencia, la adopción de modelos locales especializados en código garantiza un rendimiento de grado empresarial idóneo para despliegues institucionales sujetos a **Zero Data Retention**, maximizando la eficiencia de inferencia sin comprometer la soberanía del dato ni el presupuesto.

**Modelos excluidos de la evaluación (Ausencia de capa gratuita ilimitada):**
Es necesario mencionar que estándares de la industria tecnológica como **GPT-4o (OpenAI) [35]** o **Claude 3.5 Sonnet (Anthropic) [36]** no han sido integrados en las pruebas empíricas por requerir pago por token. Sin embargo, según la documentación técnica de los propios fabricantes y los *benchmarks* del sector, estos modelos han sido sometidos a un intenso *fine-tuning* diseñado específicamente para flujos de trabajo agénticos (*Agentic Workflows*). En particular, empresas como Anthropic afirman que la familia Claude está optimizada para la interacción impecable con herramientas externas y protocolos como MCP (*Model Context Protocol*). En consecuencia, su adecuación a este proyecto se presupone sobresaliente, y constituirían la opción más segura en un entorno corporativo con presupuesto asignado. Adicionalmente, plataformas agregadoras como **OpenRouter** (con su endpoint gratuito `llama-3.1-8b-instruct:free`) podrían constituir alternativas viables para futuras líneas de investigación sin coste económico.

## 10.2. Limitaciones del Prototipo

Todo sistema de investigación que persiga la honestidad académica debe documentar con precisión sus limitaciones inherentes. El *Agentic Deployer* es un *Minimum Viable Product* (MVP) avanzado cuya función es demostrar la viabilidad de la arquitectura, no sustituir un sistema de orquestación empresarial maduro. Las siguientes limitaciones son conscientes, deliberadas y en varios casos representan las semillas del trabajo futuro descrito en la sección 10.3.

### 10.2.1. Adaptador de Kubernetes Simulado (`FakeK8sAdapter`)

La materialización final de los manifiestos YAML se produce mediante volcado en el sistema de archivos local, no mediante una llamada real a la API de Kubernetes. El sistema genera YAML semánticamente correcto y aplicable (como certifica el Anexo A), pero no ha sido ejecutado contra un clúster físico. Esto limita la validación de:

- **Factibilidad de los recursos declarados:** Kubernetes podría rechazar el `ResourceQuota` si el *namespace* tiene límites distintos a los calculados por el `_calculate_congress_resources`.
- **Conflictos de nombres:** Un servicio con el mismo nombre que uno existente generaría un conflicto de `409 Conflict` en el API-server de K8s, no recogido actualmente por el flujo de error.
- **Certificados TLS:** El manifiesto de `Ingress` referencia a `cert-manager` como emisor de certificados. En un clúster sin `cert-manager` instalado, el `Ingress` quedaría en estado `Pending` indefinidamente.

### 10.2.2. Autenticación y Autorización Ausentes

Los endpoints del backend (`/mcp/intent`, `/hitl/approve`, `/hitl/status`) **carecen de cualquier mecanismo de autenticación** (OAuth2, JWT, API Keys). En el prototipo, cualquier proceso con acceso a la red local puede aprobar o rechazar despliegues. En un entorno productivo, esto representa una vulnerabilidad crítica de escalada de privilegios.

La integración con sistemas institucionales de identidad (como LDAP, Active Directory o Keycloak) y la implementación de un modelo RBAC (Role-Based Access Control) con roles diferenciados (`investigador`, `tecnico-sic`, `admin`) es un requisito de seguridad ineludible antes de cualquier despliegue real.

### 10.2.3. *Prompt Injection* Avanzada y Jailbreaking

El sistema ha demostrado resiliencia frente al *Prompt Injection* básico (Cap. 8.2). Sin embargo, la comunidad de seguridad en IA ha documentado vectores de ataque más sofisticados que podrían superar las defensas actuales:

- **Inyección indirecta:** Si el LLM tiene acceso a recursos externos (páginas web, correos electrónicos), un documento malicioso podría embeber instrucciones diseñadas para manipular al agente sin que el usuario sea consciente del ataque.
- **Jailbreaking mediante contexto acumulativo:** Un usuario malintencionado podría, a través de múltiples turnos de conversación, ir erosionando el `SYSTEM_PROMPT` del agente hasta conseguir que este ignore las restricciones institucionales.

La mitigación de estos vectores avanzados requiere capas defensivas adicionales no implementadas en el MVP: sanitización del contexto entre sesiones, detección de anomalías en el historial y sistemas de auditoría de los mensajes del sistema.

### 10.2.4. Cobertura de *Golden Paths* y Catálogo de Herramientas

El servidor MCP expone actualmente un catálogo de herramientas extenso y diverso para resolver las necesidades cotidianas del SIC: `deploy_congress_web`, `deploy_department_cms`, `deploy_python_app`, `deploy_static_website`, `deploy_database`, `get_deployment_status` y `delete_university_service`. Aunque estas rutas doradas cubren un amplio abanico de casos de uso, quedan excluidos del catálogo operaciones complejas de gestión continua:

- Escalado horizontal dinámico de réplicas (`scale_deployment`)
- Consulta y filtrado de estado de los pods en ejecución (`get_pod_status`)
- Gestión de *ConfigMaps* y *Secrets* de Kubernetes
- Operaciones de actualización progresiva (*rolling update*)

Cada herramienta nueva requeriría la definición de un nuevo *Golden Path* validado por el equipo de seguridad del SIC, un proceso de gobernanza que escapa al alcance del prototipo pero que está arquitectónicamente previsto.

### 10.2.5. Escalabilidad y Concurrencia del Backend

El backend FastAPI opera en modo síncrono sobre un único proceso Uvicorn. En un entorno con múltiples técnicos SIC consultando el Dashboard simultáneamente y múltiples investigadores generando intenciones a través del chat, el sistema podría experimentar cuellos de botella y requerir despliegues multi-proceso más robustos (ej. Gunicorn con múltiples *workers*), aunque el uso del repositorio en SQLite resuelve estructuralmente las condiciones de carrera locales de la máquina de estados.

### 10.2.6. Rigidez del Flujo de Decisión (Inmutabilidad Pre-Despliegue)

Actualmente, el técnico SIC en el panel HITL posee una autoridad estrictamente booleana: puede Aprobar o Rechazar el despliegue. Si el agente de IA propone una configuración correcta pero con un límite de RAM ligeramente excesivo, el técnico no puede editar ese valor (*Pre-Deployment Mutability*). Su única opción es rechazar la intención, obligando al investigador a formular una nueva petición al LLM con instrucciones más restrictivas. En futuras iteraciones, la interfaz debería permitir la "Edición Asistida", posibilitando que el técnico ajuste los parámetros de la `DeploymentIntent` justo antes de autorizar la transición al adaptador de infraestructura, flexibilizando enormemente la operatividad.

### 10.2.7. Ausencia de Validación Empírica con Usuarios Reales

Las métricas de eficiencia operativa documentadas en el Capítulo 8 se basan en una ejecución forense simulada por el propio investigador. El sistema no ha sido sometido a pruebas de usabilidad estructuradas (como la métrica SUS - *System Usability Scale*) con usuarios ajenos al proyecto. La interacción de investigadores sin perfil técnico real frente a la interfaz conversacional podría revelar barreras cognitivas o requerimientos de accesibilidad no previstos en este MVP, por lo que la afirmación sobre la usabilidad universal del sistema debe interpretarse como una viabilidad técnica, sujeta a futura validación empírica en un entorno de laboratorio.

### 10.2.8. Restricciones de Hardware y Elección de Modelos (Latencia y Capacidades)

Las métricas empíricas documentadas en el Capítulo 8 están fuertemente condicionadas por la infraestructura física subyacente. Todo el entorno de pruebas ha sido ejecutado localmente utilizando una GPU de portátil orientada al consumo (NVIDIA GeForce RTX 3060 con 6 GB de VRAM).

Esta barrera de 6 GB de memoria de vídeo forzó la elección de modelos de tamaño reducido (<8B parámetros) y el uso de técnicas agresivas de compresión (cuantización a 4 bits). Esto explica la divergencia de rendimiento: mientras **Qwen 2.5 (7B)** demostró un *fine-tuning* excelente logrando orquestar el bucle ReAct frente a Llama o Mistral, el escrutinio empírico reveló su fragilidad cognitiva subyacente. Como se demostró en las Pruebas Metamórficas (Sección 7.4), Qwen generalista fracasó en el 50% de los casos (ruido léxico y composición incremental) al colapsar su ventana de atención. Originalmente se asumía que superar esto requeriría hardware corporativo (16GB-24GB VRAM) para desplegar modelos masivos (ej. Qwen 2.5 14B/32B o Llama 3.1 70B). No obstante, la evaluación posterior de la variante especializada **Qwen 2.5 Coder (7B)** evidenció que la adaptación del corpus de entrenamiento orientado a código permite mitigar esta restricción operativa, posibilitando la consecución de métricas de fiabilidad corporativas dentro de la misma envolvente térmica y de hardware.

Del mismo modo, las latencias observadas (que alcanzan los 47 segundos en casos de multi-iteración ReAct) son un artefacto directo de la falta de ancho de banda y capacidad de cómputo del hardware portátil. En un entorno productivo con aceleración dedicada o *endpoints* gestionados corporativos, estos tiempos de inferencia se colapsarían a escasos segundos, ofreciendo una experiencia en tiempo casi real.

### 10.2.9. Barrera Lingüística y Degradación del Razonamiento en Español

Todo el prototipo y la experimentación empírica se han desarrollado forzando la interacción del agente íntegramente en castellano (tanto el *System Prompt*, como las intenciones de usuario y las definiciones semánticas de las herramientas). Dado que la inmensa mayoría del corpus de entrenamiento de los modelos fundacionales (*Large Language Models*) está en idioma inglés, existe un consenso en la literatura científica de que su capacidad de razonamiento lógico, seguimiento de instrucciones complejas y adherencia a formatos estrictos (como JSON) se degrada notablemente en lenguas secundarias. Es altamente probable que parte de los colapsos sintácticos y alucinaciones experimentados por los modelos locales (Mistral, Llama 3.2, Qwen 2.5) bajo estrés metamórfico (Sección 7.4) estén agravados por esta disonancia lingüística, donde el modelo debe "traducir" mentalmente su lógica de *Tool Calling* nativa (aprendida en inglés) a la interfaz en español.

## 10.3. Trabajo Futuro

El prototipo actual certifica empíricamente la viabilidad de la integración agéntica en sistemas deterministas. Su consolidación operativa en un entorno productivo de gran escala requiere abordar una serie de mejoras iterativas. Las futuras líneas de desarrollo se desglosan en tres horizontes temporales estratégicos.

### 10.3.1. Horizonte a Corto Plazo: Integración Física (K8s API)

El diseño Hexagonal permite la sustitución de la capa de persistencia actual (`FakeK8sAdapter`) sin impactar la lógica de negocio subyacente. El primer hito evolutivo consiste en desarrollar e inyectar un **`RealK8sAdapter`** utilizando la librería oficial de Kubernetes para Python (`kubernetes-client`). En lugar de volcar manifiestos YAML estáticos en el disco físico del servidor, el adaptador consumirá directamente el *Control Plane* de un clúster físico experimental (como Minikube, K3s o un entorno *sandbox* universitario), permitiendo que la aprobación del técnico (HITL) despierte los *pods* de forma inmediata. El código base de esta integración se documenta en el Anexo A (sección A.3).

De forma paralela a esta integración, debe abordarse la consolidación de la persistencia mediante repositorios distribuidos como PostgreSQL (evolucionando la solución actual basada en SQLite para entornos de alta disponibilidad) y la **autenticación JWT** en todos los endpoints (mitigando la limitación 10.2.2).

### 10.3.2. Horizonte a Medio Plazo: Adopción de la Filosofía GitOps

Una de las premisas fundamentales del movimiento *Platform Engineering* es la trazabilidad declarativa mediante sistemas de control de versiones. Actualmente, el flujo de ejecución sigue un modelo *Push* (el adaptador intenta empujar los recursos al clúster).

Para alinear el sistema con los más altos estándares corporativos, se propone evolucionar hacia un modelo **GitOps (Pull-based)**:
- El adaptador secundario no atacará a Kubernetes directamente, sino que realizará un *commit* de los YAML autogenerados hacia un repositorio Git (ej. GitLab o GitHub) dedicado a la topología del clúster.
- Herramientas de reconciliación consolidadas, como **ArgoCD** o **Flux**, monitorizarán dicho repositorio. Al detectar un nuevo *commit* aprobado por el sistema HITL, ArgoCD se encargará de traccionar (*pull*) los manifiestos y aplicarlos en el clúster.

Esta separación garantizará un *Disaster Recovery* altamente fiable y una trazabilidad de auditoría completa, ya que el estado real del centro de datos siempre residirá en un repositorio Git versionado. Adicionalmente, se propone escalar el catálogo de herramientas MCP para cubrir las operaciones de gestión ausentes (limitación 10.2.4).

### 10.3.3. Horizonte a Largo Plazo: Policy-as-Code y Agentic DevSecOps

El modelo de seguridad actual (`SecurityContextValidator`) debe evolucionar hacia motores empresariales de **Policy-as-Code (OPA [37] o Kyverno [38])**, permitiendo a Ciberseguridad definir reglas dinámicas (*Rego*) sin alterar el código de la API. 

No obstante, el *Policy-as-Code* tradicional sigue anclado a recetas estáticas. La evolución natural del prototipo apunta hacia el **Agentic LLM DevSecOps**, donde el agente aplica **razonamiento semántico** para integrarse de forma activa en el ciclo CI/CD. Esta arquitectura habilitaría funciones autónomas como:
1. **Triaje Inteligente:** Reducir falsos positivos aplicando contexto (ej. ignorar vulnerabilidades si el servicio está aislado tras un *API Gateway*).
2. **Auto-Remediación (*Self-healing*):** Detectar dependencias vulnerables, parchear el `Dockerfile`, lanzar tests automáticos y proponer el *commit*.
3. **Ajuste Dinámico:** Modificar *Network Policies* de Kubernetes en caliente ante amenazas (ej. alertas de *Falco*) entendiendo semánticamente el problema, sin depender de manuales estáticos (útil ante vulnerabilidades Zero-Day como *Log4j*).

Otorgar esta autonomía a la IA conlleva riesgos severos de *Shadow AI* y alucinaciones. Precisamente, **el flujo HITL desarrollado en este TFM** es el paso fundamental para un *Human-in-the-loop Agentic DevSecOps*: el agente asimila miles de telemetrías y propone acciones complejas en segundos, pero el operario humano retiene la autoridad del "clic" final para mutar la infraestructura de forma segura.

### 10.3.4. Observabilidad y Conciencia Agéntica del Entorno

Una ampliación natural y muy ambiciosa del sistema consiste en dotar al agente de herramientas MCP de **observabilidad en tiempo real** (*read-only*), permitiéndole consultar métricas y telemetría del clúster (por ejemplo, integrando herramientas MCP que lean directamente de Prometheus o Grafana).

Lejos de contradecir la filosofía restrictiva del proyecto, esto la complementa dotando a la IA de "sentidos": el agente no tendría permisos para modificar la infraestructura arbitrariamente, pero podría razonar sobre su estado. Si el clúster presenta alta saturación de CPU, el agente podría adaptar su decisión dinámicamente y negociar con el investigador en términos puramente de negocio (*"Actualmente los servidores del SIC tienen mucha carga, ¿es aceptable arrancar la web del congreso en un modo básico consumiendo la mitad de recursos por ahora?"*). 

Paralelamente, el agente podría inyectar esta telemetría como metadatos de advertencia en la intención (`DeploymentIntent`) para que el técnico del SIC disponga del contexto de saturación en el *Dashboard HITL* antes de aprobar. Esta capacidad acercaría definitivamente el prototipo a la figura ideal de un **Operador de Plataforma Autoconsciente**, preservando en todo momento la abstracción técnica del investigador.

### 10.3.5. QA Avanzado: Pruebas Metamórficas Estocásticas con LLM Adversario

La suite de pruebas actual ha demostrado la utilidad de las Relaciones Metamórficas (MR) deterministas (variaciones de orden, ruido y capitalización) para auditar el comportamiento del agente. Para escalar este modelo de aseguramiento de calidad (*QA*) hacia entornos empresariales de alta exigencia, una evolución natural propuesta consiste en implementar generadores de pruebas basados en **LLMs Adversarios**. 

En este paradigma, un segundo modelo de lenguaje actuaría como generador de casos de prueba estocásticos, encargado de redactar intenciones de despliegue con alta entropía semántica (ambigüedades deliberadas, jerga interdepartamental compleja o estructuras gramaticales inusuales). Esto permitiría automatizar la validación de la robustez cognitiva del orquestador ReAct frente a un espectro sumamente amplio de interacciones de usuario, superando las limitaciones espaciales del *testing* programado manualmente y alineando el sistema con el estado del arte en pruebas para Inteligencia Artificial.

### 10.3.6. Evolución Cognitiva: Estado Destilado y Clasificación de Intenciones

El patrón arquitectónico *ReAct* implementado en este TFM se basa en un paradigma de **Historial Sin Estado** (*Stateless History*), donde el orquestador reinyecta iterativamente la transcripción completa de la conversación en la ventana de contexto del LLM. Como se analizó en la Sección 7.4.3, este enfoque presenta vulnerabilidades cognitivas severas en modelos pequeños (como Qwen 7B) debido al fenómeno de dilución de atención (*Attention Dilution*) tras múltiples turnos conversacionales.

Para evolucionar el prototipo hacia estándares de grado de producción equivalentes a los frameworks empresariales (como los definidos en la arquitectura de memoria de *LangChain* o *LlamaIndex*), se propone transicionar hacia un patrón de **Llenado de Huecos con Estado** (*Stateful Slot Filling*) [39] combinado con **Destilación de Contexto** (*Context Distillation*) [40][41]:

1. **Destilación de Memoria:** En lugar de saturar el contexto con el histórico crudo de mensajes, el backend mantendrá un diccionario de estado temporal (ej. `{"intent": null, "image": null, "port": null}`). Una heurística de fondo purificará cada nuevo mensaje del usuario para actualizar exclusivamente este diccionario, descartando saludos, cortesías o desvíos conversacionales. Al orquestador final solo se le suministrará la "fotografía destilada" del estado actual, garantizando que el modelo mantenga un foco absoluto independientemente de lo larga que haya sido la conversación.
2. **Clasificación Prioritaria de Intenciones (*Intent-First Routing*):** Actualmente, el modelo deduce simultáneamente qué herramienta usar y qué parámetros rellenar. La nueva arquitectura obligaría al agente a priorizar la clasificación de la intención (*Intent Classification*) como paso bloqueante. El agente debe determinar primero qué acción exacta desea el usuario (ej. *"¿Quiere desplegar una web estática o un CMS complejo?"*), ya que las herramientas disponibles en el catálogo MCP (y por ende, los parámetros obligatorios que debe solicitar) dependen estrictamente de esta decisión topológica. 

Esta segregación de responsabilidades cognitivas (*Destilación de Estado* -> *Clasificación de Intención* -> *Extracción de Entidades*) representa un estándar en el diseño de agentes robustos. Para corroborar empíricamente esta hipótesis, se desarrolló y documentó una Prueba de Concepto aislada (`demos/demo_state_machine.py`). En este experimento, el modelo Qwen 2.5 (7B) generalista operó exclusivamente como extractor pasivo, logrando un éxito del 100% bajo estrés conversacional. Originalmente, esta arquitectura de "Rescate Cognitivo" se postulaba como el único horizonte viable para modelos locales limitados. Sin embargo, el rendimiento superior del modelo **Qwen 2.5 Coder (7B)** demuestra que la estabilización del sistema también puede abordarse mediante el uso de modelos especializados (*fine-tuning*). Ambas vías no son mutuamente excluyentes; la orquestación de un modelo especializado mediante una Máquina de Estado Destilado conforma una arquitectura de *Defensa en Profundidad*. Esta redundancia metodológica proporciona una red de seguridad estructural, mitigando la tasa de fallos del sistema frente a la imprevisibilidad inherente de los entornos de producción reales.

### 10.3.7. Interfaz de Usuario Generativa (*Generative UI*) y Componentes Interactivos

Una línea de trabajo futuro altamente prometedora para potenciar la usabilidad del sistema es la integración de interfaces de usuario generativas (*Generative UI*). Actualmente, el flujo de interacción es puramente conversacional basado en texto natural, lo cual puede generar fricción cuando el agente requiere que el investigador (usuario sin perfil técnico) especifique parámetros altamente acotados, como seleccionar un tipo de base de datos o definir cuotas de almacenamiento.

Evolucionar el sistema para que el orquestador (*AgentOrchestrator*) tenga la capacidad de devolver no solo texto, sino también metadatos que el *frontend* (Streamlit) renderice dinámicamente como **componentes interactivos** (formularios, botones de selección, menús desplegables), reduciría drásticamente la carga cognitiva del usuario. De este modo, en lugar de que el usuario tenga que teclear explícitamente el nombre de una imagen de contenedor, el agente podría deducir su necesidad y presentar un panel interactivo con opciones recomendadas para que el investigador simplemente haga clic. 

Más allá de la evidente mejora en usabilidad, este enfoque actúa como un mecanismo de **estabilización cognitiva para la propia Inteligencia Artificial**. Al canalizar la respuesta del usuario a través de opciones discretas y pre-validadas, se evita la inyección de ruido estocástico en la ventana de contexto (faltas de ortografía, jerga, ambigüedades lingüísticas), previniendo por diseño los colapsos documentados durante las pruebas metamórficas. Esta hibridación entre el lenguaje natural y el diseño de interacción tradicional (*Point-and-Click*) representa la vanguardia en el diseño de aplicaciones agénticas. En el contexto específico del Servicio de Informática (SIC), la transición hacia este modelo se perfila como la estrategia de menor resistencia para consolidar la viabilidad operativa y acelerar la adopción institucional del prototipo, al suprimir la curva de aprendizaje del investigador y garantizar, simultáneamente, que el orquestador reciba *inputs* matemáticamente predecibles.

### 10.3.8. Pipelines de Traducción Transparente (*Native English Reasoning*)

En consonancia con la limitación lingüística identificada para los modelos generalistas (Sección 10.2.9), una línea de investigación para elevar la fiabilidad estructural en dichos modelos es la disociación entre el idioma de interfaz y el idioma de procesamiento lógico. Dado que el razonamiento de los LLMs fundacionales alcanza su máximo rendimiento en inglés, el sistema podría adoptar un patrón de **Traducción Transparente** en el *Edge*.

En esta arquitectura, el usuario interactuaría en español a través del *frontend*, pero un modelo ligero interceptaría y traduciría la entrada al inglés. Toda la carga cognitiva (el *System Prompt*, el ciclo *ReAct*) se ejecutaría de forma nativa en inglés, deshaciendo la traducción a la salida. Si bien los hallazgos con el modelo **Qwen 2.5 Coder (7B)** indican que la especialización del corpus mitiga en gran medida la degradación sintáctica al operar en lenguas secundarias, es prudente asumir que esta protección empírica no es absoluta frente a escenarios de uso desestructurado. Por consiguiente, la implementación de *pipelines* de traducción conserva su validez como **red de seguridad algorítmica complementaria**. Al combinar un modelo especializado con un procesamiento lógico nativo en inglés, el sistema minimizaría significativamente el riesgo de colapsos estructurales derivados de la disonancia lingüística, adecuándose a las exigencias de fiabilidad de los entornos corporativos.

### 10.3.9. Inyección Dinámica de Contexto y Documentación (Context MCP)

Uno de los desafíos inherentes a la generación de infraestructura declarativa mediante LLMs es la rápida obsolescencia de las especificaciones técnicas. Kubernetes evoluciona constantemente, depreciando *apiVersions* (ej. la transición de `v1beta1` a `apps/v1`) y modificando esquemas de recursos. Dado que los modelos fundacionales operan con una fecha de corte de conocimiento (*knowledge cutoff*), corren el riesgo de generar manifiestos YAML formalmente correctos pero operacionalmente obsoletos o incompatibles con la versión exacta del clúster institucional.

Para erradicar definitivamente estas "alucinaciones de sintaxis", una línea de futuro altamente estratégica es la incorporación de **Servidores MCP de Contexto Documental** (como *Context7* o análogos). A diferencia del servidor MCP operativo desarrollado en este TFM (cuya función es ejecutar acciones), un Context MCP actuaría como un puente semántico de solo lectura. Permitiría al agente consultar en tiempo real la documentación oficial actualizada de la versión específica de Kubernetes del clúster, o incluso la Wiki interna del departamento SIC, instantes antes de proceder a la generación del manifiesto. 

Esta arquitectura equivale a implementar un RAG (*Retrieval-Augmented Generation*) dinámico integrado orgánicamente dentro del bucle ReAct. Su adopción garantizaría que el razonamiento del agente esté anclado, de forma determinista, a la realidad documental y operativa más estricta de la organización, blindando al sistema frente a la degradación temporal del conocimiento del LLM.
