# Chapter 1. Introduction

## 1.1. Context and Motivation

Over the past decade, the software engineering and systems administration ecosystem has undergone a profound structural shift. The demand for accelerating time-to-market while ensuring higher scalability and resilience has driven a transition from monolithic architectures hosted on physical bare-metal servers toward distributed microservices architectures [1] and cloud computing environments [2]. At the core of this transition lies application containerization—popularized by technologies such as Docker [3] and open standards such as the Open Container Initiative (OCI) [4]—and, critically, the orchestration of containerized workloads through industry-standard platforms such as Kubernetes [5] and enterprise distributions such as Red Hat OpenShift and OKD.

While Kubernetes has addressed fundamental challenges regarding high availability, horizontal auto-scaling, and self-healing fault management, its adoption has introduced considerable operational complexity. The Infrastructure as Code (IaC) paradigm and declarative resource management require engineers to interact with the platform through extensive and complex YAML or JSON manifests. These documents describe not only the computational workloads themselves (*Deployments* or *Pods*), but also demand the meticulous specification of network topologies (*Services*, *Ingress* / *Routes*), access control policies (*RBAC*), hardware resource allocations and limits (CPU, memory), and persistent volume claims.

Historically, this landscape has created a substantial barrier to entry for application developers, researchers, and academic staff. These stakeholders frequently possess deep domain expertise regarding application business logic, yet lack specialized systems operations backgrounds. Although the *DevOps* movement aimed to bridge the operational gap between development (Dev) and operations (Ops) teams through shared responsibility [6], in practice it has frequently resulted in excessive cognitive overhead for personnel outside platform administration. Expecting university researchers to master the declarative nuances of Kubernetes merely to publish a departmental web service introduces disproportionate operational friction.

To address this friction, the industry has turned toward **Platform Engineering** [7]. This discipline advocates the construction of Internal Developer Platforms (IDPs), designed to provide self-service portals and "Golden Paths" [8]. A *Golden Path* is a standardized, institutionally supported route that encapsulates underlying infrastructure complexities: the user specifies high-level application requirements, and the platform automatically generates compliant technical configurations in alignment with corporate security policies. However, even modern IDPs typically rely on rigid graphical user interfaces, extensive forms, or Domain-Specific Languages (DSLs) that remain unintuitive for non-specialized users.

Concurrently, recent advancements in Generative Artificial Intelligence, driven by the emergence of Large Language Models (LLMs), have expanded human-computer interaction (HCI) capabilities. Transformer-based models such as GPT, Claude, or Llama, trained on billions of parameters, have demonstrated capabilities extending beyond stochastic text generation. They exhibit emergent deductive reasoning abilities, strong technical context comprehension, and the capability to translate imprecise natural language into structured code representations.

More recently, the evolution of these models has led to the development of **Autonomous AI Agents**. Leveraging function calling and iterative reasoning paradigms such as ReAct (*Reason + Act*) [9], LLMs are no longer passive query-answering engines, but cognitive controllers capable of making decisions, querying data sources, planning execution steps, and executing actions against external systems in real time.

The motivation for this Master's Thesis lies precisely at the intersection of these two paradigms: distributed infrastructure orchestration and agentic artificial intelligence. This convergence presents an opportunity to fundamentally transform how human operators interact with distributed operating environments.

The motivation of this research is to explore and demonstrate the technical feasibility of replacing complex declarative interfaces (YAML manifests) and static IDP forms with a conversational interface driven by an intelligent agent.

Under this paradigm, the system interprets user intent expressed in natural language ("I need to host a Python web API"), reasons about technical dependencies, and interactively negotiates missing requirements. Subsequently, it translates abstract intent into secure, standardized, and production-ready infrastructure definitions compatible with Kubernetes and enterprise distributions such as OpenShift. This approach lowers the technical barrier to entry for non-specialized users and streamlines software delivery lifecycles within institutional settings.

## 1.2. Problem Formulation

Despite the operational capabilities offered by conversational agents, integrating them directly into IT operations (IT Ops) workflows and critical infrastructure introduces several systemic challenges. This thesis focuses on the IT and Communications Department (*Servicio de Informática y Comunicaciones*, SIC) of a university environment as a primary case study; however, the underlying problem and proposed architecture generalize directly to other regulated sectors undergoing digital transformation.

