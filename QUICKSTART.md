# AgenticQ — Quick Start Guide

## Installation

### 1. Install AgenticQ CLI

```bash
# Clone the repository
git clone https://github.com/sandeshbagmare/AgenticQ.git
cd AgenticQ

# Install in development mode
pip install -e .

# Verify installation
agenticq version
python -m agenticq version  # Both work!
```

### 2. Set Up Upstream Repository

```bash
# Option A: Use default location
git clone https://github.com/wshobson/agents.git ~/.agenticq/upstream

# Option B: Use custom location with environment variable
git clone https://github.com/wshobson/agents.git /path/to/agents
export AGENTICQ_UPSTREAM=/path/to/agents

# Generate catalog
agenticq update
```

### 3. Install VS Code Extension (Optional)

```bash
cd vscode-extension
npm install
npm run compile
vsce package
code --install-extension agenticq-0.1.0.vsix
```

---

## Usage Examples

### CLI Workflow

```bash
# Navigate to your project
cd my-fastapi-project/

# Get smart recommendations
agenticq recommend

# Search for specific plugins
agenticq search fastapi
agenticq search kubernetes

# Get detailed plugin info
agenticq info python-development

# Scaffold recommended plugins
agenticq scaffold python-development backend-development unit-testing

# Build a custom runtime agent
agenticq build python-development backend-development \
  --output my-agent.json

# Browse all available domains
agenticq browse
```

### Web GUI Workflow

```bash
# Launch the web dashboard
agenticq gui

# Opens at http://localhost:8080
# - Browse domains and plugins
# - Get recommendations
# - Scaffold directly from the UI
```

### VS Code Extension Workflow

1. **Open Command Palette** (Ctrl+Shift+P / Cmd+Shift+P)
2. **Type:** `AgenticQ: Get Recommendations`
3. **Select plugins** from the quick pick
4. **Choose harness** (claude-code, cursor, etc.)
5. **Done!** Plugins scaffolded to your project

**Or use the sidebar:**
- Click the AgenticQ icon in the activity bar
- Browse domains and plugins
- Click any plugin to scaffold it directly

---

## Configuration

### Environment Variables

```bash
# Set custom upstream repository path
export AGENTICQ_UPSTREAM=/path/to/wshobson-agents

# Default: ~/.agenticq/upstream
```

### VS Code Settings

```json
{
  "agenticq.pythonPath": "python",
  "agenticq.autoRecommend": false,
  "agenticq.defaultHarness": "claude-code"
}
```

**Settings explained:**
- `pythonPath` — Python interpreter to use (default: `python`)
- `autoRecommend` — Auto-run recommendations on project open (default: `false`)
- `defaultHarness` — Default scaffolding target (default: `claude-code`)

---

## Supported Harnesses

| Harness | Output Location | Description |
|---------|----------------|-------------|
| **claude-code** | `.claude/plugins/` | Claude Code plugins with agents/skills/commands |
| **cursor** | `.cursor-plugin/plugins/` | Cursor AI plugin format |
| **gemini** | `.gemini/` | Google Gemini CLI format |
| **codex** | `.codex/agents/` | OpenAI Codex format |
| **opencode** | Similar to Claude Code | OpenCode format |
| **copilot** | `.github/copilot/instructions.md` | GitHub Copilot instructions |

---

## Domain Coverage

AgenticQ provides **81 plugins** organized into **12 domains**:

### 🐍 Python Development (4 plugins, 9 agents, 16 skills)
- python-development
- unit-testing
- tdd-workflows
- code-refactoring

### ⚡ JavaScript/TypeScript (3 plugins, 7 agents, 17 skills)
- javascript-typescript
- frontend-mobile-development
- ui-design

### 🔌 Backend & APIs (4 plugins, 15 agents, 10 skills)
- backend-development
- api-scaffolding
- api-testing-observability
- backend-api-security

### ☁️ DevOps & Cloud (4 plugins, 15 agents, 16 skills)
- cloud-infrastructure
- kubernetes-operations
- cicd-automation
- deployment-strategies

### 🔒 Security (4 plugins, 8 agents, 5 skills)
- security-scanning
- security-compliance
- backend-api-security
- frontend-mobile-security

### 🤖 Data & ML (4 plugins, 9 agents, 16 skills)
- data-engineering
- machine-learning-ops
- llm-application-dev
- business-analytics

### 📚 Documentation (4 plugins, 12 agents, 4 skills)
- documentation-standards
- code-documentation
- documentation-generation
- c4-architecture

### ✅ Testing & QA (4 plugins, 7 agents, 3 commands)
- unit-testing
- tdd-workflows
- performance-testing-review
- data-validation-suite

### ⚙️ Systems Programming (3 plugins, 7 agents, 6 skills)
- systems-programming
- shell-scripting
- arm-cortex-microcontrollers

### 📈 Business & Marketing (5 plugins, 10 agents, 7 skills)
- business-analytics
- seo-analysis-monitoring
- seo-content-creation
- content-marketing
- startup-business-analyst

### 🎭 Agent Orchestration (4 plugins, 7 agents, 9 skills, 13 commands)
- agent-orchestration
- agent-teams
- conductor
- context-management

