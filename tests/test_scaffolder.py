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
