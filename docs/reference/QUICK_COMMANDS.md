# ⚡ Quick Commands Reference

**Common commands for Testbook development and testing**

This is the single source of truth for frequently used commands. Other documentation should link here instead of repeating these commands.

---

## 🐍 Python Backend Commands

### Virtual Environment

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Testing

```bash
# Run all backend tests
cd backend && pytest -v

# Run with coverage
cd backend && pytest --cov --cov-report=html

# Run specific test file
cd backend && pytest tests/unit/test_auth.py -v

# Run tests matching pattern
cd backend && pytest -k "test_login" -v
```

### Development Server

```bash
# Start backend server
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ☕ JavaScript Frontend Commands

### Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

### Testing

```bash
# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

---

## 🌐 E2E Testing Commands

### Playwright (JavaScript)

```bash
# Run E2E tests
npx playwright test

# Run specific test
npx playwright test auth.spec.js

# Run with UI mode
npx playwright test --ui

# Generate test report
npx playwright show-report
```

### Playwright (Python)

```bash
# Run Python E2E tests
cd tests/e2e-python && pytest -v

# Run with browser visible
cd tests/e2e-python && pytest -v --headed
```

---

## 🔧 Utility Commands

### Database

```bash
# Reset database (Windows)
reset-database.bat

# Reset database (macOS/Linux)
./reset-database.sh
```

### Development Mode

```bash
# Start both frontend and backend (Windows)
start-dev.bat

# Start both frontend and backend (macOS/Linux)
./start-dev.sh
```

---

## 📊 Coverage Commands

### Backend Coverage

```bash
cd backend && pytest --cov --cov-report=html
# View: open htmlcov/index.html
```

### Frontend Coverage

```bash
npm run test:coverage
# View: open coverage/index.html
```

---

## 🚀 CI/CD Commands

### Run All Tests

```bash
# Backend tests
cd backend && pytest -v

# Frontend tests
cd frontend && npm test

# E2E tests
cd tests && npx playwright test
```

### Quality Checks

```bash
# Backend linting
cd backend && black . && isort . && flake8 .

# Frontend linting
cd frontend && npm run lint && npm run format
```

---

## 💡 Pro Tips

- Use `-v` flag for verbose output
- Use `-k` to filter tests by name pattern
- Use `--lf` to run only last failed tests
- Use `--headed` to see browser during E2E tests
- Use `--ui` for interactive Playwright test runner

---

_This file serves as the single source of truth for common commands. Other documentation should reference this file instead of duplicating command examples._
