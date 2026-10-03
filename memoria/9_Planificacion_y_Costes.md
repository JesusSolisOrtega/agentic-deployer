# Capítulo 9. Gestión y Viabilidad del Proyecto

La construcción de un sistema que hibrida disciplinas clásicas de Ingeniería de Software con dominios emergentes como la Inteligencia Artificial Generativa exige un marco de planificación riguroso pero flexible. Este capítulo documenta las restricciones del proyecto, la estructura de *sprints*, el seguimiento global de desviaciones y un análisis económico completo que evalúa tanto el coste del desarrollo como la viabilidad de adopción institucional. El desglose pormenorizado de las retrospectivas por sprint se encuentra en el **Anexo B**.

---

## 9.1. Plan de Proyecto — Contexto y Restricciones

### 9.1.1. Restricciones Estructurales

El *Agentic Deployer* se desarrolla en el contexto de un Trabajo de Fin de Máster bajo las siguientes restricciones:

- **Dedicación:** Régimen parcial de investigación (~15–20 horas semanales, compatibles con actividad profesional externa).
- **Equipo:** 1 alumno investigador + 1 tutor académico (sesiones de supervisión periódicas, con cadencia condicionada a la disponibilidad de ambas partes).
- **Infraestructura:** Entorno de desarrollo local (portátil personal), sin coste de nube durante el desarrollo.
- **Metodología:** Iterativa incremental, centrada en el dominio (*Domain-First*).

### 9.1.2. Principio de Flexibilidad y Priorización Adaptativa

> [!IMPORTANT]
> La planificación aquí descrita es de carácter **indicativo y orientativo**, no normativo. Dado que el presente TFM se desarrolla en régimen de dedicación parcial, compatibilizado con compromisos profesionales y personales de carácter variable, se asume *a priori* que los intervalos temporales de cada sprint son permeables: su ejecución puede acelerarse, posponerse o solaparse según la disponibilidad real del investigador y la capacidad de respuesta del tutor en los hitos críticos de revisión.

Esta aproximación es coherente con las recomendaciones de gestión ágil de proyectos de I+D aplicados en contextos académicos (IEEE Std 12207, ISO/IEC 29110), donde la rigidez del cronograma es sustituida por la **priorización explícita de objetivos**: se garantiza primero el alcance mínimo viable (MVP) y, en función del tiempo residual, se abordan los módulos de mayor complejidad o acabado opcionales.

**Jerarquía de prioridades del proyecto:**

| Prioridad | Módulo | Estado |
|---|---|---|
| **P0 — MVP obligatorio** | Núcleo hexagonal, validador de seguridad, API REST, FSM, Dashboard HITL | Completado |
| **P1 — Diferenciador académico** | Servidor MCP (SDK oficial), agente ReAct, multiproveedor LLM, QA avanzado | Completado |
| **P2 — Excelencia y acabado** | `OllamaLLMClient`, persistencia ACID (SQLite), catálogo MCP extendido (7 herramientas), evidencias empíricas (MCP Inspector) | Completado |
| **P3 — Trabajo futuro** | `RealK8sAdapter` (integración clúster físico), RBAC, CI/CD cloud, multi-clúster | Roadmap |
<p align="center"><i><b>Tabla 16:</b> Módulos de desarrollo y jerarquía de prioridades.</i></p>

Únicamente los módulos **P0 y P1 son necesarios para la evaluación académica**. Los módulos P2 se han abordado con éxito en la recta final de consolidación, logrando un nivel de excelencia técnica que fortalece la robustez del proyecto. Los módulos P3 quedan explícitamente documentados como líneas de trabajo futuro (Sección 10.3).

---

## 9.2. Estructura de Sprints y Estimación de Esfuerzo

### 9.2.1. Diagrama de Planificación

La planificación se estructura en **5 sprints temáticos** más una fase transversal de redacción y una fase de consolidación de excelencia, con un esfuerzo total estimado de **~300 horas** (±15% de margen de contingencia estándar). Las fechas son referencias aproximadas sujetas al principio de flexibilidad enunciado en la sección anterior.

