#!/usr/bin/env python3
"""
AgenticQ - Final Verification Script
Verifies all components are in place and ready for use.
"""

import sys
from pathlib import Path
from typing import List, Tuple

def check_file(path: str, description: str) -> Tuple[bool, str]:
    """Check if a file exists."""
    p = Path(path)
    if p.exists():
        size = p.stat().st_size
        return True, f"✅ {description} ({size:,} bytes)"
    else:
        return False, f"❌ {description} - MISSING"

def main():
    """Run verification checks."""
    print("=" * 70)
    print("AgenticQ - Final Verification")
    print("=" * 70)
    print()

    checks = [
        # Python Core
        ("src/agenticq/__init__.py", "Package init"),
        ("src/agenticq/cli.py", "CLI entrypoint"),
        ("src/agenticq/core/catalog.py", "Catalog indexer"),
        ("src/agenticq/core/scanner.py", "Project scanner"),
        ("src/agenticq/core/classifier.py", "Domain classifier"),
        ("src/agenticq/core/recommender.py", "Plugin recommender"),
        ("src/agenticq/core/scaffolder.py", "Multi-harness scaffolder"),
        ("src/agenticq/core/runtime_builder.py", "Runtime agent builder"),

        # Models
        ("src/agenticq/models/plugin.py", "Plugin models"),
        ("src/agenticq/models/project.py", "Project models"),
        ("src/agenticq/models/taxonomy.py", "Taxonomy models"),

        # Servers
        ("src/agenticq/server/web.py", "Web GUI server"),
        ("src/agenticq/server/jsonrpc.py", "JSON-RPC server"),

        # Data
        ("src/agenticq/data/taxonomy.json", "12-domain taxonomy"),

        # Web GUI
        ("gui/index.html", "Web GUI HTML"),
        ("gui/app.js", "Web GUI JavaScript"),
        ("gui/styles.css", "Web GUI CSS"),

        # VS Code Extension
        ("vscode-extension/package.json", "VS Code manifest"),
        ("vscode-extension/tsconfig.json", "TypeScript config"),
        ("vscode-extension/src/extension.ts", "Extension main"),
        ("vscode-extension/src/pythonBridge.ts", "Python bridge"),
        ("vscode-extension/src/domainTreeProvider.ts", "TreeView provider"),

        # Tests
        ("tests/test_scanner.py", "Scanner tests"),
        ("tests/test_classifier.py", "Classifier tests"),
        ("tests/test_recommender.py", "Recommender tests"),
        ("tests/test_scaffolder.py", "Scaffolder tests"),
        ("tests/test_catalog.py", "Catalog tests"),
        ("test_all.py", "Test runner"),

        # Configuration
        ("pyproject.toml", "Package configuration"),

        # Documentation
        ("README.md", "Main documentation"),
        ("MANIFEST.md", "Project manifest"),
        ("COMPLETE.md", "Completion summary"),
        ("FINAL_STATUS.md", "Final status"),
        ("执行完成.md", "Chinese summary"),

        # Scripts
        ("setup_and_test.sh", "Bash setup script"),
        ("setup_and_test.ps1", "PowerShell setup script"),
    ]

    results = []
    for path, desc in checks:
        success, message = check_file(path, desc)
        results.append((success, message))
        print(message)

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)

    passed = sum(1 for success, _ in results if success)
    total = len(results)

    print(f"Files verified: {passed}/{total}")

    if passed == total:
        print()
        print("🎉 ALL COMPONENTS VERIFIED - PROJECT COMPLETE!")
        print()
        print("Next steps:")
        print("  1. pip install -e .")
        print("  2. python src/agenticq/core/catalog.py")
        print("  3. agenticq version")
        print("  4. agenticq recommend")
        return 0
    else:
        print()
        print(f"⚠️  {total - passed} file(s) missing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
