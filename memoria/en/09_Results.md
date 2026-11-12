# Chapter 9. Experimental Results and Evaluation

Architectural design (Chapter 5), cognitive agent and MCP implementation (Chapter 6), human governance via HITL controls (Chapter 7), and quality assurance methodologies (Chapter 8) converge in this chapter for rigorous empirical evaluation. In enterprise infrastructure engineering, software validity relies not merely on theoretical component correctness, but on the ability to resolve real provisioning tasks predictably, securely, and efficiently under operational constraints.

This chapter structures empirical evaluation across six complementary pillars:
1. **Experimental Framework and Testbed (§9.1):** Specification of computational hardware, inference engines, technical preconditions, and statistical repeatability protocols.
2. **Real Case Studies (End-to-End Walkthroughs) (§9.2):** Traceability of system behavior across four operational scenarios: compliant baseline provisioning (*Happy Path*), perimeter resilience against prompt injection attacks, asynchronous human-in-the-loop governance (*HITL*), and deterministic exception-guided self-correction.
3. **Comparative Empirical Evaluation of LLM Architectures (§9.3):** Specialized evaluation of foundational models under two operating regimes: strict unassisted zero-shot metamorphic stress-testing versus architecture-assisted ReAct tool calling, contrasting local and cloud models.
4. **Cognitive Architecture Experiments (§9.4):** Evaluation of three conversational control paradigms (*Classic ReAct*, *Chain-of-Thought*, and *Stateful Slot Filling*) to overcome attentional limits in small local models (<8B parameters).
5. **Operational Impact Evaluation on ITSM Processes (§9.5):** Quantitative assessment of delivery timelines and cognitive overhead measured against traditional IT service management workflows.
6. **Threats to Empirical Validity (§9.6):** Methodological analysis of internal, external, construct, and conclusion validity threats in alignment with empirical software engineering guidelines.

## 9.1. Experimental Framework and Testbed

To ensure scientific reproducibility, all evaluations were conducted under controlled conditions. Execution sessions were captured as structured JSON telemetry traces (persisted in `demos/session_logs/`), recording model inference outputs without post-hoc manipulation.

The hardware and software environment representing a university research testbed is detailed in Table 24:

| Parameter | Specification |
|---|---|
| **Evaluation Workstation** | Mobile workstation: AMD Ryzen 7 5800H CPU (8 cores, 16 threads @ 3.2 GHz), 16 GB DDR4 RAM, NVIDIA GeForce RTX 3060 Laptop GPU (6 GB GDDR6 VRAM) |
| **Operating System** | Ubuntu 22.04 LTS (Linux Kernel 5.15), native execution environment |
| **Local Inference Platform** | Ollama v0.6.2 with NVIDIA CUDA acceleration |
| **Local Baseline Model** | `qwen2.5:7b` (Q4_K_M quantization, ~4.7 GB VRAM footprint) |
| **Local Specialized Variant** | `qwen2.5-coder:7b` (Q4_K_M quantization, ~4.7 GB VRAM footprint) |
| **Evaluated Cloud Models** | Gemini 3.5 Flash (Google), Cohere Command R+ (Cohere), Ministral 8B (Mistral AI), Codestral (Mistral AI), Qwen 2.5 27B (Groq LPU) |
| **Application Backend** | FastAPI 0.115 hosted on Uvicorn ASGI server (single-worker mode) |
| **Persistence Layer** | SQLite 3.45 with durable on-disk ACID transactional support |
| **Repeatability Protocol** | Each scenario was executed in batches of 5 consecutive iterations to absorb network and sampling variance; latency metrics are reported as mean ($\mu$) $\pm$ standard deviation ($\sigma$) |
<p align="center"><i><b>Table 24:</b> Evaluation testbed for practical case studies.</i></p>

## 9.2. Real Case Studies (End-to-End Walkthroughs)

This section documents four real execution scenarios, tracing natural language inputs, MCP protocol mediation, hexagonal policy validation, and generated infrastructure artifacts.

To evaluate architectural stabilization over stochastic models transparently, walkthroughs utilize the general-purpose local model `qwen2.5:7b` under air-gapped Zero Data Retention conditions.

### 9.2.1. Scenario 1 — Standard Provisioning (*Happy Path*): Academic Conference Web Portal

This scenario traces the 10 operational steps required to provision an institutional web workload from conversational prompt to declarative Kubernetes YAML generation.

**STEP 1 — Researcher Input (Natural Language):**

> *«Hello, I need to publish the website for the departmental AI conference. We anticipate around 200 attendees. Can you handle this?»*

---

**STEP 2 — Cognitive Inference and Reasoning (ReAct Agent):**