```mermaid
gantt
  title Plan de Proyecto — Sprints de Desarrollo (Fase Core y Agéntica)
  dateFormat YYYY-MM-DD
  axisFormat %b

  section P0 · Sprint 1<br>- Núcleo Hexagonal
  Modelado de Entidades (DeploymentIntent)    :s1a, 2026-03-02, 5d
  SecurityContextValidator (Algoritmo 1)     :s1b, after s1a, 5d
  Ports y Contratos (DeployPort)         :s1c, after s1b, 4d
  Tests Unitarios y Property-Based (Hypothesis) :s1d, after s1c, 7d

  section P0 · Sprint 2<br>- Backend HITL y FSM
  API REST FastAPI (endpoints MCP + HITL)    :s2a, 2026-03-23, 6d
  FSM y transiciones de estado          :s2b, after s2a, 4d
  Dashboard HTML (polling asíncrono)       :s2c, after s2b, 5d
  Tests de integración (use_cases)        :s2d, after s2c, 6d

  section P1 · Sprint 3<br>- Golden Paths y FakeK8s
  FakeK8sAdapter (YAML Deployment+Service+Ingress):s3a, 2026-04-13, 7d
  Herramientas MCP (Golden Paths)        :s3b, after s3a, 5d
  Pipeline CI local (run_tests.sh)        :s3c, after s3b, 3d
  Linting Ruff + Type-checking Mypy       :s3d, after s3c, 3d

  section P1 · Sprint 4<br>- Agente ReAct y MCP SDK
  Integración SDK MCP oficial          :s4a, 2026-05-04, 6d
  LLMClient ABC + OllamaLLMClient        :s4b, after s4a, 5d
  AgentOrchestrator (bucle ReAct)        :s4c, after s4b, 5d
  Chat Streamlit + System Prompt SIC       :s4d, after s4c, 5d
```
<p align="center"><i><b>Figura 16:</b> Diagrama de Gantt (Parte 1). Planificación orientativa de los Sprints 1 a 4 (núcleo y agente).</i></p>

```mermaid
gantt
  title Plan de Proyecto — QA Avanzado y Consolidación Técnica
  dateFormat YYYY-MM-DD
  axisFormat %b

  section P1 · Sprint 5<br>- QA Avanzado
  Mutation Testing (mutmut)           :s5a, 2026-05-25, 7d
  Pruebas Metamórficas (MR)           :s5b, after s5a, 5d
  Pruebas de carga (Locust)           :s5c, after s5b, 4d
  E2E Playwright (Dashboard HITL)        :s5d, after s5c, 3d

  section P2 · Fase 6<br>- Redacción y Cierre
  Redacción de Capítulos 1-5           :s6a, 2026-06-15, 21d
  Redacción de Capítulos 6-9           :s6b, after s6a, 14d
  Revisión tutor + correcciones iterativas    :s6c, after s6b, 28d
  Acabado P2 (costes, evidencias, anexos)    :s6d, after s6c, 14d

  section P2 · Fase 7<br>- Excelencia Técnica
  Persistencia ACID (SQLite) e Inyección de Dep. :s7a, after s6d, 7d
  Ampliación MCP a 7 herramientas operativas   :s7b, after s7a, 5d
  QA 360: Mutmut + Pruebas Integración      :s7c, after s7b, 4d
```
<p align="center"><i><b>Figura 17:</b> Diagrama de Gantt (Parte 2). Planificación orientativa del QA avanzado y las fases de cierre/consolidación.</i></p>

### 9.2.2. Estimación de Esfuerzo por Sprint

La siguiente tabla refleja la estimación inicial de esfuerzo neto, asumiendo un ritmo de trabajo parcial y la incorporación de asistencia mediante herramientas de IA generativa, cuyo efecto es la aceleración del ciclo de implementación sin merma de la calidad del análisis.

| Sprint | Fase | Estimación (h) | Rango (±15%) | Prioridad |
|---|---|---|---|---|
| Sprint 1 | Núcleo Hexagonal | 50h | 43–58h | P0 |
| Sprint 2 | Backend HITL y FSM | 45h | 38–52h | P0 |
| Sprint 3 | Golden Paths y FakeK8s | 40h | 34–46h | P1 |
| Sprint 4 | Agente ReAct y MCP SDK | 55h | 47–63h | P1 |
| Sprint 5 | QA Avanzado | 45h | 38–52h | P1 |
| Fase 6 | Redacción y Cierre | 55h | 47–63h | P2 |
| Fase 7 | Excelencia Técnica | 10h | 8–12h | P2 |
| **Total estimado** | | **~300h** | **~255–345h** | |
<p align="center"><i><b>Tabla 17:</b> Estimación de esfuerzo neto por Sprint.</i></p>

