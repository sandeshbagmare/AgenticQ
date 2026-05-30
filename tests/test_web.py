"""Tests for the web server."""
import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import json
from pathlib import Path

from agenticq.server.web import WebServer


class TestWebServer(AioHTTPTestCase):
    async def get_application(self):
        server = WebServer()
        return server.app

    @unittest_run_loop
    async def test_get_catalog(self):
        """Test /api/catalog endpoint."""
        resp = await self.client.request("GET", "/api/catalog")
        assert resp.status == 200
        data = await resp.json()
        assert "plugins" in data

    @unittest_run_loop
    async def test_get_domains(self):
        """Test /api/domains endpoint."""
        resp = await self.client.request("GET", "/api/domains")
        assert resp.status == 200
        data = await resp.json()
        assert isinstance(data, list)

    @unittest_run_loop
    async def test_get_plugins(self):
        """Test /api/plugins endpoint."""
        resp = await self.client.request("GET", "/api/plugins")
        assert resp.status == 200
        data = await resp.json()
        assert isinstance(data, list)

    @unittest_run_loop
    async def test_scan_project(self):
        """Test /api/scan endpoint."""
        resp = await self.client.request(
            "POST",
            "/api/scan",
            json={"path": "."}
        )
        assert resp.status == 200
        data = await resp.json()
        assert "languages" in data

    @unittest_run_loop
    async def test_recommend(self):
        """Test /api/recommend endpoint."""
        resp = await self.client.request(
            "POST",
            "/api/recommend",
            json={"path": ".", "max_results": 5}
        )
        assert resp.status == 200
        data = await resp.json()
        assert isinstance(data, list)
        if len(data) > 0:
            # Check response format matches frontend expectations
            assert "name" in data[0]
            assert "score" in data[0]
            assert "tokenCost" in data[0]
            assert "reason" in data[0]
