# Capítulo 9. Conclusiones y Trabajo Futuro

La convergencia entre la Inteligencia Artificial Generativa y la automatización de la infraestructura operativa (*Platform Engineering*) representa uno de los vectores de innovación más significativos de la década. Este Trabajo de Fin de Máster nació con la ambición de gobernar dicha intersección, transformando el comportamiento impredecible de los Modelos de Lenguaje en una herramienta corporativa determinista. 

A continuación, se exponen las conclusiones extraídas tras la validación empírica del sistema y se traza la hoja de ruta para su evolución futura.

## 9.1. Conclusiones

La conceptualización, desarrollo y sometimiento a pruebas de estrés del *Agentic Deployer* ha demostrado de manera concluyente la viabilidad técnica de delegar la provisión de infraestructura a agentes autónomos, siempre y cuando se encuentren bajo un yugo arquitectónico estricto. Las conclusiones fundamentales derivadas de este trabajo de investigación se articulan en los siguientes puntos:

### 9.1.1. Superación del *Vendor Lock-In* mediante MCP
La decisión arquitectónica de aislar el catálogo de operaciones del Servicio de Informática (SIC) utilizando el **Model Context Protocol (MCP)** [3] se ha revelado como el mayor acierto estratégico del proyecto. Se ha demostrado empíricamente que es posible construir herramientas de automatización complejas sin escribir una sola línea de código acoplada a las APIs nativas de OpenAI, Google o Anthropic. El servidor MCP desarrollado actúa como un activo tecnológico universal; su capacidad para inyectar *JSON Schemas* dinámicamente mediante la introspección de funciones Python asegura que el código universitario heredará compatibilidad nativa con cualquier evolución futura de los Modelos de Lenguaje.

### 9.1.2. La Arquitectura Hexagonal como Jaula Cognitiva
Uno de los mayores hallazgos de este trabajo es la refutación práctica del mito de la "Inteligencia Artificial incontrolable" en entornos de operaciones. La adopción del patrón *Ports and Adapters* (Arquitectura Hexagonal) [2] ha demostrado ser un mecanismo de contención eficaz contra las "alucinaciones" (respuestas inventadas) del LLM. 
Al forzar a la IA a cruzar la frontera de un Dominio inmutable fuertemente tipado (`Pydantic`) y regido por un validador determinista (`SecurityContextValidator`), la estocasticidad queda fuertemente mitigada antes de alcanzar la capa de infraestructura. El sistema no confía en la precisión del LLM; asume que este fallará, intercepta sus errores y los retroalimenta (*Feedback Loop*), creando un ecosistema biológico de corrección automática.

### 9.1.3. La Ineludibilidad del Patrón *Human-In-The-Loop*
En contraste con la corriente de mercado que persigue la autonomía algorítmica total (Nivel 5), este TFM concluye que en infraestructuras críticas institucionales, el humano es un componente crítico y necesario. La implementación de la máquina de estados finita (FSM) y el *Dashboard* asíncrono demostró que la barrera humana (HITL) no erosiona la eficiencia del sistema. El agente LLM descarga al operador del 95% del esfuerzo cognitivo y sintáctico (generación de manifiestos YAML y *Golden Paths*), permitiendo al técnico humano ejercer un 100% de soberanía legal y técnica sobre el despliegue físico con un solo clic.

### 9.1.4. Redefinición del Aseguramiento de Calidad (QA) y Falsos Positivos de Cobertura
Las metodologías de *testing* convencionales son insuficientes para sistemas estocásticos. El TFM ha validado que auditar IAs generativas requiere paradigmas avanzados. La integración de *Property-Based Testing* (Hypothesis) [6] y **Pruebas Metamórficas** [12] ha demostrado que el agente extrae entidades matemáticas correctas a partir de texto con alto ruido sintáctico. De igual trascendencia ha sido el descubrimiento empírico derivado de auditar el sistema mediante *Mutation Testing* (Mutmut): se ha evidenciado que una Cobertura de Código del 100% no garantiza la resiliencia lógica. La capacidad de la mutación algorítmica para detectar y forzar la mitigación de 12 brechas de red y validación, que las métricas clásicas pasaron por alto, certifica en última instancia que la resiliencia del sistema se ha elevado a estándares propios de un entorno de producción.

