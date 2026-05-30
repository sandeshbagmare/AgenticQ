"""Project scanner to detect tech stack."""

from pathlib import Path
from typing import List, Dict, Optional
import json
from ..models.project import ProjectProfile


class ProjectScanner:
    """Scans a project directory to detect languages, frameworks, and tools."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)

    def scan(self) -> ProjectProfile:
        """Scan the project and return a profile."""
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        infrastructure = self._detect_infrastructure()
        databases = self._detect_databases()
        testing_tools = self._detect_testing()

        return ProjectProfile(
            languages=languages,
            frameworks=frameworks,
            infrastructure=infrastructure,
            databases=databases,
            testing_tools=testing_tools,
            confidence_scores=self._calculate_confidence(
                languages, frameworks, infrastructure, databases, testing_tools
            ),
        )

    def _detect_languages(self) -> List[str]:
        """Detect programming languages."""
        languages = []

        # Python
        if (self.project_path / "pyproject.toml").exists() or \
           (self.project_path / "setup.py").exists() or \
           (self.project_path / "requirements.txt").exists():
            languages.append("python")

        # JavaScript/TypeScript
        if (self.project_path / "package.json").exists():
            languages.append("javascript")
            if (self.project_path / "tsconfig.json").exists():
                languages.append("typescript")

        # Rust
        if (self.project_path / "Cargo.toml").exists():
            languages.append("rust")

        # Go
        if (self.project_path / "go.mod").exists():
            languages.append("go")

        # Java
        if (self.project_path / "pom.xml").exists() or \
           (self.project_path / "build.gradle").exists():
            languages.append("java")

        # C/C++
        if (self.project_path / "CMakeLists.txt").exists() or \
           (self.project_path / "Makefile").exists():
            languages.append("c/c++")

        # Ruby
        if (self.project_path / "Gemfile").exists():
            languages.append("ruby")

        # PHP
        if (self.project_path / "composer.json").exists():
            languages.append("php")

        return languages

    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks."""
        frameworks = []

        # Python frameworks
        if (self.project_path / "pyproject.toml").exists():
            content = (self.project_path / "pyproject.toml").read_text()
            if "fastapi" in content.lower():
                frameworks.append("fastapi")
            if "django" in content.lower():
                frameworks.append("django")
            if "flask" in content.lower():
                frameworks.append("flask")

        # JavaScript frameworks
        if (self.project_path / "package.json").exists():
            try:
                pkg = json.loads((self.project_path / "package.json").read_text())
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

                if "next" in deps:
                    frameworks.append("nextjs")
                if "react" in deps:
                    frameworks.append("react")
                if "vue" in deps:
                    frameworks.append("vue")
                if "express" in deps:
                    frameworks.append("express")
                if "nestjs" in deps or "@nestjs/core" in deps:
                    frameworks.append("nestjs")
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Check for specific config files
        if (self.project_path / "next.config.js").exists():
            frameworks.append("nextjs")
        if (self.project_path / "nuxt.config.js").exists():
            frameworks.append("nuxt")

        return frameworks

    def _detect_infrastructure(self) -> List[str]:
        """Detect infrastructure tools."""
        infra = []

        if (self.project_path / "Dockerfile").exists():
            infra.append("docker")
        if (self.project_path / "docker-compose.yml").exists():
            infra.append("docker-compose")

        # Kubernetes
        if (self.project_path / "k8s").exists() or \
           list(self.project_path.glob("**/deployment.yaml")):
            infra.append("kubernetes")

        # Terraform
        if list(self.project_path.glob("**/*.tf")):
            infra.append("terraform")

        # CI/CD
        if (self.project_path / ".github" / "workflows").exists():
            infra.append("github-actions")
        if (self.project_path / ".gitlab-ci.yml").exists():
            infra.append("gitlab-ci")
        if (self.project_path / "Jenkinsfile").exists():
            infra.append("jenkins")

        return infra

    def _detect_databases(self) -> List[str]:
        """Detect database usage."""
        databases = []

        # Check for common database files/patterns
        if (self.project_path / "prisma").exists():
            databases.append("prisma")

        # Check for migration directories
        if (self.project_path / "migrations").exists() or \
           (self.project_path / "alembic").exists():
            databases.append("sql-migrations")

        # Check package.json for database drivers
        if (self.project_path / "package.json").exists():
            try:
                pkg = json.loads((self.project_path / "package.json").read_text())
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

                if "pg" in deps or "postgres" in deps:
                    databases.append("postgresql")
                if "mysql" in deps or "mysql2" in deps:
                    databases.append("mysql")
                if "mongodb" in deps or "mongoose" in deps:
                    databases.append("mongodb")
                if "redis" in deps:
                    databases.append("redis")
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Check Python dependencies
        if (self.project_path / "pyproject.toml").exists():
            content = (self.project_path / "pyproject.toml").read_text()
            if "sqlalchemy" in content.lower():
                databases.append("sqlalchemy")
            if "psycopg" in content.lower():
                databases.append("postgresql")
            if "pymongo" in content.lower():
                databases.append("mongodb")

        return databases

    def _detect_testing(self) -> List[str]:
        """Detect testing frameworks."""
        testing = []

        # Python testing
        if (self.project_path / "pytest.ini").exists():
            testing.append("pytest")
        elif (self.project_path / "pyproject.toml").exists():
            content = (self.project_path / "pyproject.toml").read_text()
            if "pytest" in content.lower():
                testing.append("pytest")

        # JavaScript testing
        if (self.project_path / "jest.config.js").exists():
            testing.append("jest")
        if (self.project_path / "vitest.config.js").exists():
            testing.append("vitest")

        # Test directories
        if (self.project_path / "tests").exists() or \
           (self.project_path / "test").exists():
            testing.append("test-directory")

        return testing

    def _calculate_confidence(
        self,
        languages: List[str],
        frameworks: List[str],
        infrastructure: List[str],
        databases: List[str],
        testing_tools: List[str],
    ) -> Dict[str, float]:
        """Calculate confidence scores for detected components."""
        scores = {}

        # Higher confidence if multiple indicators
        for lang in languages:
            scores[f"language:{lang}"] = 0.9

        for fw in frameworks:
            scores[f"framework:{fw}"] = 0.85

        for infra in infrastructure:
            scores[f"infrastructure:{infra}"] = 0.8

        for db in databases:
            scores[f"database:{db}"] = 0.75

        for test in testing_tools:
            scores[f"testing:{test}"] = 0.7

        return scores


def scan_project(path: Optional[str] = None) -> ProjectProfile:
    """Convenience function to scan a project."""
    scanner = ProjectScanner(Path(path or "."))
    return scanner.scan()
