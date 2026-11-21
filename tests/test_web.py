"""Tests for the web server."""
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from agenticq.server.web import WebServer


class TestWebServer(AioHTTPTestCase):
    async def get_application(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.web_server = WebServer()
        self.web_server.catalog_path = root / "catalog.json"
        self.web_server.taxonomy_path = root / "taxonomy.json"
        self.web_server.upstream_path = root / "upstream"
        self.catalog = {"plugins": [{"name": "python-development", "total_tokens": 10000}]}
        self.taxonomy = {"domains": [{
            "domain_id": "python-development",
            "file_detection_heuristics": ["pyproject.toml", "*.py"],
            "plugins": ["python-development"],
        }]}
        self.web_server.catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")
        self.web_server.taxonomy_path.write_text(json.dumps(self.taxonomy), encoding="utf-8")
        self.project_path = root / "project"
        self.project_path.mkdir()
        (self.project_path / "pyproject.toml").write_text(
            '[project]\nname = "sample"\n', encoding="utf-8"
        )
        return self.web_server.app

    @unittest_run_loop
    async def test_get_catalog(self):
        """Test /api/catalog endpoint."""
        resp = await self.client.request("GET", "/api/catalog")
        assert resp.status == 200
        data = await resp.json()
        assert data == self.catalog

    @unittest_run_loop
    async def test_get_domains(self):
        """Test /api/domains endpoint."""
        resp = await self.client.request("GET", "/api/domains")
        assert resp.status == 200
        data = await resp.json()
        assert data == self.taxonomy["domains"]

    @unittest_run_loop
    async def test_get_plugins(self):
        """Test /api/plugins endpoint."""
        resp = await self.client.request("GET", "/api/plugins")
        assert resp.status == 200
        data = await resp.json()
        assert data == self.catalog["plugins"]

    @unittest_run_loop
    async def test_get_catalog_missing(self):
        self.web_server.catalog_path.unlink()
        resp = await self.client.request("GET", "/api/catalog")
        assert resp.status == 404
        assert await resp.json() == {"error": "Catalog not found"}

    @unittest_run_loop
    async def test_get_plugins_missing(self):
        self.web_server.catalog_path.unlink()
        resp = await self.client.request("GET", "/api/plugins")
        assert resp.status == 404
        assert await resp.json() == {"error": "Catalog not found"}

    @unittest_run_loop
    async def test_get_domains_missing(self):
        self.web_server.taxonomy_path.unlink()
        resp = await self.client.request("GET", "/api/domains")
        assert resp.status == 404
        assert await resp.json() == {"error": "Taxonomy not found"}

    @unittest_run_loop
    async def test_scan_project(self):
        """Test /api/scan endpoint."""
        resp = await self.client.request(
            "POST",
            "/api/scan",
            json={"path": str(self.project_path)}
        )
        assert resp.status == 200
        data = await resp.json()
        assert data["languages"] == ["python"]

    @unittest_run_loop
    async def test_recommend(self):
        """Test /api/recommend endpoint."""
        resp = await self.client.request(
            "POST",
            "/api/recommend",
            json={"path": str(self.project_path), "max_results": 5}
        )
        assert resp.status == 200
        data = await resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "python-development"
        assert data[0]["score"] == 30.0
        assert data[0]["tokenCost"] == 10000
        assert "reason" in data[0]
