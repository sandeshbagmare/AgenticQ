# AgenticQ Production Readiness Audit — Confirmed Defects

**Date:** 2026-05-30  
**Audit Method:** Parallel adversarial audit across 5 surfaces (CLI, Web, JSON-RPC, VS Code extension, Packaging)  
**Agents:** 37 subagents (5 auditors + 32 verifiers, 6 failed schema compliance)  
**Result:** 26 confirmed high/critical defects, 9 medium/low

---

## Critical Defects (Must Fix)

### Cross-Cutting: Hardcoded Paths (4 files)
- **Files:** `cli.py:30`, `catalog.py:155`, `jsonrpc.py:20`, `web.py:22`
- **Issue:** Hardcoded `C:\Users\sande\AppData\Local\Temp\wshobson-agents-research` breaks portability
- **Fix:** Use `Path(os.getenv('AGENTICQ_UPSTREAM', Path.home() / '.agenticq' / 'upstream'))`

### CLI
1. **Missing `__main__.py`** — `python -m agenticq` fails
   - Fix: Create `src/agenticq/__main__.py` with `from .cli import app; app()`

2. **ProjectProfile missing `project_path` attribute** — `runtime_builder.py:430` crashes
   - Fix: Add `project_path: str = Field(default='.')` to `models/project.py`

3. **Emoji output crashes on cp1252** — `catalog.py:123,125,127` uses plain `print()` with emoji
   - Fix: Replace emoji with ASCII or use Rich Console

4. **Runtime builder not exposed** — Feature advertised but no CLI command
   - Fix: Add `@app.command() def build(...)` that calls `runtime_builder.build_runtime_agent()`

### Web GUI
5. **Missing `/api/domains` endpoint** — Frontend calls it, server doesn't implement
   - Fix: Add route + handler returning taxonomy domains

6. **Missing `/api/plugins` endpoint** — Frontend calls it, server doesn't implement
   - Fix: Add route + handler returning catalog plugins

7. **Recommendations endpoint mismatch** — Frontend sends `{description}`, backend expects `{path}`
   - Fix: Accept `description` field and use semantic matching OR update frontend

8. **Response field mismatch** — Backend returns `{plugin_name, relevance_score, ...}`, frontend expects `{name, score, domain, ...}`
   - Fix: Align response format

9. **No Agent Builder backend** — Full UI tab but `generateAgent()` is pure client-side mock
   - Fix: Implement `/api/agent` POST endpoint

### JSON-RPC
10. **Full 200KB catalog returned on every call** — No caching
    - Fix: Add in-memory cache with TTL or implement `catalog/summary` method

11. **Missing error handling** — Returns `{plugins:[]}` when catalog missing instead of RPC error
    - Fix: Return proper JSON-RPC error `-32603` with message

### VS Code Extension
12. **Missing TreeDataProvider for `agenticqPlugins` view** — View declared but shows nothing
    - Fix: Create `PluginsTreeProvider` and register it

13. **pythonBridge ignores `agenticq.pythonPath` setting** — Hardcodes `spawn('agenticq')`
    - Fix: Read config, fall back to `python -m agenticq`

14. **No spawn error handling** — Fails silently if `agenticq` not in PATH
    - Fix: Add `.on('error', ...)` handler and notify user

15. **`autoRecommend` and `defaultHarness` settings unused** — Declared but never read
    - Fix: Read config in `activate()`, trigger recommend if enabled, pre-select harness

16. **Dashboard webview is dead stub** — Static HTML, no data or interactivity
    - Fix: Fetch catalog, render cards, add message passing

17. **Tree items not clickable** — No command to scaffold from tree
    - Fix: Set `item.command = { command: 'agenticq.scaffold', arguments: [pluginName] }`

### Packaging
18. **pyproject.toml missing package-data** — `catalog.json` / `taxonomy.json` won't ship with wheel
    - Fix: Add `[tool.setuptools.package-data]` or use `include_package_data=True`

19. **pyproject.toml missing PyPI metadata** — No readme, license, URLs
    - Fix: Add `readme`, `license`, `[project.urls]`

---

## High-Severity Defects

20. **Update command depends on hardcoded upstream** (covered by #1)
21. **No CORS headers** — Cross-origin requests blocked
    - Fix: Add `aiohttp_cors` middleware
22. **Agent Builder pure mock** — Download/deploy buttons just `alert()`
    - Fix: Implement actual download/deploy logic

---

## Medium/Low (9 defects)
- Generic exception handling exposes internals
- No request/response schema validation
- Frontend silently falls back to mock data
- Request timeout memory leak in pending map
- `.vscodeignore` excludes README.md
- Missing root CHANGELOG.md
- Test suite lacks integration tests
- Extension README claims 83 plugins (should be 81)
- Extension requires CLI in PATH with no activation check

---

## Rejected (2 false positives)
- Static route ordering (aiohttp checks exact routes first)
- Print statements corrupt JSON-RPC (build_catalog not called in RPC path)

---

## Implementation Priority

**Phase 1 (Blocking):**
1. Fix hardcoded paths (4 files) → env var
2. Add `__main__.py`
3. Fix `ProjectProfile.project_path`
4. Add missing web endpoints (`/api/domains`, `/api/plugins`)
5. Fix VS Code pythonBridge (read config, error handling)
6. Register `PluginsTreeProvider`

**Phase 2 (High-value):**
7. Wire `autoRecommend` / `defaultHarness` settings
8. Build real dashboard webview
9. Add catalog caching in JSON-RPC
10. Fix web response field mismatch
11. Add CLI `build` command for runtime builder
12. Fix pyproject.toml package-data + metadata

**Phase 3 (Polish):**
13. Implement Agent Builder backend
14. Add CORS
15. Make tree items clickable
16. Add tests for server/jsonrpc/web
17. Update all docs with correct stats (81 plugins)
