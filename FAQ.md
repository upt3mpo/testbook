# ❓ Frequently Asked Questions & Troubleshooting

**Quick answers to common questions and problems**

---

## 🚀 Getting Started

### Q: Which start script should I use?

**A:** Use `start-dev.sh` (or `start-dev.bat` on Windows) for learning!

- ✅ **Development mode** (`start-dev.sh`): Port 3000, no Docker, perfect for testing
- ⚠️ **Production mode** (`start.sh`): Port 8000, requires Docker, for deployment only

See [WHICH_START_SCRIPT.md](WHICH_START_SCRIPT.md) for full details.

---

### Q: What port should I open in my browser?

**A:** `http://localhost:3000` for development mode!

Common mistake: Opening port 8000 (that's the API, not the app).

---

### Q: Do I need Docker?

**A:** Not for learning! Only for production mode.

Development mode works without Docker and is recommended for all labs.

---

### Q: Is it safe to run start-dev.sh multiple times?

**A:** Yes! The scripts are now **idempotent**.

This means:

- ✅ Running it multiple times won't reinstall dependencies unnecessarily
- ✅ It checks if dependencies are already installed and skips if present
- ✅ It checks if ports are already in use and warns you
- ✅ Safe to run even if a previous instance is running

The script will:

1. Check if Python venv exists (create only if needed)
2. Check if dependencies are installed (install only if needed)
3. Check if node_modules exists (install only if needed)
4. Health check both services before reporting success

---

### Q: The script says "Port already in use" - what do I do?

**A:** You might have a previous instance running.

**Option 1:** Kill the process using the port:

```bash
# macOS/Linux
lsof -ti:8000 | xargs kill
lsof -ti:3000 | xargs kill

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Option 2:** Let the script continue anyway - it might work if the existing process is the one you want!

---

### Q: I'm on Windows - which approach should I use?

**A:** See the [Windows Setup Guide](docs/guides/WINDOWS_SETUP.md) for three options:

1. **Native Windows** (`start-dev.bat`) - Easiest for beginners
2. **WSL** (`start-dev.sh` in WSL) - Best Linux compatibility
3. **Docker** - Production-like environment

Most students prefer Native Windows or WSL.

---

## 🐍 Python & Virtual Environment

### Q: "pytest: command not found"

**A:** Activate your virtual environment:

```bash
# macOS/Linux
cd backend
source .venv/bin/activate

# Windows
cd backend
.venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

---

### Q: "ModuleNotFoundError: No module named 'pytest'"

**A:** Install dependencies:

```bash
cd backend
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### Q: How do I know if venv is activated?

**A:** Look for `(venv)` at the start of your terminal prompt:

```bash
(venv) $ pytest    # ✅ Activated
$ pytest           # ❌ Not activated
```

---

### Q: "pip: command not found"

**A:** Python might not be in your PATH. Try:

```bash
python -m pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

---

## 🧪 Running Tests

### Q: "Tests not found" or "collected 0 items"

**A:** Make sure you're in the right directory:

```bash
# For backend tests
cd backend
pytest tests/

# Check you're in the right place
pwd  # Should show .../Testbook/backend
```

---

### Q: Tests pass individually but fail together

**A:** Test data pollution. Tests are affecting each other.

**Fix:** Ensure each test creates its own data:

```python
# ❌ BAD - Shared state
global_user = None

# ✅ GOOD - Each test creates own data
def test_something(db_session):
    user = create_user()  # Fresh user
```

See [TESTING_ANTIPATTERNS.md](docs/reference/TESTING_ANTIPATTERNS.md) for more.

---

### Q: "Database is locked" error

**A:** Close other connections or delete the test database:

```bash
cd backend
rm test_testbook.db
pytest -v  # Will create fresh database
```

---

### Q: E2E tests fail with "Target closed" or "Page closed"

**A:** Backend might not be running:

```bash
# Terminal 1: Start backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Run E2E tests
cd tests
npx playwright test
```

---

## 🌐 Port & Connection Issues

### Q: "Port 8000 already in use"

**A:** Something is already running on that port.

**Find and kill it:**

```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Q: "Port 3000 already in use"

**A:** Frontend already running or another app using port.

```bash
# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

### Q: "Connection refused" in E2E tests

**A:** Make sure backend is running:

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"}
```

If not running, start it:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

---

## 🎭 Playwright Issues

### Q: "Timeout waiting for selector"

**A:** Element might not exist or selector is wrong.

**Debug:**

```javascript
// 1. Check what exists
console.log(await page.content());

// 2. Take screenshot
await page.screenshot({ path: 'debug.png' });

// 3. Verify selector
await page.locator('[data-testid="button"]').count()  // Should be > 0
```

Common issues:

- Typo in `data-testid`
- Element is hidden
- Page hasn't loaded yet

---

### Q: "npx playwright install" fails

**A:** Try with sudo (macOS/Linux) or run as Administrator (Windows):

```bash
# macOS/Linux
sudo npx playwright install chromium

# Windows (run as Administrator)
npx playwright install chromium
```

---

### Q: Tests are flaky (sometimes pass, sometimes fail)

**A:** Probably using `waitForTimeout()`. Don't!

```javascript
// ❌ BAD - Arbitrary timeout
await page.waitForTimeout(2000);
await page.click('button');

// ✅ GOOD - Wait for element
await page.waitForSelector('button', { state: 'visible' });
await page.click('button');

// ✅ EVEN BETTER - Playwright auto-waits!
await page.click('button');  // Already waits for element
```

See [TESTING_ANTIPATTERNS.md](docs/reference/TESTING_ANTIPATTERNS.md).

---

## 📂 File & Directory Issues

### Q: "No such file or directory"

**A:** Check you're in the right directory:

```bash
# See where you are
pwd

# Should be in Testbook root for most commands
cd /path/to/Testbook

# For pytest
cd backend
```

---

### Q: Can't find test files

**A:** Test files must start with `test_`:

```bash
# ✅ GOOD
test_auth.py              # Simple, clear
test_api_users.py         # Descriptive, standard naming

# ❌ BAD
auth_test.py
tests_auth.py
```

---

## 🔒 Permission Issues

### Q: "Permission denied" on scripts (macOS/Linux)

**A:** Make scripts executable:

```bash
chmod +x *.sh
./start-dev.sh
```

---

### Q: "Access denied" (Windows)

**A:** Run Command Prompt or PowerShell as Administrator.

Right-click → "Run as administrator"

---

## 💾 Database Issues

### Q: "User already exists" in tests

**A:** Database not clean between tests.

**Fix:** Use fixtures that clean up:

```python
@pytest.fixture
def clean_db(db_session):
    """Provides clean database."""
    yield db_session
    # Automatic cleanup
```

Or reset manually:

```bash
./reset-database.sh
```

---

### Q: How do I reset the database?

**A:** Use the reset script:

```bash
# From Testbook root
./reset-database.sh  # macOS/Linux
reset-database.bat   # Windows

# Or use API
curl -X POST http://localhost:8000/api/dev/reset
```

---

## 🎓 Learning & Labs

### Q: I'm stuck on a lab. What should I do?

**A:** Follow this checklist:

1. **Re-read instructions** - Carefully
2. **Check error message** - It usually tells you what's wrong
3. **Look at [COMMON_MISTAKES.md](docs/course/COMMON_MISTAKES.md)** - Your issue is probably there
4. **Check [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Learn to debug
5. **Look at working examples** - Check existing tests
6. **Take a break** - Fresh eyes help!

---

### Q: Where are the lab solutions?

**A:** In `labs/solutions/` (for instructors).

Students should try labs first, then check solutions if really stuck.

---

### Q: Which labs should I do first?

**A:** Follow this order:

1. **Lab 1** - Your first test (30 min)
2. **Lab 2** - Testing real functions (45 min)
3. **Lab 2.5** - Understanding fixtures (45 min) ← Important!
4. **LAB_DEBUG_01** - Reading errors (30 min) ← Very helpful!
5. **Lab 3** - API endpoints (60 min)
6. Continue with Labs 4-5...

---

### Q: How long will this take?

**A:** Approximate times:

- **Beginner labs (1-3)**: 2-3 hours
- **Debugging labs**: 1 hour
- **Intermediate labs (4-5)**: 3-4 hours
- **Full course**: 30-40 hours

Go at your own pace!

---

## 🛠️ Tool-Specific Issues

### Q: Pytest shows wrong Python version

**A:** Virtual environment not activated, or wrong Python.

```bash
# Check Python version
python --version  # Should be 3.11+

# Activate venv
source .venv/bin/activate

# Verify venv Python
which python  # Should point to venv
```

---

### Q: "npm: command not found"

**A:** Node.js not installed.

Install from [nodejs.org](https://nodejs.org/) (version 20+).

---

### Q: Coverage report not generating

**A:** Run with coverage flag:

```bash
pytest --cov --cov-report=html
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## 🔍 Debugging Tips

### Q: How do I see what's actually happening in my test?

**A:** Use print statements and run with `-s`:

```python
def test_something():
    value = calculate()
    print(f"Value is: {value}")  # Add prints
    assert value == expected
```

```bash
pytest tests/test_file.py -v -s  # -s shows prints
```

---

### Q: Test is failing but I don't know why

**A:** Use `--pdb` to drop into debugger:

```bash
pytest tests/test_file.py --pdb

# When it drops into debugger:
(Pdb) print(response)
(Pdb) print(response.status_code)
(Pdb) continue  # or quit
```

See [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md).

---

### Q: How do I see just the failing test?

**A:** Run only that test:

```bash
pytest tests/test_file.py::test_specific_name -v
```

---

## 🌐 Cross-Platform Issues

### Q: Script works on Mac but not Windows

**A:** Path separators differ:

```python
# ❌ BAD - Only works on Unix
path = "backend/tests/test_file.py"

# ✅ GOOD - Works everywhere
import os
path = os.path.join("backend", "tests", "test_file.py")
```

---

### Q: Line endings causing issues

**A:** Configure git to handle line endings:

```bash
# Configure git
git config --global core.autocrlf input  # Mac/Linux
git config --global core.autocrlf true   # Windows
```

---

## ⚡ Performance Issues

### Q: Tests are running very slowly

**A:** Run tests in parallel:

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run in parallel
pytest -n auto  # Uses all CPU cores
```

---

### Q: Pytest hangs or freezes

**A:** Might be an infinite loop or blocking call.

Stop with `Ctrl+C` and add timeout:

```bash
pip install pytest-timeout
pytest --timeout=10  # 10 seconds per test
```

---

## 📚 Documentation

### Q: Where do I find information about X?

**A:** Check the docs structure:

- **Getting started**: `README.md`, `START_HERE.md`
- **Running tests**: `docs/guides/RUNNING_TESTS.md`
- **Learning curriculum**: `docs/course/COURSE_AUTOMATION_TESTING_101.md`
- **Quick reference**: `docs/reference/QUICK_REFERENCE_*.md`
- **Common mistakes**: `docs/course/COMMON_MISTAKES.md`
- **Anti-patterns**: `docs/reference/TESTING_ANTIPATTERNS.md`
- **Learning paths**: `docs/course/LEARNING_PATHS.md`

Full index: `docs/INDEX.md`

---

### Q: Can I use this for teaching or mentoring?

**A:** Yes! While Testbook is designed for individual learning, it works great for:

- Staff engineers guiding junior developers
- Mentors introducing testing to manual QA professionals
- Tech leads onboarding team members

See:

- `labs/solutions/` - Sample solutions for guidance
- `docs/course/COURSE_AUTOMATION_TESTING_101.md` - Structured curriculum
- `docs/course/LEARNING_PATHS.md` - Different learning paths by background

---

## 🚨 Still Stuck?

If your issue isn't here:

1. **Check [COMMON_MISTAKES.md](docs/course/COMMON_MISTAKES.md)** - 24+ common errors
2. **Check [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Debug strategies
3. **Search GitHub Issues** - Someone might have asked
4. **Create an Issue** - We'll help you!

---

## 💡 Pro Tips

### Tip 1: Keep Two Terminals Open

```text
Terminal 1: Backend running
Terminal 2: Run tests
```

### Tip 2: Use Quick References

Bookmark these for fast lookups:

- `docs/reference/QUICK_REFERENCE_PYTEST.md`
- `docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md`

### Tip 3: Read Error Messages Carefully

90% of issues are explained in the error message. Read it!

### Tip 4: Start Fresh

When really stuck:

```bash
# Reset everything
./reset-database.sh
cd backend && deactivate && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

### Tip 5: Use Verbose Mode

Always use `-v` for better output:

```bash
pytest -v  # Shows test names and results
```

---

**Still have questions? Create an issue on GitHub!** 🚀
