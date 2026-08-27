# ✅ Quality Checks & Code Standards

**Maintaining code quality in Testbook**

---

<h2 id="overview">🎯 Overview</h2>

Testbook uses automated quality checks to maintain code standards:

| Check Type           | Backend (Python) | Frontend (JavaScript) |
| -------------------- | ---------------- | --------------------- |
| **Formatting**       | Black            | Prettier              |
| **Import Sorting**   | isort            | ESLint import rules   |
| **Linting**          | Flake8           | ESLint + plugins      |
| **Coverage Gate**    | 80% minimum      | No gate (~41% actual) |
| **Pre-commit Hooks** | ⚠️ Partial (Black only; isort/Flake8 not yet enabled) | ❌ Not enabled (ESLint/Prettier still commented out in `.pre-commit-config.yaml`) |

---

<h2 id="quick-start">🚀 Quick Start</h2>

### Run All Quality Checks

```bash
./scripts/quality-check.sh
```

This runs:

- ✅ Black formatting check (Python)
- ✅ isort import sort check (Python)
- ✅ Flake8 linting (Python)
- ✅ Backend tests with 80% coverage gate
- ✅ ESLint linting (JavaScript)
- ✅ Prettier formatting check (JavaScript)
- ✅ Frontend tests

---

<h2 id="backend-python">🐍 Backend (Python)</h2>

### Formatting with Black

**Check formatting:**

```bash
cd backend
black --check .
```

**Auto-fix:**

```bash
black .
```

**Configuration:** `backend/pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ['py311']
```

---

### Import Sorting with isort

**Check imports:**

```bash
cd backend
isort --check-only --diff .
```

**Auto-fix:**

```bash
isort .
```

**Configuration:** `backend/pyproject.toml`

```toml
[tool.isort]
profile = "black"
line_length = 88
```

---

### Linting with Flake8

**Run linter:**

```bash
cd backend
flake8 .
```

**Configuration:** `backend/.flake8`

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503, E501
exclude = venv, .venv, htmlcov
```

---

### Coverage Gate (80% minimum)

**Run tests with coverage gate:**

```bash
cd backend
pytest --cov --cov-fail-under=80
```

**Current coverage:** 86% (well above minimum!)

**Why 80%?**

- Industry standard for quality projects
- Ensures critical paths are tested
- Allows flexibility for edge cases
- CI fails if coverage drops below threshold

---

<h2 id="frontend-javascript">☕ Frontend (JavaScript)</h2>

### Linting with ESLint

**Check code:**

```bash
cd frontend
npm run lint
```

**Auto-fix:**

```bash
npm run lint:fix
```

**Configuration:** `frontend/eslint.config.js` (flat config, ESLint 9 — the older `frontend/.eslintrc.json` is no longer read)

**Plugins enabled:**

- eslint-plugin-react
- eslint-plugin-react-hooks
- eslint-plugin-jsx-a11y (accessibility)
- eslint-config-prettier (compatibility)

---

### Formatting with Prettier

**Check formatting:**

```bash
cd frontend
npm run format:check
```

**Auto-fix:**

```bash
npm run format
```

**Configuration:** `frontend/.prettierrc.json`

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

---

## 🪝 Pre-commit Hooks

**Automatic quality checks before every commit!**

### Setup

```bash
# Install pre-commit (already in backend/requirements.txt)
cd backend
pip install pre-commit

# Install hooks
cd ..
pre-commit install
```

### What Gets Checked

**On every commit (currently active hooks):**

1. Trailing whitespace removal
2. End-of-file fixer
3. YAML validation
4. JSON validation
5. Merge conflict markers
6. Large file check (max 1MB)
7. Case-conflict check
8. Debug statement check (Python)
9. Private key detection
10. **Markdownlint** (Markdown files)
11. **Black** (Python formatting, `--line-length=88`)

**Not currently enabled in pre-commit** (present in `.pre-commit-config.yaml` but commented out): isort, Flake8, ESLint, and `detect-secrets`. These are still enforced separately by `./scripts/quality-check.sh` and the `lint-backend`/`lint-frontend` CI jobs — they just don't run as a local pre-commit hook yet.

**Configuration:** `.pre-commit-config.yaml`

### Run Manually

```bash
# Check all files
pre-commit run --all-files

# Check specific hook
pre-commit run black --all-files
```

### Skip Hooks (Emergency Only)

```bash
git commit --no-verify
```

⚠️ **Not recommended!** CI will still fail if checks don't pass.

---

## 🤖 CI/CD Integration

### GitHub Actions Workflow

**Linting jobs run before tests:**

```text
lint-backend → backend-tests ↘
                              → e2e-tests → security → badge-update