> [!NOTE]
> La asistencia mediante un agente de IA de codificación (Google Gemini Advanced, utilizado para aceleración de *scaffolding*, generación de código *boilerplate*, revisión de lógica y apoyo en la redacción técnica) permitió comprimir el tiempo de implementación en fases que de otro modo habrían requerido un esfuerzo sustancialmente mayor. Esto es coherente con la línea de investigación del propio proyecto, que postula la utilidad de los agentes LLM como asistentes en flujos de trabajo técnicos complejos.

---

## 9.3. Esfuerzo de Desarrollo y Desviaciones

Frente a la estimación inicial de ~300 horas, el cierre empírico del proyecto arrojó un esfuerzo total de **~340 horas**, lo que representa una desviación del **+13%**. Esta inversión adicional se encuadra holgadamente dentro del margen de contingencia previsto (±15%) y se asumió de manera deliberada en la recta final para elevar el MVP a un estándar de excelencia ingenieril (implementación de persistencia ACID en SQLite, ampliación de 4 a 7 herramientas MCP e identificación exhaustiva de brechas mediante *Mutation Testing*).

La adopción de asistentes de Inteligencia Artificial (Google Gemini Advanced) demostró actuar como un multiplicador de productividad esencial. Permitió absorber esta densidad arquitectónica dentro de un cronograma manejable para un único ingeniero, validando de forma recursiva la hipótesis de investigación del TFM sobre la utilidad de los agentes LLM en ciclos de vida de software.

La siguiente tabla resume las desviaciones por fase:

| Fase | Estimación (h) | Real (h) | Desviación | Causa Principal |
|---|---|---|---|---|
| Sprint 1 · Núcleo Hexagonal | 50 | ~55 | +10% | Ampliación del validador de seguridad |
| Sprint 2 · Backend HITL y FSM | 45 | ~45 | 0% | Desarrollo ajustado a la previsión |
| Sprint 3 · Golden Paths y FakeK8s | 40 | ~46 | +15% | Integración dual SDK MCP |
| Sprint 4 · Agente ReAct y MCP SDK | 55 | ~62 | +13% | Agente ReAct + Ollama nativo |
| Sprint 5 · QA Avanzado | 45 | ~50 | +11% | Análisis forense de mutantes |
| Fase 6 · Redacción y Cierre | 55 | ~64 | +16% | Densidad técnica y extensión final (100+ págs) |
| Fase 7 · Excelencia Técnica | 10 | ~18 | +80% | Inyección dependencias SQLite y QA final |
| **Total** | **~300** | **~340** | **~+13%** | |
<p align="center"><i><b>Tabla 18:</b> Resumen de desviaciones de tiempo por fase.</i></p>

> [!NOTE]
> Una desviación del **+13%** respecto a la estimación de referencia se sitúa cómodamente dentro del margen de contingencia previsto (±15%). Esta inversión de horas extra (~40h) se asumió de manera consciente y deliberada para garantizar un acabado de excelencia académica e ingenieril en la recta final (Fase 7), demostrando que el proyecto puede escalar a estándares corporativos manteniendo la planificación original bajo control. El desglose pormenorizado por sprint con las retrospectivas detalladas, incluyendo los hitos completados y las lecciones aprendidas, se documenta en el **Anexo B**.

---

## 9.4. Análisis Económico del Desarrollo

El proyecto fue desarrollado utilizando recursos de código abierto e infraestructura personal, por lo que el coste material directo fue marginal. No obstante, para evaluar la viabilidad económica de la solución, se ha calculado el **coste de oportunidad equivalente**: la inversión que requeriría el proyecto si se externalizara en el mercado tecnológico español a tarifas de 2026.

### 9.4.1. Costes de Recursos Humanos

