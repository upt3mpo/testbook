# 📱 Testbook - Automation Testing Platform

A production-grade social media application built for learning and practicing automation testing. Features 166+ backend tests, 13 frontend component tests, comprehensive E2E coverage, and structured hands-on labs.

Perfect for individual learners, junior developers exploring testing, or manual QA professionals transitioning to automation.

**✅ 180+ Tests | Complete Testing Pyramid | 84% Coverage | Production-Ready**

---

## 🚀 Quick Start (5 Minutes)

**Development mode** (commands below) runs on port 3000 and works with all tests.

Choose your operating system:

### macOS / Linux

```bash
git clone https://github.com/upt3mpo/testbook.git
cd testbook
chmod +x start-dev.sh
./start-dev.sh
```

### Windows

```cmd
git clone https://github.com/upt3mpo/testbook.git
cd testbook
start-dev.bat
```

**That's it!** Open **<http://localhost:3000>** (not 8000!)

**📝 Note:** There's also `start.sh` for production (Docker), but use `start-dev.sh` for learning. See [WHICH_START_SCRIPT.md](WHICH_START_SCRIPT.md) for details.

---

## 🎓 Learn Automation Testing

### 🌟 **New to Testing? Start Here!**

**→ [START_HERE.md](START_HERE.md)** - Choose your learning path (2 min)

**Four ways to learn:**

1. **🧪 Hands-On Labs** - Step-by-step tutorials, start coding immediately
2. **📚 Structured Learning** - Progressive curriculum with context
3. **🔍 Self-Exploration** - Run tests, learn by example
4. **⚡ Quick Reference** - Use as reference material

### What's Available

✅ **[Structured Learning Path](docs/course/COURSE_AUTOMATION_TESTING_101.md)** - Progressive curriculum
✅ **[Hands-On Labs](labs/)** - 🆕 **9 step-by-step tutorials** (including advanced!)
✅ **[180+ Executable Tests](docs/guides/RUNNING_TESTS.md)** - Complete test suite
✅ **🆕 [Dual-Stack Support](CURRICULUM_ENHANCEMENT_COMPLETE.md)** - Python AND JavaScript tracks
✅ **🆕 [Advanced E2E Patterns](docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md)** - Professional testing
✅ **🆕 [Testing Comparison Guide](docs/guides/TESTING_COMPARISON_PYTHON_JS.md)** - Python ↔ JavaScript
✅ **[Manual QA Transition Guide](docs/guides/MANUAL_QA_TO_AUTOMATION.md)** - For manual testers
✅ **[Task Runner](docs/guides/TASK_RUNNER.md)** - Simplified commands (Make/just)
✅ **[Quick Reference Guides](docs/reference/)** - Pytest & Playwright cheat sheets
✅ **[DevContainer Support](.devcontainer/)** - One-click setup

---

## 🧪 Complete Testing Pyramid

We test at every level - backend, frontend, E2E, API, security, and performance!

### Backend Testing (Python + pytest)

**166+ tests covering:**


- ✅ Unit tests (models, auth, utilities)
- ✅ Integration tests (database operations)
- ✅ API tests (all endpoints)
- ✅ Contract tests (OpenAPI validation)
- ✅ Security tests

```bash
cd backend
pytest -v                    # Run all 166+ tests
pytest tests/test_api_contract.py  # API contract validation
```

### Frontend Component Testing (JavaScript + Vitest)


**13 tests covering:**

- ✅ React component rendering
- ✅ User interactions
- ✅ Form validation
- ✅ Accessibility (WCAG compliance)
- ✅ Keyboard navigation

```bash
cd frontend
npm test                     # Run component tests
npm test -- accessibility    # Accessibility tests
```

### End-to-End Testing (Choose Your Language!)

**Playwright (Python)** - Recommended for Python devs 🐍

```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
pytest -v
```

**Playwright (JavaScript)** - Recommended for JS devs ☕

```bash
cd tests/e2e
npm install
npx playwright install chromium
npm test
```

**Both?** - Recommended for well-rounded testers! 🚀

- Try Python version first
- Then JavaScript version
- Compare and learn both!

**Other Tools:**

- **Selenium** - Supported (any language)
- **Cypress** - Supported (JavaScript only)

### Platform-Specific Notes

