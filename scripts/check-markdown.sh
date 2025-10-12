#!/bin/bash

# Markdown validation script for local development
# Run this before committing to catch issues early

set -e

echo "🔍 Checking Markdown files..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if tools are installed
LINT_INSTALLED=false
LINK_CHECK_INSTALLED=false

if command -v markdownlint &> /dev/null; then
    LINT_INSTALLED=true
fi

if command -v markdown-link-check &> /dev/null; then
    LINK_CHECK_INSTALLED=true
fi

# Install if needed
if [ "$LINT_INSTALLED" = false ] || [ "$LINK_CHECK_INSTALLED" = false ]; then
    echo "📦 Installing required tools..."
    echo ""

    if [ "$LINT_INSTALLED" = false ]; then
        echo "Installing markdownlint-cli..."
        npm install -g markdownlint-cli
    fi

    if [ "$LINK_CHECK_INSTALLED" = false ]; then
        echo "Installing markdown-link-check..."
        npm install -g markdown-link-check
    fi

    echo ""
fi

# Run markdown linting
echo "1️⃣  Running Markdown Linting..."
echo ""

if markdownlint '**/*.md' --ignore node_modules --ignore venv --ignore backend/venv --ignore frontend/node_modules --ignore backend/htmlcov 2>&1; then
    echo -e "${GREEN}✅ Markdown linting passed!${NC}"
    LINT_STATUS=0
else
    echo -e "${RED}❌ Markdown linting found issues${NC}"
    echo ""
    echo "Run 'markdownlint --fix **/*.md' to auto-fix some issues"
    LINT_STATUS=1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run link checking
echo "2️⃣  Running Link Validation..."
echo ""

LINK_STATUS=0

# Critical files that must pass
CRITICAL_FILES=(
    "README.md"
    "START_HERE.md"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Checking: $file"
        if markdown-link-check "$file" --config .markdown-link-check.json --quiet; then
            echo -e "${GREEN}✅ $file${NC}"
        else
            echo -e "${RED}❌ $file has broken links${NC}"
            LINK_STATUS=1
        fi
    fi
done

echo ""
echo -e "${YELLOW}Checking other markdown files (non-blocking)...${NC}"

# Non-critical files (informational only)
find docs labs tests -name "*.md" -not -path "*/node_modules/*" -not -path "*/venv/*" 2>/dev/null | while read -r file; do
    echo "Checking: $file"
    markdown-link-check "$file" --config .markdown-link-check.json --quiet || echo "  ⚠️  Some links may be broken (non-blocking)"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
echo "📊 Summary:"
echo ""

if [ $LINT_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Markdown Linting: PASSED${NC}"
else
    echo -e "${RED}❌ Markdown Linting: FAILED${NC}"
fi

if [ $LINK_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Link Validation: PASSED${NC}"
else
    echo -e "${RED}❌ Link Validation: FAILED${NC}"
fi

echo ""

# Exit with error if critical checks failed
if [ $LINT_STATUS -ne 0 ] || [ $LINK_STATUS -ne 0 ]; then
    echo -e "${RED}❌ Markdown validation failed!${NC}"
    echo ""
    echo "Fix the issues above before committing."
    exit 1
fi

echo -e "${GREEN}✅ All markdown validation checks passed!${NC}"
echo ""
echo "You're good to commit! 🚀"
exit 0