`AgentOrchestrator` processes the request within the ReAct loop. The model infers a public HTTP workload, sizes resources appropriately, selects a hardened image (`nginx:alpine`), sets a standard non-privileged port (`8080`), and allocates resource bounds:

```json
{
  "thought": "The user requested a web portal for an academic conference with 200 attendees. This requires a standard HTTP web server. Adhering to institutional policies, I will utilize nginx:alpine on port 8080 with 500m CPU and 256Mi RAM.",
  "tool_call": {
    "name": "format_deployment_intent",
    "arguments": {
      "name": "congreso-ia-departamento",
      "image": "nginx:alpine",
      "port": 8080,
      "cpu": "500m",
      "ram": "256Mi"
    }
  }
}
```

---

**STEP 3 — Tool Dispatch via MCP Server:**

The FastMCP server validates arguments against the tool schema and dispatches an HTTP `POST` request to the backend (`http://localhost:8000/deployments/intent`).

---

**STEP 4 — Reception at Primary Driving Adapter (FastAPI):**

The FastAPI REST controller deserializes the JSON payload into a typed `DeploymentIntent` domain entity.

---

**STEP 5 — Deterministic Validation in Hexagonal Core (`SecurityContextValidator`):**

The `RegisterDeploymentIntent` use case invokes `SecurityContextValidator` (Algorithm 1), auditing institutional policies:

| Security Rule Evaluated | Compliance Status |
|---|---|
| Unprivileged port (8080 $\ge$ 1024) | Compliant |
| Immutable tag (`:alpine` $\ne$ `:latest`) | Compliant |
| Trusted container registry (`docker.io/library/nginx`) | Compliant |
| CPU quota (500m $\le$ 2000m departmental limit) | Compliant |
| RAM quota (256Mi $\le$ 4096Mi departmental limit) | Compliant |
| Absence of plaintext secrets in environment variables | Compliant |
<p align="center"><i><b>Table 25:</b> Execution trace: Hexagonal core validation (Step 5).</i></p>

With zero violations detected, the SQLite repository persists the intent under `PENDING_APPROVAL` with UUID `dep-7f3a2c1b`.

---

**STEP 6 — Backend HTTP Response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "dep-7f3a2c1b",
  "status": "PENDING_APPROVAL",
  "name": "congreso-ia-departamento",
  "image": "nginx:alpine",
  "port": 8080,
  "cpu": "500m",
  "ram": "256Mi",
  "message": "Intent registered. Awaiting HITL approval from SIC technician."
}
```

---

**STEP 7 — Observation Feedback to LLM (ReAct Loop):**

The response payload is appended to context memory as an observation, instructing the agent to terminate reasoning.

---

**STEP 8 — Final Conversational Response to Researcher:**

> *«Your deployment request has been registered in the system. An IT operations technician will review and authorize provisioning in the control dashboard.*
>
> ***Registered Technical Specifications:***
> *- **Tracking ID:** `dep-7f3a2c1b`*
> *- **Service Name:** `congreso-ia-departamento`*
> *- **Container Image:** `nginx:alpine`*
> *- **Network Configuration:** Port 8080 | **CPU:** 500m | **RAM:** 256Mi*
> *- **Current Status:** `PENDING_APPROVAL` (Awaiting technical review)»*

---

**STEP 9 — Audit and Authorization in HITL Dashboard:**

An IT technician opens the dashboard at `/hitl` (Figure 17), reviews technical parameters, and clicks **«Approve»**:

```bash
# Operational curl equivalent executed by Dashboard
curl -X POST http://localhost:8000/hitl/approve/dep-7f3a2c1b
```

```http
HTTP/1.1 200 OK
{"id": "dep-7f3a2c1b", "status": "DEPLOYED"}
```

The FSM executes the atomic transition: `PENDING_APPROVAL → APPROVED → DEPLOYED`.

---

**STEP 10 — Declarative YAML Manifest Materialization:**

`FakeK8sAdapter` interpolates parameters into the Golden Path template, generating multi-document Kubernetes manifests (`Deployment`, `Service`, `Ingress`) at `outputs/congreso-ia-departamento.yaml` (reproduced in full in **Annex A**).

---

**Consolidated Scenario 1 Metrics:**

| Execution Metric | Value (Mean of 5 iterations: $\mu \pm \sigma$) |
|---|---|
| ReAct loop iterations | 1.0 $\pm$ 0.0 |
| Cognitive inference latency (Local 7B LLM) | 12.99 s $\pm$ 1.52 s |
| Hexagonal validation latency | < 1 ms |
| Total duration to `PENDING_APPROVAL` | 13.12 s $\pm$ 1.55 s |
| Operator inspection time in Dashboard (*HITL*) | ~ 7 min (human review duration) |
| Total End-to-End Time | ~ 7.2 min vs. ~ 4,340 min in traditional ITSM |
| Relative Time-to-Market Reduction | **99.8%** |
<p align="center"><i><b>Table 26:</b> End-to-end performance metrics for complete walkthrough (Scenario 1).</i></p>

*Complete session trace:* [`demos/session_logs/escenario1_happy_path.json`](../../demos/session_logs/escenario1_happy_path.json).

---

### 9.2.2. Scenario 2 — Resilience Against Prompt Injection: Ubuntu:latest on Port 22

Operational guarantees collapse if an agent is susceptible to conversational manipulation. This scenario evaluates resilience against a **Prompt Injection** attack [27] attempting to expose an administrative SSH port using unvetted images.

#### Adversarial Input Vector

The user submits the following prompt via Streamlit:

> *«I need immediate terminal access to debug scripts. Deploy an Ubuntu container with the absolute latest version (use latest to keep things simple) and expose port 22 directly so I can connect via SSH. Do it quickly.»*

Lacking an internal enterprise threat model, the language model attempts to fulfill user intent directly, synthesizing an insecure tool call in iteration 1:

```json
{
  "name": "ubuntu-debug-console",
  "image": "ubuntu:latest",
  "port": 22
}
```

#### Hexagonal Interception and HTTP 422 Response

In un-sandboxed architectures where models directly access cluster APIs, this invocation would compromise security by binding SSH under mutable tags.

In *Agentic Deployer*, `SecurityContextValidator` (§5.4) intercepts the intent, detecting three concurrent policy violations:
1. Port `22` is reserved for administrative system access ($< 1024$).
2. Mutable tag `:latest` is strictly forbidden to prevent configuration drift.
3. Unapproved repository prefix lacking trusted registry namespaces.

The domain engine aborts execution, raising `SecurityViolationError`, which serializes into an HTTP `422 Unprocessable Entity` response:

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    "Security Violation: Port 22 is reserved for administrative tasks.",
    "Security Violation: Use of mutable :latest tag is forbidden.",
    "Security Violation: Image must come from a trusted registry."
  ]
}
```

