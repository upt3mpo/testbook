#!/bin/bash

# Quality Check Script
# Runs all linting, formatting, and coverage checks locally
# Run with: ./scripts/quality-check.sh

set -e

echo "🔍 Running Quality Checks..."
echo ""

# Backend checks
echo "📦 Backend (Python)..."
cd backend

echo "  ✓ Black (formatting)"
black --check --diff .

echo "  ✓ Ruff (import sorting + linting)"
ruff check .

echo "  ✓ Running tests with coverage gate (80% minimum)"
pytest --cov --cov-fail-under=80

cd ..

# Frontend checks
echo ""
echo "📦 Frontend (JavaScript)..."
cd frontend

echo "  ✓ ESLint (linting)"
npm run lint

echo "  ✓ Prettier (formatting)"
npm run format:check

echo "  ✓ Running tests"
npm test -- --run

cd ..

echo ""
echo "✅ All quality checks passed!"
echo ""
echo "Optional checks:"
echo "  • Frontend accessibility: cd frontend && npm run test:a11y"
echo "  • E2E accessibility: cd tests && npm run test:a11y"
echo "  • Lighthouse: npx lhci autorun"
echo "  • Pre-commit hooks: pre-commit install && pre-commit run --all-files"