| Perfil | Tarifa/hora | Horas | Coste de oportunidad |
|---|---|---|---|
| **Alumno Investigador** (Ingeniero Junior — equivalente mercado) | 22 €/h | ~340h | ~7.480 € |
| **Tutor Académico** (Perfil Senior / Supervisor I+D) | 75 €/h | ~24h *(sesiones periódicas)* | ~1.800 € |
| **Subtotal Recursos Humanos** | | **~364h** | **~9.280 €** |
<p align="center"><i><b>Tabla 19:</b> Costes de Recursos Humanos (CAPEX equivalente).</i></p>

> **Nota metodológica:** Los valores representan el coste de oportunidad equivalente de mercado: la inversión económica que representaría este proyecto si se ejecutase bajo contrato profesional. El alumno no percibe remuneración; el tutor es compensado institucionalmente al margen de este cálculo.

### 9.4.2. Costes de Infraestructura y Herramientas

| Recurso | Proveedor | Coste imputable | Cálculo / Observación |
|---|---|---|---|
| **Portátil de desarrollo** | Hardware personal | **~126 €** | Portátil ~1.200 € · vida útil 4 años · fracción de uso TFM (6 meses / 48 meses) ≈ 150 € · factor dedicación parcial ~84% ≈ **126 €** |
| Sistema operativo y utilidades | Linux (Ubuntu) | 0 € | Open source |
| Python 3.12 + ecosistema | Open source | 0 € | — |
| FastAPI, Pydantic, Hypothesis, Pytest | Open source | 0 € | — |
| SDK MCP oficial (`mcp==2.2.0`) | Anthropic (MIT License) | 0 € | Open source |
| Ollama (servidor LLM local) | Open source | 0 € | Modelos gratuitos |
| **Asistente IA (Google Gemini Advanced)** | Google | **~120 €** | 20 €/mes × 6 meses. Utilizado para asistencia en codificación, scaffolding, revisión de lógica y apoyo en redacción técnica |
| OpenAI API (validación puntual) | OpenAI | ~15 € | Créditos de prueba |
| **Subtotal Infraestructura y Herramientas** | | **~261 €** | |
<p align="center"><i><b>Tabla 20:</b> Costes de Infraestructura y Herramientas (Fase de Desarrollo).</i></p>

### 9.4.3. Costes Totales de Desarrollo

| Categoría | Coste |
|---|---|
| Recursos Humanos (coste de oportunidad) | ~9.280 € |
| Infraestructura y herramientas | ~261 € |
| **Coste Total del Proyecto** | **~9.541 €** |
| **Coste por hora efectiva** | **~26,2 €/h** |
<p align="center"><i><b>Tabla 21:</b> Subtotal y costes totales de la fase de desarrollo.</i></p>

---

## 9.5. Coste de Adopción Corporativa y ROI

Esta sección responde a la pregunta estratégica: **¿Cuánto costaría adaptar e implantar el *Agentic Deployer* en un entorno institucional real**, como un Servicio de Informática universitario o un departamento de IT corporativo?

### 9.5.1. Perfiles de Organización Adoptante

| Perfil | Descripción | Complejidad |
|---|---|---|
| **A — Universidad pequeña** | <5.000 usuarios, 1 técnico SIC, clúster Minikube/K3s local | Baja |
| **B — Universidad mediana** | 5.000–30.000 usuarios, equipo SIC de 5–10 personas, K8s on-premise | Media |
| **C — Administración pública / empresa** | >30.000 usuarios, multi-clúster, auditoría RGPD estricta | Alta |
<p align="center"><i><b>Tabla 22:</b> Perfiles de Organización Adoptante (Casos A, B y C).</i></p>

### 9.5.2. Costes de Implantación (CAPEX — Inversión Inicial)

