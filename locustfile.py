from locust import HttpUser, between, task


class UniversityLoadUser(HttpUser):
    """Simula el trafico de PDI/PAS hacia el Middleware Orquestador."""

    wait_time = between(1, 3)

    @task(3)
    def simulate_mcp_agent_request(self) -> None:
        """Simula al Agente MCP enviando una intencion de despliegue (Peso 3)."""
        payload = {
            "nombre": "load-test-service",
            "action": "CREATE",
            "imagen": "docker.io/library/nginx:alpine",
            "puerto_interno": 8080,
            "cpu": "250m",
            "ram": "128Mi",
        }
        self.client.post("/mcp/intent", json=payload)

    @task(1)
    def simulate_hitl_technician(self) -> None:
        """Simula al Tecnico recargando el panel de control (Peso 1)."""
        # Hacemos GET al frontend y también al endpoint de datos
        self.client.get("/frontend/index.html")
        self.client.get("/hitl/pending")
