"""Plugin recommendation engine."""

from typing import List, Tuple, Dict, Any
from pathlib import Path
import json
from ..models.project import ProjectProfile
from ..models.taxonomy import Domain


class PluginRecommendation:
    """Represents a plugin recommendation."""

    def __init__(
        self,
        plugin_name: str,
        relevance_score: float,
        token_cost_estimate: int,
        reason: str,
        conflicts: List[str] = None,
    ):
        self.plugin_name = plugin_name
        self.relevance_score = relevance_score
        self.token_cost_estimate = token_cost_estimate
        self.reason = reason
        self.conflicts = conflicts or []

    def __repr__(self):
        return f"<PluginRecommendation {self.plugin_name} score={self.relevance_score:.2f}>"


class Recommender:
    """Recommends plugins based on project profile and domains."""

    def __init__(self, catalog_path: Path, taxonomy_path: Path):
        self.catalog = self._load_catalog(catalog_path)
        self.taxonomy = self._load_taxonomy(taxonomy_path)

    def _load_catalog(self, path: Path) -> Dict[str, Any]:
        """Load catalog.json."""
        if not path.exists():
            return {"plugins": []}
        return json.loads(path.read_text(encoding='utf-8'))

    def _load_taxonomy(self, path: Path) -> Dict[str, Any]:
        """Load taxonomy.json."""
        if not path.exists():
            return {"domains": []}
        return json.loads(path.read_text(encoding='utf-8'))

    def recommend(
        self,
        profile: ProjectProfile,
        domains: List[Tuple[str, float]],
        max_results: int = 10,
    ) -> List[PluginRecommendation]:
        """Generate plugin recommendations."""
        recommendations = []

        # Build domain plugin mapping
        domain_plugins = {}
        for domain in self.taxonomy.get("domains", []):
            domain_id = domain["domain_id"]
            domain_plugins[domain_id] = domain.get("plugins", [])

        # Score each plugin
        plugin_scores = {}
        for domain_id, domain_score in domains:
            if domain_id in domain_plugins:
                for plugin_name in domain_plugins[domain_id]:
                    if plugin_name not in plugin_scores:
                        plugin_scores[plugin_name] = 0.0
                    plugin_scores[plugin_name] += domain_score

        # Get plugin details from catalog
        catalog_plugins = {p["name"]: p for p in self.catalog.get("plugins", [])}

        # Create recommendations
        for plugin_name, score in sorted(
            plugin_scores.items(), key=lambda x: x[1], reverse=True
        )[:max_results]:
            plugin_data = catalog_plugins.get(plugin_name, {})
            token_cost = plugin_data.get("total_tokens", 0)

            # Generate reason
            reason = self._generate_reason(plugin_name, plugin_data, profile, domains)

            # Detect conflicts (plugins with overlapping agents)
            conflicts = self._detect_conflicts(plugin_name, plugin_data, catalog_plugins)

            recommendations.append(
                PluginRecommendation(
                    plugin_name=plugin_name,
                    relevance_score=min(score, 100.0),
                    token_cost_estimate=token_cost,
                    reason=reason,
                    conflicts=conflicts,
                )
            )

        return recommendations

    def _generate_reason(
        self,
        plugin_name: str,
        plugin_data: Dict[str, Any],
        profile: ProjectProfile,
        domains: List[Tuple[str, float]],
    ) -> str:
        """Generate a human-readable reason for the recommendation."""
        reasons = []

        # Match languages
        if "python" in profile.languages and "python" in plugin_name.lower():
            reasons.append("matches Python project")
        if "javascript" in profile.languages or "typescript" in profile.languages:
            if "javascript" in plugin_name.lower() or "typescript" in plugin_name.lower():
                reasons.append("matches JS/TS project")

        # Match frameworks
        for fw in profile.frameworks:
            if fw.lower() in plugin_data.get("description", "").lower():
                reasons.append(f"supports {fw}")

        # Match infrastructure
        if profile.infrastructure:
            if "cloud" in plugin_name.lower() or "kubernetes" in plugin_name.lower():
                reasons.append("matches infrastructure needs")

        # Match testing
        if profile.testing_tools and "test" in plugin_name.lower():
            reasons.append("supports testing workflow")

        # Default reason
        if not reasons:
            category = plugin_data.get("category", "general")
            reasons.append(f"relevant for {category} development")

        return ", ".join(reasons)

    def _detect_conflicts(
        self,
        plugin_name: str,
        plugin_data: Dict[str, Any],
        all_plugins: Dict[str, Dict[str, Any]],
    ) -> List[str]:
        """Detect conflicting plugins (overlapping agent roles)."""
        conflicts = []

        # Get agent names from this plugin
        agent_names = {a["name"] for a in plugin_data.get("agents", [])}

        # Check other plugins for same agent names
        for other_name, other_data in all_plugins.items():
            if other_name == plugin_name:
                continue

            other_agents = {a["name"] for a in other_data.get("agents", [])}
            if agent_names & other_agents:  # Intersection
                conflicts.append(other_name)

        return conflicts


def recommend_plugins(
    profile: ProjectProfile,
    domains: List[Tuple[str, float]],
    catalog_path: Path,
    taxonomy_path: Path,
    max_results: int = 10,
) -> List[PluginRecommendation]:
    """Convenience function to get recommendations."""
    recommender = Recommender(catalog_path, taxonomy_path)
    return recommender.recommend(profile, domains, max_results)
