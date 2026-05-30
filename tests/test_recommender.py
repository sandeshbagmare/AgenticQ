"""Test the recommender."""

import pytest
from pathlib import Path
from agenticq.core.recommender import Recommender, PluginRecommendation
from agenticq.models.project import ProjectProfile


def test_recommender_basic():
    """Test basic recommendation functionality."""
    # Create mock catalog
    catalog = {
        "plugins": [
            {
                "name": "python-development",
                "description": "Python development plugin",
                "category": "languages",
                "total_tokens": 10000,
                "agents": [],
                "skills": [],
                "commands": [],
            }
        ]
    }

    # Create mock taxonomy
    taxonomy = {
        "domains": [
            {
                "domain_id": "python-development",
                "display_name": "Python Development",
                "plugins": ["python-development"],
            }
        ]
    }

    # Mock paths (won't be used since we pass data directly)
    catalog_path = Path("dummy")
    taxonomy_path = Path("dummy")

    recommender = Recommender.__new__(Recommender)
    recommender.catalog = catalog
    recommender.taxonomy = taxonomy

    profile = ProjectProfile(languages=["python"])
    domains = [("python-development", 90.0)]

    recommendations = recommender.recommend(profile, domains, max_results=5)

    assert len(recommendations) > 0
    assert isinstance(recommendations[0], PluginRecommendation)
    assert recommendations[0].plugin_name == "python-development"


def test_plugin_recommendation():
    """Test PluginRecommendation model."""
    rec = PluginRecommendation(
        plugin_name="test-plugin",
        relevance_score=85.5,
        token_cost_estimate=5000,
        reason="Test reason",
        conflicts=["other-plugin"],
    )

    assert rec.plugin_name == "test-plugin"
    assert rec.relevance_score == 85.5
    assert rec.token_cost_estimate == 5000
    assert "other-plugin" in rec.conflicts
