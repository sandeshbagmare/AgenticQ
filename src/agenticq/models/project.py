"""Project profile data models."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ProjectProfile(BaseModel):
    """Represents a detected project stack and configuration."""

    project_path: str = Field(default=".")
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    infrastructure: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    testing_tools: List[str] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)

    # Aliases for classifier compatibility
    @property
    def detected_languages(self) -> List[str]:
        return self.languages

    @property
    def detected_frameworks(self) -> List[str]:
        return self.frameworks

    @property
    def detected_tools(self) -> List[str]:
        return self.infrastructure + self.databases + self.testing_tools

    @property
    def package_managers(self) -> List[str]:
        return []

    @property
    def build_systems(self) -> List[str]:
        return []
