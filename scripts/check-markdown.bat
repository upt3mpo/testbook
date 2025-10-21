@echo off
REM Markdown validation script for Windows
REM Run this before committing to catch issues early

echo.
echo 🔍 Checking Markdown files...
echo.

REM Check if tools are installed
where markdownlint >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing markdownlint-cli...
    call npm install -g markdownlint-cli
)

where markdown-link-check >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing markdown-link-check...
    call npm install -g markdown-link-check
)

echo.

REM Run markdown linting
echo 1️⃣  Running Markdown Linting...
echo.

markdownlint "**/*.md" --ignore node_modules --ignore venv --ignore backend/venv --ignore frontend/node_modules --ignore backend/htmlcov
if errorlevel 1 (
    echo.
    echo ❌ Markdown linting found issues
    echo.
    echo Run 'markdownlint --fix **/*.md' to auto-fix some issues
    set LINT_FAILED=1
) else (
    echo ✅ Markdown linting passed!
    set LINT_FAILED=0
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Run link checking
echo 2️⃣  Running Link Validation...
echo.

set LINK_FAILED=0

echo Checking: README.md
markdown-link-check README.md --config .markdown-link-check.json --quiet
if errorlevel 1 (
    echo ❌ README.md has broken links
    set LINK_FAILED=1
) else (
    echo ✅ README.md
)

echo Checking: learn/README.md
markdown-link-check learn/README.md --config .markdown-link-check.json --quiet
if errorlevel 1 (
    echo ❌ learn/README.md has broken links
    set LINK_FAILED=1
) else (
    echo ✅ learn/README.md
)

echo.
echo ⚠️  Checking other markdown files ^(non-blocking^)...
echo.

REM Check docs
for /r docs %%f in (*.md) do (
    echo Checking: %%f
    markdown-link-check "%%f" --config .markdown-link-check.json --quiet >nul 2>&1 || echo   ⚠️  Some links may be broken ^(non-blocking^)
)

REM Check labs
for /r labs %%f in (*.md) do (
    echo Checking: %%f
    markdown-link-check "%%f" --config .markdown-link-check.json --quiet >nul 2>&1 || echo   ⚠️  Some links may be broken ^(non-blocking^)
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Summary
echo 📊 Summary:
echo.

if %LINT_FAILED%==0 (
    echo ✅ Markdown Linting: PASSED
) else (
    echo ❌ Markdown Linting: FAILED
)

if %LINK_FAILED%==0 (
    echo ✅ Link Validation: PASSED
) else (
    echo ❌ Link Validation: FAILED
)

echo.

REM Exit with error if critical checks failed
if %LINT_FAILED%==1 goto :failed
if %LINK_FAILED%==1 goto :failed

echo ✅ All markdown validation checks passed!
echo.
echo You're good to commit! 🚀
exit /b 0

:failed
echo ❌ Markdown validation failed!
echo.
echo Fix the issues above before committing.
exit /b 1