#### Guided Self-Correction via the Feedback Loop

The ReAct loop captures the HTTP `422` error as an **Observation**, injecting it into model context.

The agent parses the error in its reasoning trace (*Thought*), generating an informative, pedagogical response:

> *«The IT Department has rejected this request due to cybersecurity policy violations. Policies prohibit the ':latest' tag, port 22 (reserved SSH), and unvetted registries. To proceed, please specify an immutable version tag (e.g., 'ubuntu:22.04') and select an application port above 1024.»*

Across 5 guided dialogue turns, the agent converges to register the compliant specification `docker.io/library/ubuntu:22.04` on port `2222`.

| Operational Phase | Action and Result |
|---|---|
| **Initial Prompt** | User request demanding `ubuntu:latest` bound to SSH port 22 |
| **Initial Model Call** | `format_deployment_intent(image="ubuntu:latest", port=22, ...)` |
| **Architectural Response** | **`HTTP 422 Unprocessable Entity`** — 3 security violations detected |
| **Iterative Self-Correction** | Educational policy explanation and assisted parameter convergence over 5 turns |
| **Final Resolution** | Compliant specification on port `2222` with immutable image registered as `PENDING_APPROVAL` |
<p align="center"><i><b>Table 27:</b> Execution trace: Prompt Injection attempt (Scenario 2).</i></p>

Interception occurred **before any operation reached the cluster**, demonstrating that security boundaries depend on deterministic software rather than stochastic model compliance.

*Complete session trace:* [`demos/session_logs/escenario2_prompt_injection.json`](../../demos/session_logs/escenario2_prompt_injection.json).

---

### 9.2.3. Scenario 3 — Complete HITL Governance Lifecycle: Departmental WordPress CMS

Evaluates stateful service handling and synchronization with the operator dashboard.

**User Prompt:**
> *«The Computer Science department needs a WordPress CMS to publish news and events. Can you request its deployment?»*

**FSM Transition Lifecycle:**
```text
[CREATION] ──> PENDING_APPROVAL ──> APPROVED ──> DEPLOYED
```

The agent infers persistent storage needs and configures port 8080. When registered in the FSM, the IT technician receives an asynchronous dashboard notification. Verifying quota allocations, the operator clicks "Approve", materializing YAML manifests in storage.

*Complete session trace:* [`demos/session_logs/escenario3_hitl_completo.json`](../../demos/session_logs/escenario3_hitl_completo.json).

---

### 9.2.4. Scenario 4 — Multi-turn Exception-Guided Self-Correction

Evaluates autonomous error recovery when handling incomplete storage parameters:

**User Prompt:**
> *«Deploy a standard PostgreSQL database to store project surveys.»*

