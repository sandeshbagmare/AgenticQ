"""JSON-RPC server for VS Code extension."""

import json
import sys
from pathlib import Path
from typing import Any, Dict

from ..core.scanner import scan_project
from ..core.classifier import classify_project
from ..core.recommender import recommend_plugins
from ..core.scaffolder import scaffold_plugins


class JSONRPCServer:
    """Simple JSON-RPC server for VS Code extension communication."""

    def __init__(self):
        self.catalog_path = Path(__file__).parent.parent / "data" / "catalog.json"
        self.taxonomy_path = Path(__file__).parent.parent / "data" / "taxonomy.json"
        self.upstream_path = Path(r"C:\Users\sande\AppData\Local\Temp\wshobson-agents-research")

    def load_catalog(self) -> Dict[str, Any]:
        """Load catalog.json."""
        if not self.catalog_path.exists():
            return {"plugins": []}
        return json.loads(self.catalog_path.read_text(encoding='utf-8'))

    def load_taxonomy(self) -> Dict[str, Any]:
        """Load taxonomy.json."""
        if not self.taxonomy_path.exists():
            return {"domains": []}
        return json.loads(self.taxonomy_path.read_text(encoding='utf-8'))

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "catalog/list":
                result = self.load_catalog()
            elif method == "project/scan":
                path = params.get("path", ".")
                profile = scan_project(path)
                result = {
                    "languages": profile.languages,
                    "frameworks": profile.frameworks,
                    "infrastructure": profile.infrastructure,
                    "databases": profile.databases,
                    "testing_tools": profile.testing_tools,
                }
            elif method == "recommend":
                path = params.get("path", ".")
                max_results = params.get("max_results", 10)

                profile = scan_project(path)
                taxonomy = self.load_taxonomy()
                domains = classify_project(profile, taxonomy)
                recommendations = recommend_plugins(
                    profile, domains, self.catalog_path, self.taxonomy_path, max_results
                )

                result = [
                    {
                        "plugin_name": rec.plugin_name,
                        "relevance_score": rec.relevance_score,
                        "token_cost_estimate": rec.token_cost_estimate,
                        "reason": rec.reason,
                        "conflicts": rec.conflicts,
                    }
                    for rec in recommendations
                ]
            elif method == "scaffold":
                plugins = params.get("plugins", [])
                harness = params.get("harness", "claude-code")
                target = params.get("target", ".")

                catalog = self.load_catalog()
                scaffold_result = scaffold_plugins(
                    plugins, catalog, self.upstream_path, Path(target), harness
                )

                result = {
                    "success": scaffold_result.success,
                    "message": scaffold_result.message,
                    "files_created": scaffold_result.files_created,
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }

            return {"jsonrpc": "2.0", "id": request_id, "result": result}

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": str(e)},
            }

    def run(self):
        """Run the JSON-RPC server (stdin/stdout)."""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
                print(json.dumps(error_response), flush=True)


def main():
    """Entry point for JSON-RPC server."""
    server = JSONRPCServer()
    server.run()


if __name__ == "__main__":
    main()
