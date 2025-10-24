# Testbook Development Task Runner
# Cross-platform task automation using Make

.PHONY: help install install-backend install-frontend install-tests setup start start-backend start-frontend test test-backend test-frontend test-frontend-a11y test-frontend-contracts test-frontend-coverage test-e2e test-e2e-all test-e2e-a11y test-security test-performance test-contract test-all coverage lint format format-check quality-check verify-release install-browsers install-browsers-all run-all-tests run-tests-no-warnings clean reset-db docker-up docker-down

# Default target - show help
help:
	@echo "Testbook Task Runner"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install          - Install all dependencies (backend + frontend + tests)"
	@echo "  make install-backend  - Install backend dependencies only"
	@echo "  make install-frontend - Install frontend dependencies only"
	@echo "  make install-tests    - Install test dependencies only"
	@echo "  make setup            - Complete setup (install + seed database)"
	@echo ""
	@echo "Development Commands:"
	@echo "  make start            - Start both backend and frontend servers"
	@echo "  make start-backend    - Start backend server only"
	@echo "  make start-frontend   - Start frontend server only"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test             - Run all tests"
	@echo "  make test-backend     - Run backend unit and API tests"
	@echo "  make test-frontend    - Run frontend component tests"
	@echo "  make test-frontend-a11y - Run frontend accessibility tests"
	@echo "  make test-frontend-contracts - Run frontend contract tests"
	@echo "  make test-frontend-coverage - Run frontend tests with coverage"
	@echo "  make test-e2e         - Run E2E tests (Playwright - Chrome only)"
	@echo "  make test-e2e-all     - Run E2E tests (all browsers)"
	@echo "  make test-e2e-a11y    - Run E2E accessibility tests"
	@echo "  make test-security    - Run security tests"
	@echo "  make test-performance - Run performance tests"
	@echo "  make test-contract    - Run API contract tests"
	@echo "  make test-all         - Run comprehensive test suite"
	@echo "  make coverage         - Generate test coverage report"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make lint             - Run linters on all code"
	@echo "  make lint-backend     - Lint backend code"
	@echo "  make lint-frontend    - Lint frontend code"
	@echo "  make format           - Format all code"
	@echo "  make format-check     - Check formatting without fixing"
	@echo "  make quality-check    - Run comprehensive quality checks"
	@echo "  make verify-release   - Pre-release verification"
	@echo "  make check-markdown   - Validate markdown (lint + links)"
	@echo "  make lint-markdown    - Lint markdown only"
	@echo "  make fix-markdown     - Auto-fix markdown issues"
	@echo ""
	@echo "Database Commands:"
	@echo "  make reset-db         - Reset and seed the database"
	@echo "  make seed             - Seed database with test data"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up        - Start services with Docker Compose"
	@echo "  make docker-down      - Stop Docker services"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install-browsers - Install Playwright browsers (Chrome only)"
	@echo "  make install-browsers-all - Install all Playwright browsers"
	@echo ""
	@echo "Script Commands:"
	@echo "  make run-all-tests    - Run comprehensive test suite (script)"
	@echo "  make run-tests-no-warnings - Run tests without color warnings"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean            - Remove temporary files and caches"
	@echo "  make clean-all        - Deep clean (includes dependencies)"

# Installation
install: install-backend install-frontend install-tests

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m .venv .venv
	cd backend && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install

install-tests:
	@echo "📦 Installing test dependencies..."
	cd tests && npm install
	@if [ -f tests/e2e-python/requirements.txt ]; then \
		cd tests/e2e-python && pip install -r requirements.txt; \
	fi
	@if [ -f tests/security/requirements.txt ]; then \
		cd tests/security && pip install -r requirements.txt; \
	fi

setup: install
	@echo "🗄️  Setting up database..."
	cd backend && . .venv/bin/activate && python seed.py
	@echo "✅ Setup complete!"

# Development
start:
	@echo "Starting backend and frontend servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@bash -c "trap 'kill 0' EXIT; \
		cd backend && . .venv/bin/activate && uvicorn main:app --reload & \
		cd frontend && npm run dev & \
		wait"

start-backend:
	@echo "🚀 Starting backend server on http://localhost:8000"
	cd backend && . .venv/bin/activate && uvicorn main:app --reload

start-frontend:
	@echo "🚀 Starting frontend server on http://localhost:3000"
	cd frontend && npm run dev

# Testing
test: test-backend test-frontend

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && . .venv/bin/activate && TESTING=true pytest -v --cov=. --cov-report=html --cov-report=term-missing

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test -- --run