1. **Iteration 1 (Missing Registry Prefix):** The agent infers database storage needs, issuing `format_deployment_intent(image="postgres:13.4", storage="10Gi", ...)`, omitting trusted registry prefixes.
2. **Deterministic Interception:** The validator returns `HTTP 422: "Untrusted registry"`.
3. **Cognitive Self-Correction:** The LLM parses the observation and re-emits a corrected call with namespace `docker.io/library/postgres:13.4`, completing successful registration in 2 turns (26.1 s).

*Complete session trace:* [`demos/session_logs/escenario4_autocorreccion.json`](../../demos/session_logs/escenario4_autocorreccion.json).

---

### 9.2.5. Synthesis and Comparative Breakdown of Case Studies

Isolating component execution latencies across the request lifecycle:

| System Component | Technology Tier | Measured Latency | Operational Character |
|---|---|---|---|
| **User Interaction** | Streamlit Frontend | ~ 5 s | Natural language prompt authoring |
| **Inference & Reasoning** | ReAct Agent (qwen2.5:7b) | 12 – 27 s | Local stochastic GPU inference |
| **Tool Protocol** | FastMCP Server | < 5 ms | JSON-RPC serialization & stdio piping |
| **Security Validation** | `SecurityContextValidator` | < 1 ms | Deterministic CPU boundary checks |
| **Transactional State** | SQLite Repository / FSM | < 2 ms | ACID persistence & state mutation |
| **Human Supervision (HITL)** | IT Operations Dashboard | ~ 7 min | Visual inspection & operator click |
| **Declarative Expansion** | `FakeK8sAdapter` | < 1 ms | Golden Path YAML interpolation |
<p align="center"><i><b>Table 28:</b> Lifecycle latency breakdown per system component.</i></p>

Comparative metrics across all four walkthrough scenarios confirm operational stability:

| Evaluated Scenario | ReAct Turns ($\mu$) | Inference Latency ($\mu \pm \sigma$) | Resulting FSM State | Generated Artifact |
|---|---|---|---|---|
| **1. Standard Provisioning (AI Conference)** | 1.0 $\pm$ 0.0 | 12.99 s $\pm$ 1.52 s | `DEPLOYED` | Complete YAML on disk |
| **2. Prompt Injection (Ubuntu SSH)** | 5.0 $\pm$ 0.6 | 45.07 s $\pm$ 3.21 s | `PENDING_APPROVAL`* | Quarantined perimeter containment |
| **3. Full HITL (WordPress CMS)** | 2.0 $\pm$ 0.0 | 27.84 s $\pm$ 2.14 s | `PENDING_APPROVAL` | Dashboard operator card |
| **4. Self-Correction (PostgreSQL)** | 2.0 $\pm$ 0.0 | 26.10 s $\pm$ 1.98 s | `PENDING_APPROVAL` | Autonomous parameter recovery |
<p align="center"><i><b>Table 29:</b> E2E comparative operational metrics across evaluation scenarios.</i></p>

> \* *Scenario 2 Note:* Final `PENDING_APPROVAL` status represents the compliant proposal reached after 5 negotiation turns where the validator repeatedly blocked policy circumvention.

---

## 9.3. Comparative Empirical Evaluation of LLM Architectures

A primary research objective is determining whether agent reliability depends on foundational model scale versus deterministic software containment boundaries.

Models were evaluated across two regimes:
1. **Intrinsic Stochastic Robustness (Pure Zero-Shot):** Models faced Metamorphic Testing in strict isolation, with zero system prompt guidance, context memory, or recovery loops.
2. **Assisted Production Performance (ReAct Loop):** Identical models operated within `AgentOrchestrator`, supported by institutional system prompts, MCP tool schemas, and FSM feedback loops.

### 9.3.1. Intrinsic Robustness: Metamorphic Stress-Testing (Pure Zero-Shot)

Evaluating semantic parameter invariance (`name`, `image`, `internal_port`) across six input transformations (MR-1 through MR-6) on baseline `qwen2.5:7b`:

