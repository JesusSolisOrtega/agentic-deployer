"""
Tests for MCP Server tool helpers.
"""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from app.agent_layer.mcp_server import (
    _calculate_congress_resources,
    _send_intent,
    deploy_database,
    deploy_static_website,
    get_deployment_status,
)


# pyrefly: ignore [unannotated-return]
def test_calculate_congress_resources_high():
    for k in ["alto", "high", ">500", "1000"]:
        assert _calculate_congress_resources(k) == {"cpu": "1", "ram": "512Mi"}

# pyrefly: ignore [unannotated-return]
def test_calculate_congress_resources_medium():
    for k in ["medio", "medium", "200", "300", "400", "500"]:
        assert _calculate_congress_resources(k) == {"cpu": "500m", "ram": "256Mi"}

# pyrefly: ignore [unannotated-return]
def test_calculate_congress_resources_low():
    assert _calculate_congress_resources("bajo") == {"cpu": "250m", "ram": "128Mi"}

@patch("app.agent_layer.mcp_server.requests.post")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_send_intent_success(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_post.return_value = mock_response

    res = _send_intent({"test": "data"})

    assert res == {"status": "ok"}
    mock_post.assert_called_once_with(
        "http://localhost:8000/mcp/intent",
        json={"test": "data"},
        timeout=10
    )
    mock_response.raise_for_status.assert_called_once()

@patch("app.agent_layer.mcp_server.requests.post")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_send_intent_error(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error 500")
    mock_post.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        _send_intent({"test": "data"})


# ---------------------------------------------------------------------------
# Tests for specific tools
# ---------------------------------------------------------------------------



@patch("app.agent_layer.mcp_server._send_intent")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_deploy_static_website(mock_send_intent):
    mock_send_intent.return_value = {"id": "123"}
    res = deploy_static_website("my-site", "site.com")
    assert json.loads(res) == {"id": "123"}
    mock_send_intent.assert_called_once()
    payload = mock_send_intent.call_args[0][0]
    assert payload["name"] == "my-site"
    assert payload["image"] == "nginx:alpine"

@patch("app.agent_layer.mcp_server._send_intent")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_deploy_database(mock_send_intent):
    mock_send_intent.return_value = {"id": "456"}
    res = deploy_database("postgres", "15", 10)
    assert json.loads(res) == {"id": "456"}
    mock_send_intent.assert_called_once()
    payload = mock_send_intent.call_args[0][0]
    assert payload["name"] == "postgres-db"
    assert payload["internal_port"] == 5432

@patch("app.agent_layer.mcp_server.requests.get")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_get_deployment_status_success(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "DEPLOYED"}
    mock_get.return_value = mock_resp

    res = get_deployment_status("dep-1")
    assert json.loads(res) == {"status": "DEPLOYED"}
    mock_get.assert_called_once()

@patch("app.agent_layer.mcp_server.requests.get")
# pyrefly: ignore [implicit-any-parameter, unannotated-return]
def test_get_deployment_status_not_found(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp

    res = get_deployment_status("dep-2")
    assert "error" in json.loads(res)
