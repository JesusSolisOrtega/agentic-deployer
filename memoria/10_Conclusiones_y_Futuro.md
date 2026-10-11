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

Las metodologías de *testing* convencionales son insuficientes para sistemas estocásticos. El TFM ha validado que auditar IAs generativas requiere paradigmas avanzados. La integración de *Property-Based Testing* (Hypothesis) [34] y Pruebas Metamórficas [35] ha demostrado que el agente extrae entidades matemáticas correctas a partir de texto con alto ruido sintáctico.

De igual trascendencia ha sido el descubrimiento derivado del *Mutation Testing* (Mutmut): se ha evidenciado que una alta cobertura de líneas no garantiza la resiliencia lógica. La auditoría inicial detectó **30 mutantes supervivientes** en los parsers de recursos auxiliares (`_parse_cpu`, `_parse_ram`), brechas que las métricas clásicas reportaban como "cubiertas". Este hallazgo permitió refactorizar el código, eliminar lógica muerta y neutralizar dichos mutantes antes de la entrega final, resolviendo la deuda técnica. Esto constituye una contribución metodológica por sí misma, demostrando la superioridad epistémica del *Mutation Testing* como herramienta de mejora continua para sistemas de infraestructura crítica.

### 10.1.5. La Interfaz Conversacional como Democratizador de la Infraestructura

La evaluación empírica de los tres escenarios (Cap. 8.3) ha confirmado la hipótesis central del proyecto: es posible que un investigador sin formación en Kubernetes gestione el despliegue de servicios productivos mediante lenguaje natural. Frases como *"necesito un portal web para el congreso de IA del departamento, esperamos 200-300 personas"* son suficientes para que el sistema genere un manifiesto Kubernetes completo y válido (Deployment + Service + Ingress, véase Anexo A), atraviese la validación de seguridad hexagonal y notifique al técnico SIC para su aprobación en cuestión de segundos.

En síntesis, este Trabajo de Fin de Máster aporta una **arquitectura de referencia replicable**, demostrando que la Inteligencia Artificial no viene a reemplazar al ingeniero de infraestructuras, sino a abstraer la aridez del código declarativo bajo una capa de razonamiento lingüístico natural, preservando íntegra la cadena de responsabilidad humana.

### 10.1.6. Garantía de Persistencia (Transacciones ACID)

El desarrollo del MVP ha resuelto con éxito el desafío de la persistencia de estado en sistemas agénticos. Mediante la implementación del patrón de repositorio (`SQLiteDeploymentRepository`), el sistema ha abandonado el almacenamiento volátil en memoria para garantizar que el historial de intenciones y aprobaciones (la Máquina de Estados) sobreviva a reinicios del servidor. Esta inyección de dependencias consolida el diseño hexagonal y certifica que el prototipo es robusto y ACID-compliant frente a fallos de infraestructura.

### 10.1.7. La Estabilización Cognitiva en Hardware Modesto (7B)

La conclusión más reveladora sobre el uso empírico de LLMs locales es el impacto directo de la arquitectura sobre las capacidades intrínsecas del modelo. Durante las pruebas (documentadas en la sección 8.4), modelos de 7B (Qwen 2.5 y Mistral) presentaron severas limitaciones al intentar orquestar flujos conversacionales mediante la arquitectura clásica (ReAct o *Chain of Thought*), colapsando frecuentemente por dilución de atención y emitiendo JSONs inválidos.

Sin embargo, al transicionar hacia una arquitectura de Máquina de Estado Destilado —donde el LLM actúa únicamente como extractor semántico pasivo y la máquina de estados determinista asume el control del flujo—, **estos mismos modelos alcanzaron niveles de éxito cercanos al 100% sin necesidad de aumentar sus parámetros ni aplicar *fine-tuning***. Este hallazgo sugiere que los modelos locales de 7B no carecen de la capacidad lógica necesaria, sino que las arquitecturas agénticas tradicionales sobrecargan su capacidad cognitiva. Aliviar esta carga permite "rescatar" modelos que de otro modo serían descartados por su tasa de error, habilitando una IA corporativa mucho más predecible sobre hardware de consumo estándar.

### 10.1.8. Viabilidad Híbrida y Lecciones de la Experimentación Multi-Modelo

La validación empírica transversal —incorporando motores locales cuantizados (Ollama), aceleradores de ultra-baja latencia en LPUs (Groq) y diversos proveedores comerciales en la nube (Google Gemini, Cohere, Mistral)— trasciende la mera comparativa de rendimiento: constituye una exploración experimental sobre el **estado del arte de los LLMs en tareas de orquestación agéntica**. Este banco de pruebas permite contrastar empíricamente hipótesis teóricas, delimitar las fronteras de robustez del razonamiento automatizado y extraer principios transferibles para el diseño de sistemas de misión crítica:

