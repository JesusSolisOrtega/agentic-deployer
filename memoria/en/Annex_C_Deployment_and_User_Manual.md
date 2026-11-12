# Annex C. Installation, Deployment, and Operational Manual

This annex constitutes the technical operational manual for experimental replication, installation, deployment, and usage of the *Agentic Deployer* platform. Its structure follows software engineering standards and scientific reproducibility guidelines.

---

## C.1. Installation and Deployment Manual

### C.1.1. System Prerequisites

The following host prerequisites are required for deploying the system in a local development environment or dedicated server:

* **Operating System:** GNU/Linux (tested on Debian/Ubuntu distributions) or macOS. Fully compatible with Windows via WSL2.
* **Runtime Environment:** Python 3.11 or higher.
* **Package Management:** `pip` and native virtual environment tooling (`python3-venv`).
* **Web Browser:** Modern web browser (Chrome, Firefox, or Edge) to interact with user interfaces.
* **Local Inference Engine (Optional for on-premise execution):** Ollama (v0.3.0 or higher) with GPU acceleration (CUDA / Metal) or CPU fallback.

### C.1.2. Source Code Acquisition and Environment Setup

1. **Clone the repository and enter the root directory:**
   ```bash
   git clone https://github.com/JesusSolisOrtega/agentic-deployer.git
   cd agentic-deployer
   ```

2. **Create and activate the Python virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install production and quality assurance dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install browser binaries for end-to-end UI testing (Playwright):**
   ```bash
   playwright install chromium
   ```

### C.1.3. Environment Variable Configuration

The system is configured through a `.env` environment file. A preconfigured baseline template (`.env.example`) is provided:

```bash
cp .env.example .env
```

Key configurable environment variables include:
* `LLM_PROVIDER`: Cognitive inference provider (`ollama`, `gemini`, `openai`, or `fake`).
* `OLLAMA_HOST`: Listening address of the local Ollama daemon (defaults to `http://localhost:11434`).
* `OLLAMA_MODEL`: Identifier of the local model to load (defaults to `qwen2.5:7b` or `qwen2.5-coder:7b`).
* `OPENAI_API_KEY` / `GEMINI_API_KEY`: Authentication credentials when selecting cloud providers.
* `BACKEND_URL`: Base URL of the REST middleware (defaults to `http://localhost:8000`).
* `DATABASE_PATH`: Filesystem path to the SQLite persistence database (`agentic_deployer.db`).

*(Note: The executable script `scripts/install.sh` automates the above steps and triggers local model retrieval on compatible systems).*

### C.1.4. Installation Verification

Prior to launching production services, executing the automated test suite is strongly recommended:

```bash
pytest -v
```

Passing the unit and integration test suites validates that domain invariants, the FSM state machine, and security policy validators are fully functional.

---

## C.2. Subsystem Execution

The decoupled architecture requires the concurrent execution of two independent services:

### C.2.1. Operations Backend and MCP Server (FastAPI)

In a primary terminal with the active virtual environment, start the application server:

```bash
uvicorn app.infrastructure.main:app --host 0.0.0.0 --port 8000 --reload
```

* **HITL Operations Dashboard:** [http://localhost:8000/frontend/](http://localhost:8000/frontend/) (with automatic redirection from [http://localhost:8000](http://localhost:8000))
* **Interactive OpenAPI (Swagger) Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

### C.2.2. Agent Conversational Interface (Streamlit)

In a secondary independent terminal with the active virtual environment, launch the chat client:

* **On-Premise Mode (Data Sovereignty with Ollama):**
  ```bash
  # In an auxiliary terminal, launch the model server if not already running:
  ollama serve
  
  # Launch the agentic interface connected to the local model:
  LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5:7b streamlit run app/agent_layer/chat_app.py
  ```

* **Rapid Demonstration Mode (Deterministic, zero GPU and API key overhead):**
  ```bash
  streamlit run app/agent_layer/chat_app.py
  ```

* **Web entry point:** [http://localhost:8501](http://localhost:8501)

---

## C.3. User Manual and HITL Operation

### C.3.1. Formulating Natural Language Requests

1. The researcher accesses the conversational web interface on port `8501`.
2. In the bottom text input (or via quick suggestion buttons), the user inputs a service request in natural language. Valid examples:
   * *"I need a website for the 'ai-congress-2025' conference with medium traffic."*
   * *"Deploy a WordPress instance for the computer science department."*
   * *"Deploy a Python REST API to publish research datasets."*
   * *"I need a PostgreSQL database with 10 GB of storage capacity."*
   * *"I want to decommission the old-web service."*
3. **Dialogue and parameter negotiation:** If the request lacks mandatory attributes or violates institutional policies, the agent reasons over validator observations and prompts the user with guided questions to converge on compliant parameters.
4. **Intent registration:** Upon resolving valid parameters, the agent invokes the corresponding MCP tool and persists the deployment intent in quarantine status (`PENDING_APPROVAL`), returning the unique deployment tracking ID to the user (e.g., `120a9ea1`).

### C.3.2. Technical Supervision via the HITL Dashboard

1. The institutional IT operator accesses the Approval Dashboard at [http://localhost:8000/frontend/](http://localhost:8000/frontend/).
2. Under **"Pending Requests"**, the operator inspects the technical profile generated by the agent:
   * Allocated compute quotas (CPU and memory limits).
   * Certified container image sourced from institutional registries and exposed service ports.
   * Generated declarative Kubernetes manifest and security policy validation findings.
3. **Operator decision:**
   * **Approve:** Clicking the confirmation button transitions the FSM to `DEPLOYED`, executing deployment simulation against OpenShift/Kubernetes and recording an immutable audit trail.
   * **Reject:** If administrative discrepancies or quota violations are detected, clicking **Reject** transitions the request to the immutable terminal state `REJECTED`.

### C.3.3. Asynchronous Feedback and Status Tracking

The researcher can inspect request status at any time without full page reloads:

1. **Within the chat interface (Streamlit):** Under the bottom expander **"📬 My Pending Requests"**, clicking **"🔄 Refresh"**, or querying the conversational assistant directly:
   > *"What is the status of request 120a9ea1?"*
2. **Via the REST traceability endpoint:**
   ```bash
   curl -X GET "http://localhost:8000/hitl/status/120a9ea1"
   ```

The system responds with the current FSM lifecycle state (`PENDING_APPROVAL`, `DEPLOYED`, or `REJECTED`) along with container specifications, guaranteeing end-to-end operational traceability.

