"""
Punto de entrada para uvicorn.

Uso:
    uvicorn app.infrastructure.main:app --reload --port 8000
"""

from app.infrastructure.main import app  # noqa: F401
