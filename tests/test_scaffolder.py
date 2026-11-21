"""Test the scaffolder."""

import pytest
from pathlib import Path
from agenticq.core.scaffolder import Scaffolder, ScaffoldResult


def test_scaffold_result():
    """Test ScaffoldResult model."""
    result = ScaffoldResult(
        success=True,
        message="Scaffolded successfully",
        files_created=["file1.py", "file2.py"],
    )

    assert result.success is True
    assert result.message == "Scaffolded successfully"
    assert len(result.files_created) == 2


def test_scaffolder_initialization():
    """Test Scaffolder initialization."""
    catalog = {"plugins": []}
    upstream_path = Path("/tmp/test")

    scaffolder = Scaffolder(catalog, upstream_path)

    assert scaffolder.catalog == catalog
    assert scaffolder.upstream_path == upstream_path


def test_scaffold_unknown_harness():
    """Test scaffolding with unknown harness."""
    catalog = {"plugins": []}
    upstream_path = Path("/tmp/test")

    scaffolder = Scaffolder(catalog, upstream_path)
    result = scaffolder.scaffold(["test-plugin"], Path("."), "unknown-harness")

    assert result.success is False
    assert "Unknown harness" in result.message


@pytest.fixture
def scaffolder_with_plugin(tmp_path):
    upstream_path = tmp_path / "upstream"
    agents_dir = upstream_path / "plugins" / "python-development" / "agents"
    agents_dir.mkdir(parents=True)
    (agents_dir / "python-pro.md").write_text("# Python agent\n", encoding="utf-8")
    catalog = {"plugins": [{"name": "python-development"}]}
    return Scaffolder(catalog, upstream_path)


@pytest.mark.parametrize(
    "plugin_names",
    [
        ["pyhton-development"],
        ["python-development", "pyhton-development"],
    ],
)
def test_scaffold_unknown_plugin_creates_no_files(scaffolder_with_plugin, tmp_path, plugin_names):
    target = tmp_path / "project"

    result = scaffolder_with_plugin.scaffold(plugin_names, target)

    assert result.success is False
    assert "pyhton-development" in result.message
    assert result.files_created == []
    assert not target.exists()


def test_scaffold_known_plugin_copies_agent(scaffolder_with_plugin, tmp_path):
    target = tmp_path / "project"

    result = scaffolder_with_plugin.scaffold(["python-development"], target)

    agent_file = target / ".claude" / "plugins" / "python-development" / "agents" / "python-pro.md"
    assert result.success is True
    assert result.files_created == [str(agent_file)]
    assert agent_file.read_text(encoding="utf-8") == "# Python agent\n"