En síntesis, este Trabajo de Fin de Máster aporta una arquitectura de referencia replicable, demostrando que la Inteligencia Artificial no viene a reemplazar al ingeniero de infraestructuras, sino a abstraer la aridez del código declarativo bajo una capa de razonamiento lingüístico natural.

## 9.2. Trabajo Futuro

El prototipo actual (MVP) certifica matemáticamente la viabilidad de la integración agéntica en sistemas deterministas. Sin embargo, su consolidación operativa en un entorno productivo de gran escala requiere abordar una serie de mejoras iterativas. Las futuras líneas de desarrollo se desglosan en tres horizontes temporales estratégicos.

### 9.2.1. Horizonte a Corto Plazo: Integración Física (K8s API)

El diseño Hexagonal permite la sustitución de la capa de persistencia actual (`FakeK8sAdapter`) sin impactar la lógica de negocio subyacente. El primer hito evolutivo consiste en desarrollar e inyectar un **`RealK8sAdapter`**. 
Este adaptador hará uso de la librería oficial de Kubernetes para Python (`kubernetes-client`). En lugar de volcar manifiestos YAML estáticos en el disco físico del servidor, el adaptador consumirá directamente el *Control Plane* de un clúster físico experimental (como Minikube, K3s o un entorno *sandbox* universitario), permitiendo que la aprobación del técnico (HITL) despierte los *pods* de forma inmediata.

### 9.2.2. Horizonte a Medio Plazo: Adopción de la Filosofía GitOps

Una de las premisas fundamentales del movimiento *Platform Engineering* es la trazabilidad declarativa mediante sistemas de control de versiones. Actualmente, el flujo de ejecución sigue un modelo *Push* (el adaptador intenta empujar los recursos al clúster). 

Para alinear el sistema con los más altos estándares corporativos, se propone evolucionar hacia un modelo **GitOps (Pull-based)**:
- El adaptador secundario no atacará a Kubernetes, sino que realizará un *commit* de los YAML autogenerados hacia un repositorio Git (ej. GitLab o GitHub) dedicado exclusivamente a la topología del clúster.
- Herramientas de reconciliación consolidadas en el mercado, como **ArgoCD** o **Flux**, monitorizarán dicho repositorio. Al detectar un nuevo *commit* aprobado por el sistema HITL, ArgoCD se encargará de traccionar (*pull*) los manifiestos y aplicarlos en el clúster.
Esta separación entre el agente que redacta/audita y el orquestador físico que despliega garantizará un *Disaster Recovery* altamente fiable, ya que el estado real del centro de datos siempre residirá en un repositorio Git versionado.

### 9.2.3. Horizonte a Largo Plazo: Policy-as-Code (OPA y Kyverno)

El núcleo de seguridad actual recae en el `SecurityContextValidator`, cuyas reglas están codificadas imperativamente en lenguaje Python. Aunque robusto frente al LLM, la actualización de las políticas (por ejemplo, prohibir de repente el puerto 80) requiere el redespliegue de todo el backend de FastAPI.

Para mitigar esta rigidez, el sistema migrará su lógica de validación hacia motores estandarizados de *Policy-as-Code* (Políticas como Código), integrando el orquestador agéntico con **Open Policy Agent (OPA)** o **Kyverno**. 
Bajo este paradigma, el equipo de ciberseguridad del Servicio de Informática definirá reglas de validación en lenguaje *Rego* u objetos declarativos de K8s. El Backend, en el momento de la evaluación HITL, interrogará a la API de OPA para decidir si el despliegue es lícito. De este modo, la Inteligencia Artificial del TFM lograría integrarse fluidamente y sin fricciones en los flujos de auditoría cibernética más exigentes de la industria del *Cloud Computing*.
