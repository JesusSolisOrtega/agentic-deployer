# Lista de Acrónimos y Términos

Para facilitar la lectura y comprensión técnica de este documento, a continuación se detallan los acrónimos y términos anglosajones de uso más frecuente a lo largo de los capítulos, especialmente aquellos relativos a la Ingeniería de Plataformas, la Inteligencia Artificial Generativa y la infraestructura en la nube.

| Acrónimo | Significado Original | Definición en el contexto del TFM |
|---|---|---|
| **A2A** | Agent-to-Agent Protocol | Protocolo emergente diseñado para la comunicación estandarizada entre múltiples agentes de IA autónomos. |
| **API** | Application Programming Interface | Interfaz que permite a dos aplicaciones de software comunicarse entre sí. En este TFM, refiere principalmente a la API de Kubernetes y la del LLM. |
| **C4** | Context, Containers, Components, Code | Modelo de diagramación estandarizada creado por Simon Brown para visualizar la arquitectura de sistemas de software en 4 niveles de abstracción. |
| **CAPEX** | Capital Expenditure | Gasto de capital. Inversión inicial requerida para adquirir o desarrollar activos fijos o software propio. |
| **CI/CD** | Continuous Integration / Continuous Deployment | Prácticas DevOps que automatizan la integración del código y su entrega o despliegue hacia entornos productivos. |
| **DAG** | Directed Acyclic Graph | Grafo Dirigido Acíclico. Estructura matemática que rige la máquina de estados, donde las transiciones fluyen en una dirección sin ciclos cerrados. |
| **DSL** | Domain-Specific Language | Lenguaje de Dominio Específico. Lenguaje informático especializado en un problema de dominio particular (ej. PromQL o HCL). |
| **FSM** | Finite-State Machine | Máquina de Estados Finita. Modelo de computación que asegura que la solicitud de despliegue solo puede encontrarse en un estado determinista a la vez. |
| **HITL** | Human-In-The-Loop | Patrón arquitectónico donde un operador humano es insertado intencionalmente en un flujo de control automatizado para auditar y autorizar operaciones críticas. |
| **IaC** | Infrastructure as Code | Infraestructura como Código. Proceso de gestionar y aprovisionar recursos computacionales mediante archivos de definición legibles por máquina (ej. YAML). |
| **IDP** | Internal Developer Portal/Platform | Portal Interno para Desarrolladores. Plataforma de autoservicio que abstrae la complejidad de la infraestructura para los programadores de una organización. |
| **ITIL** | Information Technology Infrastructure Library | Conjunto de prácticas estandarizadas a nivel mundial para la Gestión de Servicios de Tecnologías de la Información (ITSM). |
| **ITSM** | Information Technology Service Management | Gestión de Servicios de TI. Procesos y políticas implementados por el departamento de sistemas para diseñar, planificar y operar servicios tecnológicos. |
| **LLM** | Large Language Model | Modelo de Lenguaje de Gran Escala. Red neuronal basada en la arquitectura Transformer capaz de interpretar y generar lenguaje natural estructurado. |
| **MCP** | Model Context Protocol | Estándar de código abierto introducido por Anthropic para estandarizar la forma en que los agentes de IA se comunican con fuentes de datos y herramientas externas. |
| **MR** | Metamorphic Relation | Relación Metamórfica. Propiedad formal de invarianza que describe cómo debe comportarse la salida de un sistema ante transformaciones controladas de la entrada, mitigando el problema del oráculo. |
| **MVP** | Minimum Viable Product | Producto Mínimo Viable. Versión inicial de un desarrollo con las funcionalidades estrictamente necesarias para satisfacer los requerimientos base y validar la propuesta técnica. |
| **OPEX** | Operational Expenditure | Gasto operativo. Costes recurrentes del funcionamiento diario (suscripciones en la nube, consumo eléctrico, horas de mantenimiento). |
| **PBT** | Property-Based Testing | Pruebas Basadas en Propiedades. Técnica de aseguramiento de calidad donde se generan automáticamente casos de prueba aleatorios para verificar invariantes lógicas universales. |
| **QA** | Quality Assurance | Aseguramiento de Calidad. Conjunto de actividades (pruebas unitarias, de propiedades, mutación y carga) orientadas a garantizar que el software cumple sus especificaciones. |
| **RBAC** | Role-Based Access Control | Control de Acceso Basado en Roles. Mecanismo que restringe el acceso a recursos computacionales en función de los roles asignados a los usuarios. |
| **ReAct** | Reason and Act | Paradigma de inferencia iterativo donde el LLM alterna fases de razonamiento deductivo interno (*Thought*) con la invocación explícita de acciones contra el entorno exterior (*Action*). |
| **ROI** | Return on Investment | Retorno de Inversión. Razón financiera que compara el beneficio neto obtenido respecto a la inversión realizada (tiempo ahorrado frente a coste de desarrollo e implantación). |
| **SIC** | Servicio de Informática y Comunicaciones | Departamento institucional encargado de administrar la infraestructura tecnológica, redes y soporte técnico universitario. |
| **TTM** | Time To Market / Time To Mitigation | Tiempo transcurrido desde la formulación de una necesidad técnica hasta que el servicio correspondiente se encuentra plenamente operativo en el entorno. |

---

## Términos Técnicos Anglosajones

Los siguientes términos en inglés se emplean en el texto en su forma original por carecer de traducción asentada o de uso generalizado en la literatura de ingeniería informática. Se documentan aquí para asegurar la precisión terminológica:

| Término | Traducción aproximada | Uso en el TFM |
|---|---|---|
| **Air-Gapped** | «Red aislada» o «entorno desconectado» | Refiere a infraestructuras de red desprovistas de conexiones físicas o lógicas hacia redes públicas externas (Internet), habituales en entornos de alta seguridad. En el TFM aplica a despliegues locales con Ollama. |
| **Boilerplate** | «Código repetitivo» o «plantilla estándar» | Fragmentos de código estándar y formulaicos que deben incluirse en múltiples puntos del proyecto con pocas variaciones estructurales (ej. inicialización de FastAPI o esquemas base). |
| **Garbage Collector** | «Recolector de basura» | Componente del entorno de ejecución responsable de liberar automáticamente memoria ocupada por objetos inalcanzables. En el TFM se menciona en relación con el sumidero de estados terminales de la FSM. |
| **Overhead** | «Sobrecarga» o «coste computacional adicional» | Recursos computacionales suplementarios (tiempo de CPU, memoria, latencia de red) consumidos por la infraestructura de mediación más allá del procesamiento de negocio estricto. |
| **Scaffolding** | «Generación de estructura base» | Proceso de creación automática del esqueleto de código de un módulo o proyecto a partir de patrones predefinidos para agilizar las fases iniciales de desarrollo. |

