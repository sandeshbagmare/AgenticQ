# AgenticQ VS Code Extension

**Intelligent Agent Scaffolding Engine** - Discover, recommend, and scaffold AI agents from the [wshobson/agents](https://github.com/wshobson/agents) marketplace directly in VS Code.

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 🔍 Smart Recommendations
Automatically analyzes your project and recommends relevant agents based on:
- Detected programming languages (Python, JavaScript, Rust, Go, etc.)
- Frameworks (FastAPI, React, Django, Next.js, etc.)
- Infrastructure (Docker, Kubernetes, CI/CD)
- Databases (PostgreSQL, MongoDB, Redis)
- Testing tools (pytest, Jest, etc.)

### 📦 Browse 83 Plugins Across 12 Domains
- 🐍 **Python Development** - FastAPI, Django, async patterns
- ⚡ **JavaScript/TypeScript** - React, Node.js, web frameworks
- 🔌 **Backend & APIs** - REST, GraphQL, microservices
- ☁️ **DevOps & Cloud** - Kubernetes, CI/CD, infrastructure
- 🔒 **Security** - Security scanning, compliance
- 🤖 **Data & ML** - Data engineering, MLOps, LLM apps
- 📚 **Documentation** - Technical docs, API docs
- ✅ **Testing & QA** - Unit testing, TDD, performance
- ⚙️ **Systems Programming** - Rust, Go, C/C++
- 📈 **Business & Marketing** - Analytics, SEO
- 🎭 **Agent Orchestration** - Multi-agent systems
- 🎯 **Specialized** - Blockchain, game dev, trading

### 🎯 Multi-Harness Scaffolding
Scaffold agents for multiple AI coding assistants:
- **Claude Code** - `.claude/plugins/`
- **Cursor** - `.cursor-plugin/plugins/`
- **Gemini CLI** - `.gemini/`
- **Codex CLI** - `.codex/agents/`
- **OpenCode** - Similar to Claude Code
- **GitHub Copilot** - `.github/copilot/instructions.md`

### 🌐 Interactive Dashboard
Built-in webview dashboard for browsing and managing agents.

## 📸 Screenshots

### Command Palette
Access all AgenticQ features from the Command Palette (Ctrl+Shift+P / Cmd+Shift+P):

![Command Palette](https://via.placeholder.com/800x200/1e1e1e/ffffff?text=AgenticQ+Commands)

### Smart Recommendations
Get personalized plugin recommendations based on your project:

![Recommendations](https://via.placeholder.com/800x400/1e1e1e/ffffff?text=Smart+Recommendations)

### Domain Browser
Explore plugins organized by domain in the sidebar:

![Domain Browser](https://via.placeholder.com/300x500/1e1e1e/ffffff?text=Domain+Browser)

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+** installed
2. **AgenticQ CLI** installed:
   ```bash
   pip install agenticq
   ```

3. **Clone the upstream marketplace** (first time only):
   ```bash
   git clone https://github.com/wshobson/agents.git /tmp/wshobson-agents-research
   ```

4. **Generate catalog**:
   ```bash
   agenticq update
   ```

### Installation

1. Install from VS Code Marketplace:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "AgenticQ"
   - Click Install

2. Or install from `.vsix`:
   ```bash
   code --install-extension agenticq-0.1.0.vsix
   ```

## 📖 Usage

### Get Recommendations

1. Open a project in VS Code
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Type: `AgenticQ: Get Recommendations`
4. Review recommended plugins
5. Select plugins to scaffold

### Browse Domains

1. Open Command Palette
2. Type: `AgenticQ: Browse Domains`
3. Explore the domain tree in the sidebar
4. Click on plugins to view details

### Scaffold Plugins

1. Open Command Palette
2. Type: `AgenticQ: Scaffold Plugins`
3. Enter plugin names (comma-separated): `python-development, unit-testing`
4. Select target harness: `claude-code`, `cursor`, etc.
5. Plugins are scaffolded into your project

### Open Dashboard

1. Open Command Palette
2. Type: `AgenticQ: Open Dashboard`
3. Interactive webview opens with full catalog

## ⚙️ Extension Settings

This extension contributes the following settings:

* `agenticq.pythonPath`: Path to Python interpreter (default: `python`)
* `agenticq.autoRecommend`: Automatically recommend on project open (default: `false`)
* `agenticq.defaultHarness`: Default harness for scaffolding (default: `claude-code`)

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `AgenticQ: Get Recommendations` | Analyze project and get plugin recommendations |
| `AgenticQ: Browse Domains` | Browse all domains and plugins |
| `AgenticQ: Scaffold Plugins` | Scaffold selected plugins into project |
| `AgenticQ: Open Dashboard` | Open interactive dashboard webview |

## 📋 Requirements

- **Python**: 3.10 or higher
- **AgenticQ CLI**: Installed via `pip install agenticq`
- **Upstream Marketplace**: Cloned from [wshobson/agents](https://github.com/wshobson/agents)

## 🐛 Known Issues

- Extension requires AgenticQ CLI to be installed and in PATH
- First-time setup requires cloning upstream marketplace
- Catalog must be generated before use (`agenticq update`)

Report issues at: [GitHub Issues](https://github.com/sandeshbagmare/AgenticQ/issues)

## 📝 Release Notes

### 0.1.0 (2026-05-30)

**Initial Release**

- ✨ Smart project analysis and recommendations
- 📦 Browse 83 plugins across 12 domains
- 🎯 Multi-harness scaffolding support
- 🌐 Interactive dashboard webview
- 🔌 JSON-RPC bridge to Python CLI
- 📊 Domain tree view in sidebar

## 🤝 Contributing

Contributions are welcome! Please visit:
- **Repository**: [github.com/sandeshbagmare/AgenticQ](https://github.com/sandeshbagmare/AgenticQ)
- **Issues**: [github.com/sandeshbagmare/AgenticQ/issues](https://github.com/sandeshbagmare/AgenticQ/issues)

## 📄 License

MIT License - see [LICENSE](https://github.com/sandeshbagmare/AgenticQ/blob/main/LICENSE)

## 🙏 Credits

AgenticQ indexes and scaffolds plugins from the **[wshobson/agents](https://github.com/wshobson/agents)** marketplace:

- **Seth Hobson** ([@wshobson](https://github.com/wshobson)) - Primary author and maintainer
- **Community Contributors** - Plugin authors and contributors

## 🔗 Links

- **Marketplace**: [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=sandeshbagmare.agenticq)
- **Repository**: [GitHub](https://github.com/sandeshbagmare/AgenticQ)
- **Documentation**: [README](https://github.com/sandeshbagmare/AgenticQ#readme)
- **Upstream Marketplace**: [wshobson/agents](https://github.com/wshobson/agents)

---

**Enjoy building smarter with AgenticQ!** 🚀
