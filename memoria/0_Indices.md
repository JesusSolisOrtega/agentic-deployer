# Índice de Contenidos

- **Capítulo 1. Introducción**
  - 1.1. Contexto y motivación
  - 1.2. Planteamiento del problema
  - 1.3. Objetivos del proyecto
  - 1.4. Alcance y Limitaciones
  - 1.5. Requisitos Formales del Sistema
  - 1.6. Estructura de la memoria
- **Capítulo 2. Estado del Arte**
  - 2.1. Agentes autónomos basados en Modelos de Lenguaje de Gran Escala (LLM)
  - 2.2. Estandarización de Integraciones: Model Context Protocol (MCP)
  - 2.3. Orquestación e Infraestructura Declarativa (Kubernetes)
  - 2.4. Arquitectura Hexagonal y Seguridad en Sistemas Estocásticos
  - 2.5. Trabajos Relacionados y Posicionamiento Diferencial
- **Capítulo 3. Metodología y Stack Tecnológico**
  - 3.1. Enfoque Metodológico
  - 3.2. Fases de Desarrollo
  - 3.3. Stack Tecnológico y Justificación Arquitectónica
- **Capítulo 4. Diseño del Sistema y Arquitectura**
  - 4.1. Modelado Topológico Arquitectónico (Estándar C4)
  - 4.2. Adopción de la Arquitectura Hexagonal (Ports and Adapters)
  - 4.3. Algoritmia de Validación de Seguridad Institucional
  - 4.4. Patrón de Abstracción: *Golden Paths* y Expansión Sintáctica
  - 4.5. Flujo de Datos *End-to-End* y Ciclo de Estados
- **Capítulo 5. Desarrollo del Agente Cognitivo y MCP**
  - 5.1. Implementación del Servidor *Model Context Protocol* (MCP)
  - 5.2. Diseño de la Abstracción Multiproveedor y Soberanía del Dato
  - 5.3. Bucle Cognitivo y Resiliencia Estocástica (Patrón ReAct)
- **Capítulo 6. Implementación del Patrón HITL y Gestión de Estados Finita (FSM)**
  - 6.1. Fundamentación del Patrón *Human-In-The-Loop* (HITL)
  - 6.2. Diseño de la Máquina de Estados Finita (FSM)
  - 6.3. El Dashboard Asíncrono de Operaciones
  - 6.4. Canal de Retorno al Investigador: Notificación Asíncrona del Estado
- **Capítulo 7. Aseguramiento de Calidad (QA) y Testing Avanzado**
  - 7.1. Pruebas de Dominio e Integración: Validando el Perímetro Hexagonal
  - 7.2. Property-Based Testing: Pruebas frente a Comportamiento Estocástico
  - 7.3. Auditoría de la Suite de Pruebas: *Mutation Testing*
  - 7.4. Pruebas Metamórficas: Inyección de Ruido Léxico y Evaluación del LLM
- **Capítulo 8. Resultados y Casos de Estudio Prácticos**
  - 8.1. Despliegue Convencional vs. Orquestación Agéntica
  - 8.2. Caso de Estudio: Resiliencia ante Ataques (*Prompt Injection*)
  - 8.3. Walkthrough Completo: Del Lenguaje Natural al Manifiesto YAML
  - 8.4. Experimentos Arquitectónicos: Superando el Límite Cognitivo (7B)
- **Capítulo 9. Gestión y Viabilidad del Proyecto**
  - 9.1. Plan de Proyecto — Contexto y Restricciones
  - 9.2. Estructura de Sprints y Estimación de Esfuerzo
  - 9.3. Esfuerzo de Desarrollo y Desviaciones
  - 9.4. Análisis Económico del Desarrollo
  - 9.5. Coste de Adopción Corporativa y ROI
  - 9.6. Conclusiones del Análisis de Viabilidad
- **Capítulo 10. Conclusiones, Limitaciones y Trabajo Futuro**
  - 10.1. Conclusiones
  - 10.2. Limitaciones del Prototipo
  - 10.3. Trabajo Futuro
- **Capítulo 11. Bibliografía y Referencias**
- **Anexo A. Manifiesto Kubernetes Generado — Escenario 1 (Happy Path)**
  - A.1. Contexto de Generación
  - A.2. Manifiesto YAML Completo
  - A.3. Relación con el Código Fuente
- **Anexo B. Retrospectivas Detalladas por Sprint**
  - B.1. Sprint 1 — Núcleo Hexagonal
  - B.2. Sprint 2 — Backend HITL y FSM
  - B.3. Sprint 3 — Golden Paths y FakeK8s
  - B.4. Sprint 4 — Agente ReAct y MCP SDK
  - B.5. Sprint 5 — QA Avanzado
  - B.6. Fase 6 — Redacción y Cierre
  - B.7. Fase 7 — Consolidación de Excelencia Técnica
