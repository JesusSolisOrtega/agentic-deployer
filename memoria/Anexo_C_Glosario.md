# Anexo C. Glosario de Acrónimos y Términos

Para facilitar la lectura y comprensión técnica de este documento, a continuación se detallan los acrónimos y términos anglosajones de uso más frecuente a lo largo de los capítulos, especialmente aquellos relativos a la Ingeniería de Plataformas, la Inteligencia Artificial Generativa y la infraestructura en la nube.

| Acrónimo | Significado Original | Definición en el contexto del TFM |
|----------|----------------------|-----------------------------------|
| **A2A** | Agent-to-Agent Protocol | Protocolo emergente (impulsado por Google) diseñado para la comunicación estandarizada entre múltiples agentes de IA autónomos. |
| **API** | Application Programming Interface | Interfaz que permite a dos aplicaciones de software comunicarse entre sí. En este TFM, refiere principalmente a la API de Kubernetes y la del LLM. |
| **C4** | Context, Containers, Components, Code | Modelo de diagramación estandarizada creado por Simon Brown para visualizar la arquitectura de sistemas de software en 4 niveles de zoom. |
| **CAPEX** | Capital Expenditure | Gasto de capital. En tecnología, se refiere a la inversión inicial requerida para adquirir activos físicos (servidores, licencias perpetuas). |
| **CI/CD** | Continuous Integration / Continuous Deployment | Prácticas DevOps que automatizan la integración del código de múltiples desarrolladores y su despliegue hacia entornos productivos. |
| **DAG** | Directed Acyclic Graph | Grafo Dirigido Acíclico. Estructura matemática que rige la máquina de estados, donde las transiciones fluyen en una dirección sin crear bucles cerrados. |
| **DSL** | Domain-Specific Language | Lenguaje de Dominio Específico. Un lenguaje informático especializado en un problema de dominio particular (ej. PromQL para Prometheus o HCL para Terraform). |
| **FSM** | Finite-State Machine | Máquina de Estados Finita. Modelo de computación matemática que asegura que la solicitud de despliegue solo puede estar en un estado (ej. PENDING) a la vez. |
| **HITL** | Human-In-The-Loop | Patrón arquitectónico donde un operador humano es insertado intencionalmente en un flujo de control automatizado para auditar y autorizar operaciones críticas. |
| **IaC** | Infrastructure as Code | Infraestructura como Código. El proceso de gestionar y aprovisionar centros de datos informáticos mediante archivos de definición legibles por máquina (ej. YAML). |
| **IDP** | Internal Developer Portal/Platform | Portal Interno para Desarrolladores. Plataforma de autoservicio que abstrae la complejidad de la infraestructura para los programadores de una organización. |
| **ITIL** | Information Technology Infrastructure Library | Conjunto de prácticas estandarizadas a nivel mundial para la Gestión de Servicios de Tecnologías de la Información (ITSM). |
| **ITSM** | Information Technology Service Management | Gestión de Servicios de TI. Procesos y políticas implementados por el departamento SIC para diseñar, planificar y operar servicios tecnológicos. |
| **LLM** | Large Language Model | Modelo de Lenguaje de Gran Escala. Red neuronal entrenada con cantidades masivas de texto (ej. GPT-4, Llama 3), capaz de entender y generar lenguaje natural. |
| **MCP** | Model Context Protocol | Estándar de código abierto introducido por Anthropic para estandarizar la forma en que los agentes de IA se comunican con fuentes de datos y herramientas externas. |
| **MVP** | Minimum Viable Product | Producto Mínimo Viable. Versión inicial de un producto con las funcionalidades estrictamente necesarias para satisfacer a los primeros adoptantes y validar la hipótesis. |
| **OPEX** | Operational Expenditure | Gasto operativo. Costes recurrentes del día a día (suscripciones en la nube, consumo eléctrico, horas de personal). |
| **QA** | Quality Assurance | Aseguramiento de Calidad. Conjunto de actividades (unit testing, property-based, mutation) orientadas a garantizar que el software cumple sus especificaciones. |
| **RBAC** | Role-Based Access Control | Control de Acceso Basado en Roles. Método que restringe el acceso a la red y a los recursos en base a las responsabilidades de los usuarios dentro de la organización. |
| **ReAct** | Reason and Act | Paradigma de *prompting* iterativo donde el LLM alterna fases de razonamiento deductivo interno con la invocación explícita de acciones contra el entorno exterior. |
| **ROI** | Return on Investment | Retorno de Inversión. Métrica financiera que compara el beneficio obtenido en relación a la inversión realizada (ej. tiempo ahorrado vs. coste de desarrollo). |
| **SIC** | Servicio de Informática y Comunicaciones | Departamento institucional (típicamente universitario o gubernamental) encargado de administrar la infraestructura tecnológica y soporte a usuarios. |
| **TTM** | Time To Market / Time To Mitigation | Tiempo desde la concepción de una necesidad (ej. necesito una web) hasta que el servicio está operativo y disponible. |
<p align="center"><i><b>Tabla 40:</b> Glosario de Acrónimos y Términos Técnicos.</i></p>

---

## Términos Técnicos Anglosajones

Los siguientes términos en inglés se emplean en el texto en su forma original por carecer de traducción establecida y de uso generalizado en el sector. Se documentan aquí para facilitar la comprensión de lectores con menor familiaridad con la terminología técnica internacional.

| Término | Traducción aproximada | Uso en el TFM |
|---|---|---|
| **Air-Gapped** | «Red aislada» o «entorno desconectado» | Se refiere a infraestructuras de red totalmente aisladas de Internet (sin ninguna conexión externa), empleadas en entornos de alta seguridad (administración pública, defensa). En el TFM es relevante para los escenarios de despliegue on-premise con Ollama sin conectividad exterior. |
| **Boilerplate** | «Código repetitivo» o «código de plantilla» | Fragmentos de código estandarizados y repetitivos que deben incluirse en múltiples lugares con pocas o ninguna alteración (ej. configuraciones base de FastAPI, imports estándar). Se distingue del código de lógica de negocio por su naturaleza formulaica. |
| **Garbage Collector** | «Recolector de basura» | Componente del entorno de ejecución (ej. CPython) responsable de liberar automáticamente la memoria ocupada por objetos que ya no son accesibles por ninguna parte del programa. En el TFM se menciona en el contexto de los nodos de sumidero de la FSM (registros `REJECTED` que el GC ignora). |
| **Overhead** | «Sobrecarga» o «coste adicional» | Recursos computacionales (tiempo de CPU, memoria, latencia de red) consumidos por la infraestructura de soporte de un sistema, más allá del trabajo útil que este realiza. En el TFM se usa principalmente para referirse a la sobrecarga del protocolo TCP/IP vs. `stdio`. |
| **Scaffolding** | «Andamiaje» o «generación de estructura inicial» | Proceso de generación automática de la estructura de código base de un proyecto (directorios, ficheros de configuración, módulos de entrada) a partir de plantillas o herramientas CLI. En el TFM se usa en el contexto de la asistencia de la IA generativa para acelerar la fase inicial de cada sprint. |
<p align="center"><i><b>Tabla 41:</b> Términos técnicos anglosajones empleados en la memoria.</i></p>