This generalizability stems from the decoupled nature of the system design: in healthcare environments, for instance, *Golden Paths* would be configured to deploy clinical analytics workloads under strict data protection regulations (such as the Spanish *Esquema Nacional de Seguridad* (ENS) and GDPR/LOPD), where Human-in-the-Loop (HITL) oversight serves as an imperative compliance gate. Similarly, in regional public administration or financial banking environments, on-premise inference with self-hosted models ensures data sovereignty, while the immutable state machine guarantees auditability without requiring architectural modifications to the core engine.

Within the target academic institution, diverse user profiles—including research groups, teaching staff, and administrative personnel—frequently require standardized technological services. Recurring requests include deploying e-learning platforms (Moodle), content management systems (WordPress) for departmental sites, static web portals for academic conferences, and hosting lightweight microservices or APIs (typically built in Python or Node.js) resulting from applied research projects.

Manually managing these requests creates substantial operational overhead for IT engineers, who spend a significant portion of their time performing repetitive triage and baseline provisioning tasks. Conversely, granting direct cluster access to university personnel is unfeasible due to security governance constraints and specialized skills gaps. Automating service provisioning through Artificial Intelligence represents a logical progression; however, delivering an enterprise-grade solution requires addressing three fundamental technological challenges:

### 1.2.1. Lack of Standardization in Tool Orchestration

For an LLM to evolve from a passive conversational agent into an operational tool, it must interact with external systems. Historically, integrating external capabilities (API invocations, script executions, database queries) required tightly coupled, proprietary middleware specific to individual AI vendors. If an institution elected to migrate from the OpenAI API to a local open-weights model (such as Ollama) to satisfy institutional data privacy mandates, large portions of the orchestration middleware had to be rewritten.

This challenge stems from the historical absence of a standardized communication protocol between language models and external tool ecosystems. A universal, bidirectional abstraction layer is required to allow IT departments to expose deployment routines in a vendor-agnostic manner, enabling any authorized agent to discover and invoke them regardless of model provider.

### 1.2.2. Infrastructure Abstraction and Hallucination Risks

The second critical challenge arises from the generative nature of LLMs. General-purpose models trained on vast internet corpora tend to produce syntactically valid Kubernetes manifests or Docker configurations that are semantically flawed or insecure within a specific corporate environment. This hallucination risk can cause an agent to propose untrusted container images [4] (e.g., using mutable `:latest` tags vulnerable to supply-chain risks), expose unapproved network ports, or ignore restrictive CPU and memory limits (*ResourceQuotas*) enforced by platform teams to prevent noisy-neighbor contention.

Consequently, naive automation approaches that delegate the unrestricted synthesis of Infrastructure as Code scripts (IaC via OpenTofu [10] or Terraform) directly to LLMs prove excessively fragile and unpredictable in production environments [11, 12]. Addressing this challenge with sound engineering requires that the agent never generate raw infrastructure definitions from scratch. Instead, the system must invoke predefined *Golden Paths*, where the model negotiates and infers high-level parameters (application name, expected traffic volume, runtime version), while the underlying architecture deterministically enforces institutional security, networking, and sizing policies.

### 1.2.3. Security and Auditability: The Human-in-the-Loop Imperative

The most critical challenge lies in delegating operational authority. Granting a stochastic system—inherently vulnerable to prompt injection attacks or reasoning lapses—unrestricted execution privileges over production clusters introduces unacceptable security risks in critical institutional infrastructure. An erroneous or adversarial instruction could trigger accidental data loss or deplete available cluster compute resources.

Therefore, fully autonomous closed-loop provisioning (where AI plans, decides, and executes without human mediation) is unacceptable. The architecture must integrate human oversight as a mandatory verification gate in the execution pipeline. The system requires an asynchronous *Human-in-the-Loop* (HITL) model where the agent shoulders the cognitive burden of eliciting and validating technical specifications, while the authority to execute deployments (*apply* / *commit*) remains strictly in the hands of authorized human engineers. This boundary ensures end-to-end traceability and operational safety, balancing AI-driven automation with classic engineering rigor.

## 1.3. Project Objectives

To address the identified challenges, this project establishes a set of structured technical objectives.

### 1.3.1. General Objective

The central objective of this Master's Thesis is to design and implement an enterprise-grade **Internal Developer Platform (IDP)**, materialized in the **«Agentic Deployer»** middleware: an advanced orchestrator that securely translates natural language requests into declarative infrastructure configurations interoperable with OpenShift and Kubernetes environments. This middleware serves as a strict security boundary between an LLM-driven conversational agent and underlying container infrastructure, leveraging the open **Model Context Protocol (MCP)** [13] standard and structured under **Hexagonal Architecture** principles.