test-frontend-a11y:
	@echo "♿ Running frontend accessibility tests..."
	cd frontend && npm run test:a11y

test-frontend-contracts:
	@echo "📋 Running frontend contract tests..."
	cd frontend && npm run test:contracts

test-frontend-coverage:
	@echo "📊 Running frontend tests with coverage..."
	cd frontend && npm run test:coverage

test-e2e:
	@echo "🧪 Running E2E tests (Chrome only)..."
	cd tests && npm test

test-e2e-all:
	@echo "🧪 Running E2E tests (all browsers)..."
	cd tests && npm run test:all-browsers

test-e2e-a11y:
	@echo "♿ Running E2E accessibility tests..."
	cd tests && npm run test:a11y

test-security:
	@echo "🔒 Running security tests..."
	cd tests/security && pytest -v

test-performance:
	@echo "⚡ Running performance tests..."
	cd tests/performance && k6 run load-test.js

test-contract:
	@echo "📋 Running API contract tests..."
	cd backend && . .venv/bin/activate && TESTING=true pytest tests/test_api_contract.py -v

test-all:
	@echo "🧪 Running comprehensive test suite..."
	@bash run-all-tests.sh

coverage:
	@echo "📊 Generating coverage report..."
	cd backend && . .venv/bin/activate && TESTING=true pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in backend/htmlcov/index.html"

# Code Quality
lint: lint-backend lint-frontend

lint-backend:
	@echo "🔍 Linting backend code..."
	cd backend && pip install ruff && ruff check .

lint-frontend:
	@echo "🔍 Linting frontend code..."
	cd frontend && npm run lint || echo "Add lint script to frontend/package.json"

format:
	@echo "✨ Formatting code..."
	cd backend && pip install black && black .
	cd frontend && npx prettier --write "src/**/*.{js,jsx,css}"

format-check:
	@echo "🔍 Checking code formatting..."
	cd backend && pip install black && black --check --diff .
	cd frontend && npx prettier --check "src/**/*.{js,jsx,css}"

quality-check:
	@echo "🔍 Running comprehensive quality checks..."
	@bash scripts/quality-check.sh

verify-release:
	@echo "🔍 Running pre-release verification..."
	@bash scripts/verify-release.sh

# Database
reset-db:
	@echo "🗄️  Resetting database..."
	@bash reset-database.sh

seed:
	@echo "🌱 Seeding database..."
	cd backend && . .venv/bin/activate && python seed.py

install-browsers:
	@echo "🌐 Installing Playwright browsers (Chrome only)..."
	cd tests && npm run install-browsers

install-browsers-all:
	@echo "🌐 Installing all Playwright browsers..."
	cd tests && npx playwright install

run-all-tests:
	@echo "🧪 Running comprehensive test suite..."
	@bash run-all-tests.sh

run-tests-no-warnings:
	@echo "🧪 Running tests without color warnings..."
	@bash scripts/run-tests-no-warnings.sh

# Docker
docker-up:
	@echo "🐳 Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose down

# Cleanup
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -rf backend/htmlcov backend/.coverage 2>/dev/null || true
	rm -rf tests/playwright-report tests/test-results 2>/dev/null || true
	rm -rf frontend/coverage 2>/dev/null || true
	@echo "✅ Cleanup complete"

clean-all: clean
	@echo "🧹 Deep cleaning (removing dependencies)..."
	rm -rf backend/.venv 2>/dev/null || true
	rm -rf frontend/node_modules 2>/dev/null || true
	rm -rf tests/node_modules 2>/dev/null || true
	@echo "✅ Deep cleanup complete"

clean-artifacts:
	@echo "🧹 Cleaning test and build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "test-results" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "playwright-report" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".hypothesis" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Artifacts cleaned!"

# Validation
check-markdown:
	@echo "🔍 Validating markdown files..."
	@bash scripts/check-markdown.sh

lint-markdown:
	@echo "🔍 Linting markdown files..."
	@markdownlint '**/*.md' --ignore node_modules --ignore .venv --ignore backend/.venv --ignore frontend/node_modules --ignore backend/htmlcov || echo "Run 'make fix-markdown' to auto-fix"

fix-markdown:
	@echo "✨ Auto-fixing markdown issues..."
	@markdownlint --fix '**/*.md' --ignore node_modules --ignore .venv --ignore backend/.venv --ignore frontend/node_modules --ignore backend/htmlcov
	@echo "✅ Markdown fixed!"
