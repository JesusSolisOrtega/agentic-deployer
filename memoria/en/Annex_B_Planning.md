# Annex B. Detailed Sprint Retrospectives

> This annex complements **Chapter 4** with granular tracking of each project sprint. For the planning framework, effort estimates, economic analysis, and ROI calculation, refer to the body of Chapter 4.

---

## B.1. Sprint 1 — Hexagonal Core

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 50h | ~55h | +10% |
| Tests (Unit + Property-Based) | ~15 | 51 tests | +240% |
| Domain coverage | >90% | >95% | +5pp |
<p align="center"><i><b>Table 39:</b> Sprint 1 Retrospective (Hexagonal Core).</i></p>

**Completed milestones:** `DeploymentIntent` with Pydantic v2, `SecurityContextValidator` (5 rules), abstract `DeployPort`, Property-Based test suite with Hypothesis.

**Notes:** Incorporating secret validation in `env_vars` and hardware quota enforcement (CPU/RAM) was not part of the initial estimate; it was identified during Property-Based Testing as a concrete operational risk vector. The associated time investment was compensated by the structural robustness gained across higher layers.

---

## B.2. Sprint 2 — HITL Backend and FSM

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 45h | ~45h | 0% |
| REST Endpoints | 4 | 5 (+`/hitl/reject`) | +25% |
| FSM States | 4 | 6 (+`FAILED`, `DELETED`) | +50% |
<p align="center"><i><b>Table 40:</b> Sprint 2 Retrospective (HITL Backend and FSM).</i></p>

**Completed milestones:** FastAPI backend with 5 endpoints, FSM with acyclic DAG, HTML Dashboard with polling, complete `DeploymentStatus` enumeration.

**Notes:** The client-polling pattern was more straightforward to implement than WebSocket alternatives, yielding net schedule savings. Adding the `FAILED` and `DELETED` states reflected proactive alignment between the academic documentation and codebase to encompass complete deployment lifecycles.

---

## B.3. Sprint 3 — Golden Paths and FakeK8s

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 40h | ~46h | +15% |
| MCP Tools | 3 | 4 | +33% |
| YAML Templates | 2 types | 3 types | +50% |
<p align="center"><i><b>Table 41:</b> Sprint 3 Retrospective (Golden Paths and FakeK8s).</i></p>

**Completed milestones:** `FakeK8sAdapter` with f-string templates and `textwrap.dedent`, 4 MCP tools decorated with `@mcp_server.tool()`, CI pipeline `scripts/run_tests.sh` (6 fail-fast stages), integrated Ruff and Mypy tooling.

**Notes:** Integrating the official MCP SDK (`mcp==2.2.0`) in dual mode—executable via `stdio` (external clients) and importable in-process (Streamlit)—required additional engineering iterations. This architectural choice represents a core differentiating asset regarding system interoperability.

---

## B.4. Sprint 4 — ReAct Agent and MCP SDK

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 55h | ~62h | +13% |
| LLM Clients | 2 (Fake + OpenAI) | 3 (+native Ollama) | +50% |
| Maximum ReAct iterations | 5 | 5 | 0% |
<p align="center"><i><b>Table 42:</b> Sprint 4 Retrospective (ReAct Agent and MCP SDK).</i></p>

**Completed milestones:** `LLMClient` ABC enforcing dependency inversion, native `OllamaLLMClient` (direct `httpx` against Ollama's REST API), `OpenAILLMClient`, `AgentOrchestrator` (ReAct loop), `LLM_PROVIDER` Factory (`fake | ollama | openai`).

**Notes:** Serializing Python tool signatures into compliant JSON Schemas for the MCP protocol required targeted debugging. The native `OllamaLLMClient` was completed during system finalization, upgrading the module from P1 baseline to full P2 production fidelity.

---

## B.5. Sprint 5 — Advanced QA

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 45h | ~50h | +11% |
| Full test suite (Unit/PBT/MR) | ~35 | 51 | +46% |
| Killed mutants | >90% | >95% | +5pp |
| Metamorphic relations | 3 MR | 6 MR | +100% |
<p align="center"><i><b>Table 43:</b> Sprint 5 Retrospective (Advanced QA).</i></p>

**Completed milestones:** Comprehensive QA pipeline implemented in `scripts/run_tests.sh` (Linter, Type-checking, Pytest, Mutmut, Playwright, Locust), Mutation Testing (12 surviving mutants mitigated), 6 Metamorphic Relations (MR-1 through MR-6), Load Testing (Locust, p99 < 200ms), Playwright E2E UI testing on the Dashboard.

**Notes:** Uncovering 12 surviving mutants in `mcp_server.py` was the most impactful finding of the sprint, driving the creation of targeted tests in `test_mcp_server.py`. This empirically substantiates adopting Mutation Testing (Section 8.3).

---

## B.6. Phase 6 — Thesis Drafting and Finalization

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Drafting hours | 55h | ~64h | +16% |
| Thesis length | ~100 pages | **~150 pages** | +50% |
| Review iterations | 2–3 | 5 | +67% |
<p align="center"><i><b>Table 44:</b> Phase 6 Retrospective (Thesis Drafting and Finalization).</i></p>

**Completed milestones:** Full monograph drafting (11 chapters), technical diagramming and visual captures (20 figures), YAML and Planning Annexes.

**Notes:** The thesis expanded beyond the initial baseline (~100 estimated pages versus ~150 resulting pages across main chapters and technical annexes). Incorporating formal architectural diagrams (C4, Hexagonal Architecture, FSM, E2E sequences, testing pyramid), four complete execution walkthroughs (Section 9.2), and three comprehensive technical annexes substantially elevated documentation depth. The drafting schedule deviation (+16%) remained constrained through the structured use of an AI assistant (Google Gemini Advanced) as an efficiency multiplier in technical drafting—an effect documented in §4.3 and §4.7. The resulting ~150-page document serves as tangible evidence of methodological rigor and thoroughness.

---

## B.7. Phase 7 — Technical Excellence Consolidation

| Metric | Estimate | Actual | Deviation |
|---|---|---|---|
| Dedicated hours | 10h | ~18h | +80% |
| Total MCP tools | 4 | 7 | +75% |
| Total tests (Unit + Integration) | 51 tests | 65 tests | +27% |
<p align="center"><i><b>Table 45:</b> Phase 7 Retrospective (Technical Excellence Consolidation).</i></p>

**Completed milestones:** Replaced ephemeral in-memory state with **SQLite** (ACID transactions), expanded tool suite to 7 MCP tools (Databases, Static Sites, Status inspection), empirical external verification (integration with **MCP Inspector** documented in README), green CI pipeline with 0 failures, **Multi-Model Cognitive Experiments** (Qwen vs Mistral vs Llama vs Coder vs Cloud).

**Notes:** This phase was planned from the outset as an optional technical excellence objective (Priority P2) and was successfully undertaken due to efficient completion of mandatory baseline modules (P0/P1). The hexagonal architecture demonstrated its ability to absorb a complete data layer migration (from RAM to SQLite) by altering adapters alone. Furthermore, empirical evaluations across diverse 7B generalist LLMs (Mistral, Llama 3.2, Qwen) documented structural degradation and attention loss under stress. Crucially, introducing the specialized **Qwen 2.5 Coder (7B)** model yielded the defining empirical insight of this phase: its ability to pass all metamorphic relations validated financial feasibility conclusions (Chapters 4 and 9), proving that enterprise-grade operational performance is achievable entirely on entry-level commodity hardware with Zero Data Retention.