### 1.3.2. Specific Objectives

To achieve the general objective, five specific technical milestones have been defined and implemented:

1. **Design of a Core based on Hexagonal Architecture (*Ports and Adapters*):**  
   Construct a strongly typed, immutable domain model that isolates business rules (provisioning workflows and institutional security policies) from volatile external dependencies, such as third-party LLM client SDKs or container orchestrator APIs.
2. **Implementation of an Open Standards Tool Server (MCP):**  
   Demonstrate the architectural advantages of open protocols over proprietary vendor lock-in by implementing an Anthropic *Model Context Protocol* server. This server exposes IT infrastructure operations (service provisioning and teardown routines) such that any compliant agent can discover and invoke them using typed schemas.
3. **Integration of an Autonomous AI Agent (ReAct Paradigm):**  
   Develop a cognitive orchestrator that moves beyond static *Zero-Shot* extraction to implement a *Reason + Act* loop. The agent must reason over error responses returned by underlying infrastructure components (e.g., policy violations) and engage in an interactive self-correcting feedback dialogue with the user.
4. **Rigid Specification of Golden Paths:**  
   Prevent unconstrained manifest generation by delegating container template instantiation to the infrastructure adapter layer. Dedicated deployment patterns are designed for the most common university workloads: static web portals (Nginx), institutional content management systems (WordPress), and backend microservices (Python APIs).
5. **Security Governance via Human-in-the-Loop (HITL) Controls:**  
   Implement an asynchronous operations dashboard that intercepts every deployment intent generated by the agent, holding it in a quarantined pending state until an authorized human engineer inspects generated configurations and issues explicit deployment approval.

## 1.4. Scope and Limitations

Delineating the precise boundary of a project combining Generative AI and Cloud-Native infrastructure is essential to ensure methodological rigor. This thesis focuses on developing the central mediation component (the intelligent middleware and its orchestration engine) as an advanced Minimum Viable Product (MVP).

Accordingly, the project scope incorporates the following deliberate methodological and architectural boundaries:

1. **Cluster Abstraction via Execution Emulation:**  
   The orchestrator fully executes domain logic, security validations, human approvals, and structured declarative YAML generation for Kubernetes resources (`Deployment`, `Service`, `Ingress`). However, live network calls against physical production cluster APIs are excluded from the current baseline. Instead, an emulation adapter (`FakeK8sAdapter`) writes generated manifests to the local filesystem. This preserves Hexagonal Architecture principles, isolates the test harness from cluster network dependencies, and enables straightforward drop-in integration of a live cluster adapter in future work (Section 10.3.1).
2. **LLM Engine Agnosticism:**  
   The platform is decoupled from specific AI vendors. By implementing an *Adapter* pattern for the LLM client with two concrete implementations (`OllamaLLMClient` for local air-gapped inference with Zero Data Retention, and `OpenAILLMClient` for commercial cloud APIs), the architecture supports both isolated private networks and public cloud endpoints.
3. **Embedded Persistence (SQLite vs. Client-Server RDBMS):**  
   Transactional persistence is vital for operational infrastructure: service restarts must not compromise auditability or discard in-flight deployment requests. While early exploratory prototypes utilized an in-memory dictionary, the final platform adopts an on-disk SQLite repository [14]. This embedded database provides full ACID transactional guarantees without the operational overhead of running a dedicated client-server database cluster (such as PostgreSQL or MySQL). Foregoing a distributed persistence backend represents a deliberate scope boundary, and migrating to enterprise databases is straightforward due to the *Repository* port abstraction (Section 10.3.1).
4. **Absence of Authentication in the Prototype:**  
   HTTP endpoints operate without authentication mechanisms (JWT, OAuth2) in the current release. This design choice is acceptable within a local research prototype and is documented as a future extension in Section 10.3.1.

A comprehensive technical analysis of prototype limitations—including advanced prompt injection considerations, backend horizontal scalability, and MCP tool catalog expansion—is provided in **Section 10.2**.

## 1.5. Formal System Requirements

To ensure traceability from project objectives (Section 1.3) through implementation, requirements are formalized into Functional Requirements (FR) and Non-Functional Requirements (NFR):

