"""AgenticQ CLI - Intelligent Agent Scaffolding Engine."""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from pathlib import Path
import json
import sys

from .core.scanner import scan_project
from .core.classifier import classify_project
from .core.recommender import recommend_plugins
from .core.scaffolder import scaffold_plugins
from .core.catalog import build_catalog
from .core.runtime_builder import build_runtime_agent
from .config import get_upstream_path, get_catalog_path, get_taxonomy_path

app = typer.Typer(
    name="agenticq",
    help="AgenticQ - Intelligent Agent Scaffolding Engine",
    add_completion=False,
)
console = Console()

# Paths
CATALOG_PATH = get_catalog_path()
TAXONOMY_PATH = get_taxonomy_path()
UPSTREAM_PATH = get_upstream_path()


def load_catalog():
    """Load catalog.json."""
    if not CATALOG_PATH.exists():
        console.print("[red]Error: catalog.json not found. Run 'agenticq update' first.[/red]")
        raise typer.Exit(1)
    return json.loads(CATALOG_PATH.read_text(encoding='utf-8'))


def load_taxonomy():
    """Load taxonomy.json."""
    if not TAXONOMY_PATH.exists():
        console.print("[red]Error: taxonomy.json not found.[/red]")
        raise typer.Exit(1)
    return json.loads(TAXONOMY_PATH.read_text(encoding='utf-8'))


@app.command()
def browse():
    """Browse available domains and plugins."""
    taxonomy = load_taxonomy()
    catalog = load_catalog()

    console.print("\n[bold cyan]AgenticQ Domain Browser[/bold cyan]\n")

    for domain in taxonomy.get("domains", []):
        icon = domain.get("icon", "📦")
        name = domain.get("display_name", "")
        desc = domain.get("description", "")
        plugins = domain.get("plugins", [])

        panel = Panel(
            f"{desc}\n\n[dim]Plugins: {len(plugins)}[/dim]",
            title=f"{icon} {name}",
            border_style="cyan",
        )
        console.print(panel)


@app.command()
def search(query: str):
    """Search plugins, agents, and skills."""
    catalog = load_catalog()
    query_lower = query.lower()

    results = []
    for plugin in catalog.get("plugins", []):
        if query_lower in plugin["name"].lower() or query_lower in plugin.get("description", "").lower():
            results.append(("plugin", plugin["name"], plugin.get("description", "")))

        for agent in plugin.get("agents", []):
            if query_lower in agent["name"].lower() or query_lower in agent.get("description", "").lower():
                results.append(("agent", f"{plugin['name']}/{agent['name']}", agent.get("description", "")))

        for skill in plugin.get("skills", []):
            if query_lower in skill["name"].lower() or query_lower in skill.get("description", "").lower():
                results.append(("skill", f"{plugin['name']}/{skill['name']}", skill.get("description", "")))

    if not results:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Description")

    for result_type, name, desc in results[:20]:
        table.add_row(result_type, name, desc[:80] + "..." if len(desc) > 80 else desc)

    console.print(table)
    console.print(f"\n[dim]Showing {min(len(results), 20)} of {len(results)} results[/dim]")


@app.command()
def info(plugin_name: str):
    """Show detailed information about a plugin."""
    catalog = load_catalog()

    plugin = None
    for p in catalog.get("plugins", []):
        if p["name"] == plugin_name:
            plugin = p
            break

    if not plugin:
        console.print(f"[red]Plugin '{plugin_name}' not found.[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold cyan]{plugin['name']}[/bold cyan] v{plugin.get('version', 'unknown')}")
    console.print(f"{plugin.get('description', '')}\n")
    console.print(f"[dim]Category: {plugin.get('category', 'general')}[/dim]")
    console.print(f"[dim]License: {plugin.get('license', 'unknown')}[/dim]\n")

    if plugin.get("agents"):
        console.print("[bold]Agents:[/bold]")
        for agent in plugin["agents"]:
            console.print(f"  • {agent['name']}: {agent.get('description', '')}")

    if plugin.get("skills"):
        console.print("\n[bold]Skills:[/bold]")
        for skill in plugin["skills"]:
            console.print(f"  • {skill['name']}: {skill.get('description', '')}")

    if plugin.get("commands"):
        console.print("\n[bold]Commands:[/bold]")
        for cmd in plugin["commands"]:
            console.print(f"  • {cmd['name']}: {cmd.get('description', '')}")

    console.print(f"\n[dim]Total tokens: ~{plugin.get('total_tokens', 0):,}[/dim]")


@app.command()
def recommend(
    path: str = typer.Option(".", help="Project path to analyze"),
    domain: str = typer.Option(None, help="Filter by specific domain"),
    max_results: int = typer.Option(10, help="Maximum number of recommendations"),
):
    """Analyze project and recommend plugins."""
    console.print("[cyan]Scanning project...[/cyan]")
    profile = scan_project(path)

    console.print(f"\n[bold]Detected:[/bold]")
    console.print(f"  Languages: {', '.join(profile.languages) or 'none'}")
    console.print(f"  Frameworks: {', '.join(profile.frameworks) or 'none'}")
    console.print(f"  Infrastructure: {', '.join(profile.infrastructure) or 'none'}")
    console.print(f"  Databases: {', '.join(profile.databases) or 'none'}")
    console.print(f"  Testing: {', '.join(profile.testing_tools) or 'none'}\n")

    taxonomy = load_taxonomy()
    catalog = load_catalog()

    console.print("[cyan]Classifying domains...[/cyan]")
    domains = classify_project(profile, taxonomy)

    console.print("\n[bold]Relevant Domains:[/bold]")
    for domain_id, score in domains[:5]:
        console.print(f"  • {domain_id}: {score:.1f}%")

    console.print("\n[cyan]Generating recommendations...[/cyan]\n")
    recommendations = recommend_plugins(profile, domains, CATALOG_PATH, TAXONOMY_PATH, max_results)

    if not recommendations:
        console.print("[yellow]No recommendations found.[/yellow]")
        return

    table = Table(title="Recommended Plugins")
    table.add_column("Plugin", style="green")
    table.add_column("Score", justify="right", style="cyan")
    table.add_column("Tokens", justify="right", style="yellow")
    table.add_column("Reason")

    for rec in recommendations:
        table.add_row(
            rec.plugin_name,
            f"{rec.relevance_score:.1f}",
            f"{rec.token_cost_estimate:,}",
            rec.reason,
        )

    console.print(table)


