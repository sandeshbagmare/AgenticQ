"""Test the catalog indexer."""

import pytest
from pathlib import Path
from agenticq.core.catalog import extract_frontmatter, estimate_tokens


def test_extract_frontmatter():
    """Test YAML frontmatter extraction."""
    content = """---
name: test-agent
description: Test description
model: opus
---

# Agent Content

This is the agent content.
"""

    frontmatter = extract_frontmatter(content)

    assert frontmatter is not None
    assert frontmatter["name"] == "test-agent"
    assert frontmatter["description"] == "Test description"
    assert frontmatter["model"] == "opus"


def test_extract_frontmatter_no_frontmatter():
    """Test extraction with no frontmatter."""
    content = "# Just a heading\n\nNo frontmatter here."

    frontmatter = extract_frontmatter(content)

    assert frontmatter is None


def test_estimate_tokens():
    """Test token estimation."""
    text = "This is a test string with some content."

    tokens = estimate_tokens(text)

    # Rough estimate: chars / 4
    expected = len(text) // 4
    assert tokens == expected


def test_estimate_tokens_empty():
    """Test token estimation with empty string."""
    tokens = estimate_tokens("")
    assert tokens == 0