### 🎯 Specialized (5 plugins, 9 agents, 16 skills)
- blockchain-web3
- game-development
- quantitative-trading
- payment-processing
- reverse-engineering

**Total: 191 agents, 155 skills, 61 commands**

---

## Common Workflows

### Workflow 1: New Python FastAPI Project

```bash
cd my-fastapi-app/

# Get recommendations
agenticq recommend

# Scaffold recommended plugins
agenticq scaffold python-development backend-development \
  api-testing-observability unit-testing \
  --harness claude-code

# Result: .claude/plugins/ with 4 plugins ready to use
```

### Workflow 2: DevOps Infrastructure Project

```bash
cd my-k8s-infra/

# Get recommendations
agenticq recommend

# Scaffold DevOps plugins
agenticq scaffold cloud-infrastructure kubernetes-operations \
  cicd-automation deployment-strategies \
  --harness claude-code

# Result: .claude/plugins/ with infrastructure agents
```

### Workflow 3: Full-Stack Web App

```bash
cd my-web-app/

# Get recommendations
agenticq recommend

# Scaffold frontend + backend
agenticq scaffold javascript-typescript frontend-mobile-development \
  ui-design backend-development api-scaffolding \
  --harness cursor

# Result: .cursor-plugin/plugins/ with full-stack agents
```

### Workflow 4: Custom Runtime Agent

```bash
# Build a specialized agent combining multiple plugins
agenticq build python-development backend-development \
  api-testing-observability security-scanning \
  --path . \
  --output production-agent.json

# Result: production-agent.json with combined capabilities
```

---

## Troubleshooting

### Issue: "Catalog not found"

```bash
# Solution: Generate the catalog
agenticq update

# If upstream repo missing:
git clone https://github.com/wshobson/agents.git ~/.agenticq/upstream
agenticq update
```

### Issue: VS Code extension can't find Python

```bash
# Solution 1: Set pythonPath in VS Code settings
{
  "agenticq.pythonPath": "/usr/bin/python3"
}

# Solution 2: Ensure agenticq is installed
pip install -e /path/to/AgenticQ

# Solution 3: Verify it works from terminal
python -m agenticq version
```

### Issue: "No recommendations found"

```bash
# This is normal for projects with no detectable tech stack
# Solution: Manually browse and select plugins
agenticq browse
agenticq search <keyword>
agenticq scaffold <plugin-name>
```

### Issue: Emoji characters display as �

```bash
# This is a Windows console encoding issue (cp1252)
# The CLI output is correct, just the terminal display
# Solution: Use Windows Terminal or set console to UTF-8
chcp 65001
```

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_web.py -v

# Run with coverage
pytest tests/ --cov=agenticq --cov-report=html
```

### Building the Extension

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode for development
npm run watch

# Package for distribution
vsce package
```

### Generating Demos

```bash
cd demos

# Render all demo GIFs
python demo1_vscode.py
python demo2_web.py
python demo3_cli.py

# Output: gifs/demo1_vscode.gif, demo2_web.gif, demo3_cli.gif
```

---

## API Reference

### Python API

```python
from agenticq.core.scanner import scan_project
from agenticq.core.classifier import classify_project
from agenticq.core.recommender import recommend_plugins

# Scan a project
profile = scan_project("/path/to/project")
print(profile.languages)  # ['python']
print(profile.frameworks)  # ['fastapi']

# Classify domains
from agenticq.config import get_taxonomy_path
import json
taxonomy = json.load(open(get_taxonomy_path()))
domains = classify_project(profile, taxonomy)

# Get recommendations
from agenticq.config import get_catalog_path
recommendations = recommend_plugins(
    profile, domains, 
    get_catalog_path(), 
    get_taxonomy_path(), 
    max_results=10
)

for rec in recommendations:
    print(f"{rec.plugin_name}: {rec.relevance_score}")
```

### JSON-RPC API (for VS Code extension)

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "recommend",
  "params": {
    "path": "/path/to/project",
    "max_results": 10
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "plugin_name": "python-development",
      "relevance_score": 90.0,
      "token_cost_estimate": 30218,
      "reason": "matches Python project",
      "conflicts": []
    }
  ]
}
```

### HTTP API (for Web GUI)

```bash
# Get catalog
curl http://localhost:8080/api/catalog

# Get domains
curl http://localhost:8080/api/domains

# Get plugins
curl http://localhost:8080/api/plugins

# Scan project
curl -X POST http://localhost:8080/api/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "."}'

# Get recommendations
curl -X POST http://localhost:8080/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"path": ".", "max_results": 10}'

# Scaffold plugins
curl -X POST http://localhost:8080/api/scaffold \
  -H "Content-Type: application/json" \
  -d '{"plugins": ["python-development"], "harness": "claude-code", "target": "."}'
```

---

## Resources

- **GitHub Repository**: https://github.com/sandeshbagmare/AgenticQ
- **Upstream Marketplace**: https://github.com/wshobson/agents
- **Issues**: https://github.com/sandeshbagmare/AgenticQ/issues
- **License**: MIT

---

## Credits

AgenticQ is built on top of the [wshobson/agents](https://github.com/wshobson/agents) marketplace created by **Seth Hobson** ([@wshobson](https://github.com/wshobson)) and community contributors.

---

**Happy scaffolding! 🚀**
