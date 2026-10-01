# Índice de Contenidos

- **Capítulo 1. Introducción**
  - 1.1. Contexto y motivación
  - 1.2. Planteamiento del problema
  - 1.3. Objetivos del proyecto
  - 1.4. Alcance y Limitaciones
  - 1.5. Estructura de la memoria
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
  - 9.1. Esfuerzo de Desarrollo y Desviaciones
  - 9.2. Análisis Económico del Desarrollo
  - 9.3. Coste de Adopción Corporativa y ROI
- **Capítulo 10. Conclusiones, Limitaciones y Trabajo Futuro**
  - 10.1. Conclusiones
  - 10.2. Limitaciones del Prototipo
  - 10.3. Trabajo Futuro
- **Capítulo 11. Bibliografía y Referencias**
- **Anexo A. Manifiesto Kubernetes Generado — Escenario 1 (Happy Path)**
  - A.1. Contexto de Generación
  - A.2. Manifiesto YAML Completo
  - A.3. Relación con el Código Fuente
- **Anexo B. Planificación Detallada del Proyecto y Costes**
  - B.1. Plan de Proyecto — Contexto y Restricciones
  - B.2. Estructura de Sprints y Estimación de Esfuerzo
  - B.3. Seguimiento Real del Proyecto — Retrospectivas por Sprint
  - B.4. Resumen de Desviaciones Globales
  - B.5. Análisis de Costes del Desarrollo
  - B.6. Estimación de Costes de Adopción para Organizaciones
  - B.7. Conclusiones del Análisis


<div style='page-break-after: always;'></div>

# Índice de Figuras y Algoritmos

El presente Trabajo de Fin de Máster hace uso intensivo de modelado visual y pseudocódigo para formalizar las decisiones arquitectónicas. A continuación se listan las figuras y algoritmos referenciados a lo largo de la memoria:

### Índice de Figuras

- **Figura 1:** Contraste arquitectónico entre el problema de integración N×M (acoplamiento propietario) y la topología de Bus Universal propuesta por el protocolo MCP. *(Capítulo 2)*
- **Figura 2:** Diagrama de componentes del Stack Tecnológico empleado, evidenciando la segregación entre las capas de interfaz, razonamiento cognitivo, backend restrictivo y las herramientas de validación de calidad continua. *(Capítulo 3)*
- **Figura 3:** Diagrama de Contenedores (Nivel 2) del Modelo C4 para el sistema Agentic Deployer. *(Capítulo 4)*
- **Figura 4:** Diagrama de despliegue a nivel de proceso. Los cuatro componentes coexisten en la misma máquina; el servidor MCP se comunica por `stdio` sin exponer ningún puerto TCP. *(Capítulo 4)*
- **Figura 5:** Topología de la Arquitectura Hexagonal. El flujo de control penetra desde los Adaptadores Primarios, pero la dependencia de código siempre fluye hacia el centro (Regla de Dependencia de Inversión). *(Capítulo 4)*
- **Figura 6:** Árbol de decisión del `SecurityContextValidator`. Cada rama de rechazo lanza un `SecurityViolationError` que el bucle ReAct captura como Observación para auto-corregirse. *(Capítulo 4)*
- **Figura 7:** Diagrama de Secuencia E2E (Fase 1). Negociación cognitiva entre el Investigador y el LLM hasta alcanzar una intención. *(Capítulo 4)*
- **Figura 8:** Diagrama de Secuencia E2E (Fase 2). El Backend procesa la petición, aplicando reglas de negocio estrictas. *(Capítulo 4)*
- **Figura 9:** Diagrama de Secuencia E2E (Fase 3). Decisión asíncrona del técnico humano, separando la inferencia de la ejecución. *(Capítulo 4)*
- **Figura 10:** Ciclo de vida completo de un mensaje MCP. El protocolo JSON-RPC define tres fases: inicialización, ejecución y observación. *(Capítulo 5)*
- **Figura 11:** Diagrama de flujo del bucle cognitivo ReAct (Reasoning and Acting). *(Capítulo 5)*
- **Figura 12:** Grafo Dirigido Acíclico (DAG) que rige la Máquina de Estados Finita (FSM) del sistema. *(Capítulo 6)*
- **Figura 13:** Diagrama de Secuencia del flujo HITL: polling del Dashboard, vector de aprobación (PENDING → APPROVED → DEPLOYED) y vector de rechazo (PENDING → REJECTED). *(Capítulo 6)*
- **Figura 14:** Arquitectura de la Pirámide Híbrida de Testing implementada en el Agentic Deployer, adaptando el modelo clásico a las exigencias de la Inteligencia Artificial Generativa. *(Capítulo 7)*
- **Tabla 1:** Comparativa ITSM Convencional vs. Modelo Agéntico (reducción TTM). *(Sección 8.1.2)*
- **Tabla 2:** Resultados del Mutation Testing por módulo. *(Sección 7.3.3)*
- **Anexo A:** Manifiesto YAML completo generado por FakeK8sAdapter — Escenario 1. *(Sección 8.3.1 y Anexo A)*

### Índice de Algoritmos (Pseudocódigo)

- **Algoritmo 1:** Validación Estricta de Entidades de Dominio Hexagonal. *(Sección 4.3.1)*
- **Algoritmo 2:** Introspección Dinámica de Contratos de Herramientas. *(Sección 5.1.1)*
- **Algoritmo 3:** Bucle de Orquestación Cognitiva (ReAct Loop). *(Sección 5.3.1)*
- **Algoritmo 4:** Transición Inmutable de la Máquina de Estados (FSM_Transition). *(Sección 6.2.2)*
- **Algoritmo 5:** Property-Based Test para Invariantes Hexagonales (Fuzzing). *(Sección 7.2.1)*