1. **Alineamiento de dominio frente a escala de parámetros:** La creencia convencional asume que la solvencia agéntica escala directamente con el tamaño del modelo o la capacidad del clúster de inferencia. La experimentación refuta esta premisa para la interacción con herramientas formales: modelos masivos o altamente competentes en programación procedural (como `codestral-latest`) colapsaron ante pruebas de esfuerzo *Zero-Shot* (0/6) por carecer de un ajuste fino específico para *Tool Calling*. En contraste, variantes compactas pero estrictamente alineadas con esquemas estructurados (`qwen2.5-coder:7b` en local o `ministral-8b-latest` en la nube) exhibieron una disciplina sintáctica sobresaliente. Esto sitúa la clave del estado del arte no en la masa crítica de parámetros, sino en el entrenamiento orientado a contratos de interfaz formales (JSON Schema / MCP).
2. **La universalidad de la contención determinista:** Ningún modelo generalista evaluado operando en aislamiento estricto superó el 66% de éxito frente a perturbaciones léxicas y cruce idiomático. Sin embargo, cuando estos mismos motores fueron tutelados por el bucle ReAct, el *System Prompt* y la Máquina de Estados Finita, la tasa de éxito convergió al 100%. Este contraste establece una conclusión metodológica fundamental: **la IA generativa actual no es autosuficiente para la administración de infraestructura sensible**. Su viabilidad productiva depende de que la arquitectura de software (patrón *Ports and Adapters*) actúe como un perímetro determinista que intercepte y absorba la estocasticidad intrínseca de la red neuronal.
3. **El valor del desacoplamiento mediante MCP y Arquitectura Hexagonal:** La integración transparente de motores heterogéneos a través del adaptador `OpenAILLMClient` valida que el diseño desacoplado es esencial en un campo de rápida obsolescencia. Permite a una organización desplegar hoy un modelo soberano local a coste cero (`qwen2.5-coder`) y, en el futuro, conmutar selectivamente hacia modelos de frontera o aceleradores especializados sin alterar la lógica de negocio ni las herramientas del catálogo MCP.
4. **Equilibrio entre soberanía operativa y gobernanza de infraestructura:** La inferencia en la nube ofrece elasticidad computacional, pero introduce fricciones de gobernanza: latencias de red variables, riesgo de fragmentación del catálogo del proveedor y límites de concurrencia (`HTTP 429 Rate Limit Exceeded`). Para entornos institucionales y administraciones públicas, el despliegue soberano *on-premise* bajo el principio de *Zero Data Retention* se consolida como una estrategia viable y de alta resiliencia.

En conjunto, estos hallazgos proporcionan un mapa conceptual claro de dónde se sitúa la tecnología agéntica contemporánea y confirman que la robustez operativa no se compra delegando ciegamente en la nube, sino diseñando sistemas donde la ingeniería de software clásica y la inteligencia estocástica se complementen armónicamente.

### 10.1.9. Resumen Comparativo de Modelos Evaluados

Como consolidación de la extensa experimentación desarrollada a lo largo de este trabajo —cuyos resultados cuantitativos detallados se recogen en las **Tablas 6, 7 y 8** (evaluación metamórfica, Capítulo 7) y en las **Tablas 16 y 17** (matrices comparativas y experimentación multi-modelo, Capítulo 8)—, la siguiente síntesis clasifica los motores cognitivos según su idoneidad para la orquestación agéntica institucional:

| Motor / Modelo | Ámbito | Idoneidad Global | Hallazgo Clave y Referencia Empírica |
|---|---|---|---|
| **`qwen2.5-coder:7b`** (Ollama) | Local | **Excelente (Soberana)** | Motor de máxima fiabilidad. 100% de éxito metamórfico (*Tabla 8*) y 1,0 iteraciones promedio (*Tabla 16*). La especialización en código suple las limitaciones de hardware. |
| **`qwen2.5:7b`** (Ollama) | Local | **Alta (Soberana)** | Resiliencia notable (50% metamórfico, *Tablas 7 y 8*). Viable con refinamiento conversacional, proyectando gran potencial para modelos de 14B/32B. |
| **`gemini-3.5-flash`** (Google) | Cloud | **Alta** | Modelo generalista en la nube más robusto estructuralmente (66% metamórfico, *Tabla 8*). Sujeto a cuotas y políticas de privacidad externas. |
| **`command-r-plus`** (Cohere) | Cloud | **Alta** | Excelente diseño para *Tool Calling*; empata con Gemini (66% metamórfico, *Tabla 8*), si bien sufre degradación bajo lenguaje coloquial extremo. |
| **`ministral-8b-latest`** (Mistral) | Cloud | **Media-Alta** | Desempeño óptimo guiado por la FSM (*Tabla 16*), aunque vulnerable en modo *Zero-Shot* no tutelado (0% metamórfico, *Tabla 8*). |
| **`codestral-latest`** (Mistral) | Cloud | **No Apto** | Inadecuado para orquestación: carece de *fine-tuning* estricto de herramientas JSON, emitiendo texto plano (0% metamórfico, *Tabla 8*). |