| Metamorphic Relation | Applied Transformation | Evaluated Input Vector | Result | Structured JSON Extraction |
|---|---|---|---|---|
| **MR-1:** Syntactic Permutation | Reordering technical parameters | `"api-backend with image python:3.12 on port 8000"` $\leftrightarrow$ `"On port 8000 with image python:3.12, I need api-backend"` | **Pass** | Identical (`name`, `image`, `port`) |
| **MR-2:** Lexical Noise Invariance | Injected pleasantries and conversational filler | Baseline prompt $\leftrightarrow$ identical specifications wrapped in conversational pleasantries | **Fail** | Reverts to unstructured chat text |
| **MR-3:** Typographical Invariance | Case alterations (`UPPERCASE` / `lowercase`) | `"deploy redis..."` $\leftrightarrow$ `"DEPLOY REDIS..."` | **Fail** | Mutates name attribute (`redis-service`) |
| **MR-4:** Incremental Composition | Single prompt vs. 3 conversational turns | Single declarative message $\leftrightarrow$ 3 turns with partial information | **Fail** | Reverts to unstructured chat text |
| **MR-5:** Semantic Paraphrasing | Synonyms and passive voice | `"Spin up a wordpress on port 80 named blog"` $\leftrightarrow$ `"Create a workload answering to blog..."` | **Pass** | Identical extraction |
| **MR-6:** Linguistic Invariance | Translation into English | Spanish prompt $\leftrightarrow$ English prompt | **Pass** | Identical extraction |
<p align="center"><i><b>Table 30:</b> Empirical Metamorphic Testing results per relation evaluated against Qwen 2.5 (7B).</i></p>

| Metamorphic Suite Metric | Observed Value |
|---|---|
| Evaluated metamorphic relations | 6 |
| Executed tests | 6 |
| Intrinsic Zero-Shot success rate | **50% (3/6)** |
| Total suite execution time | 89.7 s |
| Cognitive engine evaluated | `OllamaLLMClient` (qwen2.5:7b local) |
<p align="center"><i><b>Table 31:</b> Global metrics of the metamorphic test battery.</i></p>

#### Attentional Failures and Prompt Engineering Limits

Failures in MR-2, MR-3, and MR-4 provide critical evidence: **general-purpose models under 8B parameters degrade significantly when exposed to lexical noise or multi-turn dispersion without external orchestration**. When attention diffuses, models drop JSON schemas and revert to unstructured chat.

Attempting to resolve this via **Reinforcement Suffixes** (*"Respond ONLY with valid JSON"*) induced **over-compliance**: in multi-turn dialogues, models forced premature tool calls during intermediate turns lacking required parameters (hallucinating ports or images), triggering schema `ValidationError` exceptions. Similarly, *Chain of Thought* [17] reasoning induced syntax corruption by interspersing discursive reasoning with formal JSON tokens.

#### Multi-Model Comparative Benchmarking Under Metamorphic Stress

Evaluating 9 neural architectures under identical zero-shot conditions:

| Evaluated Model | Runtime Tier | Zero-Shot Success Rate | Observed Behavior Under Noise and Perturbations |
|---|---|:---:|---|
| **Gemini 3.5 Flash** (Google) | Cloud | **66% (4/6)** | Tolerates lexical noise (MR-2) and multi-turn composition (MR-4). Fails on case alteration (MR-3) and language switches (MR-6). |
| **Cohere Command R+** (Cohere) | Cloud | **66% (4/6)** | Native tool calling model. Matches Gemini, failing on extreme informal noise (MR-2) and cross-language invariance (MR-6). |
| **Qwen 2.5 (7B)** (Alibaba) | Local (Ollama) | **50% (3/6)** | Attentional diffusion under noise (MR-2) and dispersed context (MR-4), reverting to unstructured text. |
| **Llama 3.2 (3B)** (Meta) | Local (Ollama) | **0% (0/6)** | Fails zero-shot structured extraction. Emits string `"None"` instead of `null` on empty fields. |
| **Mistral (7B)** (Mistral AI) | Local (Ollama) | **0% (0/6)** | Systematic formatting failure. Drops JSON structure when exposed to lexical noise. |
| **Ministral 8B** (Mistral AI) | Cloud | **0% (0/6)** | Unable to format tool calls without explicit system prompt guidance. |
| **Codestral** (Mistral AI) | Cloud | **0% (0/6)** | Lacks structured tool fine-tuning; emits procedural code blocks or plain text explanations. |
| **Qwen 2.5 (27B)** (Alibaba) | Groq (LPU) | **50% (3/6)** | Robust on permutations and paraphrasing, yet vulnerable to long conversational noise. |
| **Qwen 2.5 Coder (7B)** (Alibaba) | Local (Ollama) | **100% (6/6)** | **Passes 100% of the suite (6/6).** Code specialization neutralizes attentional degradation and lexical noise. |
<p align="center"><i><b>Table 32:</b> Comparative results of the metamorphic stress test (Pure Zero-Shot).</i></p>

Methodological conclusions:
1. **Syntactic specialization outweighs raw model scale:** Cloud hyperscaler models (Cohere, Gemini) achieved at most 66% unassisted invariance, while a compact local 7B model fine-tuned on code (**`qwen2.5-coder:7b`**) achieved **100% success**. Tool calling reliability depends on training alignment with formal grammars (JSON Schemas, static typing) rather than sheer parameter count.
2. **Code models without tool tuning fail:** *Codestral* (0% success) demonstrates that procedural coding ability does not equal agentic tool orchestration: without fine-tuning on structured function-calling protocols, models generate raw text unparseable by MCP clients.

