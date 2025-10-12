# Testbook Task Runner (just)
# Modern command runner - Install: https://github.com/casey/just

# Show all available commands
default:
    @just --list

# Clean test and build artifacts
clean-artifacts:
    #!/usr/bin/env bash
    echo "🧹 Cleaning test and build artifacts..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name ".coverage" -delete 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "test-results" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "playwright-report" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".hypothesis" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    echo "✅ Artifacts cleaned!"

# Validate markdown files (linting + link checking)
check-markdown:
    #!/usr/bin/env bash
    echo "🔍 Validating markdown files..."
    bash scripts/check-markdown.sh

# Lint markdown files only
lint-markdown:
    #!/usr/bin/env bash
    echo "🔍 Linting markdown files..."
    markdownlint '**/*.md' --ignore node_modules --ignore venv --ignore backend/venv --ignore frontend/node_modules --ignore backend/htmlcov || echo "Run 'just fix-markdown' to auto-fix"

# Auto-fix markdown issues
fix-markdown:
    #!/usr/bin/env bash
    echo "✨ Auto-fixing markdown issues..."
    markdownlint --fix '**/*.md' --ignore node_modules --ignore venv --ignore backend/venv --ignore frontend/node_modules --ignore backend/htmlcov
    echo "✅ Markdown fixed!"

# Install all dependencies
install: install-backend install-frontend install-tests

# Install backend dependencies
install-backend:
    #!/usr/bin/env bash
    echo "📦 Installing backend dependencies..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

# Install frontend dependencies
install-frontend:
    #!/usr/bin/env bash
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install

# Install test dependencies
install-tests:
    #!/usr/bin/env bash
    echo "📦 Installing test dependencies..."
    cd tests && npm install
    if [ -f tests/e2e-python/requirements.txt ]; then
        cd tests/e2e-python && pip install -r requirements.txt
    fi
    if [ -f tests/security/requirements.txt ]; then
        cd tests/security && pip install -r requirements.txt
    fi

# Complete setup (install + seed)
setup: install seed
    @echo "✅ Setup complete!"

# Start both backend and frontend
start:
    #!/usr/bin/env bash
    echo "🚀 Starting backend and frontend..."
    trap 'kill 0' EXIT
    cd backend && source venv/bin/activate && uvicorn main:app --reload &
    cd frontend && npm run dev &
    wait

# Start backend only
start-backend:
    #!/usr/bin/env bash
    echo "🚀 Starting backend on http://localhost:8000"
    cd backend
    source venv/bin/activate
    uvicorn main:app --reload

# Start frontend only
start-frontend:
    #!/usr/bin/env bash
    echo "🚀 Starting frontend on http://localhost:5173"
    cd frontend && npm run dev

# Run all tests
test: test-backend test-frontend
    @echo "✅ All tests complete"

# Run backend tests
test-backend:
    #!/usr/bin/env bash
    echo "🧪 Running backend tests..."
    cd backend
    source venv/bin/activate
    TESTING=true pytest -v

# Run frontend tests
test-frontend:
    #!/usr/bin/env bash
    echo "🧪 Running frontend tests..."
    cd frontend && npm test -- --run

# Run E2E tests
test-e2e:
    #!/usr/bin/env bash
    echo "🧪 Running E2E tests..."
    cd tests && npx playwright test

# Run security tests
test-security:
    #!/usr/bin/env bash
    echo "🔒 Running security tests..."
    cd tests/security && pytest -v

# Run performance tests
test-performance:
    #!/usr/bin/env bash
    echo "⚡ Running performance tests..."
    cd tests/performance && k6 run load-test.js

# Run API contract tests
test-contract:
    #!/usr/bin/env bash
    echo "📋 Running contract tests..."
    cd backend
    source venv/bin/activate
    TESTING=true pytest tests/test_api_contract.py -v

# Generate coverage report
coverage:
    #!/usr/bin/env bash
    echo "📊 Generating coverage..."
    cd backend
    source venv/bin/activate
    TESTING=true pytest --cov=. --cov-report=html --cov-report=term
    echo "Report: backend/htmlcov/index.html"

# Lint all code
lint: lint-backend lint-frontend

# Lint backend
lint-backend:
    #!/usr/bin/env bash
    echo "🔍 Linting backend..."
    cd backend && pip install ruff && ruff check .

# Lint frontend
lint-frontend:
    #!/usr/bin/env bash
    echo "🔍 Linting frontend..."
    cd frontend && npm run lint || echo "Add lint script to package.json"

# Format all code
format:
    #!/usr/bin/env bash
    echo "✨ Formatting code..."
    cd backend && pip install black && black .
    cd frontend && npx prettier --write "src/**/*.{js,jsx,css}"

# Reset database
reset-db:
    #!/usr/bin/env bash
    echo "🗄️ Resetting database..."
    bash reset-database.sh

# Seed database
seed:
    #!/usr/bin/env bash
    echo "🌱 Seeding database..."
    cd backend
    source venv/bin/activate
    python seed.py

# Start Docker services
docker-up:
    @echo "🐳 Starting Docker..."
    docker-compose up -d

# Stop Docker services
docker-down:
    @echo "🐳 Stopping Docker..."
    docker-compose down

# Clean temporary files
clean:
    #!/usr/bin/env bash
    echo "🧹 Cleaning..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name ".DS_Store" -delete 2>/dev/null || true
    rm -rf backend/htmlcov backend/.coverage 2>/dev/null || true
    rm -rf tests/playwright-report tests/test-results 2>/dev/null || true
    rm -rf frontend/coverage 2>/dev/null || true
    echo "✅ Cleanup complete"

# Deep clean (including dependencies)
clean-all: clean
    #!/usr/bin/env bash
    echo "🧹 Deep cleaning..."
    rm -rf backend/venv 2>/dev/null || true
    rm -rf frontend/node_modules 2>/dev/null || true
    rm -rf tests/node_modules 2>/dev/null || true
    echo "✅ Deep cleanup complete"