| Componente | Perfil A | Perfil B | Perfil C |
|---|---|---|---|
| **Adaptación del código** *(personalizar `SYSTEM_PROMPT`, herramientas MCP y políticas de seguridad al catálogo corporativo)* | 20h × 40 €/h = **800 €** | 60h × 50 €/h = **3.000 €** | 160h × 60 €/h = **9.600 €** |
| **Implementación `RealK8sAdapter`** *(integración con clúster físico vía `kubernetes-client`)* | 20h × 40 €/h = **800 €** | 40h × 50 €/h = **2.000 €** | 80h × 60 €/h = **4.800 €** |
| **Configuración y despliegue** *(CI/CD, variables de entorno, SSL, LDAP/SAML)* | 10h × 40 €/h = **400 €** | 30h × 50 €/h = **1.500 €** | 60h × 60 €/h = **3.600 €** |
| **Formación del equipo técnico** | 4h × 5 pers = **400 €** | 8h × 10 pers = **1.600 €** | 16h × 20 pers = **4.800 €** |
| **CAPEX Total** | **2.400 €** | **8.100 €** | **22.800 €** |
<p align="center"><i><b>Tabla 23:</b> Costes de Implantación (CAPEX - Inversión Inicial).</i></p>

### 9.5.3. Costes Operativos Anuales (OPEX)

#### Infraestructura de Servidor

| Componente | Perfil A | Perfil B | Perfil C |
|---|---|---|---|
| Servidor aplicación (FastAPI + MCP) | VPS 4 vCPU / 8 GB ≈ **600 €/año** | Servidor on-premise amortizado ≈ **300 €/año** | 3 réplicas en nube ≈ **3.600 €/año** |
| Almacenamiento (BD + logs YAML) | 50 GB SSD ≈ **60 €/año** | 200 GB ≈ **200 €/año** | 1 TB + backups ≈ **800 €/año** |
<p align="center"><i><b>Tabla 24:</b> Costes Operativos Anuales de Infraestructura (OPEX).</i></p>

#### Motor LLM — La Variable Determinante del OPEX

**Opción 1 — Ollama local (modelos open-source, recomendado para instituciones públicas)**

| Modelo | VRAM necesaria | Inversión hardware (única vez) | Coste API | Privacidad |
|---|---|---|---|---|
| `qwen2.5:7b` | 8 GB | ~400 € GPU consumer | **0 €/año** | Total (Zero Data Retention) |
| `llama3.1:8b` | 8 GB | ~400 € GPU consumer | **0 €/año** | Total |
| `mistral:7b` | 4 GB | ~250 € GPU consumer | **0 €/año** | Total |
<p align="center"><i><b>Tabla 25:</b> Costes Operativos Anuales de Motor LLM (Local vs Cloud).</i></p>

**Opción 2 — API en la nube**

| Proveedor | Modelo | Precio entrada | Precio salida | Estimación anual* |
|---|---|---|---|---|
| OpenAI | GPT-4o-mini | 0,15 $/MTok | 0,60 $/MTok | **~600–2.400 €/año** |
| OpenAI | GPT-4o | 2,50 $/MTok | 10,00 $/MTok | **~6.000–24.000 €/año** |
| Anthropic | Claude Haiku | 0,25 $/MTok | 1,25 $/MTok | **~800–3.200 €/año** |
| Google | Gemini Flash | 0,075 $/MTok | 0,30 $/MTok | **~300–1.200 €/año** |
<p align="center"><i><b>Tabla 26:</b> OPEX Total Anual consolidado por Perfil de Adopción.</i></p>

> *Para 50–200 solicitudes diarias con conversaciones de ~2.000 tokens promedio.

#### OPEX Total Anual por Perfil

| Componente | Perfil A | Perfil B | Perfil C |
|---|---|---|---|
| Servidor aplicación | 600 €/año | 300 €/año | 3.600 €/año |
| Almacenamiento | 60 €/año | 200 €/año | 800 €/año |
| LLM Ollama local (hardware, única vez) | +400 € (año 0) | +400 € (año 0) | +400 € (año 0) |
| LLM API nube (alternativa) | ~600 €/año | ~2.400 €/año | ~6.000 €/año |
| Mantenimiento y actualizaciones | 10h × 40 €/h = **400 €/año** | 20h × 50 €/h = **1.000 €/año** | 40h × 60 €/h = **2.400 €/año** |
| **OPEX Total (con Ollama)** | **~1.060 €/año** | **~1.500 €/año** | **~6.800 €/año** |
| **OPEX Total (con API nube)** | **~1.660 €/año** | **~3.900 €/año** | **~12.800 €/año** |
<p align="center"><i><b>Tabla 27:</b> Cálculo del ahorro anual operativo (Escenario de Perfil B).</i></p>

