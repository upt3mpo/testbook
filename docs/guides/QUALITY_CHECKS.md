# ✅ Quality Checks & Code Standards

**Maintaining code quality in Testbook**

---

## 🎯 Overview

Testbook uses automated quality checks to maintain code standards:

| Check Type | Backend (Python) | Frontend (JavaScript) |
|------------|------------------|----------------------|
| **Formatting** | Black | Prettier |
| **Import Sorting** | isort | ESLint import rules |
| **Linting** | Flake8 | ESLint + plugins |
| **Coverage Gate** | 80% minimum | No gate (95%+ actual) |
| **Pre-commit Hooks** | ✅ Enabled | ✅ Enabled |

---

## 🚀 Quick Start

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

## 🐍 Backend (Python)

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
line-length = 100
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
line_length = 100
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

## ☕ Frontend (JavaScript)

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

**Configuration:** `frontend/.eslintrc.json`

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

**On every commit:**

1. Trailing whitespace removal
2. End-of-file fixer
3. YAML validation
4. Large file check (max 1MB)
5. Merge conflict markers
6. **Black** (Python formatting)
7. **isort** (Python imports)
8. **Flake8** (Python linting)
9. **Prettier** (JavaScript formatting)
10. **ESLint** (JavaScript linting)

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

```
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

---

## 📊 Quality Metrics

### Current Status

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Backend Coverage | 86% | 80% | ✅ +6% |
| Frontend Coverage | 95% | N/A | ✅ Excellent |
| Linting Violations | 0 | 0 | ✅ Clean |
| Accessibility Violations | 0 | 0 | ✅ WCAG 2.1 AA |

---

## 🛠️ IDE Integration

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

## 🐛 Common Issues & Fixes

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
console.log('Debug info');
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

## 🎯 Best Practices

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
   const x = users.filter(u => u.active);

   // Good
   const activeUsers = users.filter(user => user.isActive);
   ```

2. **Add prop-types or TypeScript**

   ```javascript
   import PropTypes from 'prop-types';

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

## 📚 Additional Resources

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
