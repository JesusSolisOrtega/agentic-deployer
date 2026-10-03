"""
Locust load testing script.

Simulates the traffic of users (PDI/PAS) against the orchestrator middleware.
"""

from locust import HttpUser, between, task


class UniversityLoadUser(HttpUser):
    """Simulates PDI/PAS traffic towards the Orchestrator Middleware."""

    wait_time = between(1, 3)

    @task(3)
    def simulate_mcp_agent_request(self) -> None:
        """Simulates the MCP Agent sending a deployment intent (Weight 3)."""
        payload = {
            "name": "load-test-service",
            "action": "CREATE",
            "image": "docker.io/library/nginx:alpine",
            "internal_port": 8080,
            "cpu": "250m",
            "ram": "128Mi",
        }
        self.client.post("/mcp/intent", json=payload)

    @task(1)
    def simulate_hitl_technician(self) -> None:
        """Simulates the Technician reloading the dashboard (Weight 1)."""
        # We perform GET to the frontend and also to the data endpoint
        self.client.get("/frontend/index.html")
        self.client.get("/hitl/pending")
