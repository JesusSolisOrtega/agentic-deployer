# List of Acronyms and Terms

To facilitate technical reading and conceptual clarity, this section outlines the acronyms and terms frequently used throughout this thesis, particularly those pertaining to Platform Engineering, Generative Artificial Intelligence, and Cloud Infrastructure.

| Acronym | Original Meaning | Definition in the Context of this Thesis |
|---|---|---|
| **A2A** | Agent-to-Agent Protocol | Emerging protocol designed for standardized communication between multiple autonomous AI agents. |
| **API** | Application Programming Interface | Interface that enables two software applications to communicate. In this thesis, it primarily refers to the Kubernetes API and the LLM inference endpoints. |
| **C4** | Context, Containers, Components, Code | Standardized architectural diagramming model created by Simon Brown to visualize software architectures across four levels of abstraction. |
| **CAPEX** | Capital Expenditure | Upfront capital investment required to acquire, develop, or license permanent assets or custom software. |
| **CI/CD** | Continuous Integration / Continuous Deployment | DevOps practices that automate code integration, testing, packaging, and delivery to deployment targets. |
| **DAG** | Directed Acyclic Graph | Directed Acyclic Graph. A mathematical structure governing state machines, where transitions flow unidirectionally without closed cycles. |
| **DSL** | Domain-Specific Language | Specialized computer language tailored to a specific problem domain (e.g., PromQL, HCL, or Kubernetes declarative YAML). |
| **FSM** | Finite-State Machine | Finite-State Machine. A computational model ensuring that a deployment request resides in exactly one deterministic state at any point in time. |
| **HITL** | Human-In-The-Loop | Architectural pattern where human operators are intentionally placed in an automated control loop to audit, validate, and authorize critical actions. |
| **IaC** | Infrastructure as Code | Practice of managing and provisioning computational resources through machine-readable definition files (e.g., YAML manifests or OpenTofu scripts). |
| **IDP** | Internal Developer Portal/Platform | Internal Developer Platform. A self-service platform that abstracts infrastructure complexity for software engineers and researchers within an organization. |
| **ITIL** | Information Technology Infrastructure Library | Worldwide framework of standardized practices for Information Technology Service Management (ITSM). |
| **ITSM** | Information Technology Service Management | Activities, policies, and processes conducted by IT departments to design, deliver, operate, and control IT services. |
| **LLM** | Large Language Model | Deep neural network based on Transformer architectures capable of understanding and generating natural language and structured code. |
| **MCP** | Model Context Protocol | Open standard introduced by Anthropic to standardize how AI agents discover and interact with external data sources and tools. |
| **MR** | Metamorphic Relation | Metamorphic Relation. A formal invariance property describing expected system output behaviors under controlled input transformations, addressing the test oracle problem. |
| **MVP** | Minimum Viable Product | Minimum Viable Product. An initial release containing core functional capabilities sufficient to validate technical feasibility and satisfy core requirements. |
| **OPEX** | Operational Expenditure | Operational expenditure. Ongoing recurring operational costs (cloud subscriptions, electrical power, maintenance hours). |
| **PBT** | Property-Based Testing | Testing methodology where automated testing frameworks generate randomized inputs to verify universal logical invariants across domain models. |
| **QA** | Quality Assurance | System of procedures, testing layers (unit, property-based, mutation, and performance), and verification gates ensuring software satisfies formal specifications. |
| **RBAC** | Role-Based Access Control | Access control mechanism restricting computational resource access according to authorized roles assigned to users and service accounts. |
| **ReAct** | Reason and Act | Iterative prompting paradigm where the LLM alternates between internal deductive reasoning (*Thought*) and environment action invocations (*Action*). |
| **ROI** | Return on Investment | Financial metric comparing net economic benefits against total investment expenditures (personnel time saved versus development and deployment costs). |
| **SIC** | Servicio de Informática y Comunicaciones | University IT and Communications Department responsible for managing institutional infrastructure, networks, and computing facilities. |
| **TTM** | Time To Market / Time To Mitigation | Elapsed duration between the inception of an infrastructure requirement and the full operational availability of the corresponding service. |

---

## Technical Terminology

The following technical terms are retained in English according to conventional industry and academic practice:

| Term | Contextual Meaning | Usage in this Thesis |
|---|---|---|
| **Air-Gapped** | Disconnected or isolated network environment | Refers to network topologies physically or logically severed from public networks (the Internet), standard in high-security datacenters. In this thesis, it describes on-premise inference with Ollama. |
| **Boilerplate** | Standardized repetitive code templates | Reusable code structures required in multiple project components with minimal variation (e.g., FastAPI initialization or baseline schemas). |
| **Garbage Collector** | Runtime memory manager | Execution environment component that reclaims memory occupied by unreachable objects. Referenced in the context of the FSM terminal state transitions. |
| **Overhead** | Additional computational or latency cost | Supplementary resources (CPU cycles, RAM footprint, network latency) consumed by mediation middleware beyond raw business logic processing. |
| **Scaffolding** | Baseline project code generation | Automated generation of code skeletons and directory structures from predefined architectural archetypes. |
