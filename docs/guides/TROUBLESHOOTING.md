# 🔧 Troubleshooting Guide

**Real-world errors and exact solutions**

This guide contains actual error messages you might encounter and the exact commands to fix them. Each entry includes the error, why it happens, and step-by-step resolution.

---

## 📑 Quick Index

Jump to your error:

- [Python Virtual Environment](#python-virtual-environment-errors)
- [Node.js & npm](#nodejs--npm-errors)
- [Docker & Permissions](#docker--permissions-errors)
- [Database Issues](#database-issues)
- [Port Conflicts](#port-conflicts)
- [Test Execution](#test-execution-errors)
- [Coverage & Reporting](#coverage--reporting-errors)
- [Playwright Issues](#playwright-issues)
- [Platform-Specific](#platform-specific-issues)

---

## 🐍 Python Virtual Environment Errors

### Error: `command not found: pytest`

**Full Error:**

```bash
$ pytest
-bash: pytest: command not found
```

**Why:** Virtual environment not activated.

**Fix:**

```bash
cd backend
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Verify - should see (venv) in prompt:
(venv) $
```

**Verify it worked:**

```bash
which python  # Should point to venv/bin/python
pytest --version  # Should show pytest version
```

---

### Error: `ModuleNotFoundError: No module named 'fastapi'`

**Full Error:**

```python
ModuleNotFoundError: No module named 'fastapi'
```

**Why:** Dependencies not installed or wrong Python interpreter.

**Fix:**

```bash
# Activate venv first
cd backend
source .venv/bin/activate  # macOS/Linux

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

**Still not working?**

```bash
# Check which Python you're using
which python  # Should be in venv/

# Recreate venv if corrupted
deactivate
rm -rf venv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

### Error: `Python.h: No such file or directory`

**Full Error:**

```bash
fatal error: Python.h: No such file or directory
compilation terminated.
error: command 'gcc' failed with exit status 1
```

**Why:** Python development headers not installed (Linux only).

**Fix by OS:**

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip build-essential
```

**Fedora/RHEL:**

```bash
sudo dnf install python3-devel gcc
```

**macOS:**

```bash
xcode-select --install
```

**Then retry:**

```bash
pip install -r requirements.txt
```

---

### Error: `virtualenv: command not found`

**Full Error:**

```bash
$ python -m venv .venv
Error: No module named venv
```

**Why:** Python installed without venv module (some Linux distros).

**Fix:**

**Ubuntu/Debian:**

```bash
sudo apt-get install python3-venv
```

**Then create venv:**

```bash
python3 -m venv .venv
```

---

## 📦 Node.js & npm Errors

### Error: `npm: command not found`

**Full Error:**

```bash
$ npm install
-bash: npm: command not found
```

**Why:** Node.js not installed.

**Fix by OS:**

**macOS:**

```bash
brew install node
```

**Ubuntu/Debian:**

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows:**
Download from [nodejs.org](https://nodejs.org/) and install.

**Verify:**

```bash
node --version  # Should show v18+ or v20+
npm --version   # Should show 9+ or 10+
```

---

### Error: `EACCES: permission denied`

**Full Error:**

```bash
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules
npm ERR! errno -13
npm ERR! Error: EACCES: permission denied
```

**Why:** Trying to install globally without permissions.

**Fix (use npx instead):**

```bash
# Don't use: npm install -g playwright
# Use: npx playwright install

# For Testbook frontend
cd frontend
npm install  # No sudo needed

# For Testbook E2E tests
cd tests
npm install  # No sudo needed
npx playwright install chromium
```

**Prevention:** Never use `sudo npm install` - it causes permission issues.

---

### Error: `ERESOLVE unable to resolve dependency tree`

**Full Error:**

```bash
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! Found: react@18.2.0
npm ERR! Could not resolve dependency:
npm ERR! peer react@"^17.0.0" from some-package@1.0.0
```

**Why:** Dependency version conflicts.

**Fix:**

```bash
# Use legacy peer deps (temporary fix)
npm install --legacy-peer-deps

# Better: Update package.json if needed
# or wait for package updates
```

**For Testbook:**

```bash
cd frontend  # or cd tests
rm -rf node_modules package-lock.json
npm install
```

---

### Error: Node version mismatch

**Full Error:**

```bash
error: The engine "node" is incompatible with this module
Expected version ">=18.0.0". Got "16.14.0"
```

**Why:** Node version too old.

**Fix:**

**Using nvm (recommended):**

```bash
# Install nvm: https://github.com/nvm-sh/nvm
nvm install 20
nvm use 20
node --version  # Should show v20.x.x
```

**Using brew (macOS):**

```bash
brew upgrade node
```

**Then reinstall:**

```bash
cd frontend  # or cd tests
npm install
```

---

## 🐳 Docker & Permissions Errors

### Error: `docker: Got permission denied`

**Full Error:**

```bash
docker: Got permission denied while trying to connect to the Docker daemon socket
```

**Why:** User not in docker group (Linux).

**Fix (Linux):**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, then verify
docker ps
```

**Alternative (don't need docker for learning):**

```bash
# Use development mode instead
./start-dev.sh  # Doesn't require Docker
```

---

### Error: `Cannot connect to the Docker daemon`

**Full Error:**

```bash
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
Is the docker daemon running?
```

**Why:** Docker Desktop not running.

**Fix:**

**macOS/Windows:**

1. Open Docker Desktop application
2. Wait for it to start (whale icon in tray)
3. Retry command

**Linux:**

```bash
sudo systemctl start docker
sudo systemctl enable docker  # Start on boot
```

**For Testbook learning:**

```bash
# You don't need Docker - use dev mode
./start-dev.sh
```

---

## 🗄️ Database Issues

### Error: `database is locked`

**Full Error:**

```bash
sqlite3.OperationalError: database is locked
```

**Why:** Database file in use by another process or test.

**Fix:**

```bash
# Stop all processes
# Ctrl+C in all terminals

# Delete test database
cd backend
rm test_testbook.db

# Delete lock file if exists
rm test_testbook.db-shm test_testbook.db-wal

# Run tests again
pytest -v
```

**Prevention:**

```bash
# Reset database between test runs
./reset-database.sh
```

---

### Error: `no such table: users`

**Full Error:**

```bash
sqlite3.OperationalError: no such table: users
```

**Why:** Database not initialized or missing tables.

**Fix:**

```bash
cd backend

# Delete old database
rm testbook.db test_testbook.db

# Restart backend (creates tables automatically)
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn main:app --reload

# Or run the seed script
python seed.py
```

---

### Error: `UNIQUE constraint failed`

**Full Error:**

```bash
sqlite3.IntegrityError: UNIQUE constraint failed: users.email
```

**Why:** Trying to create duplicate data (common in tests).

**Fix for tests:**

```bash
# This is expected! Tests should handle it:
def test_duplicate_email(client):
    # First user
    client.post("/api/auth/register", json=user_data)

    # Second with same email - should fail
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400  # Expect error
```

**Fix for database:**

```bash
# Reset database
./reset-database.sh
```

---

## 🔌 Port Conflicts

### Error: `Address already in use`

**Full Error:**

```bash
ERROR: [Errno 48] Address already in use
# or
Error: listen EADDRINUSE: address already in use :::8000
```

**Why:** Another process using port 8000 or 3000.

**Fix macOS/Linux:**

```bash
# Find process on port 8000
lsof -ti:8000

# Kill it
lsof -ti:8000 | xargs kill

# Or for port 3000
lsof -ti:3000 | xargs kill
```

**Fix Windows:**

```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (use PID from above)
taskkill /PID <PID> /F
```

**Or just use different ports:**

```bash
# Backend on different port
uvicorn main:app --reload --port 8001

# Frontend on different port
npm run dev -- --port 3001
```

---

## 🧪 Test Execution Errors

### Error: `fixture 'test_user' not found`

**Full Error:**

```python
E   fixture 'test_user' not found
>   available fixtures: cache, capfd, capsys, ...
>   use 'pytest --fixtures' to see available fixtures
```

**Why:** Fixture not imported or not in scope.

**Fix:**

**Check conftest.py exists:**

```bash
ls backend/tests/conftest.py  # Should exist
```

**Check you're in correct directory:**

```bash
cd backend
pytest tests/unit/test_auth.py -v
```

**See all available fixtures:**

```bash
pytest --fixtures
```

**If fixture missing, add to conftest.py:**

```python
# backend/tests/conftest.py
@pytest.fixture
def test_user(db_session):
    # Create and return test user
    pass
```

---

### Error: `ImportError: cannot import name 'app'`

**Full Error:**

```python
ImportError: cannot import name 'app' from 'main'
```

**Why:** Import path issue or wrong directory.

**Fix:**

```bash
# Must run from backend directory
cd backend
pytest -v

# Not from root:
# cd testbook  # ❌ Wrong
# pytest backend/tests/  # ❌ Will fail
```

**Check sys.path in conftest.py:**

```python
# backend/tests/conftest.py should have:
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
```

---

### Error: Tests pass individually but fail together

**Full Error:**

```bash
$ pytest tests/integration/test_api_auth.py::test_login -v
PASSED  # ✅ Works alone

$ pytest tests/integration/ -v
FAILED  # ❌ Fails in suite
ERROR: KeyError: 'access_token'
```

**Why:** Rate limiting or shared state between tests.

**Fix:**

```bash
# Run backend in TESTING mode
cd backend
TESTING=true uvicorn main:app --reload

# Or add delay between tests
pytest tests/integration/ -v --dist loadscope
```

**See:** [Lab 6: Testing with Rate Limits](../../labs/LAB_06_Testing_With_Rate_Limits.md) for complete explanation.

---

## 📊 Coverage & Reporting Errors

### Error: `Coverage.py warning: No data was collected`

**Full Error:**

```bash
Coverage.py warning: No data was collected. (no-data-collected)
```

**Why:** Tests didn't run or coverage config wrong.

**Fix:**

```bash
# Check pytest.ini exists
ls backend/pytest.ini

# Run with explicit coverage
cd backend
pytest --cov=. --cov-report=html tests/

# Check .coveragerc
cat .coveragerc
```

---

### Error: `pytest-cov: module 'coverage' has no attribute 'version'`

**Full Error:**

```bash
AttributeError: module 'coverage' has no attribute 'version'
```

**Why:** Coverage plugin version mismatch.

**Fix:**

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Reinstall coverage tools
pip uninstall pytest-cov coverage -y
pip install pytest-cov coverage

# Verify
pytest --version
```

---

## 🎭 Playwright Issues

### Error: `Executable doesn't exist at /path/to/chromium`

**Full Error:**

```bash
Error: Executable doesn't exist at /Users/user/Library/Caches/ms-playwright/chromium-1084/chrome-mac/Chromium.app
```

**Why:** Playwright browsers not installed.

**Fix Python:**

```bash
cd tests/e2e-python
source .venv/bin/activate  # Windows: .venv\Scripts\activate
playwright install chromium

# Or install all browsers
playwright install
```

**Fix JavaScript:**

```bash
cd tests
npx playwright install chromium

# Or install all browsers
npx playwright install
```

---

### Error: `page.goto: net::ERR_CONNECTION_REFUSED`

**Full Error:**

```bash
playwright._impl._api_types.Error: page.goto: net::ERR_CONNECTION_REFUSED
```

**Why:** Frontend not running on <http://localhost:3000>.

**Fix:**

```bash
# Start development servers
./start-dev.sh  # macOS/Linux
start-dev.bat   # Windows

# Verify frontend is accessible
curl http://localhost:3000  # Should return HTML
curl http://localhost:8000/api/health  # Should return JSON

# Then run E2E tests
cd tests/e2e-python
pytest -v
```

---

### Error: `Timeout 30000ms exceeded`

**Full Error:**

```bash
playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.
waiting for locator('[data-testid="post-item"]')
```

**Why:** Element not appearing or selector wrong.

**Fix:**

**1. Check element exists:**

```bash
# Run in headed mode to see what's happening
HEADLESS=false pytest test_posts.py::test_name
```

**2. Increase timeout:**

```python
# In test
await expect(page.locator('[data-testid="post-item"]')).to_be_visible(timeout=60000)
```

**3. Check selector:**

```python
# Debug selector
await page.screenshot(path="debug.png")
page.pause()  # Opens inspector
```

---

## 🌐 Network & API Errors

### Error: `Connection refused [Errno 61]`

**Full Error:**

```python
requests.exceptions.ConnectionError:
HTTPConnectionPool(host='localhost', port=8000):
Max retries exceeded with url: /api/auth/login
(Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x...>:
Failed to establish a new connection: [Errno 61] Connection refused'))
```

**Why:** Backend API not running.

**Fix:**

```bash
# Terminal 1: Start backend
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn main:app --reload

# Wait for "Application startup complete"

# Terminal 2: Run tests
cd tests/security  # or wherever
pytest -v
```

**Verify backend is running:**

```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

---

### Error: `429 Too Many Requests`

**Full Error:**

```python
assert response.status_code == 200
E   AssertionError: assert 429 == 200
```

**Why:** Hit rate limit (security feature working!).

**Fix:**

```bash
# Option 1: Run in TESTING mode (higher limits)
cd backend
TESTING=true uvicorn main:app --reload

# Option 2: Wait 60 seconds
sleep 60

# Option 3: Restart backend (resets limits)
# Ctrl+C then uvicorn main:app --reload
```

**See:** [Rate Limiting Guide](RATE_LIMITING.md) for details.

---

## 🪟 Platform-Specific Issues

### Windows: `'source' is not recognized`

**Full Error:**

```bash
'source' is not recognized as an internal or external command
```

**Why:** `source` is a Unix command, doesn't exist on Windows.

**Fix:**

```bash
# On Windows use:
cd backend
.venv\Scripts\activate

# NOT: source .venv/bin/activate
```

**PowerShell:**

```powershell
cd backend
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Windows: `Execution of scripts is disabled`

**Full Error:**

```powershell
.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts
is disabled on this system.
```

**Why:** Windows PowerShell execution policy.

**Fix:**

```powershell
# Allow scripts for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv
.\venv\Scripts\Activate.ps1
```

**Alternative (use cmd.exe):**

```bash
# Open Command Prompt instead of PowerShell
cd backend
.venv\Scripts\activate.bat
```

---

### macOS: `Permission denied: './start-dev.sh'`

**Full Error:**

```bash
$ ./start-dev.sh
-bash: ./start-dev.sh: Permission denied
```

**Why:** Script not executable.

**Fix:**

```bash
chmod +x start-dev.sh
chmod +x reset-database.sh
chmod +x run-all-tests.sh

# Then run
./start-dev.sh
```

---

### Linux: `sh: 1: playwright: not found`

**Full Error:**

```bash
sh: 1: playwright: not found
```

**Why:** Playwright not in PATH or not installed globally.

**Fix:**

```bash
# Use npx instead
cd tests/e2e-python
npx playwright install

# Or use Python playwright
pip install playwright
playwright install
```

---

## 🐛 Test Framework Errors

### Error: `ScopeMismatch: You tried to access the function scoped fixture`

**Full Error:**

```python
ScopeMismatch: You tried to access the function scoped fixture 'db_session'
with a session scoped request object
```

**Why:** Fixture scope mismatch.

**Fix:**

```python
# Change fixture scope to match
@pytest.fixture(scope="session")  # ❌ Wrong
def my_fixture(db_session):  # db_session is function-scoped
    pass

# Fix:
@pytest.fixture(scope="function")  # ✅ Correct
def my_fixture(db_session):
    pass
```

---

### Error: `PytestCollectionWarning: cannot collect test class`

**Full Error:**

```bash
PytestCollectionWarning: cannot collect test class 'TestConfig'
because it has a __init__ constructor
```

**Why:** Test classes shouldn't have `__init__` methods.

**Fix:**

```python
# ❌ Wrong
class TestLogin:
    def __init__(self):
        self.url = "..."

# ✅ Correct - use fixtures or class variables
class TestLogin:
    url = "..."

    def test_something(self):
        pass
```

---

## 🔍 Common Test Failures

### Error: `AssertionError: assert 401 == 403`

**Full Error:**

```python
def test_unauthorized(client):
    response = client.get("/api/posts")
>   assert response.status_code == 401
E   AssertionError: assert 403 == 401
```

**Why:** Both 401 and 403 are valid auth errors, but FastAPI returns 403 by default.

**Fix:**

```python
# Accept both
assert response.status_code in [401, 403]

# Or be specific about what you're testing
# 401 = not authenticated (no token)
# 403 = authenticated but forbidden (bad token or no permission)
```

---

### Error: `json.decoder.JSONDecodeError`

**Full Error:**

```python
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Why:** Response isn't JSON (might be HTML error page or empty).

**Fix:**

```python
# Check status first
print(f"Status: {response.status_code}")
print(f"Content: {response.text}")  # Don't call .json() yet

# Only parse if 200
if response.status_code == 200:
    data = response.json()
else:
    print("Error:", response.text)
```

---

## 📋 Quick Diagnostic Commands

### Check Everything is Working

```bash
# Python version (need 3.11+)
python3 --version

# Node version (need 18+)
node --version

# Pip packages installed
cd backend && source .venv/bin/activate && pip list  # Windows: cd backend, .venv\Scripts\activate, pip list

# npm packages installed
cd frontend && npm list --depth=0

# Ports available
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Backend running
curl http://localhost:8000/api/health

# Frontend running
curl http://localhost:3000

# Database exists
ls backend/testbook.db

# Run single test
cd backend && pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed -v
```

---

## 🆘 Still Stuck?

### Step-by-Step Debug Process

1. **Read the error message carefully**
   - What's the exact error?
   - What line/file?
   - What was expected vs actual?

2. **Check the basics**
   - [ ] Are you in the correct directory?
   - [ ] Is virtual environment activated?
   - [ ] Are dependencies installed?
   - [ ] Are servers running?

3. **Isolate the problem**

   ```bash
   # Run single test
   pytest tests/unit/test_auth.py::test_one_thing -v

   # Run with verbose output
   pytest -vv -s

   # Check imports work
   python -c "from main import app; print('OK')"
   ```

4. **Check related guides**
   - [Common Mistakes](../course/COMMON_MISTAKES.md) - Code errors
   - [Running Tests](RUNNING_TESTS.md) - How to run tests
   - [Windows Setup](WINDOWS_SETUP.md) - Windows-specific help

5. **Reset everything**

   ```bash
   # Nuclear option - reset everything
   ./reset-database.sh
   cd backend && rm -rf __pycache__ tests/__pycache__
   cd frontend && rm -rf node_modules && npm install
   ```

---

## 📞 Getting Help

**If you're still stuck:**

1. **Search error message** - Copy exact error to Google
2. **Check GitHub Issues** - Someone might have had same problem
3. **Read documentation** - [docs/INDEX.md](../INDEX.md)
4. **Ask in Discussions** - Describe what you tried

**When asking for help, include:**

- Exact error message (copy-paste)
- What you were trying to do
- What you've already tried
- Your OS and Python/Node versions
- Output of `pytest --version` and `node --version`

---

## 🎯 Prevention Checklist

Before starting any work:

- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] In correct directory (`backend/` or `frontend/` or `tests/`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Servers running if needed (`./start-dev.sh`)
- [ ] Database reset if needed (`./reset-database.sh`)
- [ ] Latest code pulled (`git pull`)

---

*Remember: Errors are learning opportunities! Each error you fix teaches you something new. 💪*
