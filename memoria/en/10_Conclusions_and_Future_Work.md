# Chapter 10. Conclusions, Limitations, and Future Work

Integrating Large Language Models (LLMs) into infrastructure operations automation (*Platform Engineering*) demands strict architectural safeguards to mitigate their inherent stochastic nature. This Master's Thesis has addressed this challenge through the design, implementation, and empirical evaluation of a decoupled architecture engineered to guarantee deterministic invariant validation, transactional traceability, and human-in-the-loop governance across the service provisioning lifecycle.

Below, we detail the primary conclusions derived from empirical system validation, the operational limitations inherent in the prototype's scope, and the strategic roadmap for future evolution.

---

## 10.1. Conclusions

The conceptualization, development, and empirical evaluation of *Agentic Deployer* validate the technical feasibility of intermediating natural language infrastructure requests through intelligent agents, provided their execution remains strictly confined within a deterministic architectural boundary. The core conclusions of this research are organized around the following dimensions:

### 10.1.1. Objectives Compliance and Traceability Matrix

To formally certify the correspondence between initial technical commitments and delivered outcomes, Table 36 synthesizes the bijective traceability matrix connecting the five specific objectives (*O*₁ through *O*₅) established in Section 1.3.2, associated functional and non-functional requirements, implemented software artifacts, and empirical validation evidence:

| Specific Objective | Linked Requirements | Artifacts & Implementation | Empirical Validation Evidence | Completion Degree |
|---|---|---|---|:---:|
| ***O*₁: Decoupled Hexagonal Core (*Ports & Adapters*)** | NFR-02, NFR-04 | Immutable Pydantic domain, pure use cases, and `SecurityContextValidator` (Chap. 5, §5.1–5.4). | Isolation verified against non-compliant parameter injection (§9.2.2) and 100% unit test coverage. | **100% (Completed)** |
| ***O*₂: Standardized Tool Server (MCP)** | FR-03, NFR-01 | Autonomous FastMCP server over `stdio` exposing the institutional IT catalog (Chap. 6, §6.1). | External interoperability certification via official **MCP Inspector** and decoupling from proprietary APIs (§9.1, §10.1.3). | **100% (Completed)** |
| ***O*₃: ReAct Agent Orchestrator with Feedback Loop** | FR-02, NFR-04 | Cognitive orchestrator `AgentOrchestrator` with ReAct loop and *Stateful Slot Filling* pattern (Chap. 6, §6.2). | Convergence in 1.0 iterations with `qwen2.5-coder:7b` (§9.3) and resolution of attentional limits with 100% success (§9.4). | **100% (Completed)** |
| ***O*₄: Declarative Golden Paths** | FR-01, FR-03 | Pre-audited Kubernetes templates (`Deployment`, `Service`, `Ingress`) and `FakeK8sAdapter` (Chap. 5, §5.4.3; Annex A). | Deterministic, hallucination-free generation across 4 practical walkthroughs (§9.2) and syntactic manifest validation. | **100% (Completed)** |
| ***O*₅: Human-In-The-Loop (HITL) Security Governance** | FR-04, FR-05, NFR-03 | Finite State Machine (FSM), ACID SQLite persistence, and Streamlit operational console (Chap. 7, §7.1–7.3). | Zero unauthorized executions; 98.5% reduction in Time-To-Market and 76.7% reduction in active technician time (§9.5). | **100% (Completed)** |
<p align="center"><i><b>Table 36:</b> Traceability matrix and degree of fulfillment of specific project objectives.</i></p>

### 10.1.2. Synthesis of Tangible Engineering Contributions

As a result of system development and empirical evaluation, this Master's Thesis contributes the following methodological frameworks and tangible engineering assets:

