# Quick Setup & Test (PowerShell)

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "AgenticQ Setup & Test" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Install package
Write-Host "`n1. Installing AgenticQ..." -ForegroundColor Yellow
pip install -e . --quiet

# Generate catalog
Write-Host "`n2. Generating catalog from upstream..." -ForegroundColor Yellow
python src/agenticq/core/catalog.py

# Test CLI
Write-Host "`n3. Testing CLI commands..." -ForegroundColor Yellow
python -m agenticq.cli version
Write-Host ""
python -m agenticq.cli browse | Select-Object -First 50

# Run tests
Write-Host "`n4. Running test suite..." -ForegroundColor Yellow
pytest tests/ -v

Write-Host "`n==================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host "`nTry these commands:"
Write-Host "  agenticq recommend"
Write-Host "  agenticq search python"
Write-Host "  agenticq info python-development"
Write-Host ""