**Conclusiones Clave de la Evaluación:**
1. **La especialización supera a la escala bruta:** El rendimiento de `qwen2.5-coder:7b` certifica que el ajuste fino específico sobre código y JSON Schema es más crítico para la invocación de herramientas que el volumen de parámetros o la capacidad de cómputo en la nube. Esto habilita despliegues locales de alta confiabilidad sujetos a políticas de **Zero Data Retention** sobre hardware institucional asequible.
2. **La necesidad ineludible de la contención determinista:** El hecho de que ningún modelo generalista comercial alcanzase el 100% de éxito en solitario ante ruido léxico confirma que la fiabilidad del sistema no puede descansar únicamente en el LLM, ratificando la necesidad de las defensas deterministas provistas por la Arquitectura Hexagonal y la FSM.
3. **Perspectivas comerciales:** Modelos de referencia sujetos a tarifación por token (como **GPT-4o [40]** o **Claude 3.5 Sonnet [41]**) disponen de optimizaciones específicas de fabricante para protocolos como MCP, por lo que su adopción en entornos con presupuesto comercial aseguraría una integración directa de grado empresarial.


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

El modelo de seguridad actual (`SecurityContextValidator`) debe evolucionar hacia motores empresariales de **Policy-as-Code (OPA [42] o Kyverno [43])**, permitiendo a Ciberseguridad definir reglas dinámicas (*Rego*) sin alterar el código de la API. 

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

La viabilidad conceptual y el impacto del patrón de **Llenado de Huecos con Estado (*Stateful Slot Filling*) y Destilación de Contexto** quedaron empíricamente demostrados en el banco de pruebas experimental (Sección 8.4.3, alcanzando una convergencia del 100% en la Tabla 17). No obstante, en la arquitectura de referencia actual del *Agentic Deployer*, el orquestador agéntico continúa gobernando los flujos mediante el bucle reactivo tradicional *ReAct*, reinyectando la transcripción conversacional acumulativa en la ventana de contexto.

Como línea prioritaria de evolución a medio plazo, se propone la **industrialización nativa de este paradigma en el backend productivo del sistema**, estructurada en dos fases:

1. **Transición hacia Orquestación con Estado Persistido:** Evolucionar el motor agéntico desde un bucle de historial acumulativo no estructurado hacia una arquitectura de gestión transaccional de ranuras (*Slot Management*). En lugar de transferir historiales conversacionales completos al LLM, la capa de control mantiene el estado de las variables y parámetros requeridos. Cada nueva interacción del usuario es procesada de forma atómica y aislada por el modelo para extraer o actualizar las ranuras pendientes, liberando la ventana de contexto de ruidos ambientales y garantizando una escalabilidad conversacional indefinida sin degradación atencional.
2. **Clasificación Prioritaria de Intenciones (*Intent-First Routing*):** Actualmente, el modelo deduce simultáneamente qué herramienta usar y qué parámetros rellenar. La arquitectura productiva incorporará un clasificador semántico previo (*Intent Routing*) que determinará la categoría operativa antes de exponer el catálogo MCP (ej. *"¿Desea aprovisionar una web estática o un CMS complejo?"*), presentando al extractor únicamente los esquemas estrictamente pertinentes.

**Sinergia y Defensa en Profundidad:**  
Lejos de ser una alternativa excluyente frente a la especialización del modelo, la industrialización del Estado Destilado junto al modelo local especializado **Qwen 2.5 Coder (7B)** conforma una arquitectura de **Defensa en Profundidad**. La especialización del modelo garantiza una generación sintáctica impecable, mientras que la máquina de estados determinista actúa como red de contención lógica, blindando al sistema frente a la estocasticidad del lenguaje natural en entornos de producción reales.

### 10.3.7. Interfaz de Usuario Generativa (*Generative UI*) y Componentes Interactivos

Una línea de trabajo futuro altamente prometedora para potenciar la usabilidad del sistema es la integración de interfaces de usuario generativas (*Generative UI*). Actualmente, el flujo de interacción es puramente conversacional basado en texto natural, lo cual puede generar fricción cuando el agente requiere que el investigador (usuario sin perfil técnico) especifique parámetros altamente acotados, como seleccionar un tipo de base de datos o definir cuotas de almacenamiento.