1. **Deterministic Perimeter Architecture for Infrastructure Agents:** Specification and validation of a hexagonal architectural pattern that strictly decouples probabilistic language model reasoning from physical execution layers, confining stochastic behavior via domain invariant validators.
2. **Autonomous, Interoperable FastMCP Server for IT Operations:** A reference implementation conforming to the open *Model Context Protocol* (MCP) standard exposing university datacenter operations (`deploy_congress_web`, `deploy_department_cms`, `deploy_python_app`, `deploy_static_website`, `deploy_database`), externally certified via the official *MCP Inspector*.
3. **Conversational State Decoupling Pattern (*Stateful Slot Filling*):** Empirical demonstration of an engineering technique that isolates point-in-time semantic extraction from transactional dialogue tracking via a deterministic FSM, elevating the multi-turn reliability of local 7B-parameter models from 0% to 100%.
4. **Hybrid Quality Assurance Framework for AI Systems:** A holistic verification methodology that transcends traditional code coverage through the synergistic combination of Property-Based Testing (Hypothesis), Metamorphic Testing, and Mutation Testing (Mutmut), surfacing logical vulnerabilities invisible to standard unit test suites.
5. **Multi-Model Empirical Benchmark and Reproducible Evaluation:** A systematic testbed and experimental trace catalog across 8 neural model families (local via Ollama, LPUs via Groq, and commercial cloud APIs), establishing empirical guidelines for sovereign agent adoption (*Zero Data Retention*) within public sector institutions.

### 10.1.3. Overcoming Vendor Lock-In through MCP

Adopting the **Model Context Protocol (MCP)** [13] to isolate the IT Service operations catalog formally decouples tool specifications from proprietary AI vendor APIs. We empirically verified the feasibility of structuring an interoperable, modular operational capability suite. The FastMCP server dynamically generates contracts via static type introspection, ensuring compatibility with any cognitive engine conforming to the open standard.

This decoupling was empirically verified along two complementary dimensions:
1. **Transparent Inference Engine Substitution:** Implementing the native `OllamaLLMClient` (Section 6.2.1) enabled swapping commercial OpenAI models for open-weight models executed locally (`qwen2.5:7b`), requiring zero modifications to hexagonal domain logic or MCP tool definitions.
2. **Certified External Interoperability:** Protocol compliance was formally evaluated using the official protocol inspection utility (**MCP Inspector**). Operating independently of the Streamlit interface, the tool discovered (`tools/list`) and executed catalog operations over standard `stdio`, confirming that the server serves as a reusable asset for external audit tooling and third-party orchestration agents.

### 10.1.4. Hexagonal Architecture as a Deterministic Containment Perimeter

A central finding of this research is the efficacy demonstrated by Hexagonal Architecture (*Ports and Adapters*) [19] in confining and neutralizing LLM hallucinations and stochastic variations. By requiring all inference proposals to satisfy the contracts of an immutable, strongly-typed domain model (`Pydantic`) evaluated by a deterministic validator (`SecurityContextValidator`), model stochasticity is intercepted prior to interacting with physical infrastructure adapters.

The system methodologically assumes LLM fallibility: it intercepts non-compliant proposals and feeds structured exceptions back into the conversational context (*Feedback Loop*), facilitating guided self-correction. The adversarial instruction injection case study documented in Section 9.2.2 demonstrates that requests violating security baselines (such as unpinned `ubuntu:latest` images or privileged port `22` allocations) are blocked at the application core, returning `HTTP 422 Unprocessable Entity` status codes and steering convergence toward compliant configurations over successive turns without compromising the physical environment.

### 10.1.5. The Necessity of the Human-In-The-Loop (HITL) Pattern in Critical Infrastructure

In contrast to paradigms advocating full algorithmic autonomy (Level 5), this research concludes that human supervision remains an indispensable safeguard for compliance, legal liability, and IT governance in institutional environments. Implementing the Finite State Machine (FSM) and asynchronous control console proved that the HITL pattern introduces minimal operational friction while establishing an effective segregation of duties:
- The language model handles intent extraction and technical parameter negotiation in natural language.
- The IT specialist audits, verifies, and formally authorizes deployment orders in the operations console.
- The requesting researcher tracks deployment lifecycles in real time via the conversational interface.

The empirical delivery time reductions demonstrated—reducing active engineering overhead from 30 minutes to 7 minutes (a 76.7% reduction) and total delivery time (*Time-To-Market*) from ~4,342 minutes under conventional ticketing to ~67 minutes in the assisted flow (a 98.5% reduction, Section 9.5)—confirm that human governance and operational efficiency converge when cognitive automation absorbs administrative triage.

