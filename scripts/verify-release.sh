#!/bin/bash

# Release Verification Script for Testbook v1.1
# Runs comprehensive checks before tagging release
# Run with: ./scripts/verify-release.sh

set -e
set -o pipefail

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║  🔍 Testbook v1.1 Release Verification                            ║"
echo "║                                                                   ║"
echo "║  Running comprehensive checks before release...                   ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

FAILED=0

# Function to run a check
run_check() {
  local name="$1"
  local command="$2"

  echo "▶ $name"
  if eval "$command" > /dev/null 2>&1; then
    echo "  ✅ PASS"
  else
    echo "  ❌ FAIL"
    FAILED=$((FAILED + 1))
  fi
  echo ""
}

# 1. Verify all critical files exist
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Critical Files Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

FILES=(
  "README.md"
  "CHANGELOG.md"
  "LICENSE"
  "backend/requirements.txt"
  "frontend/package.json"
  ".github/workflows/testbook-ci.yml"
  "learn/README.md"
  "docs/guides/PORTFOLIO.md"
  "docs/guides/QUALITY_CHECKS.md"
  "docs/guides/ACCESSIBILITY_TESTING.md"
)

for file in "${FILES[@]}"; do
  run_check "File exists: $file" "test -f $file"
done

# 2. Documentation cross-linking
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Documentation Links Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_check "README links to learn/" "grep -q 'learn/' README.md"
run_check "README links to PORTFOLIO" "grep -q 'PORTFOLIO' README.md"
run_check "START_HERE mentions learn/" "grep -q 'learn/' START_HERE.md"
run_check "INDEX has all guides" "grep -q 'QUALITY_CHECKS' docs/INDEX.md && grep -q 'ACCESSIBILITY_TESTING' docs/INDEX.md"

# 3. Backend tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Backend Tests (this will take ~1 minute)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd backend
source .venv/bin/activate 2>/dev/null || true

run_check "Backend linting (Black)" "black --check ."
run_check "Backend linting (Flake8)" "flake8 ."
run_check "Backend tests" "TESTING=true pytest -q"
run_check "Backend coverage ≥80%" "TESTING=true pytest --cov --cov-fail-under=80 -q"

cd ..

# 4. Frontend tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Frontend Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd frontend

run_check "Frontend linting (ESLint)" "npm run lint"
run_check "Frontend formatting (Prettier)" "npm run format:check"
run_check "Frontend tests" "npm test -- --run"

cd ..

# 5. Configuration files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Configuration Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_check "CI workflow valid" "grep -q 'lint-backend' .github/workflows/testbook-ci.yml"
run_check "Pre-commit config valid" "test -f .pre-commit-config.yaml"
run_check "Lighthouse config valid" "test -f lighthouserc.js"
run_check "Accessibility tests exist" "test -f tests/e2e/accessibility-axe.spec.js"

# 6. Check screenshots
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Visual Assets"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_check "Screenshots directory exists" "[ -d docs/screenshots ]"
run_check "Dashboard screenshot exists" "[ -f docs/screenshots/testbook-dashboard.png ]"
run_check "Backend tests screenshot exists" "[ -f docs/screenshots/backend-tests-passing.png ]"
run_check "Coverage screenshot exists" "[ -f docs/screenshots/coverage_report.png ]"
run_check "Frontend tests screenshot exists" "[ -f docs/screenshots/frontend-tests.png ]"
run_check "E2E GIF exists" "[ -f docs/screenshots/e2e-test-running.gif ]"

# 7. Check badges
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. README Badges"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_check "CI badge exists" "grep -q 'CI Status' README.md"
run_check "Coverage badges exist" "grep -q 'Backend Coverage' README.md && grep -q 'Frontend Coverage' README.md"
run_check "Test count badge" "grep -q '210' README.md"

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VERIFICATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "✅ ALL CHECKS PASSED!"
  echo ""
  echo "🎉 Testbook v1.1 is ready for release!"
  echo ""
  echo "Next steps:"
  echo "  1. Review CHANGELOG.md"
  echo "  2. git add ."
  echo "  3. git commit -m 'Release v1.1: Full Journey Release'"
  echo "  4. git tag v1.1"
  echo "  5. git push origin dev"
  echo "  6. git push origin v1.1"
  echo ""
  exit 0
else
  echo "❌ $FAILED CHECK(S) FAILED"
  echo ""
  echo "Please fix the issues above before releasing."
  echo ""
  exit 1
fi