### 9.5.4. Análisis de Retorno de Inversión (ROI)

El valor generado se cuantifica a partir de la reducción de tiempo operativo documentada en el Capítulo 8 (Tabla 8).

**Cálculo del ahorro anual — Perfil B (Universidad mediana, 500 solicitudes/año)**

| Proceso eliminado | Tiempo ahorrado/solicitud | Solicitudes/año | Coste hora técnico N3 | Ahorro anual |
|---|---|---|---|---|
| Negociación de requisitos (email asíncrono) | 1.440 min → 0,5 min | 500 | 50 €/h | **11.995 €** |
| Traducción manual a YAML | 15 min → 0,01 min | 500 | 50 €/h | **6.242 €** |
| Validación de políticas | 5 min → 0,001 min | 500 | 50 €/h | **2.083 €** |
| **Ahorro total anual** | | | | **~20.320 €** |
<p align="center"><i><b>Tabla 27:</b> Cálculo del ahorro anual operativo (Escenario de Perfil B).</i></p>

> **Nota sobre el cálculo de tiempos:** El valor de 1.440 minutos (~24 horas) para la "Negociación de requisitos" es una estimación conservadora basada en el SLA (*Service Level Agreement*) típico de un Service Desk universitario, donde el intercambio asíncrono de tickets o correos electrónicos (solicitud → falta de datos → respuesta del investigador → nueva validación) consume al menos un día hábil (24h de tiempo de reloj) hasta alcanzar un estado de intención completa.

**ROI a 3 años — Perfil B con Ollama**

| Concepto | Año 0 | Año 1 | Año 2 | Año 3 |
|---|---|---|---|---|
| Inversión CAPEX | -8.100 € | — | — | — |
| Hardware LLM (Ollama GPU, única vez) | -400 € | — | — | — |
| OPEX anual | — | -1.500 € | -1.500 € | -1.500 € |
| Ahorro operativo | — | +20.320 € | +20.320 € | +20.320 € |
| **Flujo neto** | **-8.500 €** | **+18.820 €** | **+18.820 €** | **+18.820 €** |
| **Acumulado** | -8.500 € | +10.320 € | +29.140 € | +47.960 € |
<p align="center"><i><b>Tabla 28:</b> Retorno de Inversión (ROI) a 3 años (Perfil B con Ollama).</i></p>

> **Período de retorno (Payback Period): ~5,4 meses** tras la implantación.
> **ROI a 3 años: ~464%**

---

## 9.6. Conclusiones del Análisis de Viabilidad

1. **La flexibilidad de la planificación es una característica del diseño, no una deficiencia.** La naturaleza parcial y asincrónica del desarrollo impide la aplicación de cronogramas rígidos; la priorización explícita (P0→P3) garantiza que el núcleo de valor académico se complete antes que cualquier módulo de acabado opcional.

2. **La asistencia de IA generativa es un multiplicador de productividad consistente con el objeto de estudio.** El uso de un agente de codificación (Google Gemini Advanced, ~120 € de coste imputable) permitió abordar un alcance técnico ambicioso —arquitectura hexagonal, SDK MCP oficial, QA multicapa, agente ReAct— dentro de un esfuerzo total contenido (~340h), que de otro modo habría requerido un equipo de al menos 2 personas.

3. **El modelo de coste cero es viable con Ollama para instituciones públicas.** La combinación Ollama + servidor on-premise reduce el OPEX a menos de 2.000 €/año, con garantía total de privacidad del dato (Zero Data Retention), lo que lo convierte en la opción recomendada para organismos con restricciones presupuestarias o de soberanía del dato.

4. **El ROI superior al 460% en 3 años justifica la adopción institucional.** El umbral de rentabilidad se alcanza en menos de 6 meses para un volumen mínimo de 500 solicitudes de infraestructura anuales.

5. **La arquitectura hexagonal protege la inversión tecnológica a largo plazo.** La sustitución de cualquier adaptador —`FakeK8sAdapter` → `RealK8sAdapter`, Ollama → GPT-4o, etc.— no requiere modificar la lógica de negocio. El coste de evolución tecnológica está estructuralmente minimizado por el Principio de Inversión de Dependencias (DIP).
