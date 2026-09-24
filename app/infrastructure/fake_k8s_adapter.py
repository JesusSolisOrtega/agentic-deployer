"""
Fake Kubernetes/OKD adapter.

Implements the DeployPort without depending on a real cluster.
Simulates generating a YAML and returns a mock URL.
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

from app.domain.models import DeploymentAction, DeploymentIntent
from app.domain.ports import DeployPort

# Output directory for the generated manifests
OUTPUT_DIR = Path(os.getcwd()) / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


class FakeK8sAdapter(DeployPort):
    """
    Deployment adapter for local testing and development.

    Generates a simulated YAML, prints it to the console, and returns
    a mock URL as if the service were deployed on OKD.
    """

    def deploy(self, intent: DeploymentIntent) -> str:
        if intent.action == DeploymentAction.DELETE:
            return self._simulate_delete(intent)
        return self._simulate_create(intent)

    def _simulate_create(self, intent: DeploymentIntent) -> str:
        """Simulates a CREATE on OKD and saves the manifest."""
        fake_yaml = textwrap.dedent(f"""\
            ---
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {intent.name}
              labels:
                app: {intent.name}
            spec:
              replicas: 1
              selector:
                matchLabels:
                  app: {intent.name}
              template:
                metadata:
                  labels:
                    app: {intent.name}
                spec:
                  containers:
                    - name: {intent.name}
                      image: {intent.image}
                      ports:
                        - containerPort: {intent.internal_port}
                      resources:
                        requests:
                          cpu: {intent.cpu}
                          memory: {intent.ram}
            ---
            apiVersion: v1
            kind: Service
            metadata:
              name: {intent.name}-svc
            spec:
              selector:
                app: {intent.name}
              ports:
                - protocol: TCP
                  port: 80
                  targetPort: {intent.internal_port}
            ---
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: {intent.name}-ingress
            spec:
              rules:
                - host: {intent.name}.apps.universidad.edu
                  http:
                    paths:
                      - path: /
                        pathType: Prefix
                        backend:
                          service:
                            name: {intent.name}-svc
                            port:
                              number: 80
        """)

        # Save to file to have evidence of the "Golden Path"
        output_file = OUTPUT_DIR / f"{intent.name}.yaml"
        output_file.write_text(fake_yaml)

        print("=" * 60)
        print(f"🚀 K8s ADAPTER -- Manifest generated at: {output_file}")
        print("=" * 60)

        return f"https://{intent.name}.apps.universidad.edu"

    def _simulate_delete(self, intent: DeploymentIntent) -> str:
        """Simulates a DELETE on OKD."""
        # If the previous manifest exists, we delete it (simulating the delete applied)
        output_file = OUTPUT_DIR / f"{intent.name}.yaml"
        deleted = False
        if output_file.exists():
            output_file.unlink()
            deleted = True

        print("=" * 60)
        print(f"🗑️  K8s ADAPTER -- Deletion of '{intent.name}'")
        if deleted:
            print(f"   File {output_file.name} deleted.")
        print("=" * 60)

        return f"https://{intent.name}.apps.universidad.edu [DELETED]"
