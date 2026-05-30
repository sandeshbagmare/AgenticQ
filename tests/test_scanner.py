"""Test the project scanner."""

import pytest
from pathlib import Path
from agenticq.core.scanner import ProjectScanner, scan_project


def test_scanner_detects_python(tmp_path):
    """Test scanner detects Python projects."""
    # Create a pyproject.toml
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'")

    scanner = ProjectScanner(tmp_path)
    profile = scanner.scan()

    assert "python" in profile.languages


def test_scanner_detects_javascript(tmp_path):
    """Test scanner detects JavaScript projects."""
    # Create a package.json
    (tmp_path / "package.json").write_text('{"name": "test"}')

    scanner = ProjectScanner(tmp_path)
    profile = scanner.scan()

    assert "javascript" in profile.languages


def test_scanner_detects_docker(tmp_path):
    """Test scanner detects Docker."""
    (tmp_path / "Dockerfile").write_text("FROM python:3.11")

    scanner = ProjectScanner(tmp_path)
    profile = scanner.scan()

    assert "docker" in profile.infrastructure


def test_scanner_detects_testing(tmp_path):
    """Test scanner detects testing tools."""
    (tmp_path / "pytest.ini").write_text("[pytest]")

    scanner = ProjectScanner(tmp_path)
    profile = scanner.scan()

    assert "pytest" in profile.testing_tools or "test-directory" in profile.testing_tools


def test_scan_project_convenience():
    """Test the convenience function."""
    profile = scan_project(".")

    # Should return a valid profile
    assert isinstance(profile.languages, list)
    assert isinstance(profile.frameworks, list)
