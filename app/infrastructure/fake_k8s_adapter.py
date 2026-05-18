"""
Adaptador fake de Kubernetes/OKD.

Implementa el puerto DeployPort sin depender de un clúster real.
Simula la generación de un YAML y devuelve una URL inventada.
"""

from __future__ import annotations

import textwrap

from app.domain.models import DeploymentIntent
from app.domain.ports import DeployPort


class FakeK8sAdapter(DeployPort):
    """
    Adaptador de despliegue para pruebas y desarrollo local.

    Genera un YAML simulado, lo imprime en consola y devuelve
    una URL ficticia como si el servicio estuviese levantado en OKD.
    """

    def deploy(self, intent: DeploymentIntent) -> str:
        # Simular generación del manifiesto YAML
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
        print("🚀 FAKE K8s ADAPTER — Desplegado en OKD fake")
        print("=" * 60)
        print(fake_yaml)
        print("=" * 60)

        # URL ficticia que simula el servicio desplegado
        fake_url = f"https://{intent.nombre}.apps.okd-fake.local:{intent.puerto_interno}"
        return fake_url