- **Anexo C. Glosario de Acrónimos y Términos**


<div style='page-break-after: always;'></div>

# Índice de Figuras y Algoritmos

El presente Trabajo de Fin de Máster hace uso intensivo de modelado visual y pseudocódigo para formalizar las decisiones arquitectónicas. A continuación se listan las figuras y algoritmos referenciados a lo largo de la memoria:

### Índice de Figuras

- **Figura 1:** Contraste arquitectónico entre el problema de integración N×M (acoplamiento propietario) y la topología de Bus Universal propuesta por el protocolo MCP. *(Capítulo 2)*
- **Figura 2:** Diagrama de componentes del Stack Tecnológico empleado, evidenciando la segregación entre las capas de interfaz, razonamiento cognitivo, backend restrictivo y las herramientas de validación de calidad continua. *(Capítulo 3)*
- **Figura 3:** Diagrama de Contenedores (Nivel 2) del Modelo C4 para el sistema Agentic Deployer. *(Capítulo 4)*
- **Figura 4:** Diagrama de despliegue a nivel de proceso. Los cuatro componentes coexisten en la misma máquina; el servidor MCP se comunica por <code>stdio</code> sin exponer ningún puerto TCP. *(Capítulo 4)*
- **Figura 5:** Diagrama de Clases (UML) resumiendo las principales entidades y contratos del núcleo lógico, destacando el uso del polimorfismo para la inyección de dependencias (LLMClient, DeployPort). *(Capítulo 4)*
- **Figura 6:** Topología de la Arquitectura Hexagonal. El flujo de control penetra desde los Adaptadores Primarios, pero la dependencia de código siempre fluye hacia el centro (Regla de Dependencia de Inversión). *(Capítulo 4)*
- **Figura 7:** Visión general simplificada del <code>SecurityContextValidator</code>. Una rama de rechazo lanza el error para que ReAct se auto-corrija. *(Capítulo 4)*
- **Figura 8:** Diagrama de Secuencia E2E (Etapa 1). Negociación cognitiva entre el Investigador y el LLM hasta alcanzar una intención. *(Capítulo 4)*
- **Figura 9:** Diagrama de Secuencia E2E (Etapa 2). (Arriba) Camino feliz. (Abajo) Camino de error y autocorrección. *(Capítulo 4)*
- **Figura 10:** Diagrama de Secuencia E2E (Etapa 3). Decisión asíncrona del técnico humano, separando la inferencia de la ejecución. *(Capítulo 4)*
- **Figura 11:** Ciclo de vida completo de un mensaje MCP. El protocolo JSON-RPC define tres fases: inicialización (handshake y descubrimiento de herramientas), ejecución (invocación y respuesta) y observación (retroalimentación al LLM). *(Capítulo 5)*
- **Figura 12:** Diagrama de flujo del bucle cognitivo ReAct (Reasoning and Acting). *(Capítulo 5)*
- **Figura 13:** Grafo Dirigido Acíclico (DAG) que rige la Máquina de Estados Finita (FSM) del sistema. *(Capítulo 6)*
- **Figura 14:** Diagrama de Secuencia del flujo HITL. (Arriba) Polling asíncrono y Vector de Aprobación. (Abajo) Vector de Rechazo (estado inmutable terminal). *(Capítulo 6)*
- **Figura 15:** Arquitectura de la Pirámide Híbrida de Testing implementada en el Agentic Deployer, adaptando el modelo clásico a las exigencias de la Inteligencia Artificial Generativa. *(Capítulo 7)*
- **Figura 16:** Diagrama de Gantt (Parte 1). Planificación orientativa de los Sprints 1 a 4 (núcleo y agente). *(Capítulo 9)*
- **Figura 17:** Diagrama de Gantt (Parte 2). Planificación orientativa del QA avanzado y las fases de cierre/consolidación. *(Capítulo 9)*

### Índice de Tablas