**Functional Requirements (FR):**
- **FR-01 (Conversational Interface):** The system must provide a web chat interface allowing users to request infrastructure provisioning using natural language.
- **FR-02 (Agentic Orchestration):** The system must infer missing parameters, query runtime state, and iteratively resolve errors through a reasoning loop (ReAct).
- **FR-03 (MCP Tool Catalog):** The backend must expose infrastructure capabilities (Golden Paths) in a decoupled, standardized manner via the MCP protocol.
- **FR-04 (HITL Approval Dashboard):** The system must provide an independent dashboard for IT operators to review, inspect, approve, or reject deployment intents generated by the AI agent.
- **FR-05 (Asynchronous Status Polling):** Users must be able to query the real-time status of their requests (Pending, Approved, Rejected) asynchronously.

**Non-Functional Requirements (NFR):**
- **NFR-01 (Data Sovereignty):** The architecture must support local inference models (e.g., Ollama) ensuring no institutional data leaks to third-party APIs.
- **NFR-02 (Domain Isolation):** Business logic must follow Hexagonal Architecture principles, ensuring core domain invariants remain independent of AI models and persistence technologies.
- **NFR-03 (Quality and Robustness):** Core validation logic must exceed 80% unit test coverage, complemented by advanced verification techniques including Property-Based Testing and Mutation Testing.
- **NFR-04 (Operational Resilience):** The system must not mutate state under ambiguous linguistic inputs, ensuring that erroneous or incomplete model inferences fail safely without applying unverified configurations (*Fail-Safe*).

## 1.6. Structure of the Thesis

To facilitate structural traceability from theoretical foundations to software verification, this document is organized as follows:

- **Chapter 2** presents the **State of the Art**, reviewing autonomous conversational agents, the genesis and architecture of the *Model Context Protocol* (MCP), declarative Kubernetes infrastructure, Hexagonal Architecture principles, and—in Section 2.5—a comparative analysis of related works highlighting the differential positioning of *Agentic Deployer*.
- **Chapter 3** outlines the **Methodology and Technology Stack**, detailing software lifecycle practices and justifying architectural choices. It describes post-MVP consolidation phases (Phases 6 and 7), focusing on HITL hardening, Ollama local inference integration, SQLite persistence, and multi-model benchmarking.
- **Chapter 4** covers **Project Management and Viability**, detailing development constraints, sprint schedules (Gantt charts in Figures 3 and 4), effort tracking and deviation analyses, economic assessments (personnel and infrastructure costs), and institutional ROI projections.
- **Chapter 5** details **System Design and Architecture**, beginning with requirements traceability (Tables 18 and 19), presenting C4 topology models (Level 1 Context and Level 2 Containers), and examining the hexagonal core and validation contracts. Figures 11, 12, and 13 document complete end-to-end flows, including self-correction (HTTP 422) and HITL governance.
- **Chapter 6** examines the **Cognitive Agent and MCP Server**, analyzing the ReAct reasoning loop, dynamic tool discovery, and multi-provider client abstractions (`OllamaLLMClient` / `OpenAILLMClient`).
- **Chapter 7** describes the **HITL Pattern and Finite State Machine (FSM)** implementation, detailing the asynchronous human approval workflow, the status tracking endpoint, and user notification mechanics.
- **Chapter 8** presents the **Quality Assurance (QA) and Advanced Testing Plan**, covering unit testing, Property-Based Testing with Hypothesis, formal Metamorphic Testing to address the test oracle problem, and Mutation Testing with Mutmut survivor analyses.
- **Chapter 9** documents **Experimental Results and Empirical Evaluation**, structured across six sections: experimental testbed setup (§9.1), provisioning walkthroughs (§9.2), comparative multi-model benchmarking in Zero-Shot and ReAct loops (§9.3), cognitive architecture evaluations for 7B models (§9.4), quantitative ITSM Time-to-Market impact models (§9.5), and threats to validity (§9.6).
- **Chapter 10** summarizes **Conclusions, Limitations, and Future Work**, synthesizing the objective compliance matrix and engineering contributions (§10.1), detailing prototype limitations (§10.2), and outlining short- and medium-term research directions (§10.3).
- **Chapter 11** compiles the **Bibliography and References** supporting the theoretical foundation of this thesis.
- **Annex A** provides the complete Kubernetes YAML manifest (`Deployment` + `Service` + `Ingress`) generated during Scenario 1 (Happy Path), accompanied by technical annotations.
- **Annex B** documents **Detailed Sprint Retrospectives**, breaking down metrics, effort deviations, and technical milestones achieved across all development phases.
- **Annex C** provides the **Deployment, Installation, and User Manual**, detailing step-by-step setup requirements, subsystem execution commands, and operator instructions for the HITL dashboard.
