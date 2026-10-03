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
  - 7.1. Pruebas de Dominio e Integración: Validando la Jaula Hexagonal
  - 7.2. Property-Based Testing: Asedio Estocástico
  - 7.3. Auditoría de la Suite de Pruebas: *Mutation Testing*
  - 7.4. Pruebas Metamórficas: Inyección de Ruido Léxico y Evaluación del LLM
- **Capítulo 8. Resultados y Casos de Estudio Prácticos**
  - 8.1. Despliegue Convencional vs. Orquestación Agéntica
  - 8.2. Caso de Estudio: Resiliencia ante Ataques (*Prompt Injection*)
  - 8.3. Walkthrough Completo: Del Lenguaje Natural al Manifiesto YAML
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
- **Figura 4:** Diagrama de despliegue a nivel de proceso. Los cuatro componentes coexisten en la misma máquina; el servidor MCP se comunica por `stdio` sin exponer ningún puerto TCP. *(Capítulo 4)*
- **Figura 5:** Diagrama de Clases (UML) resumiendo las principales entidades y contratos del núcleo lógico, destacando el uso del polimorfismo para la inyección de dependencias. *(Capítulo 4)*
- **Figura 6:** Topología de la Arquitectura Hexagonal. El flujo de control penetra desde los Adaptadores Primarios, pero la dependencia de código siempre fluye hacia el centro (Regla de Dependencia de Inversión). *(Capítulo 4)*
- **Figura 7:** Árbol de decisión del `SecurityContextValidator`. Cada rama de rechazo lanza un `SecurityViolationError` que el bucle ReAct captura como Observación para auto-corregirse. *(Capítulo 4)*
- **Figura 8:** Diagrama de Secuencia E2E (Fase 1). Negociación cognitiva entre el Investigador y el LLM hasta alcanzar una intención. *(Capítulo 4)*
- **Figura 9:** Diagrama de Secuencia E2E (Fase 2). El Backend procesa la petición, aplicando reglas de negocio estrictas. *(Capítulo 4)*
- **Figura 10:** Diagrama de Secuencia E2E (Fase 3). Decisión asíncrona del técnico humano, separando la inferencia de la ejecución. *(Capítulo 4)*
- **Figura 11:** Ciclo de vida completo de un mensaje MCP. El protocolo JSON-RPC define tres fases: inicialización, ejecución y observación. *(Capítulo 5)*
- **Figura 12:** Diagrama de flujo del bucle cognitivo ReAct (Reasoning and Acting). *(Capítulo 5)*
- **Figura 13:** Grafo Dirigido Acíclico (DAG) que rige la Máquina de Estados Finita (FSM) del sistema. *(Capítulo 6)*
- **Figura 14:** Diagrama de Secuencia del flujo HITL: polling del Dashboard, vector de aprobación (PENDING → APPROVED → DEPLOYED) y vector de rechazo (PENDING → REJECTED). *(Capítulo 6)*
- **Figura 15:** Arquitectura de la Pirámide Híbrida de Testing implementada en el Agentic Deployer, adaptando el modelo clásico a las exigencias de la Inteligencia Artificial Generativa. *(Capítulo 7)*
- **Figura 16:** Diagrama de Gantt (Parte 1). Planificación orientativa de los Sprints 1 a 4 (núcleo y agente). *(Capítulo 9)*
- **Figura 17:** Diagrama de Gantt (Parte 2). Planificación orientativa del QA avanzado y las fases de cierre/consolidación. *(Capítulo 9)*
- **Anexo A:** Manifiesto YAML completo generado por FakeK8sAdapter — Escenario 1. *(Sección 8.3.1 y Anexo A)*

### Índice de Tablas

