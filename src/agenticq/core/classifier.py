"""Domain classifier that maps ProjectProfile to Domains with scoring."""

from typing import List, Tuple, Dict, Set
import json
from pathlib import Path

from agenticq.models.project import ProjectProfile
from agenticq.models.taxonomy import Domain, DomainMapping


class Taxonomy:
    """Container for taxonomy data including domains and mappings."""

    def __init__(self, domains: List[Domain], mapping: DomainMapping):
        self.domains = domains
        self.mapping = mapping
        self._domain_by_id = {d.id: d for d in domains}

    def get_domain(self, domain_id: str) -> Domain:
        """Get domain by ID."""
        return self._domain_by_id.get(domain_id)

    @classmethod
    def from_json(cls, json_path: str) -> "Taxonomy":
        """Load taxonomy from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        domains = [Domain(**d) for d in data.get('domains', [])]
        mapping = DomainMapping(**data.get('mapping', {}))

        return cls(domains=domains, mapping=mapping)


def classify_project(profile: ProjectProfile, taxonomy_data: dict) -> List[Tuple[str, float]]:
    """
    Classify a project profile against taxonomy domains.

    Args:
        profile: The detected project profile
        taxonomy_data: The taxonomy dict with domains

    Returns:
        List of (domain_id, score) tuples, sorted by score descending.
        Scores range from 0-100.
    """
    domain_scores: Dict[str, float] = {}

    language_aliases = {
        "python": [".py", "pyproject.toml", "requirements.txt", "setup.py"],
        "javascript": [".js", "package.json", "node", "npm", "yarn"],
        "typescript": [".ts", "tsconfig.json"],
        "rust": [".rs", "cargo.toml"],
        "go": [".go", "go.mod"],
        "java": [".java", "pom.xml", "build.gradle"],
        "c/c++": [".c", ".cc", ".cpp", ".h", "cmakelists.txt", "makefile"],
        "ruby": [".rb", "gemfile"],
        "php": [".php", "composer.json"],
    }

    # Initialize all domains with 0 score
    for domain in taxonomy_data.get("domains", []):
        domain_id = domain["domain_id"]
        domain_scores[domain_id] = 0.0

        # Score based on file detection heuristics
        heuristics = [h.lower() for h in domain.get("file_detection_heuristics", [])]

        def matches_tokens(tokens: List[str]) -> bool:
            return any(any(token in h for h in heuristics) for token in tokens)

        # Match languages
        for lang in profile.languages:
            lang_lower = lang.lower()
            tokens = [lang_lower] + language_aliases.get(lang_lower, [])
            if matches_tokens([t.lower() for t in tokens]):
                domain_scores[domain_id] += 30.0
                break

        # Match frameworks
        for fw in profile.frameworks:
            if matches_tokens([fw.lower()]):
                domain_scores[domain_id] += 40.0
                break

        # Match infrastructure
        for infra in profile.infrastructure:
            if matches_tokens([infra.lower()]):
                domain_scores[domain_id] += 20.0
                break

    # Build result list
    results = [(domain_id, score) for domain_id, score in domain_scores.items() if score > 0]
    results.sort(key=lambda x: x[1], reverse=True)

    return results


