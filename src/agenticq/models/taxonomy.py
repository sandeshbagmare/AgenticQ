"""Taxonomy and domain mapping data models."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Domain(BaseModel):
    """Represents a domain in the taxonomy."""

    id: str
    name: str
    description: str
    parent: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    related_domains: List[str] = Field(default_factory=list)


class DomainMapping(BaseModel):
    """Maps project indicators to domains."""

    languages: Dict[str, List[str]] = Field(default_factory=dict)
    frameworks: Dict[str, List[str]] = Field(default_factory=dict)
    tools: Dict[str, List[str]] = Field(default_factory=dict)
    file_patterns: Dict[str, List[str]] = Field(default_factory=dict)