- **Tabla 1:** Comparativa de herramientas declarativas vs imperativas. *(Capítulo)*
- **Tabla 2:** Posicionamiento del sistema respecto al estado del arte. *(Capítulo)*
- **Tabla 3:** Vectores de mutación REST del Dashboard de Operaciones. *(Capítulo)*
- **Tabla 4:** Cobertura de pruebas unitarias por componente. *(Capítulo)*
- **Tabla 5:** Resultados del Mutation Testing por módulo. *(Capítulo)*
- **Tabla 6:** Resultados de las Pruebas Metamórficas por Relación. *(Capítulo)*
- **Tabla 7:** Métricas globales de la batería metamórfica. *(Capítulo)*
- **Tabla 8:** Impacto temporal operativo (ITSM tradicional vs Agentic Deployer). *(Capítulo)*
- **Tabla 9:** Traza de ejecución: Análisis de contexto y herramienta (Paso 1). *(Capítulo)*
- **Tabla 10:** Traza de ejecución: Validación en el núcleo hexagonal (Paso 5). *(Capítulo)*
- **Tabla 11:** Métricas de rendimiento del walkthrough completo (Escenario 1). *(Capítulo)*
- **Tabla 12:** Traza de ejecución: Intento de Prompt Injection (Escenario 2). *(Capítulo)*
- **Tabla 13:** Desglose de latencias por componente en el ciclo de vida. *(Capítulo)*
- **Tabla 14:** Comparativa E2E de métricas operativas (ITSM vs Agentic Deployer). *(Capítulo)*
- **Tabla 15:** Módulos de desarrollo y jerarquía de prioridades. *(Capítulo)*
- **Tabla 16:** Estimación de esfuerzo neto por Sprint. *(Capítulo)*
- **Tabla 17:** Resumen de desviaciones de tiempo por fase. *(Capítulo)*
- **Tabla 18:** Costes de Recursos Humanos (CAPEX equivalente). *(Capítulo)*
- **Tabla 19:** Costes de Infraestructura y Herramientas (Fase de Desarrollo). *(Capítulo)*
- **Tabla 20:** Subtotal y costes totales de la fase de desarrollo. *(Capítulo)*
- **Tabla 21:** Perfiles de Organización Adoptante (Casos A, B y C). *(Capítulo)*
- **Tabla 22:** Costes de Implantación (CAPEX - Inversión Inicial). *(Capítulo)*
- **Tabla 23:** Costes Operativos Anuales de Infraestructura (OPEX). *(Capítulo)*
- **Tabla 24:** Costes Operativos Anuales de Motor LLM (Local vs Cloud). *(Capítulo)*
- **Tabla 25:** OPEX Total Anual consolidado por Perfil de Adopción. *(Capítulo)*
- **Tabla 26:** Cálculo del ahorro anual operativo (Escenario de Perfil B). *(Capítulo)*
- **Tabla 27:** Retorno de Inversión (ROI) a 3 años (Perfil B con Ollama). *(Capítulo)*
- **Tabla 28:** Contexto de Generación del Manifiesto YAML (Escenario 1). *(Capítulo)*
- **Tabla 29:** Retrospectiva del Sprint 1 (Núcleo Hexagonal). *(Anexo)*
- **Tabla 30:** Retrospectiva del Sprint 2 (Backend HITL y FSM). *(Anexo)*
- **Tabla 31:** Retrospectiva del Sprint 3 (Golden Paths y FakeK8s). *(Anexo)*
- **Tabla 32:** Retrospectiva del Sprint 4 (Agente ReAct y MCP SDK). *(Anexo)*
- **Tabla 33:** Retrospectiva del Sprint 5 (QA Avanzado). *(Anexo)*
- **Tabla 34:** Retrospectiva de la Fase 6 (Redacción y Cierre). *(Anexo)*
- **Tabla 35:** Retrospectiva de la Fase 7 (Consolidación de Excelencia Técnica). *(Anexo)*
- **Tabla 36:** Glosario completo de Acrónimos y Términos Técnicos. *(Anexo)*
- **Tabla 37:** Datos tabulares adicionales. *(Anexo)*

### Índice de Algoritmos (Pseudocódigo)

- **Algoritmo 1:** Validación Estricta de Entidades de Dominio Hexagonal. *(Sección 4.3.1)*
- **Algoritmo 2:** Introspección Dinámica de Contratos de Herramientas. *(Sección 5.1.1)*
- **Algoritmo 3:** Bucle de Orquestación Cognitiva (ReAct Loop). *(Sección 5.3.1)*
- **Algoritmo 4:** Transición Inmutable de la Máquina de Estados (FSM_Transition). *(Sección 6.2.2)*
- **Algoritmo 5:** Property-Based Test para Invariantes Hexagonales (Fuzzing). *(Sección 7.2.1)*
