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

app = typer.Typer(
    name="agenticq",
    help="AgenticQ - Intelligent Agent Scaffolding Engine",
    add_completion=False,
)
console = Console()

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CATALOG_PATH = DATA_DIR / "catalog.json"
TAXONOMY_PATH = DATA_DIR / "taxonomy.json"
UPSTREAM_PATH = Path(r"C:\Users\sande\AppData\Local\Temp\wshobson-agents-research")


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
def gui():
    """Launch web GUI."""
    console.print("[cyan]Starting web GUI...[/cyan]")
    console.print("[yellow]Web GUI not yet implemented. Use CLI commands for now.[/yellow]")


@app.command()
def version():
    """Show version information."""
    console.print("[bold cyan]AgenticQ[/bold cyan] v0.1.0")
    console.print("Intelligent Agent Scaffolding Engine")
    console.print("\nSource: https://github.com/wshobson/agents")


if __name__ == "__main__":
    app()
