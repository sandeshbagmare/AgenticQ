# Change Log

All notable changes to the AgenticQ VS Code extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-30

### Added
- Initial release of AgenticQ VS Code extension
- Smart project analysis and plugin recommendations
- Browse 83 plugins across 12 domains
- Multi-harness scaffolding support (Claude Code, Cursor, Gemini, Codex, OpenCode, Copilot)
- Interactive dashboard webview
- JSON-RPC bridge to Python CLI backend
- Domain tree view in sidebar
- Four main commands:
  - `AgenticQ: Get Recommendations` - Analyze project and recommend plugins
  - `AgenticQ: Browse Domains` - Browse all domains and plugins
  - `AgenticQ: Scaffold Plugins` - Scaffold selected plugins
  - `AgenticQ: Open Dashboard` - Open interactive dashboard
- Progress notifications for long-running operations
- Error handling and user feedback
- TypeScript implementation with strict type checking

### Features
- **Smart Detection**: Automatically detects languages, frameworks, infrastructure, databases, and testing tools
- **Token Optimization**: Shows estimated token costs for each plugin
- **Relevance Scoring**: Ranks plugins by relevance to your project
- **Multi-Selection**: Select multiple plugins to scaffold at once
- **Harness Support**: Choose target harness for scaffolding
- **Real-time Updates**: Refresh domain tree on demand

### Technical Details
- TypeScript 5.0+
- VS Code API 1.80.0+
- Python bridge using JSON-RPC protocol
- Async/await for all operations
- Event-driven tree data provider
- Webview integration for dashboard

## [Unreleased]

### Planned Features
- Configuration settings for Python path and default harness
- Auto-recommend on project open (configurable)
- Plugin conflict detection and resolution
- Custom taxonomy support
- Plugin usage analytics
- Inline plugin documentation
- Quick actions in tree view
- Search functionality in domain browser
- Plugin comparison view
- Export recommendations to file
- Integration with VS Code tasks
- Keyboard shortcuts for common actions

### Future Enhancements
- LLM-powered recommendations (optional, with API key)
- Plugin dependency visualization
- Token cost calculator
- Custom plugin creation wizard
- Marketplace integration for custom plugins
- Team sharing of plugin configurations
- Project templates with pre-configured plugins

---

## Version History

- **0.1.0** (2026-05-30) - Initial release

---

For more information, visit:
- [GitHub Repository](https://github.com/sandeshbagmare/AgenticQ)
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=sandeshbagmare.agenticq)
- [Documentation](https://github.com/sandeshbagmare/AgenticQ#readme)
