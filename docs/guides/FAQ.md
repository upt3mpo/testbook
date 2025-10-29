# ❓ Frequently Asked Questions

## 🚀 Getting Started

### Q: Which start script should I use?

**A:** Use `start-dev.sh` (or `start-dev.bat` on Windows) for learning and testing. This runs the app on port 3000 and works with all tests. Don't use `start.sh` unless you're specifically testing production deployment.

### Q: I opened localhost:8000 but don't see the app?

**A:** That's the API! The app is on port 3000. After running `start-dev.sh`, open `http://localhost:3000` in your browser.

### Q: Do I need Docker to run Testbook?

**A:** No! Use development mode (`start-dev.sh`) - it runs everything locally without Docker. Only production mode (`start.sh`) requires Docker.

### Q: The app won't start, what should I check?

**A:**

1. Make sure ports 3000 and 8000 are free
2. Check both terminals are running (backend and frontend)
3. Look for error messages in the terminals
4. See [Troubleshooting Guide](../reference/TROUBLESHOOTING.md) for specific errors

### Q: Can I run this on Windows?

**A:** Yes! Use `start-dev.bat` instead of `start-dev.sh`. See [Windows Setup Guide](WINDOWS_SETUP.md) for detailed instructions.

---

## 🐍 Python

### Q: Do I need Python 3.13?

**A:** Python 3.8+ works, but 3.13 is recommended and matches CI. The app uses modern Python features and type hints.

### Q: Should I use uv or pip?

**A:** Use `uv` - it's much faster! The scripts automatically use `uv` if available, otherwise fall back to `pip`.

### Q: How do I activate the virtual environment?

**A:**

- **macOS/Linux:** `source backend/.venv/bin/activate`
- **Windows:** `backend\.venv\Scripts\activate`

### Q: I'm getting import errors in Python tests?

**A:** Make sure you're in the `backend` directory and have activated the virtual environment:

```bash
cd backend
# Linux/Mac
source .venv/bin/activate
pytest -v

# Windows (PowerShell)
.venv\Scripts\activate
pytest -v
```

### Q: What's the difference between pytest and unittest?

**A:** Testbook uses pytest (more powerful, better fixtures, cleaner syntax). The labs teach pytest patterns that work in most Python projects.

---

## 🧪 Testing

### Q: How many tests are there?

**A:**

- **Backend:** 180 tests (87% coverage)
- **Frontend:** 40 tests (unit + integration)
- **E2E:** 15 tests (Playwright)
- **Total:** 235+ tests

### Q: Which testing framework should I learn?

**A:**

- **Python:** pytest (industry standard)
- **JavaScript:** Vitest (modern, fast)
- **E2E:** Playwright (cross-browser)

### Q: Why do tests fail when I switch to production mode?

**A:** Tests are configured for development mode ports (3000 for frontend, 8000 for backend). Switch back to `start-dev.sh` to run tests.

### Q: How do I run specific tests?

**A:**

- **Python:** `pytest tests/unit/test_auth.py -v`
- **JavaScript:** `npm test -- --grep "login"`
- **E2E:** `npx playwright test tests/e2e/login.spec.js`

### Q: What's the difference between unit, integration, and E2E tests?

**A:**

- **Unit:** Test individual functions in isolation
- **Integration:** Test multiple components working together
- **E2E:** Test complete user workflows in a browser

---

## 🎓 Learning Path

### Q: I'm new to testing, where do I start?

**A:** Start with [Stage 1: Unit Testing](../../learn/stage_1_unit/README.md). Choose Python or JavaScript based on your preference.

### Q: Should I learn Python or JavaScript testing?

**A:** Both! The concepts are the same, just different syntax. Start with the language you're most comfortable with.

### Q: How long does it take to complete all labs?

**A:**

- **Stage 1:** 2-3 hours (unit testing basics)
- **Stage 2:** 3-4 hours (integration testing)
- **Stage 3:** 4-5 hours (E2E testing)
- **Stage 4:** 2-3 hours (performance & security)
- **Total:** 11-15 hours

### Q: Can I skip stages?

**A:** Each stage builds on the previous one. However, you can jump to specific topics if you're already familiar with the basics.

### Q: What if I get stuck on a lab?

**A:**

1. Check the lab's troubleshooting section
2. Look at the solution files in `learn/solutions/`
3. Ask for help in [Discussions](https://github.com/upt3mpo/testbook/discussions)

---

## 🔧 Technical Issues

### Q: I'm getting "port already in use" errors?

**A:**

1. Stop any running instances (Ctrl+C in terminals)
2. Check what's using the ports: `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows)
3. Kill the process or use different ports

### Q: The database seems corrupted?

**A:** Reset it:

```bash
# macOS/Linux
rm backend/testbook.db
./start-dev.sh

# Windows
del backend\testbook.db
start-dev.bat
```

### Q: I'm getting "command not found" errors?

**A:**

- **Python:** Make sure you're in the `backend` directory and virtual environment is activated
- **Node:** Make sure you're in the `frontend` or `tests` directory
- **Scripts:** Make sure you're in the project root directory

### Q: Tests are running but failing?

**A:**

1. Make sure the app is running (`start-dev.sh`)
2. Check you're using the right test command
3. Look at the test output for specific error messages
4. See [Troubleshooting Guide](../reference/TROUBLESHOOTING.md)

---

## 🎯 Best Practices

### Q: Should I commit my test files?

**A:** Yes! Tests are part of your codebase. Commit them along with your application code.

### Q: How often should I run tests?

**A:**

- **During development:** Run relevant tests after each change
- **Before committing:** Run all tests
- **CI/CD:** Run all tests automatically

### Q: What's a good test coverage percentage?

**A:**

- **Minimum:** 70%
- **Good:** 80-90%
- **Excellent:** 90%+

Testbook currently has 87% coverage as an example.

### Q: Should I test everything?

**A:** Focus on:

- ✅ Critical business logic
- ✅ User-facing features
- ✅ Edge cases and error conditions
- ❌ Third-party library code
- ❌ Simple getters/setters

---

## 🚀 Advanced Topics

### Q: How do I add new test data?

**A:** See [Test Data Management](../../learn/stage_2_integration/exercises/LAB_07_Test_Data_Management_Python.md) lab for patterns and best practices.

### Q: Can I run tests in parallel?

**A:**

- **pytest:** `pytest -n auto` (requires pytest-xdist)
- **Vitest:** Parallel by default
- **Playwright:** `npx playwright test --workers=4`

### Q: How do I mock external APIs?

**A:**

- **Python:** Use `unittest.mock` or `pytest-mock`
- **JavaScript:** Use MSW (Mock Service Worker)
- See the integration testing labs for examples

### Q: What's the difference between mocks and stubs?

**A:**

- **Mock:** Verifies interactions (did the function get called?)
- **Stub:** Provides fake responses (what should the function return?)
- **Spy:** Records calls for later verification

---

## 🆘 Still Need Help?

- **Technical issues:** [Troubleshooting Guide](../reference/TROUBLESHOOTING.md)
- **Learning questions:** [GitHub Discussions](https://github.com/upt3mpo/testbook/discussions)
- **Bug reports:** [GitHub Issues](https://github.com/upt3mpo/testbook/issues)
- **Feature requests:** [GitHub Discussions](https://github.com/upt3mpo/testbook/discussions)

---

**💡 Pro Tip:** Most issues are solved by using development mode (`start-dev.sh`) and making sure you're in the right directory with the right environment activated!
