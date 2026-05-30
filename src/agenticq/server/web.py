"""Web server for standalone GUI."""

from aiohttp import web
from pathlib import Path
import json

from ..core.scanner import scan_project
from ..core.classifier import classify_project
from ..core.recommender import recommend_plugins
from ..core.scaffolder import scaffold_plugins


class WebServer:
    """Web server for AgenticQ GUI."""

    def __init__(self):
        self.app = web.Application()
        self.setup_routes()

        self.catalog_path = Path(__file__).parent.parent / "data" / "catalog.json"
        self.taxonomy_path = Path(__file__).parent.parent / "data" / "taxonomy.json"
        self.upstream_path = Path(r"C:\Users\sande\AppData\Local\Temp\wshobson-agents-research")
        self.gui_path = Path(__file__).parent.parent.parent.parent / "gui"

    def setup_routes(self):
        """Setup HTTP routes."""
        self.app.router.add_get("/", self.serve_index)
        self.app.router.add_get("/api/catalog", self.get_catalog)
        self.app.router.add_post("/api/scan", self.scan_project_handler)
        self.app.router.add_post("/api/recommend", self.recommend_handler)
        self.app.router.add_post("/api/scaffold", self.scaffold_handler)
        self.app.router.add_static("/", self.gui_path, show_index=True)

    async def serve_index(self, request):
        """Serve index.html."""
        index_file = self.gui_path / "index.html"
        if not index_file.exists():
            return web.Response(text="GUI not found", status=404)
        return web.FileResponse(index_file)

    async def get_catalog(self, request):
        """Get catalog data."""
        if not self.catalog_path.exists():
            return web.json_response({"error": "Catalog not found"}, status=404)

        catalog = json.loads(self.catalog_path.read_text(encoding='utf-8'))
        return web.json_response(catalog)

    async def scan_project_handler(self, request):
        """Scan project endpoint."""
        data = await request.json()
        path = data.get("path", ".")

        try:
            profile = scan_project(path)
            return web.json_response({
                "languages": profile.languages,
                "frameworks": profile.frameworks,
                "infrastructure": profile.infrastructure,
                "databases": profile.databases,
                "testing_tools": profile.testing_tools,
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def recommend_handler(self, request):
        """Recommend plugins endpoint."""
        data = await request.json()
        path = data.get("path", ".")
        max_results = data.get("max_results", 10)

        try:
            profile = scan_project(path)
            taxonomy = json.loads(self.taxonomy_path.read_text(encoding='utf-8'))
            domains = classify_project(profile, taxonomy)
            recommendations = recommend_plugins(
                profile, domains, self.catalog_path, self.taxonomy_path, max_results
            )

            return web.json_response([
                {
                    "plugin_name": rec.plugin_name,
                    "relevance_score": rec.relevance_score,
                    "token_cost_estimate": rec.token_cost_estimate,
                    "reason": rec.reason,
                    "conflicts": rec.conflicts,
                }
                for rec in recommendations
            ])
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def scaffold_handler(self, request):
        """Scaffold plugins endpoint."""
        data = await request.json()
        plugins = data.get("plugins", [])
        harness = data.get("harness", "claude-code")
        target = data.get("target", ".")

        try:
            catalog = json.loads(self.catalog_path.read_text(encoding='utf-8'))
            result = scaffold_plugins(
                plugins, catalog, self.upstream_path, Path(target), harness
            )

            return web.json_response({
                "success": result.success,
                "message": result.message,
                "files_created": result.files_created,
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    def run(self, host="127.0.0.1", port=8080):
        """Run the web server."""
        print(f"Starting AgenticQ Web GUI at http://{host}:{port}")
        web.run_app(self.app, host=host, port=port)


def main():
    """Entry point for web server."""
    server = WebServer()
    server.run()


if __name__ == "__main__":
    main()
