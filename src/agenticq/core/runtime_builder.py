"""Runtime agent builder for dynamic, token-optimized agent generation."""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
import re

from ..models.project import ProjectProfile
from ..models.plugin import Plugin, Agent, Skill


@dataclass
class RuntimeAgentConfig:
    """Configuration for a dynamically generated runtime agent."""

    agent_prompt: str
    skills_included: List[str]
    token_estimate: int
    token_savings: int
    metadata: Optional[Dict[str, Any]] = None


class Catalog:
    """Catalog interface for plugin lookup."""

    def __init__(self, plugins: List[Plugin]):
        self.plugins = {p.id: p for p in plugins}

    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Retrieve a plugin by ID."""
        return self.plugins.get(plugin_id)

    def get_plugins(self, plugin_ids: List[str]) -> List[Plugin]:
        """Retrieve multiple plugins by ID."""
        return [self.plugins[pid] for pid in plugin_ids if pid in self.plugins]


class RuntimeBuilder:
    """Builds token-optimized runtime agents from project profiles and plugins."""

    # Estimated tokens per character (rough approximation: ~4 chars per token)
    CHARS_PER_TOKEN = 4

    def __init__(self):
        self.section_extractors = {
            'python': self._extract_python_sections,
            'javascript': self._extract_javascript_sections,
            'typescript': self._extract_typescript_sections,
            'react': self._extract_react_sections,
            'vue': self._extract_vue_sections,
            'django': self._extract_django_sections,
            'fastapi': self._extract_fastapi_sections,
            'express': self._extract_express_sections,
        }

    def build_runtime_agent(
        self,
        profile: ProjectProfile,
        plugins: List[str],
        catalog: Catalog
    ) -> RuntimeAgentConfig:
        """
        Build a runtime agent configuration optimized for the project.

        Args:
            profile: Detected project profile with languages, frameworks, tools
            plugins: List of plugin IDs to include
            catalog: Plugin catalog for lookup

        Returns:
            RuntimeAgentConfig with condensed prompt and token estimates
        """
        # Retrieve selected plugins
        selected_plugins = catalog.get_plugins(plugins)

        # Analyze project context
        project_context = self._analyze_project_context(profile)

        # Extract relevant sections from each plugin
        condensed_sections = []
        skills_included = []
        full_token_count = 0

        for plugin in selected_plugins:
            # Extract relevant agent prompts
            for agent in plugin.agents:
                relevant_sections = self._extract_relevant_sections(
                    agent, profile, project_context
                )
                if relevant_sections:
                    condensed_sections.append(relevant_sections)
                    full_token_count += self._estimate_full_agent_tokens(agent)

            # Include skill definitions
            for skill in plugin.skills:
                if self._is_skill_relevant(skill, profile, project_context):
                    skills_included.append(skill.name)
                    condensed_sections.append(self._format_skill(skill))

        # Generate condensed agent prompt
        agent_prompt = self._generate_condensed_prompt(
            profile, condensed_sections, project_context
        )

        # Calculate token estimates
        token_estimate = len(agent_prompt) // self.CHARS_PER_TOKEN
        token_savings = full_token_count - token_estimate

        return RuntimeAgentConfig(
            agent_prompt=agent_prompt,
            skills_included=skills_included,
            token_estimate=token_estimate,
            token_savings=max(0, token_savings),
            metadata={
                'profile': profile.model_dump(),
                'plugins': plugins,
                'context': project_context
            }
        )

    def _analyze_project_context(self, profile: ProjectProfile) -> Dict[str, Any]:
        """Analyze project to understand specific architecture and needs."""
        context = {
            'primary_language': None,
            'primary_framework': None,
            'architecture_patterns': set(),
            'testing_frameworks': set(),
            'build_tools': set(),
            'deployment_targets': set(),
        }

        # Determine primary language
        if profile.detected_languages:
            context['primary_language'] = profile.detected_languages[0]

        # Determine primary framework
        if profile.detected_frameworks:
            context['primary_framework'] = profile.detected_frameworks[0]

        # Detect architecture patterns
        for framework in profile.detected_frameworks:
            if framework.lower() in ['django', 'fastapi', 'flask', 'express']:
                context['architecture_patterns'].add('web_api')
            if framework.lower() in ['react', 'vue', 'angular', 'svelte']:
                context['architecture_patterns'].add('spa_frontend')
            if framework.lower() in ['nextjs', 'nuxt', 'sveltekit']:
                context['architecture_patterns'].add('fullstack_framework')

        # Detect testing frameworks
        for tool in profile.detected_tools:
            if tool.lower() in ['pytest', 'jest', 'vitest', 'mocha', 'jasmine']:
                context['testing_frameworks'].add(tool.lower())

        # Detect build tools
        for build_sys in profile.build_systems:
            context['build_tools'].add(build_sys.lower())

        return context

    def _extract_relevant_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract only relevant sections from an agent prompt."""
        sections = []

        # Add core capabilities that match project needs
        relevant_capabilities = self._filter_capabilities(
            agent.capabilities, profile, context
        )

        if relevant_capabilities:
            sections.append(f"## {agent.name}\n")
            sections.append(f"{agent.description}\n")
            sections.append("\nCapabilities:\n")
            for cap in relevant_capabilities:
                sections.append(f"- {cap}\n")

        # Use specialized extractors based on project type
        primary_lang = context.get('primary_language', '').lower()
        primary_fw = context.get('primary_framework', '').lower()

        for key in [primary_lang, primary_fw]:
            if key in self.section_extractors:
                extracted = self.section_extractors[key](agent, profile, context)
                if extracted:
                    sections.append(extracted)

        return ''.join(sections)

    def _filter_capabilities(
        self,
        capabilities: List[str],
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> List[str]:
        """Filter capabilities to only those relevant to the project."""
        relevant = []

        # Keywords from project profile
        keywords = set()
        keywords.update(lang.lower() for lang in profile.detected_languages)
        keywords.update(fw.lower() for fw in profile.detected_frameworks)
        keywords.update(tool.lower() for tool in profile.detected_tools)
        keywords.update(domain.lower() for domain in profile.domains)

        for capability in capabilities:
            cap_lower = capability.lower()
            # Include if capability mentions any project keyword
            if any(keyword in cap_lower for keyword in keywords):
                relevant.append(capability)
            # Include if capability matches architecture patterns
            elif any(pattern in cap_lower for pattern in context.get('architecture_patterns', [])):
                relevant.append(capability)

        return relevant

    def _extract_python_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract Python-specific sections."""
        sections = []

        # Check for Python-specific capabilities
        python_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['python', 'pip', 'venv', 'pytest', 'django', 'fastapi', 'flask'])
        ]

        if python_caps:
            sections.append("\n### Python-specific:\n")
            for cap in python_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_javascript_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract JavaScript-specific sections."""
        sections = []

        js_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['javascript', 'npm', 'node', 'jest', 'webpack', 'babel'])
        ]

        if js_caps:
            sections.append("\n### JavaScript-specific:\n")
            for cap in js_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_typescript_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract TypeScript-specific sections."""
        sections = []

        ts_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['typescript', 'tsc', 'types', 'interface'])
        ]

        if ts_caps:
            sections.append("\n### TypeScript-specific:\n")
            for cap in ts_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_react_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract React-specific sections."""
        sections = []

        react_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['react', 'jsx', 'hooks', 'component'])
        ]

        if react_caps:
            sections.append("\n### React-specific:\n")
            for cap in react_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_vue_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract Vue-specific sections."""
        sections = []

        vue_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['vue', 'composition', 'options api'])
        ]

        if vue_caps:
            sections.append("\n### Vue-specific:\n")
            for cap in vue_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_django_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract Django-specific sections."""
        sections = []

        django_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['django', 'orm', 'models', 'views', 'templates'])
        ]

        if django_caps:
            sections.append("\n### Django-specific:\n")
            for cap in django_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_fastapi_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract FastAPI-specific sections."""
        sections = []

        fastapi_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['fastapi', 'pydantic', 'async', 'endpoint'])
        ]

        if fastapi_caps:
            sections.append("\n### FastAPI-specific:\n")
            for cap in fastapi_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _extract_express_sections(
        self,
        agent: Agent,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> str:
        """Extract Express-specific sections."""
        sections = []

        express_caps = [
            cap for cap in agent.capabilities
            if any(kw in cap.lower() for kw in ['express', 'middleware', 'route', 'req', 'res'])
        ]

        if express_caps:
            sections.append("\n### Express-specific:\n")
            for cap in express_caps:
                sections.append(f"- {cap}\n")

        return ''.join(sections)

    def _is_skill_relevant(
        self,
        skill: Skill,
        profile: ProjectProfile,
        context: Dict[str, Any]
    ) -> bool:
        """Determine if a skill is relevant to the project."""
        # Check if skill tags match project domains or tools
        skill_tags_lower = {tag.lower() for tag in skill.tags}

        project_keywords = set()
        project_keywords.update(lang.lower() for lang in profile.detected_languages)
        project_keywords.update(fw.lower() for fw in profile.detected_frameworks)
        project_keywords.update(tool.lower() for tool in profile.detected_tools)
        project_keywords.update(domain.lower() for domain in profile.domains)

        # Skill is relevant if any tag matches project keywords
        return bool(skill_tags_lower & project_keywords)

    def _format_skill(self, skill: Skill) -> str:
        """Format a skill for inclusion in the agent prompt."""
        lines = [f"\n## Skill: {skill.name}\n"]
        lines.append(f"{skill.description}\n")

        if skill.commands:
            lines.append("\nCommands:\n")
            for cmd in skill.commands:
                lines.append(f"- `{cmd.name}`: {cmd.description}\n")

        return ''.join(lines)

    def _generate_condensed_prompt(
        self,
        profile: ProjectProfile,
        sections: List[str],
        context: Dict[str, Any]
    ) -> str:
        """Generate the final condensed agent prompt."""
        prompt_parts = []

        # Header with project context
        prompt_parts.append("# Runtime Agent Configuration\n\n")
        prompt_parts.append(f"Project: {profile.project_path}\n")

        if context.get('primary_language'):
            prompt_parts.append(f"Primary Language: {context['primary_language']}\n")

        if context.get('primary_framework'):
            prompt_parts.append(f"Primary Framework: {context['primary_framework']}\n")

        if context.get('architecture_patterns'):
            patterns = ', '.join(context['architecture_patterns'])
            prompt_parts.append(f"Architecture: {patterns}\n")

        prompt_parts.append("\n---\n\n")

        # Add all condensed sections
        prompt_parts.extend(sections)

        return ''.join(prompt_parts)

    def _estimate_full_agent_tokens(self, agent: Agent) -> int:
        """Estimate tokens for a full agent prompt (before condensing)."""
        # Rough estimate: agent description + all capabilities
        full_text = agent.description + ' '.join(agent.capabilities)
        # Assume full agent prompts are typically 3-5x longer than just description+caps
        estimated_full_length = len(full_text) * 4
        return estimated_full_length // self.CHARS_PER_TOKEN


def build_runtime_agent(
    profile: ProjectProfile,
    plugins: List[str],
    catalog: Catalog
) -> RuntimeAgentConfig:
    """
    Build a runtime agent configuration optimized for the project.

    This is the main entry point for dynamic agent generation.

    Args:
        profile: Detected project profile with languages, frameworks, tools
        plugins: List of plugin IDs to include
        catalog: Plugin catalog for lookup

    Returns:
        RuntimeAgentConfig with condensed prompt and token estimates

    Example:
        >>> profile = ProjectProfile(
        ...     project_path="/path/to/project",
        ...     detected_languages=["python"],
        ...     detected_frameworks=["fastapi"],
        ...     domains=["web_api"]
        ... )
        >>> plugins = ["python-dev", "fastapi-expert"]
        >>> catalog = Catalog(load_plugins())
        >>> config = build_runtime_agent(profile, plugins, catalog)
        >>> print(f"Token savings: {config.token_savings}")
    """
    builder = RuntimeBuilder()
    return builder.build_runtime_agent(profile, plugins, catalog)