- **Tabla 1:** Comparativa entre Asistentes Cloud Propietarios y el Agentic Deployer. *(Capítulo 2)*
- **Tabla 2:** Posicionamiento del sistema respecto al estado del arte. *(Capítulo 2)*
- **Tabla 3:** Mapeo de estados FSM a indicadores visuales del panel de notificaciones del investigador. *(Capítulo 6)*
- **Tabla 4:** Casos de prueba de la capa de consulta de estado del investigador. *(Capítulo 7)*
- **Tabla 5:** Resultados del Mutation Testing por módulo. *(Capítulo 7)*
- **Tabla 6:** Resultados empíricos de las Pruebas Metamórficas por Relación frente a Qwen 2.5 (7B). *(Capítulo 7)*
- **Tabla 7:** Métricas globales de la batería metamórfica. *(Capítulo 7)*
- **Tabla 8:** Resultados comparativos del stress-test metamórfico (Zero-Shot puro). *(Capítulo 7)*
- **Tabla 9:** Impacto temporal operativo (ITSM tradicional vs Agentic Deployer). *(Capítulo 8)*
- **Tabla 10:** Entorno de evaluación para los casos de estudio prácticos. *(Capítulo 8)*
- **Tabla 11:** Traza de ejecución: Validación en el núcleo hexagonal (Paso 5). *(Capítulo 8)*
- **Tabla 12:** Métricas de rendimiento del walkthrough completo (Escenario 1). *(Capítulo 8)*
- **Tabla 13:** Traza de ejecución: Intento de Prompt Injection (Escenario 2). *(Capítulo 8)*
- **Tabla 14:** Desglose de latencias por componente en el ciclo de vida. *(Capítulo 8)*
- **Tabla 15:** Comparativa E2E de métricas operativas (multi-escenario). *(Capítulo 8)*
- **Tabla 16:** Rendimiento comparativo real de modelos alternativos en el bucle ReAct. *(Capítulo 8)*
- **Tabla 17:** Resultados de los Experimentos de Arquitectura Cognitiva ampliado con modelos Cloud. *(Capítulo 8)*
- **Tabla 18:** Módulos de desarrollo y jerarquía de prioridades. *(Capítulo 9)*
- **Tabla 19:** Estimación de esfuerzo neto por Sprint. *(Capítulo 9)*
- **Tabla 20:** Resumen de desviaciones de tiempo por fase. *(Capítulo 9)*
- **Tabla 21:** Costes de Recursos Humanos (CAPEX equivalente). *(Capítulo 9)*
- **Tabla 22:** Costes de Infraestructura y Herramientas (Fase de Desarrollo). *(Capítulo 9)*
- **Tabla 23:** Subtotal y costes totales de la fase de desarrollo. *(Capítulo 9)*
- **Tabla 24:** Perfiles de Organización Adoptante (Casos A, B y C). *(Capítulo 9)*
- **Tabla 25:** Costes de Implantación (CAPEX - Inversión Inicial). *(Capítulo 9)*
- **Tabla 26:** Costes Operativos Anuales de Infraestructura (OPEX). *(Capítulo 9)*
- **Tabla 27:** Costes Operativos Anuales de Motor LLM (Local vs Cloud) según niveles de adopción. *(Capítulo 9)*
- **Tabla 28:** Estimación de Costes de Motor LLM (API en la Nube). *(Capítulo 9)*
- **Tabla 29:** OPEX Total Anual consolidado por Perfil de Adopción. *(Capítulo 9)*
- **Tabla 30:** Cálculo del ahorro anual operativo (Escenario de Perfil B). *(Capítulo 9)*
- **Tabla 31:** Retorno de Inversión (ROI) a 3 años (Perfil B con Ollama). *(Capítulo 9)*
- **Tabla 32:** Contexto de Generación del Manifiesto YAML (Escenario 1). *(Anexo A)*
- **Tabla 33:** Retrospectiva del Sprint 1 (Núcleo Hexagonal). *(Anexo B)*
- **Tabla 34:** Retrospectiva del Sprint 2 (Backend HITL y FSM). *(Anexo B)*
- **Tabla 35:** Retrospectiva del Sprint 3 (Golden Paths y FakeK8s). *(Anexo B)*
- **Tabla 36:** Retrospectiva del Sprint 4 (Agente ReAct y MCP SDK). *(Anexo B)*
- **Tabla 37:** Retrospectiva del Sprint 5 (QA Avanzado). *(Anexo B)*
- **Tabla 38:** Retrospectiva de la Fase 6 (Redacción y Cierre). *(Anexo B)*
- **Tabla 39:** Retrospectiva de la Fase 7 (Consolidación de Excelencia Técnica). *(Anexo B)*
- **Tabla 40:** Glosario de Acrónimos y Términos Técnicos. *(Anexo C)*

### Índice de Algoritmos (Pseudocódigo)

- **Algoritmo 1:** Validación Estricta de Entidades de Dominio Hexagonal (SecurityContextValidator). *(Capítulo 4)*
- **Algoritmo 2:** Introspección Dinámica de Contratos de Herramientas. *(Capítulo 5)*
- **Algoritmo 3:** Bucle de Orquestación Cognitiva (ReAct Loop). *(Capítulo 5)*
- **Algoritmo 4:** Transición Inmutable de la Máquina de Estados (FSM_Transition). *(Capítulo 6)*
- **Algoritmo 5:** Property-Based Test para Invariantes Hexagonales (Fuzzing). *(Capítulo 7)*

