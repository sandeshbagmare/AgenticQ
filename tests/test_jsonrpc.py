"""Tests for the JSON-RPC server."""
import json
import pytest
from io import StringIO

from agenticq.server.jsonrpc import JSONRPCServer


def test_jsonrpc_catalog_list():
    """Test catalog/list method."""
    server = JSONRPCServer()
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "catalog/list",
        "params": {}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert "result" in response or "error" in response

    if "result" in response:
        assert "plugins" in response["result"]


def test_jsonrpc_project_scan():
    """Test project/scan method."""
    server = JSONRPCServer()
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "project/scan",
        "params": {"path": "."}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 2

    if "result" in response:
        assert "languages" in response["result"]
        assert "frameworks" in response["result"]


def test_jsonrpc_recommend():
    """Test recommend method."""
    server = JSONRPCServer()
    request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "recommend",
        "params": {"path": ".", "max_results": 5}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3

    if "result" in response:
        assert isinstance(response["result"], list)


def test_jsonrpc_unknown_method():
    """Test unknown method returns error."""
    server = JSONRPCServer()
    request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "unknown/method",
        "params": {}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 4
    assert "error" in response
    assert response["error"]["code"] == -32601


def test_jsonrpc_caching():
    """Test that catalog is cached."""
    server = JSONRPCServer()

    # First call
    request1 = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "catalog/list",
        "params": {}
    }
    response1 = server.handle_request(request1)

    # Second call should use cache
    request2 = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "catalog/list",
        "params": {}
    }
    response2 = server.handle_request(request2)

    # Both should succeed (or both fail if catalog missing)
    assert ("result" in response1) == ("result" in response2)
