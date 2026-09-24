import pytest
from unittest.mock import patch, Mock
import requests
from app.agent_layer.mcp_server import _calculate_congress_resources, _send_intent

def test_calculate_congress_resources_alto():
    for k in ["alto", "high", ">500", "1000"]:
        assert _calculate_congress_resources(k) == {"cpu": "1", "ram": "512Mi"}

def test_calculate_congress_resources_medio():
    for k in ["medio", "medium", "200", "300", "400", "500"]:
        assert _calculate_congress_resources(k) == {"cpu": "500m", "ram": "256Mi"}

def test_calculate_congress_resources_bajo():
    assert _calculate_congress_resources("bajo") == {"cpu": "250m", "ram": "128Mi"}

@patch("app.agent_layer.mcp_server.requests.post")
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
def test_send_intent_error(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error 500")
    mock_post.return_value = mock_response
    
    with pytest.raises(requests.exceptions.HTTPError):
        _send_intent({"test": "data"})