Evolucionar el sistema para que el orquestador (*AgentOrchestrator*) tenga la capacidad de devolver no solo texto, sino también metadatos que el *frontend* (Streamlit) renderice dinámicamente como **componentes interactivos** (formularios, botones de selección, menús desplegables), reduciría drásticamente la carga cognitiva del usuario. De este modo, en lugar de que el usuario tenga que teclear explícitamente el nombre de una imagen de contenedor, el agente podría deducir su necesidad y presentar un panel interactivo con opciones recomendadas para que el investigador simplemente haga clic. 

Más allá de la evidente mejora en usabilidad, este enfoque actúa como un mecanismo de **estabilización cognitiva para la propia Inteligencia Artificial**. Al canalizar la respuesta del usuario a través de opciones discretas y pre-validadas, se evita la inyección de ruido estocástico en la ventana de contexto (faltas de ortografía, jerga, ambigüedades lingüísticas), previniendo por diseño los colapsos documentados durante las pruebas metamórficas. Esta hibridación entre el lenguaje natural y el diseño de interacción tradicional (*Point-and-Click*) representa la vanguardia en el diseño de aplicaciones agénticas. En el contexto específico del Servicio de Informática (SIC), la transición hacia este modelo se perfila como la estrategia de menor resistencia para consolidar la viabilidad operativa y acelerar la adopción institucional del prototipo, al suprimir la curva de aprendizaje del investigador y garantizar, simultáneamente, que el orquestador reciba entradas deterministas y predecibles.

### 10.3.8. Pipelines de Traducción Transparente (*Native English Reasoning*)

En consonancia con la limitación lingüística identificada para los modelos generalistas (Sección 10.2.9), una línea de investigación para elevar la fiabilidad estructural en dichos modelos es la disociación entre el idioma de interfaz y el idioma de procesamiento lógico. Dado que el razonamiento de los LLMs fundacionales alcanza su máximo rendimiento en inglés, el sistema podría adoptar un patrón de **Traducción Transparente** en el *Edge*.

En esta arquitectura, el usuario interactuaría en español a través del *frontend*, pero un modelo ligero interceptaría y traduciría la entrada al inglés. Toda la carga cognitiva (el *System Prompt*, el ciclo *ReAct*) se ejecutaría de forma nativa en inglés, deshaciendo la traducción a la salida. Si bien los hallazgos con el modelo **Qwen 2.5 Coder (7B)** indican que la especialización del corpus mitiga en gran medida la degradación sintáctica al operar en lenguas secundarias, es prudente asumir que esta protección empírica no es absoluta frente a escenarios de uso desestructurado. Por consiguiente, la implementación de *pipelines* de traducción conserva su validez como **red de seguridad algorítmica complementaria**. Al combinar un modelo especializado con un procesamiento lógico nativo en inglés, el sistema minimizaría significativamente el riesgo de colapsos estructurales derivados de la disonancia lingüística, adecuándose a las exigencias de fiabilidad de los entornos corporativos.

### 10.3.9. Inyección Dinámica de Contexto y Documentación (Context MCP)

Uno de los desafíos inherentes a la generación de infraestructura declarativa mediante LLMs es la rápida obsolescencia de las especificaciones técnicas. Kubernetes evoluciona constantemente, depreciando *apiVersions* (ej. la transición de `v1beta1` a `apps/v1`) y modificando esquemas de recursos. Dado que los modelos fundacionales operan con una fecha de corte de conocimiento (*knowledge cutoff*), corren el riesgo de generar manifiestos YAML formalmente correctos pero operacionalmente obsoletos o incompatibles con la versión exacta del clúster institucional.

Para erradicar definitivamente estas "alucinaciones de sintaxis", una línea de futuro altamente estratégica es la incorporación de **Servidores MCP de Contexto Documental** (como *Context7* o análogos). A diferencia del servidor MCP operativo desarrollado en este TFM (cuya función es ejecutar acciones), un Context MCP actuaría como un puente semántico de solo lectura. Permitiría al agente consultar en tiempo real la documentación oficial actualizada de la versión específica de Kubernetes del clúster, o incluso la Wiki interna del departamento SIC, instantes antes de proceder a la generación del manifiesto. 

Esta arquitectura equivale a implementar un RAG (*Retrieval-Augmented Generation*) dinámico integrado orgánicamente dentro del bucle ReAct. Su adopción garantizaría que el razonamiento del agente esté anclado, de forma determinista, a la realidad documental y operativa más estricta de la organización, blindando al sistema frente a la degradación temporal del conocimiento del LLM.
