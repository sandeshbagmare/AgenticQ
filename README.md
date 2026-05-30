# AgenticQ — Intelligent Agent Scaffolding Engine

> Build smarter with curated agents from the [wshobson/agents](https://github.com/wshobson/agents) marketplace

## What is AgenticQ?

AgenticQ is a **CLI tool + Web GUI + VS Code extension** that helps you discover, recommend, and scaffold the right agents/skills/plugins for your project — minimizing token cost and maximizing AI output quality.

The [wshobson/agents](https://github.com/wshobson/agents) marketplace contains **83 plugins**, **191 agents**, **155 skills**, and **102 commands** across multiple domains. AgenticQ makes it easy to find and install exactly what you need.

## Features

- 🔍 **Smart Recommendations**: Scans your project and recommends relevant plugins based on detected languages, frameworks, and infrastructure
- 📦 **Multi-Harness Support**: Scaffolds for Claude Code, Cursor, Gemini CLI, Codex, OpenCode, and GitHub Copilot
- 🎯 **Token Optimization**: Estimates token costs and suggests lean configurations
- 🤖 **Runtime Agent Builder**: Generates custom agents tailored to your specific project
- 🌐 **Three Interfaces**: CLI, standalone Web GUI, and VS Code extension
- 📊 **12 Domain Taxonomy**: Organized classification of plugins across Python, JavaScript, Backend, DevOps, Security, Data/ML, Documentation, Testing, Systems Programming, Business, Agent Orchestration, and Specialized domains

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for VS Code extension)
- Git

### Install from source

```bash
git clone <this-repo>
cd AgenticQ
pip install -e .
```

### First-time setup

Clone the upstream marketplace and generate the catalog:

```bash
# Clone the upstream repo
git clone https://github.com/wshobson/agents.git /tmp/wshobson-agents-research

# Generate catalog (or run: agenticq update)
python src/agenticq/core/catalog.py
```

## Quick Start

### CLI Usage

```bash
# Get recommendations for your project
agenticq recommend

# Browse all domains
agenticq browse

# Search for specific plugins
agenticq search fastapi

# Get detailed info about a plugin
agenticq info python-development

# Scaffold plugins into your project
agenticq scaffold python-development unit-testing --harness claude-code

# Update catalog from upstream
agenticq update
```

### Example: Python FastAPI Project

```bash
cd my-fastapi-project/

# Get recommendations
agenticq recommend

# Output:
# Detected:
#   Languages: python
#   Frameworks: fastapi
#   Infrastructure: docker
#   Databases: postgresql
#   Testing: pytest
#
# Recommended Plugins:
# ┌─────────────────────────┬───────┬────────┬──────────────────────────┐
# │ Plugin                  │ Score │ Tokens │ Reason                   │
# ├─────────────────────────┼───────┼────────┼──────────────────────────┤
# │ python-development      │  90.0 │ 12,450 │ matches Python project   │
# │ backend-development     │  85.0 │ 15,230 │ supports fastapi         │
# │ api-testing-observ...   │  75.0 │  8,920 │ supports testing workflow│
# │ unit-testing            │  70.0 │  6,340 │ supports testing workflow│
# └─────────────────────────┴───────┴────────┴──────────────────────────┘

# Scaffold the top recommendations
agenticq scaffold python-development backend-development unit-testing
```

### Web GUI

```bash
# Launch standalone web dashboard
agenticq gui

# Opens at http://localhost:8080
```

### VS Code Extension

1. Open `vscode-extension/` in VS Code
2. Run `npm install`
3. Press F5 to launch Extension Development Host
4. Use Command Palette: `AgenticQ: Get Recommendations`

## Architecture

```
agenticq/
├── src/agenticq/
│   ├── cli.py                    # Typer CLI entrypoint
│   ├── core/
│   │   ├── catalog.py            # Marketplace indexer
│   │   ├── scanner.py            # Project tech-stack detector
│   │   ├── classifier.py         # Domain classification engine
│   │   ├── recommender.py        # Plugin recommendation engine
│   │   ├── scaffolder.py         # Multi-harness scaffolder
│   │   └── runtime_builder.py    # Dynamic agent generator
│   ├── models/
│   │   ├── plugin.py             # Plugin/Agent/Skill models
│   │   ├── project.py            # ProjectProfile model
│   │   └── taxonomy.py           # Domain taxonomy models
│   ├── data/
│   │   ├── catalog.json          # Indexed marketplace catalog
│   │   └── taxonomy.json         # 12-domain taxonomy
│   └── server/
│       ├── web.py                # Web GUI server (aiohttp)
│       └── jsonrpc.py            # JSON-RPC server for VS Code
├── gui/                          # Standalone Web GUI
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── vscode-extension/             # VS Code Extension
│   ├── src/
│   │   ├── extension.ts
│   │   ├── pythonBridge.ts
│   │   └── domainTreeProvider.ts
│   └── package.json
└── tests/                        # pytest test suite
```

## Domain Taxonomy

AgenticQ organizes the 83 plugins into 12 domains:

| Domain | Icon | Plugins | Description |
|--------|------|---------|-------------|
| **Python Development** | 🐍 | 4 | Modern Python with FastAPI, Django, async patterns |
| **JavaScript/TypeScript** | ⚡ | 3 | React, Node.js, and web frameworks |
| **Backend & APIs** | 🔌 | 4 | API design, GraphQL, REST, microservices |
| **DevOps & Cloud** | ☁️ | 4 | Kubernetes, CI/CD, cloud infrastructure |
| **Security** | 🔒 | 4 | Security scanning, compliance, secure coding |
| **Data & ML** | 🤖 | 4 | Data engineering, MLOps, LLM applications |
| **Documentation** | 📚 | 4 | Technical docs, API docs, architecture diagrams |
| **Testing & QA** | ✅ | 4 | Unit testing, TDD, performance testing |
| **Systems Programming** | ⚙️ | 3 | Rust, Go, C/C++, embedded systems |
| **Business & Marketing** | 📈 | 5 | Analytics, SEO, content marketing |
| **Agent Orchestration** | 🎭 | 4 | Multi-agent systems, context management |
| **Specialized** | 🎯 | 5 | Blockchain, game dev, trading, payments |

## How It Works

1. **Scanner** detects your project's tech stack by analyzing:
   - Language files (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.)
   - Framework configs (`next.config.js`, Django settings, etc.)
   - Infrastructure (`Dockerfile`, `k8s/`, `.github/workflows/`)
   - Databases (migration dirs, ORM configs)
   - Testing tools (`pytest.ini`, `jest.config.js`)

2. **Classifier** maps detected stack to domains using file detection heuristics

3. **Recommender** scores plugins by:
   - Domain relevance (from classifier)
   - Token cost (prefers lower)
   - Dependency chains (plugins that pair well)
   - Conflict detection (overlapping agent roles)

4. **Scaffolder** generates harness-specific output:
   - **Claude Code**: `.claude/plugins/` with agents/skills/commands
   - **Cursor**: `.cursor-plugin/plugins/*.json` + `.cursor/rules/*.mdc`
   - **Gemini CLI**: `.gemini/` + `GEMINI.md`
   - **Codex CLI**: `.codex/agents/` + `.codex/skills/`
   - **OpenCode**: Similar to Claude Code
   - **GitHub Copilot**: `.github/copilot/instructions.md`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/test_scanner.py -v
pytest tests/test_classifier.py -v

# Run comprehensive test script
python test_all.py
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Credits

AgenticQ indexes and scaffolds plugins from the **[wshobson/agents](https://github.com/wshobson/agents)** marketplace created by:

- **Seth Hobson** ([@wshobson](https://github.com/wshobson)) — Primary author and maintainer
- **Community Contributors** — Plugin authors and contributors

All plugin content is licensed under their respective licenses (MIT, Apache-2.0). AgenticQ is a discovery and scaffolding tool that makes the marketplace more accessible.

### Upstream Repository

- **Repository**: https://github.com/wshobson/agents
- **Version**: 1.7.1
- **Plugins**: 83
- **Agents**: 191
- **Skills**: 155
- **Commands**: 102

## License

MIT License

Copyright (c) 2025 AgenticQ

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Roadmap

- [ ] LLM-powered recommendations (optional, with API key)
- [ ] Plugin conflict resolution UI
- [ ] Custom taxonomy support
- [ ] Plugin usage analytics
- [ ] Integration with more harnesses
- [ ] Web GUI deployment (Docker image)
- [ ] VS Code Marketplace publication

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Upstream Marketplace**: [wshobson/agents](https://github.com/wshobson/agents)
