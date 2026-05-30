#!/usr/bin/env python3
"""Comprehensive test script for AgenticQ."""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✓ PASSED")
            return True
        else:
            print(f"✗ FAILED (exit code: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print("✗ TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    """Run all tests."""
    project_root = Path(__file__).parent

    tests = [
        # Installation
        ("pip install -e .", "Install AgenticQ package"),

        # Generate catalog
        ("python src/agenticq/core/catalog.py", "Generate catalog from upstream"),

        # CLI tests
        ("python -m agenticq.cli version", "CLI version command"),
        ("python -m agenticq.cli browse", "CLI browse command"),
        ("python -m agenticq.cli search python", "CLI search command"),
        ("python -m agenticq.cli info python-development", "CLI info command"),
        ("python -m agenticq.cli recommend", "CLI recommend command"),

        # Unit tests
        ("pytest tests/test_classifier.py -v", "Classifier unit tests"),
        ("pytest tests/test_scanner.py -v", "Scanner unit tests"),

        # Verify files
        ("python -c \"from pathlib import Path; p = Path('src/agenticq/data/catalog.json'); print(f'Catalog exists: {p.exists()}'); print(f'Size: {p.stat().st_size if p.exists() else 0} bytes')\"", "Verify catalog.json"),
    ]

    results = []
    for cmd, desc in tests:
        passed = run_command(cmd, desc)
        results.append((desc, passed))

    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for desc, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {desc}")

    print(f"\n{passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