### 10.1.6. Redefining Quality Assurance (QA) Against the Coverage Fallacy

Conventional QA methodologies reliant solely on deterministic unit tests are insufficient for certifying systems containing probabilistic components. Integrating Property-Based Testing (Hypothesis) [37] and Metamorphic Testing [38] verified that the agent maintains semantic invariance and structured schema compliance across linguistic, syntactic, and typographical transformations.

Furthermore, Mutation Testing (Mutmut) revealed that high line coverage does not imply logical resilience. Initial analysis uncovered **30 surviving mutants** within resource parsing functions (`_parse_cpu`, `_parse_ram`), despite reporting 100% line coverage. This finding guided the systematic refactoring of parsing algorithms and invariant assertions, substantiating mutation analysis as an indispensable requirement for auditing AI-driven infrastructure platforms.

### 10.1.7. Feasibility and Stabilization of Small-Scale (7B) Models

Local inference experiments showed that generalist 7B-parameter models exhibit attentional degradation when managing multi-turn workflows through purely reactive architectures, demonstrating schema adherence failures as dialogue histories expand.

However, incorporating the **Stateful Slot Filling** architectural pattern (Section 9.4.3)—wherein the language model serves strictly as an isolated semantic extractor per turn while a deterministic Python state machine tracks accumulated intent vectors—**enables these same models to reach 100% reliability without parameter expansion or fine-tuning overhead**. This architectural segregation between semantic extraction and transactional state tracking confirms the feasibility of deploying agentic systems on standard, modest hardware.

### 10.1.8. Cross-Cutting Findings from Multi-Model Evaluation

The systematic evaluation across 9 heterogeneous neural architectures (local quantized via Ollama, LPUs via Groq, and commercial cloud APIs) yields four transferrable engineering principles:

1. **Domain Alignment Prevails Over Parameter Scale:** Structured tool-calling efficacy depends on alignment with formal grammars and strict typing rather than raw parameter volume. Models with high general algorithmic capability (e.g., `codestral-latest`) scored 0% in zero-shot tool invocation, defaulting to free-form text. Conversely, compact code-specialized models (`qwen2.5-coder:7b`) achieved 100% metamorphic success in local sovereign mode.
2. **Complementarity of Probabilistic Inference and Deterministic Control:** No generalist language model operating in isolation exceeded 66% semantic invariance against lexical noise and language-switching. Integrated into the ReAct loop bounded by Hexagonal Architecture and the FSM, success rates converged to 100%. Agentic resilience resides in the surrounding deterministic software architecture, not in model infallibility.
3. **Technological Insulation Against Obsolescence:** Protocol abstraction via MCP and the `OpenAILLMClient` adapter ensures that organizations can deploy sovereign, zero-cost local engines initially and progressively adopt specialized accelerators or frontier cloud models without modifying domain logic or tool contracts.
4. **Data Sovereignty and Institutional Governance:** While cloud providers offer low inference latencies, adoption introduces external vendor dependencies, rate-limiting constraints (`HTTP 429 Rate Limit Exceeded`), and sensitive metadata exposure. For public administrations with strict regulatory constraints, local deployments of specialized models under Zero Data Retention principles represent a technically sound and economically sustainable path.

### 10.1.9. Comparative Synthesis of Evaluated Models

Consolidating experimental results from Chapter 9 (**Tables 30, 31, and 32** for zero-shot metamorphic evaluations, and **Tables 33 and 34** for ReAct orchestration and cognitive architecture), **Table 37** classifies the evaluated cognitive engines by institutional agentic suitability:

