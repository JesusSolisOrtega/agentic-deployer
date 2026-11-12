# Agentic Deployer: Internal Developer Platform (IDP) on OpenShift Governed by AI Agents and the MCP Protocol

<p align="center">
  <b>English Version</b> | <b><a href="README.es.md">Versión en Español</a></b>
</p>

**Master's Thesis (TFM)**  
*Master's Degree in Software Engineering: Cloud, Data and IT Management*  
*International Postgraduate School — University of Seville*  
**Author:** Jesús Solís Ortega | **Advisor:** Dr. Manuel Resinas Arias de Reyna  
**Academic Year:** 2025/2026  

---

This repository contains the reference implementation of **Agentic Deployer**, an Internal Developer Platform (IDP) that delegates the interpretation and provisioning of infrastructure workloads to Large Language Model (LLM) agents. The system governs the stochastic behavior of Artificial Intelligence through declarative contracts based on the **Model Context Protocol (MCP)** open standard, a decoupled Ports and Adapters (Hexagonal) architecture, and an immutable finite state machine with mandatory **Human-In-The-Loop (HITL)** governance.

---

## 🏗️ Architecture and Repository Structure

The architecture strictly isolates AI reasoning from privileged execution within the container cluster, guaranteeing that the cognitive model never directly accesses datacenter credentials or the Kubernetes/OpenShift API.

```text
agentic-deployer/
├── app/
│   ├── domain/               # Core Layer: Pure domain models (DeploymentIntent) and port contracts (DeployPort)
│   │   ├── exceptions.py     # Domain exceptions and security violations
│   │   ├── models.py         # Immutable entities and state machine (FSM: PENDING, DEPLOYED, REJECTED)
│   │   └── ports.py          # Abstract interfaces (DeployPort, DeploymentRepositoryPort)
│   ├── application/          # Application Logic Layer
│   │   ├── security_validator.py # Deterministic corporate security policy validation
│   │   └── use_cases.py      # Use cases for request processing, approval, and rejection
│   ├── infrastructure/       # Inbound and Outbound Adapters Layer
│   │   ├── fake_k8s_adapter.py # Test adapter that emulates deployments and generates YAML manifests
│   │   ├── main.py           # FastAPI REST server, CORS middleware, and HITL event dispatcher
│   │   └── repository.py     # SQLite persistence adapter (agentic_deployer.db)
│   ├── agent_layer/          # Cognitive Layer and Agent Orchestration
│   │   ├── agent.py          # ReAct engine with multi-provider support (Ollama, Gemini, OpenAI)
│   │   ├── chat_app.py       # Conversational interface for researchers (Streamlit)
│   │   ├── mcp_server.py     # Stdio MCP server exposing an infrastructure tool catalog
│   │   └── tools.py          # Agent tool definitions and SDK adaptation
│   ├── frontend/             # Web dashboard for the HITL Infrastructure Operator (HTML5/CSS3/JS)
│   │   ├── index.html        # Operational view of pending requests and audit trail
│   │   ├── styles.css        # Responsive stylesheet with adapted tables
│   │   └── app.js            # REST API client logic and state transitions
│   └── tests/                # Automated test suite (unit, integration, PBT, mutation)
├── demos/                    # Empirical test evidence and real execution transcripts
│   ├── session_logs/         # JSON traces of real sessions with Ollama (Chapter 8 of the thesis)
│   └── README.md             # Documentation of demonstration scenarios
├── memoria/                  # Comprehensive academic documentation and official technical thesis
│   ├── en/                   # Master's thesis chapters and annexes in English
│   ├── es/                   # Master's thesis chapters and annexes in Spanish
│   └── TFM_JesusSolisOrtega_ES.pdf # Final consolidated thesis in Spanish (with official vector cover)
├── scripts/                  # Development, quality assurance, and reproducibility scripts
│   ├── install.sh            # Automated virtual environment initialization and dependencies
│   ├── run_tests.sh          # Full quality assurance (QA) pipeline
│   ├── run_tests_only.sh     # Rapid execution of the Pytest test suite
│   ├── clean.sh              # Cleanup of caches, mutants, and runtime artifacts
│   ├── locustfile.py         # Stress testing and API latency evaluation
│   ├── compare_models.py     # Multi-model comparative benchmark
│   └── generate_demos.py     # Automated empirical session evidence generation
├── requirements.txt          # Fixed production and testing dependencies
├── pyproject.toml            # Tool configuration for linters, static analysis, and testing
└── .env.example              # Environment variables template
```

