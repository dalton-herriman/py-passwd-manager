# Password Manager Makefile
# Provides common commands to prevent errors and simplify development

.PHONY: help install test run clean validate quick-start

# Default target
help:
	@echo "🔐 Password Manager - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install      - Install dependencies"
	@echo "  validate     - Validate project setup"
	@echo "  quick-start  - Quick start with validation"
	@echo ""
	@echo "Development Commands:"
	@echo "  test         - Run all tests"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  lint         - Run code linting"
	@echo ""
	@echo "Run Commands:"
	@echo "  cli          - Run CLI interface"
	@echo "  gui          - Run GUI interface"
	@echo "  demo         - Run demo script"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean        - Clean up temporary files"
	@echo "  check        - Run all checks (install, validate, test)"

# Setup commands
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

validate:
	@echo "🔍 Validating project setup..."
	python scripts/validate_setup.py

quick-start:
	@echo "🚀 Running quick start..."
	python scripts/quick_start.py

# Development commands
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

test-verbose:
	@echo "🧪 Running tests with verbose output..."
	python -m pytest tests/ -vv --tb=short

test-cov:
	@echo "🧪 Running tests with coverage..."
	python -m pytest tests/ --cov=pm_core --cov-report=html --cov-report=term-missing

test-fast:
	@echo "🧪 Running fast tests only..."
	python -m pytest tests/ -m "not slow" -v

test-security:
	@echo "🔒 Running security tests..."
	python -m pytest tests/ -m security -v

test-performance:
	@echo "⚡ Running performance tests..."
	python -m pytest tests/ -m performance -v

test-parallel:
	@echo "🧪 Running tests in parallel..."
	python -m pytest tests/ -n auto -v

lint:
	@echo "🔍 Running linting..."
	python -m flake8 pm_core/ cli/ gui/ tests/
	python -m black --check pm_core/ cli/ gui/ tests/

# Run commands
cli:
	@echo "💻 Starting CLI..."
	python -m cli.main

gui:
	@echo "🖥️  Starting GUI..."
	python -m gui.app

demo:
	@echo "🎬 Running demo..."
	python scripts/run_tests.py

# Utility commands
clean:
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.db" -delete
	@find . -type f -name "test_*.db" -delete
	@find . -type f -name "demo_*.db" -delete
	@echo "✅ Cleanup complete"

check: install validate test
	@echo "✅ All checks passed!"

# Platform-specific commands
install-dev:
	@echo "📦 Installing in development mode..."
	pip install -e .

install-prod:
	@echo "📦 Installing in production mode..."
	pip install .

# Documentation
docs:
	@echo "📚 Generating documentation..."
	python -c "import pm_core; help(pm_core)"

# Security check
security-check:
	@echo "🔒 Running security checks..."
	python -c "from pm_core.crypto import generate_salt, encrypt_data, decrypt_data; print('✅ Crypto functions available')"
	python -c "from pm_core.utils import generate_password, validate_password_strength; print('✅ Security utils available')"

# Full validation
full-check: install validate security-check test
	@echo "🎉 All validations passed!" 