lint-frontend → frontend-tests ↗
```

**Benefits:**

- Fast feedback (linting is quick)
- Saves compute (don't run tests if code doesn't pass lint)
- Clear separation of concerns

### CI Configuration

**Location:** `.github/workflows/testbook-ci.yml`

**Jobs:**

1. `lint-backend` - Black, isort, Flake8
2. `lint-frontend` - ESLint, Prettier
3. `backend-tests` - Tests with 80% coverage gate
4. `frontend-tests` - Component tests
5. `e2e-tests-js` - Playwright JS
6. `e2e-tests-python` - Playwright Python
7. `security-tests` - OWASP checks
8. `badge-update` - Update status

### Recommended Branch Protection Rules

This repo doesn't currently document what branch protection to enable on `main`, so a maintainer setting this up has to guess. If you're configuring GitHub's branch protection for `main` (Settings → Branches → Add rule), these settings match what the CI above is already built to support:

- **Require a pull request before merging** - at least 1 approval, since this is a teaching repo where a second pair of eyes on curriculum changes matters as much as on code
- **Require status checks to pass before merging** - select `lint-backend`, `lint-frontend`, `backend-tests`, `frontend-tests` at minimum (these are fast and should gate every merge); `e2e-tests-js`/`e2e-tests-python`/`security-tests` are worth requiring too once they're stable enough not to block contributors on flakiness
- **Require branches to be up to date before merging** - avoids merging a PR whose CI ran against a stale base
- **Do not allow bypassing the above settings** - including for administrators, so the rule actually holds
- Force pushes and branch deletion should stay disabled for `main`

None of this is enforced by anything in this repository — it has to be configured in the GitHub repo's own settings, which aren't tracked in version control.

---

<h2 id="quality-metrics">📊 Quality Metrics</h2>

### Current Status

| Metric                   | Value | Target | Status         |
| ------------------------ | ----- | ------ | -------------- |
| Backend Coverage         | 86%   | 80%    | ✅ +6%         |
| Frontend Coverage        | 41%   | N/A    | ⚠️ Below typical bar |
| Linting Violations       | 0     | 0      | ✅ Clean       |
| Accessibility Violations | 0     | 0      | ✅ WCAG 2.1 AA |

---

<h2 id="ide-integration">🛠️ IDE Integration</h2>

### VS Code

**Install extensions:**

- Python (Microsoft)
- Black Formatter
- ESLint
- Prettier

**Settings (`.vscode/settings.json`):**

```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

---

<h2 id="common-issues-fixes">🐛 Common Issues & Fixes</h2>

### Issue: "Black would make changes"

**Fix:**

```bash
cd backend
black .
git add .
git commit
```

### Issue: "ESLint: Unexpected console statement"

**Fix:**

```javascript
// Option 1: Remove console.log

// Option 2: Disable for specific line
// eslint-disable-next-line no-console
console.log("Debug info");
```

### Issue: "Coverage below 80%"

**Options:**

1. Write more tests (preferred)
2. Exclude non-critical files from coverage
3. Check if tests are actually running

**Investigate:**

```bash
cd backend
pytest --cov --cov-report=html
open htmlcov/index.html
```

---

<h2 id="best-practices">🎯 Best Practices</h2>

### For Backend (Python)

1. **Run Black before committing**

   ```bash
   black .
   ```

2. **Use type hints**

   ```python
   def calculate_total(price: float, quantity: int) -> float:
       return price * quantity
   ```

3. **Write docstrings**

   ```python
   def complex_function(param):
       """
       Brief description.

       Args:
           param: Description

       Returns:
           Description
       """
   ```

---

### For Frontend (JavaScript)

1. **Use meaningful variable names**

   ```javascript
   // Bad
   const x = users.filter((u) => u.active);

   // Good
   const activeUsers = users.filter((user) => user.isActive);
   ```

2. **Add prop-types or TypeScript**

   ```javascript
   import PropTypes from "prop-types";

   MyComponent.propTypes = {
     name: PropTypes.string.isRequired,
     age: PropTypes.number,
   };
   ```

3. **Use semantic HTML**

   ```jsx
   // Bad
   <div onClick={handleClick}>Click me</div>

   // Good
   <button onClick={handleClick}>Click me</button>
   ```

---

<h2 id="additional-resources">📚 Additional Resources</h2>

- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Rules](https://flake8.pycqa.org/en/latest/user/error-codes.html)
- [ESLint Rules](https://eslint.org/docs/latest/rules/)
- [Prettier Options](https://prettier.io/docs/en/options.html)
- [Pre-commit Hooks](https://pre-commit.com/)

---

## ✅ Checklist

Before pushing code:

- [ ] Run `./scripts/quality-check.sh`
- [ ] All linting passes
- [ ] Coverage above 80% (backend)
- [ ] No console.log statements
- [ ] Code formatted (Black/Prettier)
- [ ] Imports sorted (isort)
- [ ] Pre-commit hooks installed

---

**Quality is not an accident — it's a habit!** 🚀