---

## 🚀 Installation and Environment Setup

The system requires **Python 3.11 or higher** and a UNIX-like operating system (GNU/Linux or macOS; compatible with Windows via WSL2).

### Option A. Automated Quick Installation (Recommended)

A setup script is provided to configure the virtual environment, install dependencies, provision headless browsers for E2E testing, and initialize `.env`:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Option B. Manual Step-by-Step Installation

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install project dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Provision browsers for E2E UI testing (Playwright)
playwright install chromium

# 4. Create environment variable file from template
cp .env.example .env
```

---

## ⚙️ Running Subsystems

The platform consists of two decoupled processes that run concurrently in separate terminals with the virtual environment activated (`source .venv/bin/activate`).

### 1. Operations Backend and HITL Middleware (FastAPI)

Exposes the REST API, orchestrates deterministic policy validation, and serves the operator web interface:

```bash
uvicorn app.infrastructure.main:app --host 0.0.0.0 --port 8000 --reload
```

* **Operations Dashboard (HITL):** [http://localhost:8000/](http://localhost:8000/) *(automatic redirect to `/frontend/`)*
* **Interactive API Documentation (Swagger / OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Request status tracking endpoint:** `GET http://localhost:8000/hitl/status/{deployment_id}`

### 2. Conversational Assistant Interface (Streamlit)

The chat interface assists users in formulating infrastructure requests using ReAct reasoning:

#### On-Premise / Data Sovereignty Mode (Ollama — Recommended)
Enables local inference without data leakage to external third-party cloud providers (Zero Data Retention). The official baseline model evaluated in the research is `qwen2.5:7b` (also compatible with `qwen2.5-coder:7b`):

```bash
# In an auxiliary terminal, launch Ollama and pull the model:
ollama serve
ollama pull qwen2.5:7b

# Launch the chat interface connected to the local model:
LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
```

> **Remote GPU Servers:** If the IT department hosts Ollama on a centralized corporate server, simply configure `OLLAMA_HOST=http://<gpu-ip-or-domain>:11434` in the `.env` file.

#### Fast Deterministic Demo Mode (No GPU or API Keys Required)
```bash
streamlit run app/agent_layer/chat_app.py   # Uses LLM_PROVIDER=fake by default
```

#### Commercial Models Mode (OpenAI / Gemini)
```bash
OPENAI_API_KEY=sk-... LLM_PROVIDER=openai streamlit run app/agent_layer/chat_app.py
```

