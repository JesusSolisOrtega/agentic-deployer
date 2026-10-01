"""
REST API — Infrastructure layer (HTTP input adapter).

Exposes the endpoints connecting:
  • The MCP Agent  →  POST /mcp/intent
  • The HITL Panel →  GET  /hitl/pending
  • The HITL Panel →  POST /hitl/approve/{id}
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.application.use_cases import ProcessDeploymentUseCase
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentIntent, DeploymentRecord, DeploymentStatus
from app.infrastructure.fake_k8s_adapter import FakeK8sAdapter
from app.infrastructure.repository import SQLiteDeploymentRepository

# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Deployment Orchestrator Middleware",
    description="MVP with HITL (Human-in-the-Loop) and MCP protocol",
    version="0.1.0",
)

# CORS — allows the frontend (served on file:// or another port) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend at /frontend
_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount("/frontend", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")

# Dependency injection (manual, no DI framework — prototype)
repository = SQLiteDeploymentRepository()
use_case = ProcessDeploymentUseCase(repository=repository)
k8s_adapter = FakeK8sAdapter()


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------

class IntentResponse(BaseModel):
    id: str
    status: str
    message: str


class ApproveResponse(BaseModel):
    id: str
    status: str
    result_url: str


class RejectResponse(BaseModel):
    id: str
    status: str
    message: str


class ErrorResponse(BaseModel):
    detail: str
    violations: list[str] | None = None


class StatusResponse(BaseModel):
    id: str
    name: str
    status: str
    image: str
    port: int
    message: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/mcp/intent",
    response_model=IntentResponse,
    status_code=201,
    summary="Receive deployment intent from the MCP Agent",
    tags=["MCP"],
)
def create_intent(intent: DeploymentIntent) -> IntentResponse:
    """
    Simulates the MCP Agent input.

    Receives the deployment intent JSON, executes security validation,
    and if successful, saves it with PENDING_APPROVAL status.
    """
    try:
        record = use_case.execute(intent)
    except SecurityViolationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "The intent violates security policies",
                "violations": exc.violations,
            },
        ) from exc

    return IntentResponse(
        id=record.id,
        status=record.status.value,
        message="Intent registered. Pending human approval.",
    )


@app.get(
    "/hitl/pending",
    response_model=list[DeploymentRecord],
    summary="List deployments pending approval",
    tags=["HITL"],
)
def list_pending() -> list[DeploymentRecord]:
    """Returns all records with PENDING_APPROVAL status."""
    return [
        record
        for record in repository.get_all()
        if record.status == DeploymentStatus.PENDING_APPROVAL
    ]


@app.post(
    "/hitl/approve/{deployment_id}",
    response_model=ApproveResponse,
    summary="Approve a pending deployment",
    tags=["HITL"],
)
def approve_deployment(deployment_id: str) -> ApproveResponse:
    """
    Changes status to APPROVED and executes the FakeK8sAdapter.

    Returns the (mock) URL of the deployed service.
    """
    record = repository.get(deployment_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"Deployment '{deployment_id}' not found")

    if record.status != DeploymentStatus.PENDING_APPROVAL:
        raise HTTPException(
            status_code=409,
            detail=f"Deployment '{deployment_id}' is not pending (current status: {record.status.value})",
        )

    # Approve and deploy
    record.status = DeploymentStatus.APPROVED
    try:
        result_url = k8s_adapter.deploy(record.intent)
        record.result_url = result_url
        record.status = DeploymentStatus.DEPLOYED
    except Exception as exc:
        record.status = DeploymentStatus.FAILED
        repository.save(record)
        raise HTTPException(status_code=500, detail=f"Deployment error: {exc}") from exc

    repository.save(record)

    return ApproveResponse(
        id=record.id,
        status=record.status.value,
        result_url=result_url,
    )


@app.post(
    "/hitl/reject/{deployment_id}",
    response_model=RejectResponse,
    summary="Reject a pending deployment",
    tags=["HITL"],
)
def reject_deployment(deployment_id: str) -> RejectResponse:
    """
    Rejects a PENDING_APPROVAL deployment, transitioning it to REJECTED.

    This is a terminal state in the FSM: the deployment is permanently
    cancelled and preserved in the store for audit purposes only.
    """
    record = repository.get(deployment_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"Deployment '{deployment_id}' not found")

    if record.status != DeploymentStatus.PENDING_APPROVAL:
        raise HTTPException(
            status_code=409,
            detail=f"Deployment '{deployment_id}' is not pending (current status: {record.status.value})",
        )

    record.status = DeploymentStatus.REJECTED
    repository.save(record)

    return RejectResponse(
        id=record.id,
        status=record.status.value,
        message="Deployment rejected by operator.",
    )


# ---------------------------------------------------------------------------
# Status query — researcher-facing channel
# ---------------------------------------------------------------------------

@app.get(
    "/hitl/status/{deployment_id}",
    response_model=StatusResponse,
    summary="Query deployment status (researcher-facing)",
    tags=["HITL"],
)
def get_deployment_status(deployment_id: str) -> StatusResponse:
    """
    Returns the current status of a deployment intent.

    Designed as the researcher-facing channel: after the agent informs
    the researcher that their request is PENDING_APPROVAL, the researcher
    (or the chat UI) can poll this endpoint to learn when the SIC
    technician has approved or rejected the deployment.

    Status transitions visible here:
      PENDING_APPROVAL  →  still waiting for technician
      APPROVED          →  approved, deployment in progress
      DEPLOYED          →  deployment complete
      REJECTED          →  technician rejected the request
      FAILED            →  deployment attempted but failed
    """
    record = repository.get(deployment_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment '{deployment_id}' not found. Check the ID provided by the assistant.",
        )

    status_messages = {
        "PENDING_APPROVAL": "Your request is queued and awaiting review by the SIC technician.",
        "APPROVED": "The SIC technician has approved your request. Deployment is in progress.",
        "DEPLOYED": "Your service has been successfully deployed. ",
        "REJECTED": "The SIC technician has rejected this request. Please contact the SIC for details.",
        "FAILED": "Deployment was approved but encountered a technical error. The SIC team has been notified.",
    }

    return StatusResponse(
        id=record.id,
        name=record.intent.name,
        status=record.status.value,
        image=record.intent.image or "",
        port=record.intent.internal_port or 0,
        message=status_messages.get(record.status.value, "Unknown status."),
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}