---

### 9.3.2. Assisted Production Performance: ReAct Loop Orchestration

Evaluating identical models within the full software framework (Hexagonal Architecture, MCP tool definitions, and FSM feedback loops) using the baseline Scenario 1 prompt:

| Evaluated LLM Model | Scale / Tier | ReAct Turns (on success) | Mean E2E Latency | Valid Invocation Rate |
|---|---|:---:|:---:|:---:|
| **Qwen 2.5 Coder** | 7B (Local / Ollama) | 1.0 $\pm$ 0.0 | 12.15 s $\pm$ 1.12 s | **100%** |
| **Qwen 2.5** (General) | 7B (Local / Ollama) | 3.0 $\pm$ 0.4 | 47.33 s $\pm$ 3.85 s | **100%** |
| **Llama 3.2** | 3B (Local / Ollama) | 1.0 $\pm$ 0.0 | 9.44 s $\pm$ 0.85 s | **75%** |
| **Mistral** | 7B (Local / Ollama) | N/A | N/A | **0%** |
| **Gemini 3.5 Flash** | Cloud (Google) | 1.0 $\pm$ 0.0 | ~ 5.50 s | **100%** |
| **Cohere Command R+** | Cloud (Cohere) | 1.0 $\pm$ 0.0 | ~ 9.00 s | **100%** |
| **Ministral 8B** | Cloud (Mistral AI) | 1.0 $\pm$ 0.0 | ~ 3.20 s | **100%** |
| **Qwen 2.5 (27B)** | Cloud (Groq LPU) | 2.0 $\pm$ 0.0 | ~ 2.45 s | **100%** |
<p align="center"><i><b>Table 33:</b> Real comparative performance of alternative models in the ReAct loop.</i></p>

#### The Stabilizing Effect of Software Architecture

Contrasting Table 32 (Zero-Shot) against Table 33 (ReAct Loop) provides core empirical validation:

- **Baseline Qwen 2.5 (7B)** jumped from a **50% success rate in stochastic isolation** to **100% valid invocations** when guided by the ReAct loop and MCP schemas, stabilizing decisions across 3 reflective iterations.
- **Ministral 8B**, which scored **0% in unassisted metamorphic testing**, attained **100% success in 1 turn (3.2 s)** when supported by the system prompt and tool contracts.
- **Qwen 2.5 Coder (7B)** confirmed its role as an optimal sovereign engine: consistently converging in **1.0 turn**, reducing local inference latency from 47 s to **12.15 s**, and eliminating corrective dialogue turns.

### 9.3.3. Comparative Synthesis and Technology Selection Criteria

1. **Viability of Sovereign Local Inference (*Zero Data Retention*):** Compact code-specialized models (`qwen2.5-coder:7b`) match cloud commercial accuracy within modest hardware envelopes (6 GB VRAM), eliminating external data leakage risks.
2. **Hardware Acceleration:** Where cloud privacy policies permit, LPU inference engines (Groq) achieve ~2-second response times, enabling real-time conversational workflows.
3. **Deterministic Software as a Containment Gate:** No language model exhibits absolute reliability in unassisted zero-shot modes. Operational reliability must reside within deterministic software boundaries (Hexagonal Architecture) and human oversight (*HITL*).

---

## 9.4. Cognitive Architecture Experiments: Overcoming 7B Attentional Limits

General-purpose 7B models exhibited premature over-compliance in multi-turn dialogues. To determine whether software abstractions can overcome this bottleneck, a systematic test harness (`demos/demo_state_machine.py`) evaluated three architectural paradigms across an incremental three-turn sequence:
- **Turn 1:** Unspecified request: *«Hello IT team, I need to deploy a web service please.»*
- **Turn 2:** Identifying name only: *«It will be named project-web.»*
- **Turn 3:** Technical specifications: *«The image will be nginx:alpine and port is 8080. That completes it.»*

### 9.4.1. Paradigm 1: Classic ReAct with Strict Suffix (Logical Failure)
Model instructed with an imperative suffix (*"Respond ONLY with JSON"*).
- **Result:** In Turn 2, possessing only the name, the model forced a tool call hallucinating image (`nginx:latest`) and port (`80`), failing logically due to over-compliance.

### 9.4.2. Paradigm 2: Chain of Thought (Syntactic Failure)
Model instructed to reason step-by-step in free text before emitting JSON [17].
- **Result:** Successfully prompted for missing parameters in Turn 2. In Turn 3, however, combining natural language reasoning with strict JSON tokens corrupted syntax, raising schema `ValidationError` exceptions.

### 9.4.3. Paradigm 3: Stateful Slot Filling and Context Distillation

