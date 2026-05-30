#!/usr/bin/env bash
# Quick setup script for AgenticQ

set -e

echo "=================================="
echo "AgenticQ Setup & Test"
echo "=================================="

# Install package
echo ""
echo "1. Installing AgenticQ..."
pip install -e . --quiet

# Generate catalog
echo ""
echo "2. Generating catalog from upstream..."
python src/agenticq/core/catalog.py

# Test CLI
echo ""
echo "3. Testing CLI commands..."
python -m agenticq.cli version
echo ""
python -m agenticq.cli browse | head -50

# Run tests
echo ""
echo "4. Running test suite..."
pytest tests/ -v

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Try these commands:"
echo "  agenticq recommend"
echo "  agenticq search python"
echo "  agenticq info python-development"
echo ""