| Platform | Start Command | Python Activation | Notes |
|----------|---------------|-------------------|-------|
| **macOS** | `./start-dev.sh` | `source venv/bin/activate` | Use Terminal |
| **Linux** | `./start-dev.sh` | `source venv/bin/activate` | Use Terminal |
| **Windows** | `start-dev.bat` | `venv\Scripts\activate` | Use CMD or PowerShell |

---

## 📚 Documentation (Organized!)

### Essential (Start Here)

- **[START_HERE.md](START_HERE.md)** - Choose your learning path ⭐
- **[QUICKSTART.md](QUICKSTART.md)** - Get app running in 5 minutes
- **[FAQ.md](FAQ.md)** - Quick answers to common questions & troubleshooting
- **[WHICH_START_SCRIPT.md](WHICH_START_SCRIPT.md)** - Dev vs production explained
- **This file** - Project overview

### For Learning

- **[Learning Path](docs/course/COURSE_AUTOMATION_TESTING_101.md)** - Structured curriculum
- **[Labs](labs/)** - Hands-on tutorials
- **[Learning Paths](docs/course/LEARNING_PATHS.md)** - Choose path for your background
- **[Running Tests Guide](docs/guides/RUNNING_TESTS.md)** - How to run everything
- **[Common Mistakes](docs/course/COMMON_MISTAKES.md)** - Avoid common errors

### For Reference

- **[Testing Guide](docs/guides/TESTING_GUIDE.md)** - Comprehensive examples
- **[Pytest Quick Reference](docs/reference/QUICK_REFERENCE_PYTEST.md)** - One-page pytest guide
- **[Playwright Quick Reference](docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md)** - One-page Playwright guide
- **[Cheat Sheet](docs/reference/TESTING_CHEATSHEET.md)** - Quick lookups
- **[Testing Patterns](docs/reference/TESTING_PATTERNS.md)** - Advanced techniques
- **[Testing Anti-Patterns](docs/reference/TESTING_ANTIPATTERNS.md)** - What NOT to do
- **[Debugging Guide](docs/reference/DEBUGGING_GUIDE.md)** - Debug like a pro
- **[API Reference](docs/reference/PROJECT_INFO.md)** - Technical details

### New Guides ✨

- **[Task Runner Guide](docs/guides/TASK_RUNNER.md)** - Simplified commands (Make/just)
- **[Logging & Observability](docs/guides/LOGGING.md)** - Structured logging
- **[Rate Limiting](docs/guides/RATE_LIMITING.md)** - Configuration & tuning
- **[Manual QA → Automation](docs/guides/MANUAL_QA_TO_AUTOMATION.md)** - Career transition guide

---

## ✨ Features

### Social Media Features

- ✅ User authentication & profiles
- ✅ Posts (text, images, videos)
- ✅ Comments & reactions (6 types)
- ✅ Follow/unfollow users
- ✅ Block/unblock users
- ✅ Feed filtering (All / Following)
- ✅ Reposts
- ✅ Theme switching (dark/light)
- ✅ Settings management

### Testing Features

- ✅ 138+ data-testid attributes
- ✅ Dev API for test data management
- ✅ Database reset functionality
- ✅ Predictable seed data
- ✅ File upload testing
- ✅ Cross-platform scripts

---

## 🧪 What Can You Test?

### Backend (Python/pytest) - 166+ Tests

- ✅ Unit tests (password hashing, JWT tokens)
- ✅ Integration tests (all API endpoints)
- ✅ Database tests (models, relationships)
- ✅ Contract tests (OpenAPI schema validation)
- ✅ Security tests (auth, input validation)
- **84% code coverage achieved**

### Frontend Component (JavaScript/Vitest) - 13 Tests ✨

- ✅ Component rendering tests
- ✅ User interaction tests
- ✅ Form validation tests
- ✅ **Accessibility tests (WCAG compliance)**
- ✅ **Keyboard navigation tests**

### End-to-End (Playwright) - 60+ Tests

- ✅ Complete user flows
- ✅ Cross-browser testing (Chrome, Firefox, Safari)
- ✅ Mobile testing
- ✅ Visual regression
- Available in **both Python and JavaScript**

### API Testing (Multiple Tools)

- ✅ Postman/Newman collections
- ✅ Python requests examples
- ✅ **Schemathesis contract testing**
- ✅ Any HTTP client supported

### Performance (K6)

- ✅ Smoke tests
- ✅ Load tests
- ✅ Stress tests
- ✅ Spike tests

### Security

