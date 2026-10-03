# Anexo B. Retrospectivas Detalladas por Sprint

> Este anexo complementa el **Capítulo 9** con el seguimiento granular de cada sprint del proyecto. Para el marco de planificación, las estimaciones de esfuerzo, el análisis económico y el cálculo de ROI, véase el cuerpo del Capítulo 9.

---

## B.1. Sprint 1 — Núcleo Hexagonal

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 50h | ~55h | +10% |
| Tests (Unitarios + Property-Based) | ~15 | 51 tests | +240% |
| Cobertura dominio | 90% | 100% | +10pp |
<p align="center"><i><b>Tabla 30:</b> Retrospectiva del Sprint 1 (Núcleo Hexagonal).</i></p>

**Hitos completados:** `DeploymentIntent` con Pydantic v2, `SecurityContextValidator` (5 reglas), `DeployPort` abstracto, Suite Property-Based con Hypothesis.

**Notas:** La incorporación de validación de secretos en `env_vars` y de cuotas de hardware (CPU/RAM) no estaba en la estimación inicial; fue identificada durante el Property-Based Testing como un vector de riesgo real. El coste en tiempo fue compensado por la robustez ganada en capas superiores.

---

## B.2. Sprint 2 — Backend HITL y FSM

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 45h | ~45h | 0% |
| Endpoints REST | 4 | 5 (+`/hitl/reject`) | +25% |
| Estados FSM | 4 | 6 (+`FAILED`, `DELETED`) | +50% |
<p align="center"><i><b>Tabla 31:</b> Retrospectiva del Sprint 2 (Backend HITL y FSM).</i></p>

**Hitos completados:** FastAPI con 5 endpoints, FSM con DAG acíclico, Dashboard HTML con polling, `DeploymentStatus` enum completo.

**Notas:** El patrón de polling fue más directo de implementar que la alternativa WebSocket, generando un adelanto neto. La adición de los estados `FAILED` y `DELETED` reflejó un alineamiento proactivo entre la memoria y el código para cubrir ciclos de vida completos.

---

## B.3. Sprint 3 — Golden Paths y FakeK8s

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 40h | ~46h | +15% |
| Herramientas MCP | 3 | 4 | +33% |
| Templates YAML | 2 tipos | 3 tipos | +50% |
<p align="center"><i><b>Tabla 32:</b> Retrospectiva del Sprint 3 (Golden Paths y FakeK8s).</i></p>

**Hitos completados:** `FakeK8sAdapter` con templates f-string + `textwrap.dedent`, 4 herramientas MCP con `@mcp_server.tool()`, Pipeline CI `run_tests.sh` (6 pasos fail-fast), Ruff + Mypy integrados.

**Notas:** La integración del SDK MCP oficial (`mcp==2.2.0`) en modo dual —ejecutable vía `stdio` (clientes externos) e importable en-proceso (Streamlit)— requirió iteraciones adicionales no previstas. Esta decisión es el principal activo diferencial del sistema en términos de interoperabilidad.

---

## B.4. Sprint 4 — Agente ReAct y MCP SDK

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 55h | ~62h | +13% |
| Clientes LLM | 2 (Fake + OpenAI) | 3 (+Ollama nativo) | +50% |
| Iteraciones ReAct máximas | 5 | 5 | 0% |
<p align="center"><i><b>Tabla 33:</b> Retrospectiva del Sprint 4 (Agente ReAct y MCP SDK).</i></p>

**Hitos completados:** `LLMClient` ABC con inversión de dependencias, `OllamaLLMClient` nativo (`httpx` directo a la API REST de Ollama), `OpenAILLMClient`, `AgentOrchestrator` (bucle ReAct), Factory `LLM_PROVIDER` (`fake | ollama | openai`).

**Notas:** La serialización de firmas de herramientas Python a JSON Schema para el protocolo MCP requirió depuración adicional. El `OllamaLLMClient` nativo se completó en la fase de cierre, elevando el módulo de P1 a un acabado P2.

---

## B.5. Sprint 5 — QA Avanzado

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 45h | ~50h | +11% |
| Tests suite completa (Unit/PBT/MR) | ~35 | 51 | +46% |
| Mutantes eliminados | >90% | 100% | +10pp |
| Relaciones metamórficas | 3 MR | 4 MR | +33% |
<p align="center"><i><b>Tabla 34:</b> Retrospectiva del Sprint 5 (QA Avanzado).</i></p>

**Hitos completados:** Pipeline de QA integral implantado en `run_tests.sh` (Linter, Type-checking, Pytest, Mutmut, Playwright, Locust), Mutation Testing (12 mutantes mitigados), 4 Relaciones Metamórficas, Pruebas de Carga (Locust, p99 < 200ms), Playwright E2E sobre Dashboard.

**Notas:** La detección de 12 mutantes supervivientes en `mcp_server.py` fue el hallazgo más valioso del sprint, requiriendo la creación de `test_mcp_server.py` focalizado. Justifica empíricamente la adopción de Mutation Testing (Cap. 7.3).

---

## B.6. Fase 6 — Redacción y Cierre

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas de redacción | 55h | ~64h | +16% |
| Extensión de la memoria | ~55–70 páginas | **100+ páginas** | +43% |
| Iteraciones de revisión | 2–3 | 5 | +67% |
<p align="center"><i><b>Tabla 35:</b> Retrospectiva de la Fase 6 (Redacción y Cierre).</i></p>

**Hitos completados:** Redacción íntegra (11 capítulos), Diagramación Mermaid (14 figuras), Anexos YAML y de Planificación.

**Notas:** La memoria creció por encima de las previsiones iniciales. La inclusión de diagramas formales (C4, Arquitectura Hexagonal, FSM, secuencias E2E, pirámide de testing) y los tres *walkthroughs* forenses completos (Cap. 8.3) elevaron la densidad técnica de forma sustancial. El documento final de más de 100 páginas es el indicador más tangible del rigor y exhaustividad del trabajo.

---

## B.7. Fase 7 — Consolidación de Excelencia Técnica

| Métrica | Estimación | Real | Desviación |
|---|---|---|---|
| Horas dedicadas | 10h | ~18h | +80% |
| Herramientas MCP totales | 4 | 7 | +75% |
| Tests totales (Unitarios + Integración) | 51 tests | 61 tests | +19% |
<p align="center"><i><b>Tabla 36:</b> Retrospectiva de la Fase 7 (Consolidación de Excelencia Técnica).</i></p>

**Hitos completados:** Sustitución de persistencia volátil por **SQLite** (Transacciones ACID), Ampliación a 7 herramientas MCP (BD, Sitios Estáticos, Estado), Verificación externa empírica (Integración con **MCP Inspector** documentada en README), Cierre del *pipeline* CI con 0 fallos.

**Notas:** Esta fase, aunque no estaba prevista en el alcance original P0/P1, se abordó para elevar el proyecto a los máximos estándares de calidad. Se demostró que la Arquitectura Hexagonal es capaz de absorber un cambio completo de capa de datos (de RAM a SQLite) modificando únicamente los adaptadores, sin que la lógica de negocio se vea afectada, validando empíricamente la hipótesis principal de diseño (Cap. 4.2).
