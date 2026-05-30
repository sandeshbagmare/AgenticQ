"""Catalog indexer for wshobson/agents marketplace."""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import yaml


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None


def estimate_tokens(text: str) -> int:
    """Rough token estimate: chars / 4."""
    return len(text) // 4


def index_plugin(plugin_dir: Path, plugin_meta: Dict[str, Any]) -> Dict[str, Any]:
    """Index a single plugin directory."""
    plugin_data = {
        "name": plugin_meta.get("name", plugin_dir.name),
        "version": plugin_meta.get("version", "1.0.0"),
        "description": plugin_meta.get("description", ""),
        "category": plugin_meta.get("category", "general"),
        "author": plugin_meta.get("author", {}),
        "homepage": plugin_meta.get("homepage", ""),
        "license": plugin_meta.get("license", "MIT"),
        "agents": [],
        "skills": [],
        "commands": [],
        "total_tokens": 0,
    }

    # Index agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            content = agent_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            if frontmatter:
                agent_data = {
                    "name": frontmatter.get("name", agent_file.stem),
                    "description": frontmatter.get("description", ""),
                    "model": frontmatter.get("model"),
                    "token_estimate": estimate_tokens(content),
                }
                plugin_data["agents"].append(agent_data)
                plugin_data["total_tokens"] += agent_data["token_estimate"]

    # Index skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    content = skill_file.read_text(encoding='utf-8')
                    frontmatter = extract_frontmatter(content)
                    if frontmatter:
                        skill_data = {
                            "name": frontmatter.get("name", skill_dir.name),
                            "description": frontmatter.get("description", ""),
                            "token_estimate": estimate_tokens(content),
                        }
                        plugin_data["skills"].append(skill_data)
                        plugin_data["total_tokens"] += skill_data["token_estimate"]

    # Index commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.exists():
        for command_file in commands_dir.glob("*.md"):
            content = command_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            if frontmatter:
                command_data = {
                    "name": frontmatter.get("name", command_file.stem),
                    "description": frontmatter.get("description", ""),
                    "token_estimate": estimate_tokens(content),
                }
                plugin_data["commands"].append(command_data)
                plugin_data["total_tokens"] += command_data["token_estimate"]

    return plugin_data


def build_catalog(upstream_repo: Path, output_path: Path) -> Dict[str, Any]:
    """Build catalog from upstream repo."""
    # Read marketplace.json
    marketplace_file = upstream_repo / ".claude-plugin" / "marketplace.json"
    if not marketplace_file.exists():
        raise FileNotFoundError(f"Marketplace file not found: {marketplace_file}")

    marketplace = json.loads(marketplace_file.read_text(encoding='utf-8'))

    catalog = {
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_repo": "https://github.com/wshobson/agents",
        "source_version": marketplace.get("metadata", {}).get("version", "unknown"),
        "plugins": [],
    }

    plugins_dir = upstream_repo / "plugins"

    # Index each plugin
    for plugin_meta in marketplace.get("plugins", []):
        plugin_name = plugin_meta["name"]
        plugin_dir = plugins_dir / plugin_name

        if plugin_dir.exists():
            try:
                plugin_data = index_plugin(plugin_dir, plugin_meta)
                catalog["plugins"].append(plugin_data)
                print(f"✓ Indexed {plugin_name}: {len(plugin_data['agents'])} agents, {len(plugin_data['skills'])} skills, {len(plugin_data['commands'])} commands")
            except Exception as e:
                print(f"✗ Failed to index {plugin_name}: {e}")
        else:
            print(f"⚠ Plugin directory not found: {plugin_dir}")

    # Write catalog
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(catalog, indent=2), encoding='utf-8')

    # Print summary
    total_agents = sum(len(p["agents"]) for p in catalog["plugins"])
    total_skills = sum(len(p["skills"]) for p in catalog["plugins"])
    total_commands = sum(len(p["commands"]) for p in catalog["plugins"])
    total_tokens = sum(p["total_tokens"] for p in catalog["plugins"])

    print(f"\n{'='*60}")
    print(f"Catalog generated: {output_path}")
    print(f"{'='*60}")
    print(f"Plugins:  {len(catalog['plugins'])}")
    print(f"Agents:   {total_agents}")
    print(f"Skills:   {total_skills}")
    print(f"Commands: {total_commands}")
    print(f"Total estimated tokens: {total_tokens:,}")
    print(f"{'='*60}")

    return catalog


if __name__ == "__main__":
    import sys

    upstream = Path(r"C:\Users\sande\AppData\Local\Temp\wshobson-agents-research")
    output = Path(__file__).parent.parent / "data" / "catalog.json"

    if not upstream.exists():
        print(f"Error: Upstream repo not found at {upstream}")
        print("Run: git clone https://github.com/wshobson/agents.git <path>")
        sys.exit(1)

    try:
        catalog = build_catalog(upstream, output)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
