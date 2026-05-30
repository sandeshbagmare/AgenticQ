"""Configuration helpers for AgenticQ.

Centralizes path resolution and environment-based configuration.
"""
import os
from pathlib import Path


def get_upstream_path() -> Path:
    """Get the upstream marketplace repository path.

    Checks AGENTICQ_UPSTREAM environment variable first, then falls back to
    a default location in the user's home directory.

    Returns:
        Path to the wshobson/agents repository clone.
    """
    env_path = os.getenv('AGENTICQ_UPSTREAM')
    if env_path:
        return Path(env_path)

    # Default: ~/.agenticq/upstream
    default = Path.home() / '.agenticq' / 'upstream'
    return default


def get_catalog_path() -> Path:
    """Get the path to catalog.json (in the package data directory)."""
    return Path(__file__).parent / "data" / "catalog.json"


def get_taxonomy_path() -> Path:
    """Get the path to taxonomy.json (in the package data directory)."""
    return Path(__file__).parent / "data" / "taxonomy.json"
