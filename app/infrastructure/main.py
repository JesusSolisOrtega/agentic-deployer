"""
API REST — Capa de infraestructura (adaptador de entrada HTTP).

Expone los endpoints que conectan:
  • El Agente MCP  →  POST /mcp/intent
  • El panel HITL  →  GET  /hitl/pending
  • El panel HITL  →  POST /hitl/approve/{id}
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.application.use_cases import ProcessDeploymentUseCase, deployment_store
from app.domain.exceptions import SecurityViolationError
from app.domain.models import DeploymentIntent, DeploymentRecord, DeploymentStatus
from app.infrastructure.fake_k8s_adapter import FakeK8sAdapter

# ---------------------------------------------------------------------------
# App FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Middleware Orquestador de Despliegues",
    description="MVP con HITL (Human-in-the-Loop) y protocolo MCP",
    version="0.1.0",
)

# CORS — permite que el frontend (servido en file:// o distinto puerto) acceda a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend estático en /frontend
_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount("/frontend", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")

# Inyección de dependencias (manual, sin framework DI — prototipo)
use_case = ProcessDeploymentUseCase()
k8s_adapter = FakeK8sAdapter()


# ---------------------------------------------------------------------------
# Schemas de respuesta
# ---------------------------------------------------------------------------

class IntentResponse(BaseModel):
    id: str
    status: str
    message: str


class ApproveResponse(BaseModel):
    id: str
    status: str
    result_url: str


class ErrorResponse(BaseModel):
    detail: str
    violations: list[str] | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/mcp/intent",
    response_model=IntentResponse,
    status_code=201,
    summary="Recibir intención de despliegue del Agente MCP",
    tags=["MCP"],
)
def create_intent(intent: DeploymentIntent) -> IntentResponse:
    """
    Simula la entrada del Agente MCP.

    Recibe el JSON de la intención de despliegue, ejecuta la validación
    de seguridad y, si pasa, la guarda con estado PENDING_APPROVAL.
    """
    try:
        record = use_case.execute(intent)
    except SecurityViolationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "La intención viola políticas de seguridad",
                "violations": exc.violations,
            },
        ) from exc

    return IntentResponse(
        id=record.id,
        status=record.status.value,
        message="Intención registrada. Pendiente de aprobación humana.",
    )


@app.get(
    "/hitl/pending",
    response_model=list[DeploymentRecord],
    summary="Listar despliegues pendientes de aprobación",
    tags=["HITL"],
)
def list_pending() -> list[DeploymentRecord]:
    """Devuelve todos los registros con estado PENDING_APPROVAL."""
    return [
        record
        for record in deployment_store.values()
        if record.status == DeploymentStatus.PENDING_APPROVAL
    ]


@app.post(
    "/hitl/approve/{deployment_id}",
    response_model=ApproveResponse,
    summary="Aprobar un despliegue pendiente",
    tags=["HITL"],
)
def approve_deployment(deployment_id: str) -> ApproveResponse:
    """
    Cambia el estado a APPROVED y ejecuta el FakeK8sAdapter.

    Devuelve la URL (ficticia) del servicio desplegado.
    """
    record = deployment_store.get(deployment_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"Despliegue '{deployment_id}' no encontrado")

    if record.status != DeploymentStatus.PENDING_APPROVAL:
        raise HTTPException(
            status_code=409,
            detail=f"El despliegue '{deployment_id}' no está pendiente (estado actual: {record.status.value})",
        )

    # Aprobar y desplegar
    record.status = DeploymentStatus.APPROVED
    try:
        result_url = k8s_adapter.deploy(record.intent)
        record.result_url = result_url
        record.status = DeploymentStatus.DEPLOYED
    except Exception as exc:
        record.status = DeploymentStatus.FAILED
        raise HTTPException(status_code=500, detail=f"Error en despliegue: {exc}") from exc

    return ApproveResponse(
        id=record.id,
        status=record.status.value,
        result_url=result_url,
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}