| Engine / Model | Execution Environment | Suitability Rating | Observed Behavior & Empirical Evidence |
|---|---|---|---|
| **`qwen2.5-coder:7b`** (Alibaba / Ollama) | Local | **High (Sovereign - Code)** | Maximum reliability. 100% metamorphic pass rate (*Table 32*) and convergence in 1.0 iterations (*Table 33*). Code-specific fine-tuning overcomes hardware constraints. |
| **`qwen2.5:7b`** (Alibaba / Ollama) | Local | **Medium-High (Sovereign - Generalist)** | Moderate standalone reliability (50% metamorphic, *Table 32*). Requires external state machine support to avoid multi-turn context dilution. |
| **`gemini-3.5-flash`** (Google Cloud) | Cloud | **High (Commercial)** | Most consistent cloud model in structured extraction (66% metamorphic, *Table 32*). Subject to external quotas and cloud commercial retention policies. |
| **`command-r-plus`** (Cohere Cloud) | Cloud | **High (Commercial)** | Explicitly optimized for tool calling (66% metamorphic, *Table 32*); shows susceptibility to extreme colloquial phrasing. |
| **`ministral-8b-latest`** (Mistral AI) | Cloud | **Medium (Commercial)** | Optimal performance under FSM guidance (*Table 33*), but vulnerable in unassisted zero-shot extraction (0% metamorphic, *Table 32*). |
| **`codestral-latest`** (Mistral AI) | Cloud | **Unsuitable for Tool Calling** | Unsuitable for orchestration: lacks fine-tuning for structured JSON Schema invocation, emitting unstructured explanatory text (0% metamorphic, *Table 32*). |
<p align="center"><i><b>Table 37:</b> Cognitive engine ranking and empirical justification for institutional agentic orchestration.</i></p>

**Key Comparative Insights:**
1. **Syntactic specialization outweighs scale:** Specialization in formal grammars and interface contracts is more critical than parameter scale, enabling reliable institutional deployments under **Zero Data Retention** on commodity hardware.
2. **Invariance and deterministic containment:** The failure of commercial models to achieve 100% standalone invariance under linguistic variation confirms that production reliability must rest upon traditional deterministic software defenses.
3. **Adoption horizons for commercial platforms:** Frontier models billed by token consumption (such as **GPT-4o [44]** or **Claude 3.5 Sonnet [45]**) feature vendor optimizations for agentic workflows and MCP, offering viable alternatives in environments where data governance policies permit external cloud processing.

---

## 10.2. Prototype Limitations

In adherence to scientific rigor and transparency, the following technical limitations of the research prototype delineate operational boundaries relative to a mature enterprise deployment:

### 10.2.1. Simulated Infrastructure Adapter (`FakeK8sAdapter`)

Declarative configuration manifests are rendered and persisted to local disk rather than dispatched interactively against a live Kubernetes API. While the syntactic validity of generated YAML is certified (Annex A), this simulation omits physical cluster feedback:
- **Dynamic Quota Validation:** The Kubernetes Control Plane may reject creation requests if namespaces exceed concurrent compute quotas.
- **Concurrency and Naming Collisions:** Duplicate service identifiers trigger `HTTP 409 Conflict` errors on API servers, unmodeled in local simulation.
- **External Controller Dependencies:** Automated TLS certificates via `cert-manager` require active cluster operators; without them, `Ingress` resources remain pending indefinitely.

### 10.2.2. Absence of Perimeter Authentication and Authorization

Backend endpoints (`/mcp/intent`, `/hitl/approve`, `/hitl/status`) **lack cryptographic authentication and authorization** (OAuth2, OpenID Connect, JWT, or API keys). In this research prototype, any process with local network access can inspect or approve intents. In production, this represents a vulnerability requiring integration with enterprise directories (LDAP/Keycloak) and Role-Based Access Control (RBAC).

### 10.2.3. Resilience Against Complex Prompt Injection Vectors

While direct instruction injections are intercepted by deterministic validation (Section 9.2.2), the prototype does not incorporate defenses against advanced adversarial vectors:
- **Indirect Prompt Injection:** Adversarial payloads embedded in external documentation consumed dynamically by the agent.
- **Context Jailbreaking:** Multi-turn conversational drift designed to dilute system prompt constraints.

### 10.2.4. Constrained Tool Catalog and Lifecycle Scope

The MCP server implements tools focused on initial provisioning (`deploy_congress_web`, `deploy_department_cms`, `deploy_python_app`, `deploy_static_website`, `deploy_database`, `get_deployment_status`, and `delete_university_service`). Day-2 operational capabilities—such as dynamic pod autoscaling, secret management, certificate rotation, and real-time log streaming—remain outside the current prototype scope.

