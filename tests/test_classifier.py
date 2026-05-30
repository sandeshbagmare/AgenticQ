"""Test the classifier."""

import pytest
from pathlib import Path
from agenticq.core.classifier import classify_project
from agenticq.models.project import ProjectProfile


def test_classify_python_project():
    """Test classification of a Python project."""
    profile = ProjectProfile(
        languages=["python"],
        frameworks=["fastapi"],
        infrastructure=["docker"],
        databases=["postgresql"],
        testing_tools=["pytest"],
    )

    taxonomy = {
        "domains": [
            {
                "domain_id": "python-development",
                "display_name": "Python Development",
                "file_detection_heuristics": ["pyproject.toml", "*.py", "fastapi"],
            },
            {
                "domain_id": "backend-apis",
                "display_name": "Backend & APIs",
                "file_detection_heuristics": ["fastapi", "api"],
            },
        ]
    }

    results = classify_project(profile, taxonomy)

    assert len(results) > 0
    assert results[0][0] in ["python-development", "backend-apis"]
    assert results[0][1] > 0


def test_classify_javascript_project():
    """Test classification of a JavaScript project."""
    profile = ProjectProfile(
        languages=["javascript", "typescript"],
        frameworks=["react", "nextjs"],
        infrastructure=[],
        databases=[],
        testing_tools=["jest"],
    )

    taxonomy = {
        "domains": [
            {
                "domain_id": "javascript-typescript",
                "display_name": "JavaScript/TypeScript",
                "file_detection_heuristics": ["package.json", "*.ts", "*.js"],
            }
        ]
    }

    results = classify_project(profile, taxonomy)

    assert len(results) > 0
    assert results[0][0] == "javascript-typescript"


def test_empty_profile():
    """Test classification with empty profile."""
    profile = ProjectProfile()

    taxonomy = {"domains": []}

    results = classify_project(profile, taxonomy)

    assert len(results) == 0
