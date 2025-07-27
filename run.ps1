# Password Manager PowerShell Script
# Windows alternative to the Makefile

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Password Manager - Available Commands" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Setup Commands:" -ForegroundColor Yellow
    Write-Host "  install      - Install dependencies"
    Write-Host "  validate     - Validate project setup"
    Write-Host "  quick-start  - Quick start with validation"
    Write-Host ""
    Write-Host "Development Commands:" -ForegroundColor Yellow
    Write-Host "  test         - Run all tests"
    Write-Host "  test-verbose - Run tests with verbose output"
    Write-Host "  lint         - Run code linting"
    Write-Host ""
    Write-Host "Run Commands:" -ForegroundColor Yellow
    Write-Host "  cli          - Run CLI interface"
    Write-Host "  gui          - Run GUI interface"
    Write-Host "  demo         - Run demo script"
    Write-Host "  demo-multi   - Run Multi-Vault demo script"
    Write-Host ""
    Write-Host "Utility Commands:" -ForegroundColor Yellow
    Write-Host "  clean        - Clean up temporary files"
    Write-Host '  check        - Run all checks (install, validate, test)'
    Write-Host ""
    Write-Host "Usage: .\run.ps1 [command]" -ForegroundColor Green
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
    Write-Host "Dependencies installed" -ForegroundColor Green
}

function Validate-Setup {
    Write-Host "Validating project setup..." -ForegroundColor Green
    python scripts/validate_setup.py
}

function Quick-Start {
    Write-Host "Running quick start..." -ForegroundColor Green
    python scripts/quick_start.py
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    python -m pytest tests/ -v
}

function Run-TestsVerbose {
    Write-Host "Running tests with verbose output..." -ForegroundColor Green
    python -m pytest tests/ -vv --tb=short
}

function Run-TestsCov {
    Write-Host "Running tests with coverage..." -ForegroundColor Green
    python -m pytest tests/ --cov=pm_core --cov-report=html --cov-report=term-missing
}

function Run-TestsFast {
    Write-Host "Running fast tests only..." -ForegroundColor Green
    python -m pytest tests/ -m "not slow" -v
}

function Run-TestsSecurity {
    Write-Host "Running security tests..." -ForegroundColor Green
    python -m pytest tests/ -m security -v
}

function Run-TestsPerformance {
    Write-Host "Running performance tests..." -ForegroundColor Green
    python -m pytest tests/ -m performance -v
}

function Run-TestsParallel {
    Write-Host "Running tests in parallel..." -ForegroundColor Green
    python -m pytest tests/ -n auto -v
}

function Run-Lint {
    Write-Host "Running linting..." -ForegroundColor Green
    python -m flake8 pm_core/ cli/ gui/ tests/
    python -m black --check pm_core/ cli/ gui/ tests/
}

function Start-CLI {
    Write-Host "Starting CLI..." -ForegroundColor Green
    python -m cli.multi_vault_cli
}



function Start-GUI {
    Write-Host "Starting GUI..." -ForegroundColor Green
    python -m gui.app
}

function Run-Demo {
    Write-Host "Running demo..." -ForegroundColor Green
    python scripts/run_tests.py
}

function Run-MultiVaultDemo {
    Write-Host "Running Multi-Vault demo..." -ForegroundColor Green
    python scripts/demo_multi_vault.py
}

function Clean-Up {
    Write-Host "Cleaning up..." -ForegroundColor Green
    Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force
    Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Name "*.db" | Remove-Item -Force
    Get-ChildItem -Recurse -Name "test_*.db" | Remove-Item -Force
    Get-ChildItem -Recurse -Name "demo_*.db" | Remove-Item -Force
    Write-Host "Cleanup complete" -ForegroundColor Green
}

function Run-Check {
    Install-Dependencies
    Validate-Setup
    Run-Tests
    Write-Host "All checks passed!" -ForegroundColor Green
}

function Install-Dev {
    Write-Host "Installing in development mode..." -ForegroundColor Green
    pip install -e .
}

function Install-Prod {
    Write-Host "Installing in production mode..." -ForegroundColor Green
    pip install .
}

function Show-Docs {
    Write-Host "Generating documentation..." -ForegroundColor Green
    python -c "import pm_core; help(pm_core)"
}

function Security-Check {
    Write-Host "Running security checks..." -ForegroundColor Green
    python -c "from pm_core.crypto import generate_salt, encrypt_data, decrypt_data; print('Crypto functions available')"
    python -c "from pm_core.utils import generate_password, validate_password_strength; print('Security utils available')"
}

function Full-Check {
    Install-Dependencies
    Validate-Setup
    Security-Check
    Run-Tests
    Write-Host "All validations passed!" -ForegroundColor Green
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "validate" { Validate-Setup }
    "quick-start" { Quick-Start }
    "test" { Run-Tests }
    "test-verbose" { Run-TestsVerbose }
    "test-cov" { Run-TestsCov }
    "test-fast" { Run-TestsFast }
    "test-security" { Run-TestsSecurity }
    "test-performance" { Run-TestsPerformance }
    "test-parallel" { Run-TestsParallel }
    "lint" { Run-Lint }
    "cli" { Start-CLI }
    "gui" { Start-GUI }
    "demo" { Run-Demo }
    "demo-multi" { Run-MultiVaultDemo }
    "clean" { Clean-Up }
    "check" { Run-Check }
    "install-dev" { Install-Dev }
    "install-prod" { Install-Prod }
    "docs" { Show-Docs }
    "security-check" { Security-Check }
    "full-check" { Full-Check }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run '.\run.ps1 help' to see available commands" -ForegroundColor Yellow
    }
} 