* **Chat Interface URL:** [http://localhost:8501](http://localhost:8501)

---

## 🔄 Human-In-The-Loop (HITL) Workflow

1. **Natural Language Request:** The user submits a prompt in the chat interface ([http://localhost:8501](http://localhost:8501)), for example:  
   *«I need to deploy the web portal for the departmental AI conference.»*
2. **Agentic Reasoning and Policy Validation:** The agent derives compute resources, container image, and ports, invoking the corresponding MCP tool. If the deployment violates security policies (e.g., privileged port `< 1024` or `:latest` tag), the validator raises a deterministic error and the agent negotiates safe parameters.
3. **Quarantine Registration:** A deployment record with a unique identifier (e.g., `120a9ea1`) is persisted in the `PENDING_APPROVAL` state.
4. **Human Supervision:** The IT infrastructure operator opens the Dashboard ([http://localhost:8000/](http://localhost:8000/)), inspects the technical manifest card, and verifies quota allocations.
5. **Decision:**
   * **Approve:** The finite state machine transitions to `DEPLOYED`, executing the deployment adapter and storing audit logs.
   * **Reject:** The state machine transitions to `REJECTED`, notifying the justification and cancelling the provision.
6. **Asynchronous Polling:** The user can click **«Refresh»** in the chat or ask *«What is the status of request 120a9ea1?»* to track progress in real time.

---

## 🛠️ Customization and Extension Guide for Enterprise IT

This section describes extension points designed for systems engineering teams to adapt the platform to corporate infrastructure via a dedicated Git branch.

### 1. Recommended Branching Strategy

To preserve the canonical TFM codebase and manage institutional customizations cleanly:

```bash
git checkout -b corp/sic-deploy
```

### 2. Connecting to a Production OpenShift Cluster (`app/infrastructure/`)

The platform implements the Hexagonal pattern. To deploy real container workloads to Red Hat OpenShift or Kubernetes instead of emulating them:

1. Implement a concrete adapter matching the [`DeployPort`](file:///home/jesus/projects/TFM/app/domain/ports.py) contract:
   ```python
   # app/infrastructure/openshift_adapter.py
   from app.domain.ports import DeployPort
   from app.domain.models import DeploymentIntent, DeploymentAction
   from kubernetes import client, config

   class OpenshiftK8sAdapter(DeployPort):
       def __init__(self, kubeconfig_path: str = None, namespace: str = "idp-workloads"):
           self.namespace = namespace
           if kubeconfig_path:
               config.load_kube_config(config_file=kubeconfig_path)
           else:
               config.load_incluster_config()
           self.apps_api = client.AppsV1Api()
           self.core_api = client.CoreV1Api()

       def deploy(self, intent: DeploymentIntent) -> str:
           if intent.action == DeploymentAction.DELETE:
               self.apps_api.delete_namespaced_deployment(name=intent.name, namespace=self.namespace)
               return f"Resource {intent.name} deleted."
           
           # Generate and apply OpenShift Deployment / Service / Route
           # ...
           return f"https://{intent.name}.apps.openshift.us.es"
   ```

2. Inject the concrete adapter into [`app/infrastructure/main.py`](file:///home/jesus/projects/TFM/app/infrastructure/main.py):
   ```python
   # app/infrastructure/main.py (around line 58)
   from app.infrastructure.openshift_adapter import OpenshiftK8sAdapter

   # Replace FakeK8sAdapter with the real cluster adapter:
   k8s_adapter = OpenshiftK8sAdapter(namespace="sic-idp-apps")
   ```

### 3. Tuning Institutional Security Policies

Operational constraints are centralized in [`app/application/security_validator.py`](file:///home/jesus/projects/TFM/app/application/security_validator.py):

* **Trusted Container Registries (`ALLOWED_REGISTRIES`):**  
  Add internal or corporate registries:
  ```python
  ALLOWED_REGISTRIES = (
      "docker.io/library/",
      "quay.io/",
      "registry.redhat.io/",
      "harbor.sic.us.es/",
  )
  ```
* **Departmental Resource Quotas:**  
  Modify `MAX_CPU_MILLICORES` (default 4 Cores) and `MAX_RAM_MI` (default 8 GiB) according to OpenShift project limits.
* **Secret Protection:**  
  Extend the `FORBIDDEN_ENV_KEYS` list to enforce Kubernetes `Secrets` / `ConfigMaps` rather than raw environment variables.

### 4. Extending the MCP Tool Catalog (`mcp_server.py`)

To expose additional institutional services (e.g., departmental MariaDB instances, Drupal portals, or Celery task workers):

1. Define the tool in [`app/agent_layer/mcp_server.py`](file:///home/jesus/projects/TFM/app/agent_layer/mcp_server.py) with `@server.list_tools()` and `@server.call_tool()`.
2. Configure declarative parameters (hardened images, ports $\ge 1024$, non-sensitive variables).
3. The agent dynamically discovers new tools at initialization without requiring modifications to the orchestrator core.

### 5. Production Database Persistence

The prototype uses SQLite (`SQLiteDeploymentRepository`). For production environments, create a class implementing [`DeploymentRepositoryPort`](file:///home/jesus/projects/TFM/app/domain/ports.py) backed by a PostgreSQL cluster and instantiate it in `app/infrastructure/main.py`.

---

## 🧪 Quality Assurance (QA) and Reproducibility

The repository implements a multi-layer formal verification strategy designed to ensure system robustness against LLM stochasticity:

* **Property-Based Testing (Hypothesis):** Systematic fuzzing over the security validator with thousands of pseudo-randomly generated inputs.
* **Mutation Testing (Mutmut):** Introduction of logical mutants in `SecurityContextValidator` to evaluate test suite fault-detection capabilities.
* **Metamorphic Testing:** Empirical robustness evaluation of LLMs under semantic perturbations, lexical noise, and temperature variations.
* **End-to-End UI Testing (Playwright):** Full-flow verification automating the browser interaction through the HITL dashboard.
* **Performance and Load Testing (Locust):** Concurrency simulation and API latency auditing under high request loads.

### Test Execution

```bash
# 1. Quick test suite execution (65 tests in ~3.5 s):
./scripts/run_tests_only.sh

# 2. Comprehensive QA pipeline (Linters, Type Checks, Tests, Mutmut, Locust):
./scripts/run_tests.sh

# 3. Reproduction of empirical sessions documented in Chapter 8:
PYTHONPATH=. python3 scripts/generate_demos.py

# 4. Multi-model comparative benchmark (Qwen, Llama, Mistral):
PYTHONPATH=. python3 scripts/compare_models.py
```

To reset and clean up test fixtures and generated reports:
```bash
./scripts/clean.sh
```

---

## 🔌 Formal Validation with MCP Inspector

The MCP server is interoperable with any compliant MCP client. Its declarative schema can be inspected and tools invoked in real time using the official MCP tool:

```bash
# Requires Node.js / npx
npx @modelcontextprotocol/inspector .venv/bin/python app/agent_layer/mcp_server.py
```

Once launched, navigate to `http://localhost:5173` to inspect JSON Schema signatures for `deploy_congress_web`, `deploy_python_app`, `deploy_wordpress`, etc.

---

## 📄 Master's Thesis Documentation

Comprehensive formal academic documentation is available in the [`memoria/`](memoria/) directory:

* **Thesis Chapters:** Symmetrically structured in English ([`memoria/en/`](memoria/en/)) and Spanish ([`memoria/es/`](memoria/es/)), authored in standalone Markdown and optimized for direct rendering on GitHub.
* **Official Consolidated PDF:** Final compiled thesis document (161 pages) assembled with the official vector cover of the University of Seville:  
  👉 **[`memoria/TFM_JesusSolisOrtega_ES.pdf`](memoria/TFM_JesusSolisOrtega_ES.pdf)**

---

## ⚖️ License and Terms of Use

Copyright (C) 2026 Jesús Solís Ortega.

* **Software and Source Code:** Distributed under the terms of the **GNU Affero General Public License v3.0 (GNU AGPLv3)**. Refer to the [`LICENSE`](LICENSE) file for the full license text.
  * *Open and Academic Use:* Copying, running, inspecting, and modifying the software is authorized for educational, personal, research, and non-profit purposes, subject to the reciprocal obligation to share derived source code under the same license if hosted over a computer network (Section 13).
  * *Commercial Licensing and Professional Services:* Organizations wishing to integrate, deploy, or operate this platform in proprietary enterprise environments without AGPLv3 obligations, or seeking architectural guidance and custom OpenShift/Kubernetes integrations, may contact the author directly:  
    📫 **Jesús Solís Ortega** — [jesussolisortega@gmail.com](mailto:jesussolisortega@gmail.com)

* **Technical Thesis and Documentation:** The academic Master's Thesis and its formal specifications are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