### 10.2.5. Concurrency and Scalability in the Application Layer

FastAPI runs synchronously across a single ASGI Uvicorn process. Under concurrent multi-user load, thread exhaustion bottlenecks may emerge. While SQLite addresses local race conditions via file-level locking, enterprise deployments require distributed relational database systems.

### 10.2.6. Prior Immutability in the Human Supervision (HITL) Channel

The HITL operations console enforces binary operator actions (Approve or Reject). If an intent contains reasonable parameters with slightly oversized memory requests, operators cannot modify fields in-flight (*Pre-Deployment Mutability*), forcing full rejection and dialogue restart.

### 10.2.7. Bounded Usability Evaluation and End-User Validation

Operational efficiency metrics (Chapter 9) were captured in controlled experimental environments. Formal usability evaluations (e.g., System Usability Scale, SUS) involving non-developer administrative and academic staff have not yet been conducted, leaving non-technical linguistic barriers unquantified.

### 10.2.8. Hardware Constraints and Quantization Limitations

Local evaluations were executed on a workstation with 6 GB VRAM, restricting models to <8B parameters quantized to 4 bits (Q4_K_M). While `qwen2.5-coder:7b` proved stable, evaluating larger architectures (14B or 32B parameters) on higher-memory compute infrastructure would establish definitive upper bounds on latency and context retention.

### 10.2.9. Linguistic Dissonance in Structured Reasoning Tasks

Evaluations enforced Spanish-language interactions across prompts, user inputs, and tool metadata. Because foundational models are trained predominantly on English corpora, syntactic adherence and formal schema compliance degrade in secondary languages. Certain formatting inconsistencies in generalist 7B models stem from this representational disparity.

---

## 10.3. Future Work

To address these limitations and transition *Agentic Deployer* toward institutional production in university datacenters, the following technical roadmap defines short- and medium-term priorities:

### 10.3.1. Evolution Toward Institutional Production (Short Term)

The immediate roadmap equips the platform with live execution capabilities, concurrency, and perimeter security:

- **Physical Kubernetes Adapter (`RealK8sAdapter`) and Persistent Storage:** Replace simulated disk serialization with a live adapter connected to the Kubernetes API via `kubernetes-client`, executing authenticated API calls upon HITL approval. Incorporate declarative `PersistentVolumeClaim` (PVC) management to support production databases with physical disk persistence.
- **Distributed Relational Persistence (PostgreSQL):** Migrate the embedded SQLite database to a client-server PostgreSQL engine. The hexagonal *Repository* abstraction isolates this transition from domain logic, enabling high-availability backend deployments across multiple Uvicorn/Gunicorn workers.
- **Role-Based Access Control (RBAC) and Federated Authentication:** Integrate OAuth2 and OpenID Connect with JWT tokens, federated via enterprise identity providers (Keycloak, LDAP), distinguishing researcher request privileges from authorized IT operator approval rights.
- **In-Flight Intent Editing in HITL:** Allow operators to adjust intent parameters (such as CPU allocations or port assignments) directly within the dashboard prior to authorization, eliminating unnecessary rejection cycles.

### 10.3.2. Platform Integration and Declarative Governance (Medium Term)

The medium-term roadmap focuses on integration into GitOps workflows and declarative platform engineering ecosystems:

- **GitOps Paradigm Adoption (ArgoCD / Flux):** Commit generated Kubernetes manifests to version-controlled Git repositories rather than applying them directly (*Push Model*), leveraging declarative reconciliation controllers (ArgoCD, Flux) to ensure immutable audit trails and disaster recovery.
- **Real-Time Observability (Prometheus & Grafana):** Equip the agent with telemetry tools to query live cluster metrics and quota reservations prior to drafting deployment proposals, providing contextual decision support.
- **Policy-as-Code Governance:** Externalize security validation rules into declarative policy engines such as Open Policy Agent (OPA) [46] or Kyverno [47], enabling security teams to update compliance policies independently of backend deployment lifecycles.
- **Consolidated Stateful Slot Filling:** Solidify the decoupled entity extraction architecture across all workflow categories, permanently eliminating conversational history accumulation and eliminating context dilution risks.