@app.command()
def scaffold(
    plugins: list[str] = typer.Argument(..., help="Plugin names to scaffold"),
    harness: str = typer.Option("claude-code", help="Target harness (claude-code, cursor, gemini, codex, opencode, copilot)"),
    target: str = typer.Option(".", help="Target directory"),
):
    """Scaffold plugins into your project."""
    catalog = load_catalog()

    console.print(f"[cyan]Scaffolding {len(plugins)} plugins for {harness}...[/cyan]\n")

    result = scaffold_plugins(
        plugins, catalog, UPSTREAM_PATH, Path(target), harness
    )

    if result.success:
        console.print(f"[green]✓ {result.message}[/green]")
        console.print(f"\n[dim]Created {len(result.files_created)} files[/dim]")
    else:
        console.print(f"[red]✗ {result.message}[/red]")
        raise typer.Exit(1)


@app.command()
def build(
    plugins: list[str] = typer.Argument(..., help="Plugin names to include in the agent"),
    path: str = typer.Option(".", help="Project path to analyze"),
    output: str = typer.Option(None, help="Output file path (default: agent-config.json)"),
):
    """Build a custom runtime agent from selected plugins."""
    console.print("[cyan]Building runtime agent...[/cyan]\n")

    profile = scan_project(path)
    taxonomy = load_taxonomy()
    catalog = load_catalog()

    console.print(f"[bold]Project Profile:[/bold]")
    console.print(f"  Languages: {', '.join(profile.languages) or 'none'}")
    console.print(f"  Frameworks: {', '.join(profile.frameworks) or 'none'}\n")

    try:
        agent_config = build_runtime_agent(profile, plugins, catalog, taxonomy)

        output_path = Path(output) if output else Path("agent-config.json")
        output_path.write_text(json.dumps(agent_config, indent=2), encoding='utf-8')

        console.print(f"[green]✓ Runtime agent built successfully[/green]")
        console.print(f"\n[dim]Saved to: {output_path}[/dim]")
        console.print(f"[dim]Plugins: {len(plugins)}[/dim]")
        console.print(f"[dim]Total capabilities: {len(agent_config.get('capabilities', []))}[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Error building agent: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def update():
    """Update catalog from upstream repository."""
    console.print("[cyan]Updating catalog from upstream...[/cyan]\n")

    if not UPSTREAM_PATH.exists():
        console.print(f"[red]Upstream repository not found at {UPSTREAM_PATH}[/red]")
        console.print("[yellow]Clone it first: git clone https://github.com/wshobson/agents.git[/yellow]")
        raise typer.Exit(1)

    try:
        catalog = build_catalog(UPSTREAM_PATH, CATALOG_PATH)
        console.print("\n[green]✓ Catalog updated successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def gui(
    host: str = typer.Option("127.0.0.1", help="Host to bind the web server to"),
    port: int = typer.Option(8080, help="Port to serve the web GUI on"),
):
    """Launch the standalone web GUI dashboard."""
    if not CATALOG_PATH.exists():
        console.print("[yellow]Catalog not found. Run 'agenticq update' first.[/yellow]")
        raise typer.Exit(1)

    from .server.web import WebServer

    console.print(f"[cyan]Starting AgenticQ Web GUI at http://{host}:{port}[/cyan]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]")
    WebServer().run(host=host, port=port)


@app.command()
def serve(
    jsonrpc: bool = typer.Option(
        False, "--jsonrpc", help="Run the JSON-RPC server over stdin/stdout (used by the VS Code extension)"
    ),
    host: str = typer.Option("127.0.0.1", help="Host for the HTTP server (when --jsonrpc is not set)"),
    port: int = typer.Option(8080, help="Port for the HTTP server (when --jsonrpc is not set)"),
):
    """Run a backend server.

    With --jsonrpc, speaks JSON-RPC 2.0 over stdin/stdout for the VS Code
    extension. Without it, serves the HTTP API + web GUI.
    """
    if jsonrpc:
        from .server.jsonrpc import JSONRPCServer

        JSONRPCServer().run()
    else:
        from .server.web import WebServer

        console.print(f"[cyan]Starting AgenticQ HTTP server at http://{host}:{port}[/cyan]")
        WebServer().run(host=host, port=port)


@app.command()
def version():
    """Show version information."""
    console.print("[bold cyan]AgenticQ[/bold cyan] v0.1.0")
    console.print("Intelligent Agent Scaffolding Engine")
    console.print("\nSource: https://github.com/wshobson/agents")


if __name__ == "__main__":
    app()
