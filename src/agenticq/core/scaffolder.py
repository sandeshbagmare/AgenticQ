"""Multi-harness scaffolder for agent plugins."""

from pathlib import Path
from typing import List, Dict, Any
import json
import shutil


class ScaffoldResult:
    """Result of a scaffolding operation."""

    def __init__(self, success: bool, message: str, files_created: List[str] = None):
        self.success = success
        self.message = message
        self.files_created = files_created or []


class Scaffolder:
    """Scaffolds plugins for multiple harnesses."""

    def __init__(self, catalog: Dict[str, Any], upstream_path: Path):
        self.catalog = catalog
        self.upstream_path = upstream_path
        self.catalog_plugins = {p["name"]: p for p in catalog.get("plugins", [])}

    def scaffold(
        self, plugin_names: List[str], target_dir: Path, harness: str = "claude-code"
    ) -> ScaffoldResult:
        """Scaffold plugins for the specified harness."""
        harness_methods = {
            "claude-code": self.scaffold_claude_code,
            "cursor": self.scaffold_cursor,
            "gemini": self.scaffold_gemini,
            "codex": self.scaffold_codex,
            "opencode": self.scaffold_opencode,
            "copilot": self.scaffold_copilot,
        }

        method = harness_methods.get(harness)
        if not method:
            return ScaffoldResult(
                False, f"Unknown harness: {harness}. Supported: {list(harness_methods.keys())}"
            )

        return method(plugin_names, target_dir)

    def scaffold_claude_code(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for Claude Code."""
        files_created = []
        plugins_dir = target_dir / ".claude" / "plugins"
        plugins_dir.mkdir(parents=True, exist_ok=True)

        for plugin_name in plugin_names:
            if plugin_name not in self.catalog_plugins:
                continue

            source_plugin = self.upstream_path / "plugins" / plugin_name
            if not source_plugin.exists():
                continue

            target_plugin = plugins_dir / plugin_name
            target_plugin.mkdir(exist_ok=True)

            # Copy agents
            if (source_plugin / "agents").exists():
                target_agents = target_plugin / "agents"
                target_agents.mkdir(exist_ok=True)
                for agent_file in (source_plugin / "agents").glob("*.md"):
                    shutil.copy2(agent_file, target_agents / agent_file.name)
                    files_created.append(str(target_agents / agent_file.name))

            # Copy skills
            if (source_plugin / "skills").exists():
                target_skills = target_plugin / "skills"
                target_skills.mkdir(exist_ok=True)
                for skill_dir in (source_plugin / "skills").iterdir():
                    if skill_dir.is_dir():
                        target_skill = target_skills / skill_dir.name
                        shutil.copytree(skill_dir, target_skill, dirs_exist_ok=True)
                        files_created.append(str(target_skill))

            # Copy commands
            if (source_plugin / "commands").exists():
                target_commands = target_plugin / "commands"
                target_commands.mkdir(exist_ok=True)
                for cmd_file in (source_plugin / "commands").glob("*.md"):
                    shutil.copy2(cmd_file, target_commands / cmd_file.name)
                    files_created.append(str(target_commands / cmd_file.name))

        return ScaffoldResult(
            True,
            f"Scaffolded {len(plugin_names)} plugins for Claude Code",
            files_created,
        )

    def scaffold_cursor(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for Cursor."""
        files_created = []
        cursor_dir = target_dir / ".cursor-plugin"
        cursor_dir.mkdir(parents=True, exist_ok=True)

        plugins_dir = cursor_dir / "plugins"
        plugins_dir.mkdir(exist_ok=True)

        for plugin_name in plugin_names:
            if plugin_name not in self.catalog_plugins:
                continue

            # Read upstream cursor plugin.json
            source_cursor = (
                self.upstream_path / "plugins" / plugin_name / ".cursor-plugin"
            )
            if not source_cursor.exists():
                continue

            # Copy plugin.json if exists
            source_json = source_cursor / "plugin.json"
            if source_json.exists():
                target_json = plugins_dir / f"{plugin_name}.json"
                shutil.copy2(source_json, target_json)
                files_created.append(str(target_json))

        # Create .cursor/rules/ directory for MDC files
        rules_dir = target_dir / ".cursor" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        return ScaffoldResult(
            True, f"Scaffolded {len(plugin_names)} plugins for Cursor", files_created
        )

    def scaffold_gemini(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for Gemini CLI."""
        files_created = []
        gemini_dir = target_dir / ".gemini"
        gemini_dir.mkdir(parents=True, exist_ok=True)

        # Create GEMINI.md with plugin references
        gemini_md = target_dir / "GEMINI.md"
        content = "# Gemini CLI Configuration\n\n"
        content += "## Installed Plugins\n\n"

        for plugin_name in plugin_names:
            if plugin_name in self.catalog_plugins:
                plugin = self.catalog_plugins[plugin_name]
                content += f"- **{plugin_name}**: {plugin.get('description', '')}\n"

        gemini_md.write_text(content, encoding='utf-8')
        files_created.append(str(gemini_md))

        return ScaffoldResult(
            True, f"Scaffolded {len(plugin_names)} plugins for Gemini CLI", files_created
        )

    def scaffold_codex(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for Codex CLI."""
        files_created = []
        codex_dir = target_dir / ".codex"
        codex_dir.mkdir(parents=True, exist_ok=True)

        agents_dir = codex_dir / "agents"
        skills_dir = codex_dir / "skills"
        agents_dir.mkdir(exist_ok=True)
        skills_dir.mkdir(exist_ok=True)

        for plugin_name in plugin_names:
            if plugin_name not in self.catalog_plugins:
                continue

            source_plugin = self.upstream_path / "plugins" / plugin_name

            # Copy agents
            if (source_plugin / "agents").exists():
                for agent_file in (source_plugin / "agents").glob("*.md"):
                    target_file = agents_dir / agent_file.name
                    shutil.copy2(agent_file, target_file)
                    files_created.append(str(target_file))

            # Copy skills
            if (source_plugin / "skills").exists():
                for skill_dir in (source_plugin / "skills").iterdir():
                    if skill_dir.is_dir():
                        target_skill = skills_dir / skill_dir.name
                        shutil.copytree(skill_dir, target_skill, dirs_exist_ok=True)
                        files_created.append(str(target_skill))

        return ScaffoldResult(
            True, f"Scaffolded {len(plugin_names)} plugins for Codex CLI", files_created
        )

    def scaffold_opencode(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for OpenCode."""
        # OpenCode uses a similar structure to Claude Code
        return self.scaffold_claude_code(plugin_names, target_dir)

    def scaffold_copilot(
        self, plugin_names: List[str], target_dir: Path
    ) -> ScaffoldResult:
        """Scaffold for GitHub Copilot."""
        files_created = []
        copilot_dir = target_dir / ".github" / "copilot"
        copilot_dir.mkdir(parents=True, exist_ok=True)

        instructions_file = copilot_dir / "instructions.md"
        content = "# GitHub Copilot Instructions\n\n"

        for plugin_name in plugin_names:
            if plugin_name in self.catalog_plugins:
                plugin = self.catalog_plugins[plugin_name]
                content += f"## {plugin_name}\n\n"
                content += f"{plugin.get('description', '')}\n\n"

        instructions_file.write_text(content, encoding='utf-8')
        files_created.append(str(instructions_file))

        return ScaffoldResult(
            True,
            f"Scaffolded {len(plugin_names)} plugins for GitHub Copilot",
            files_created,
        )


def scaffold_plugins(
    plugin_names: List[str],
    catalog: Dict[str, Any],
    upstream_path: Path,
    target_dir: Path,
    harness: str = "claude-code",
) -> ScaffoldResult:
    """Convenience function to scaffold plugins."""
    scaffolder = Scaffolder(catalog, upstream_path)
    return scaffolder.scaffold(plugin_names, target_dir, harness)
