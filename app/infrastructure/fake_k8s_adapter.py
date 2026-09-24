"""
Adaptador fake de Kubernetes/OKD.

Implementa el puerto DeployPort sin depender de un cluster real.
Simula la generacion de un YAML y devuelve una URL inventada.
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

from app.domain.models import DeploymentAction, DeploymentIntent
from app.domain.ports import DeployPort

# Directorio de salida para los manifiestos generados
OUTPUT_DIR = Path(os.getcwd()) / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


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
        """Simula un CREATE en OKD y guarda el manifiesto."""
        fake_yaml = textwrap.dedent(f"""\
            ---
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {intent.nombre}
              labels:
                app: {intent.nombre}
            spec:
              replicas: 1
              selector:
                matchLabels:
                  app: {intent.nombre}
              template:
                metadata:
                  labels:
                    app: {intent.nombre}
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
            ---
            apiVersion: v1
            kind: Service
            metadata:
              name: {intent.nombre}-svc
            spec:
              selector:
                app: {intent.nombre}
              ports:
                - protocol: TCP
                  port: 80
                  targetPort: {intent.puerto_interno}
            ---
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: {intent.nombre}-ingress
            spec:
              rules:
                - host: {intent.nombre}.apps.universidad.edu
                  http:
                    paths:
                      - path: /
                        pathType: Prefix
                        backend:
                          service:
                            name: {intent.nombre}-svc
                            port:
                              number: 80
        """)

        # Guardar en archivo para tener la evidencia del "Golden Path"
        output_file = OUTPUT_DIR / f"{intent.nombre}.yaml"
        output_file.write_text(fake_yaml)

        print("=" * 60)
        print(f"🚀 K8s ADAPTER -- Manifiesto generado en: {output_file}")
        print("=" * 60)

        return f"https://{intent.nombre}.apps.universidad.edu"

    def _simulate_delete(self, intent: DeploymentIntent) -> str:
        """Simula un DELETE en OKD."""
        # Si existe el manifiesto previo, lo borramos (simulando que se aplica el delete)
        output_file = OUTPUT_DIR / f"{intent.nombre}.yaml"
        deleted = False
        if output_file.exists():
            output_file.unlink()
            deleted = True

        print("=" * 60)
        print(f"🗑️  K8s ADAPTER -- Borrado de '{intent.nombre}'")
        if deleted:
            print(f"   Archivo {output_file.name} eliminado.")
        print("=" * 60)

        return f"https://{intent.nombre}.apps.universidad.edu [DELETED]"
