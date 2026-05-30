"""Plugin-related data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Command(BaseModel):
    """Represents a command within a skill."""

    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None


class Skill(BaseModel):
    """Represents a skill provided by a plugin."""

    name: str
    description: str
    commands: List[Command] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Agent(BaseModel):
    """Represents an agent provided by a plugin."""

    name: str
    description: str
    capabilities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Plugin(BaseModel):
    """Represents a plugin in the catalog."""

    id: str
    name: str
    version: str
    description: str
    author: Optional[str] = None
    repository: Optional[str] = None
    domains: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    agents: List[Agent] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
