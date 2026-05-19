"""
Adaptador fake de Kubernetes/OKD.

Implementa el puerto DeployPort sin depender de un cluster real.
Simula la generacion de un YAML y devuelve una URL inventada.
"""

from __future__ import annotations

import textwrap

from app.domain.models import DeploymentAction, DeploymentIntent
from app.domain.ports import DeployPort


class FakeK8sAdapter(DeployPort):
    """
    Adaptador de despliegue para pruebas y desarrollo local.

    Genera un YAML simulado, lo imprime en consola y devuelve
    una URL ficticia como si el servicio estuviese levantado en OKD.
    """

    def deploy(self, intent: DeploymentIntent) -> str:
        if intent.action == DeploymentAction.DELETE:
            return self._simulate_delete(intent)
        return self._simulate_create(intent)

    def _simulate_create(self, intent: DeploymentIntent) -> str:
        """Simula un CREATE en OKD."""
        fake_yaml = textwrap.dedent(f"""\
            ---
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {intent.nombre}
            spec:
              replicas: 1
              template:
                spec:
                  containers:
                    - name: {intent.nombre}
                      image: {intent.imagen}
                      ports:
                        - containerPort: {intent.puerto_interno}
                      resources:
                        requests:
                          cpu: {intent.cpu}
                          memory: {intent.ram}
        """)

        print("=" * 60)
        print("🚀 FAKE K8s ADAPTER -- Desplegado en OKD fake")
        print("=" * 60)
        print(fake_yaml)
        print("=" * 60)

        fake_url = f"https://{intent.nombre}.apps.okd-fake.local:{intent.puerto_interno}"
        return fake_url

    def _simulate_delete(self, intent: DeploymentIntent) -> str:
        """Simula un DELETE en OKD."""
        print("=" * 60)
        print(f"🗑️  FAKE K8s ADAPTER -- Borrado de '{intent.nombre}' en OKD fake")
        print("=" * 60)

        return f"https://{intent.nombre}.apps.okd-fake.local [DELETED]"
