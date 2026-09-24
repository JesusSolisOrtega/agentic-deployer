# Capítulo 8. Resultados y Demostración

Este capítulo consolida los resultados técnicos del proyecto, demostrando mediante escenarios prácticos y documentados (End-to-End) la viabilidad de delegar el aprovisionamiento de infraestructura universitaria a un orquestador agéntico supervisado.

## 8.1. Escenarios End-to-End (Golden Paths)

Para evaluar el sistema, se diseñaron tres escenarios operativos representativos de las peticiones habituales recibidas por un Servicio de Informática y Comunicaciones (SIC) universitario. 

### Escenario 1: Provisión de Infraestructura Estática (Congreso)
Un perfil de investigación solicita el alta para la web de un congreso. 

- **Petición en Lenguaje Natural:** *"Hola, necesito desplegar la web estática para el congreso de IA de 2025. El nombre del proyecto es congreso-ia-2025 y esperamos bastante tráfico (alto)."*
- **Acción del Agente (MCP Tool Call):** El modelo intercepta la petición, localiza la herramienta pertinente y ejecuta un POST estructurado con el nombre del congreso y la previsión de tráfico pre-validada.
- **Respuesta Conversacional:** *"✅ Solicitud enviada a revisión. He configurado el servidor web para el congreso con recursos ampliados (1 CPU, 512Mi RAM) para soportar el tráfico alto esperado."*

El técnico recibe la petición en el panel HITL y, tras aprobarla, el adaptador de Kubernetes genera de forma automática un *Deployment* con la imagen `nginx:alpine`, un *Service* asociado al puerto 8080 y un *Ingress* exponiendo la URL `.apps.universidad.edu`, sin intervención declarativa por parte del usuario final.

### Escenario 2: Gestor de Contenidos Institucional
Un departamento solicita un CMS (WordPress) para el claustro docente.

- **Petición en Lenguaje Natural:** *"Queremos un WordPress para el departamento de informatica."*
- **Reacción del Sistema:** El agente omite preguntar por cuotas de CPU o puertos y asume, mediante la herramienta MCP `deploy_department_cms`, que todo CMS departamental obedece a un *Golden Path* estricto de 500m de CPU y 1024Mi de memoria, utilizando la imagen oficial de WordPress asegurada por la organización. El YAML generado es automáticamente alineado a estos estándares.

### Escenario 3: API Python Personalizada
Un grupo de estudiantes desarrolla un backend y requiere alojamiento en el clúster.

- **Petición en Lenguaje Natural:** *"Necesito subir una API llamada api-notas. Está hecha en Python 3.12."*
- **Reacción del Sistema:** El modelo mapea la petición a la herramienta genérica `deploy_python_app`. El agente traduce correctamente "Python 3.12" al tag interno `python:3.12-slim` y enruta el tráfico interno automáticamente al puerto 8000, estándar predefinido para microservicios.

*(NOTA PARA LA VERSIÓN FINAL: Insertar aquí CAPTURAS DE PANTALLA del chat de Streamlit procesando estas tres peticiones)*

## 8.2. Validación del Bucle de Autocorrección (Feedback Loop)

Más allá de los escenarios "felices", se demostró el valor del agente en la mitigación de errores del usuario. En las pruebas de campo, se forzó al agente solicitándole el despliegue de una imagen en el puerto prohibido 80.

Al intentar invocar la herramienta, el *SecurityContextValidator* de la capa Hexagonal rechazó la petición devolviendo un `SecurityViolationError` debido a la vulneración de puertos privilegiados (<1024). Lejos de mostrar un error crítico al usuario, el orquestador (*AgentOrchestrator*) volcó el error como una observación dentro del bucle ReAct. El agente LLM interpretó el rechazo de la infraestructura, generó un mensaje de disculpa, explicó al investigador la normativa del SIC y le solicitó amablemente un puerto alternativo (por ejemplo, el 8080). 

Esta resiliencia demuestra el abismo entre la simple invocación programática de APIs y la verdadera automatización agéntica inteligente.

## 8.3. Supervisión HITL e Interoperabilidad

Las operaciones fueron exitosamente monitoreadas desde el panel *Dashboard HITL*. Se constató que ninguna orden emitida por el agente surtió efecto en el clúster sin la confirmación asíncrona del técnico operador.

*(NOTA PARA LA VERSIÓN FINAL: Insertar aquí CAPTURAS DE PANTALLA del panel en modo oscuro mostrando las intenciones en rojo y verde)*

Finalmente, se validó la adherencia al estándar Model Context Protocol (MCP) integrando el servidor local directamente con *Claude Desktop* (Anthropic). El cliente externo fue capaz de leer el catálogo de herramientas del SIC universitario de la misma forma que lo hace el cliente web Streamlit nativo del proyecto. Esto confirma el absoluto desacoplamiento logrado en la arquitectura y posiciona al SIC para integrarse con futuras soluciones empresariales habilitadas por IA sin necesidad de re-escribir su infraestructura.

*(NOTA PARA LA VERSIÓN FINAL: Insertar aquí CAPTURA DE PANTALLA de Claude Desktop mostrando el icono del enchufe conectando a tu servidor local)*