- ✅ Authentication/authorization tests
- ✅ Input validation tests
- ✅ OWASP best practices
- ✅ 23+ security test scenarios

---

## 🎯 Quick Commands

### Using Task Runners (Recommended) ✨


**Make (Traditional):**

```bash
make setup          # Complete setup
make start          # Start both servers
make test           # Run all tests
make test-backend   # Backend only
make test-frontend  # Frontend only
make test-e2e       # E2E only
make coverage       # Generate coverage

```

**Just (Modern):**

```bash
just setup          # Complete setup
just start          # Start both servers
just test           # Run all tests
```

See **[Task Runner Guide](docs/guides/TASK_RUNNER.md)** for all commands.

### Platform-Specific Commands

**macOS / Linux:**

```bash
# Start app
./start-dev.sh

# Reset database
./reset-database.sh

# Run tests
cd backend && source venv/bin/activate && pytest -v
```

**Windows:**

```cmd
REM Start app
start-dev.bat

REM Reset database
reset-database.bat

REM Run tests
cd backend
venv\Scripts\activate
pytest -v
```

### Language-Specific Testing

**Prefer Python?**

```bash
# Backend testing (Python/pytest)
cd backend && pytest -v

# Security testing (Python)
pytest tests/security/ -v

# API testing (Python)
python tests/api/python_api_examples.py
```

**Prefer JavaScript?**

```bash
# E2E testing (JavaScript/Playwright)
cd tests/e2e && npm test

# API testing (JavaScript/Postman)
newman run tests/api/Testbook.postman_collection.json

# Performance testing (K6/JavaScript)
k6 run tests/performance/smoke-test.js
```

**Learn Both? (Recommended!)**

```bash
# Python backend + Python E2E
cd backend && pytest -v
cd ../tests/e2e-python && pytest -v

# JavaScript E2E for comparison
cd ../e2e && npm test

# Now you know both! 🚀
```

---

## 👥 Test Accounts

Pre-seeded accounts with known passwords:

| Email | Password | Platform |
|-------|----------|----------|
| <sarah.johnson@testbook.com> | Sarah2024! | All |
| <mike.chen@testbook.com> | MikeRocks88 | All |
| <emma.davis@testbook.com> | EmmaLovesPhotos | All |
| <newuser@testbook.com> | NewUser123! | All |

---

## 🏗️ Tech Stack

**Backend:** FastAPI (Python) | SQLAlchemy | SQLite | JWT
**Frontend:** React 18 | Vite | React Router
**Testing:** pytest | Playwright | K6 | Postman
**DevOps:** Docker | GitHub Actions

---

## 🐛 Troubleshooting

### Cross-Platform Issues

**Port already in use:**

```bash
# macOS/Linux
lsof -ti:8000 | xargs kill

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Permission denied on scripts:**

```bash
# macOS/Linux
chmod +x *.sh

# Windows: Run as Administrator
```

**Python venv issues:**

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

See [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md) for complete troubleshooting.

---


## 📞 Getting Help

### Quick Troubleshooting


- **[FAQ.md](FAQ.md)** - Common issues solved
- **[COMMON_MISTAKES.md](docs/course/COMMON_MISTAKES.md)** - Common errors cataloged
- **[DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Step-by-step debugging

### Learning Resources

1. **Starting out?** → [START_HERE.md](START_HERE.md)

2. **Running tests?** → [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md)
3. **Learning?** → [labs/](labs/) or [docs/course/](docs/course/)
4. **Pytest commands?** → [docs/reference/QUICK_REFERENCE_PYTEST.md](docs/reference/QUICK_REFERENCE_PYTEST.md)
5. **Playwright commands?** → [docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md](docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md)

### Contributing


- **Want to help?** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **Report issues** → Create GitHub Issue
- **Suggest improvements** → Create GitHub Discussion
- **Documentation changes** → Run `./scripts/check-markdown.sh` before committing

**Automated CI Checks:**

- ✅ Markdown linting & link validation
- ✅ Backend tests (pytest)
- ✅ E2E tests (Playwright)
- ✅ Security tests
- ✅ Code coverage (80%+ required)

---

## 📄 License

MIT License - Use freely for learning and testing!

---

## 🎓 Ready to Learn?

**→ [START_HERE.md](START_HERE.md)** - Begin your testing journey!

**→ [labs/LAB_01_Your_First_Test.md](labs/LAB_01_Your_First_Test.md)** - Write your first test in 30 minutes!