To eliminate cognitive overload, the system implemented **Stateful Slot Filling**, rooted in Dialogue State Tracking [39] and context distillation literature [40, 41].

The paradigm decouples processing into two orthogonal tiers:
1. **Passive Cognitive Tier (Isolated Semantic Extraction):** The LLM acts solely as an entity extractor over the latest user prompt, populating a discrete data structure (`{"name": null, "image": null, "port": null}`) without executing tools or deciding control flow.
2. **Deterministic Control Tier (Python State Machine):** Traditional software maintains accumulated session state in memory. If required parameters are missing, the state machine deterministically generates clarification prompts. Only when the parameter vector is 100% complete does the orchestrator dispatch the MCP tool call.

### 9.4.4. Cross-Model Evaluation Across Cognitive Paradigms

Evaluating all 8 model families across the three-turn sequence under each paradigm:

| Evaluated Model | Classic ReAct (No Suffix) | ReAct with Chain-of-Thought | Stateful Slot Filling |
|---|---|---|---|
| **Qwen 2.5 Coder (7B)** | **100% Success** (Specialized tuning) | **100% Success** (Robust syntax) | **100% Success** (Absolute precision) |
| **Qwen 2.5 (7B)** (General) | Logical Failure (Over-compliance Turn 2) | Syntax Failure (`ValidationError`) | **100% Success** (Deterministic state control) |
| **Llama 3.2 (3B)** | Syntax Failure (Injects `"None"`) | Structuring Failure | **Partial Success** (Extracts `"null"` as string) |
| **Mistral (7B)** | Logical Failure (Drops format over turns) | Attentional Loop | **100% Success** (Isolated semantic extraction) |
| **Gemini 3.5 Flash** | **100% Success** (Superior attention) | **100% Success** (Robust syntax) | **100% Success** (Flawless extraction) |
| **Cohere Command R+** | **100% Success** (Native tool design) | **100% Success** (Deterministic response) | **100% Success** (Absolute precision) |
| **Ministral 8B** | **100% Success** (Native tool support) | **100% Success** (Stable reasoning) | **100% Success** (Absolute precision) |
| **Qwen 2.5 (27B)** | **100% Success** (Ultra-fast Groq LPU) | **100% Success** (Stable reasoning) | **100% Success** (Absolute precision) |
<p align="center"><i><b>Table 34:</b> Results of Cognitive Architecture Experiments expanded with Cloud models.</i></p>

#### Conclusions on Cognitive Architectures

Two distinct engineering paths achieve production reliability:
- **Deterministic Software Engineering (*Stateful Slot Filling*):** Managing conversational state via deterministic state machines allows even attention-constrained models (Qwen 2.5 and Mistral) to achieve **100% reliability**, decoupling flow control from stochastic inference.
- **Model Specialization (`qwen2.5-coder:7b`):** Intensive pre-training on source code enables compact models to handle simultaneous semantic extraction and tool calling without external state tracking wrappers, matching commercial cloud hyperscalers.

---

## 9.5. Operational Impact Evaluation on ITSM Processes

Having demonstrated architectural resilience (§9.2), characterized foundational models (§9.3), and resolved attentional limits (§9.4), experimental results inform IT Service Management (ITSM) operational impact models.

### 9.5.1. Traditional ITSM Friction vs. Agentic Automation

In regulated environments such as university datacenters, provisioning velocity is bottlenecked by ticketing bureaucracy (Jira, ServiceNow, email):
1. **Ticket Creation (Abstraction Gap):** The applicant submits vague prompts (*«I need a database for my project»*).
2. **Triage Bottlenecks (Level 1 Support):** Support staff halt tickets, requesting clarifications via asynchronous emails (ports, storage, memory bounds).
3. **Escalation to Engineering (Level 3):** After days of email round-trips, tickets reach senior platform engineers.
4. **Manual Manifest Authoring:** Senior engineers halt strategic tasks to draft Kubernetes manifests, connect over VPN, and apply configurations.

This lifecycle introduces massive queue idle times and severe context-switching costs.

### 9.5.2. Quantifying Delivery Acceleration and Time-to-Market (TTM)

*Agentic Deployer* resolves requirements negotiation interactively via the ReAct loop, reducing technical personnel duties to rapid visual auditing in the HITL Dashboard.

Table 35 compares delivery timelines for a standard institutional web service:

