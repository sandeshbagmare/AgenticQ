"""Tests for the JSON-RPC server."""
import json
import pytest

from agenticq.server.jsonrpc import JSONRPCServer


@pytest.fixture
def server(tmp_path):
    instance = JSONRPCServer()
    instance.catalog_path = tmp_path / "catalog.json"
    instance.taxonomy_path = tmp_path / "taxonomy.json"
    instance.upstream_path = tmp_path / "upstream"
    instance.catalog_path.write_text(json.dumps({
        "plugins": [{
            "name": "python-development",
            "description": "Python development plugin",
            "category": "languages",
            "total_tokens": 10000,
            "agents": [],
            "skills": [],
            "commands": [],
        }]
    }), encoding="utf-8")
    instance.taxonomy_path.write_text(json.dumps({
        "domains": [{
            "domain_id": "python-development",
            "file_detection_heuristics": ["pyproject.toml", "*.py"],
            "plugins": ["python-development"],
        }]
    }), encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "sample"\n', encoding="utf-8")
    return instance


def test_jsonrpc_catalog_list(server):
    """Test catalog/list method."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "catalog/list",
        "params": {}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert "error" not in response
    assert response["result"]["plugins"][0]["name"] == "python-development"


def test_jsonrpc_project_scan(server, tmp_path):
    """Test project/scan method."""
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "project/scan",
        "params": {"path": str(tmp_path)}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 2

    assert response["result"]["languages"] == ["python"]
    assert response["result"]["frameworks"] == []


def test_jsonrpc_recommend(server, tmp_path):
    """Test recommend method."""
    request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "recommend",
        "params": {"path": str(tmp_path), "max_results": 5}
    }
    response = server.handle_request(request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3

    assert response["result"] == [{
        "plugin_name": "python-development",
        "relevance_score": 30.0,
        "token_cost_estimate": 10000,
        "reason": "matches Python project",
        "conflicts": [],
    }]


def test_jsonrpc_unknown_method(server):
    """Test unknown method returns error."""
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


def test_jsonrpc_caching(server):
    """Test that catalog is cached."""
    # First call
    request1 = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "catalog/list",
        "params": {}
    }
    response1 = server.handle_request(request1)
    server.catalog_path.write_text('{"plugins": []}', encoding="utf-8")

    # Second call should use cache
    request2 = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "catalog/list",
        "params": {}
    }
    response2 = server.handle_request(request2)

    assert response1["result"]["plugins"][0]["name"] == "python-development"
    assert response2 == {"jsonrpc": "2.0", "id": 6, "result": response1["result"]}


def test_jsonrpc_catalog_list_missing_catalog_can_retry(server):
    catalog = server.catalog_path.read_text(encoding="utf-8")
    server.catalog_path.unlink()
    request = {"jsonrpc": "2.0", "id": "catalog-missing", "method": "catalog/list"}

    response = server.handle_request(request)

    assert response == {
        "jsonrpc": "2.0",
        "id": "catalog-missing",
        "error": {
            "code": -32603,
            "message": "Catalog not found. Run 'agenticq update' first.",
        },
    }

    server.catalog_path.write_text(catalog, encoding="utf-8")
    assert server.handle_request(request) == {
        "jsonrpc": "2.0", "id": "catalog-missing", "result": json.loads(catalog)
    }


def test_jsonrpc_scaffold_missing_catalog_can_retry(server, tmp_path):
    catalog = server.catalog_path.read_text(encoding="utf-8")
    server.catalog_path.unlink()
    agents_dir = server.upstream_path / "plugins" / "python-development" / "agents"
    agents_dir.mkdir(parents=True)
    (agents_dir / "python-pro.md").write_text("# Python agent\n", encoding="utf-8")
    target = tmp_path / "target"
    request = {
        "jsonrpc": "2.0",
        "id": "scaffold-missing",
        "method": "scaffold",
        "params": {"plugins": ["python-development"], "target": str(target)},
    }

    response = server.handle_request(request)

    assert response == {
        "jsonrpc": "2.0",
        "id": "scaffold-missing",
        "error": {
            "code": -32603,
            "message": "Catalog not found. Run 'agenticq update' first.",
        },
    }
    assert not target.exists()

    server.catalog_path.write_text(catalog, encoding="utf-8")
    result = server.handle_request(request)["result"]
    agent_file = target / ".claude" / "plugins" / "python-development" / "agents" / "python-pro.md"
    assert result["success"] is True
    assert result["files_created"] == [str(agent_file)]
    assert agent_file.read_text(encoding="utf-8") == "# Python agent\n"


def test_jsonrpc_recommend_missing_taxonomy_can_retry(server, tmp_path):
    taxonomy = server.taxonomy_path.read_text(encoding="utf-8")
    server.taxonomy_path.unlink()
    request = {
        "jsonrpc": "2.0",
        "id": "taxonomy-missing",
        "method": "recommend",
        "params": {"path": str(tmp_path)},
    }

    response = server.handle_request(request)

    assert response == {
        "jsonrpc": "2.0",
        "id": "taxonomy-missing",
        "error": {
            "code": -32603,
            "message": "Taxonomy not found. Run 'agenticq update' first.",
        },
    }

    server.taxonomy_path.write_text(taxonomy, encoding="utf-8")
    result = server.handle_request(request)["result"]
    assert result[0]["plugin_name"] == "python-development"
    assert result[0]["relevance_score"] == 30.0