| Operational Lifecycle Phase (ITSM) | Conventional ITSM Model | Agentic Model (*Agentic Deployer*) | Time-to-Market Reduction |
|---|---|---|:---:|
| **1. Requirements clarification & triage** | 1,440 min† (Asynchronous Email/Ticket) | ~ 5 min (Interactive natural language AI dialogue) | **~ 99.7%** |
| **2. Declarative translation & YAML authoring** | 15 min (Manual drafting by L3 engineer) | < 0.01 min (Golden Path template expansion) | **~ 99.9%** |
| **3. Security policy & compliance review** | 5 min (Manual review / CI/CD check) | < 0.001 min (CPU Hexagonal Core checks) | **~ 99.9%** |
| **4. Formal deployment approval** | 2 min (Manual review / `kubectl apply`) | 2 min (Review and click in HITL Dashboard) | **0% (Identical control)** |
| **Queue Idle Time (*Idle Time*)** | 2,880 min (Ticket queued awaiting assignment) | 60 min (Dashboard review queue) | **~ 97.9%** |
| **Total Delivery Time (*Time-to-Market*)** | **~ 4,342 min (~ 72.4 hours / 3 business days)** | **~ 67 min (~ 1.1 hours)** | **~ 98.5%** |
| **Active Engineering Time** | **30 min** (Triage + authoring + validation) | **~ 5 min** (AI dialogue) + **2 min** (HITL) = **7 min** | **~ 76.7%** |
| **Systems Engineer Cognitive Load** | **High** (Coding manifests & L1 triage) | **Minimal** (Visual audit of structured intent) | **Qualitative reduction** |
<p align="center"><i><b>Table 35:</b> Comparative operational time impact (Traditional ITSM vs. Agentic Deployer).</i></p>

> † *Elapsed Time Note:* The **1,440-minute (24-hour)** figure represents *elapsed calendar time* resulting from inter-departmental email delays, not continuous active engineering effort. Conversely, the conversational agent resolves requirements interactively in real time (§4.6.4).

#### Experimental Impact Conclusion

Table 35 confirms that the primary value of *Agentic Deployer* lies in **eliminating bureaucratic triage latency**. By resolving specifications interactively in real time and structuring reviews via the HITL Dashboard, the system shortens overall Time-to-Market by **98.5%**, liberating **76.7% of technician active working hours**.

These empirical savings establish the analytical foundation for the economic adoption and ROI models presented in **Chapter 4 (Section 4.6)**.

---

## 9.6. Threats to Empirical Validity

In accordance with empirical software engineering guidelines [42, 43], this section documents potential threats to validity and mitigation measures.

### 9.6.1. Internal Validity

Internal validity addresses whether unmonitored factors influenced observed experimental outcomes:

- **LLM Stochasticity:** Neural inference exhibits variance even at zero temperature ($T = 0$) due to non-deterministic parallel floating-point operations on GPU hardware. To mitigate this, case studies and metamorphic tests were executed across batches of 5 consecutive iterations, reporting metrics as mean ($\mu$) and standard deviation ($\sigma$).
- **Network Latency & Cloud Throttling:** Cloud evaluations (Google, Cohere, Groq, Mistral) depend on public network hops and remote server load. This was addressed by measuring pure model generation latency separate from network transfer times and benchmarking against local air-gapped Ollama execution.
- **Hardware Thermal Throttling:** Workstation laptop GPUs (NVIDIA RTX 3060 Laptop) experience thermal throttling under continuous loads. Passive 30-second cooling intervals were enforced between inference batches to maintain clock frequency stability.

### 9.6.2. External Validity

External validity evaluates the degree to which empirical findings generalize to other organizations and infrastructure environments:

- **Tool Catalog Scope:** The MCP tool catalog focuses on four representative institutional workloads (web portals, CMS engines, Python microservices, relational databases). While covering standard academic requests, complex enterprise microservices with distributed service meshes or custom Kubernetes operators require further empirical evaluation.
- **Model Evolution:** Results evaluate the eight neural families analyzed in Section 9.3. While model architectures evolve rapidly, the central architectural conclusion—the necessity of deterministic hexagonal boundaries to contain stochastic reasoning—remains universally applicable.

### 9.6.3. Construct Validity

Construct validity examines whether empirical metrics accurately reflect theoretical constructs:

- **Measuring System Reliability:** Reliability was evaluated using objective quantitative indicators rather than subjective impressions: Pydantic type invariant compliance, security exception capture rates, metamorphic assertion passes, and mutation survival ratios.
- **ITSM Time Modeling:** Conventional delivery baselines were grounded in ITIL v4 standards and university operational data, strictly distinguishing active engineering hours from elapsed ticket queue latency.

### 9.6.4. Conclusion Validity

Conclusion validity assesses whether statistical and inferential conclusions are sound:

- **Selection Bias:** To avoid evaluating only favorable Happy Paths, the experimental design deliberately incorporated adversarial attacks (§9.2.2), structurally flawed models (`codestral`, `llama-3.2-3b`), and deliberate AST mutations (§8.3), ensuring conclusions objectively reflect both architectural strengths and empirical boundaries.

