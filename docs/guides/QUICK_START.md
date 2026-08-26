# 🚀 Quick Start Guide

Get Testbook running in 5 minutes on any platform!

**⚠️ IMPORTANT:** Use the **development mode** scripts below (`start-dev.sh` / `start-dev.bat`). These run the app on port 3000 and work with all tests. Do NOT use `start.sh` - it's for production deployment only!

> **🪟 Windows Users:** We show both PowerShell (recommended) and Command Prompt alternatives. Use PowerShell unless you have a specific reason to use Command Prompt. See [Windows Setup Guide](WINDOWS_SETUP.md) for details.

---

## 🖥️ Choose Your Platform

<details>
<summary><b>🍎 macOS / Linux</b> (click to expand)</summary>

### Step 1: Clone Repository

```bash
git clone https://github.com/upt3mpo/testbook.git
cd testbook
```

### Step 2: Start Application (Development Mode)

```bash
chmod +x start-dev.sh
./start-dev.sh
```

**What happens:**

- Backend starts on <http://localhost:8000>
- Frontend starts on <http://localhost:3000> ← **This is your app!**
- Database automatically seeded

**Expected output:**

```bash
🚀 Starting Testbook in development mode...

🔧 Setting up backend...
📦 Creating Python virtual environment...
📦 Installing backend dependencies with uv (fast!)...
🌱 Seeding database...
🚀 Starting backend server on port 8000...
✅ Backend is ready!

⚛️  Setting up frontend...
📦 Installing frontend dependencies...
🚀 Starting frontend server on port 3000...
✅ Frontend is ready!

==========================================
✅ Testbook is running in development mode!
==========================================

📱 Frontend:    http://localhost:3000
🔌 Backend API: http://localhost:8000/api
📚 API Docs:    http://localhost:8000/docs

Test accounts:
  • sarah.johnson@testbook.com / Sarah2024!
  • mike.chen@testbook.com / MikeRocks88

🎯 What to do now:
  1. Open http://localhost:3000 in your browser
  2. Login with: sarah.johnson@testbook.com / Sarah2024!
  3. Explore the app for 5 minutes
  4. Then start learning: ./docs/INDEX.md#learning-path

Ready to start? → learn/README.md
```

**Why development mode?**

- No Docker required
- All tests pre-configured for port 3000
- Hot reload enabled
- Perfect for learning!

### Step 3: Open Browser

Frontend: <http://localhost:3000> ← Open this!
Backend API: <http://localhost:8000/api>
API Docs: <http://localhost:8000/docs>

### Step 4: Login

```text
Email: sarah.johnson@testbook.com
Password: Sarah2024!
```

✅ **Done!** You're ready to test!

</details>

<details>
<summary><b>🖥️ Windows</b> (click to expand)</summary>

### Windows Step 1: Clone Repository

```bat
git clone https://github.com/upt3mpo/testbook.git
cd testbook
```

### Windows Step 2: Start Application (Development Mode)

```bat
start-dev.bat
```

**What happens:**

- Backend starts on <http://localhost:8000>
- Frontend starts on <http://localhost:3000> ← **This is your app!**
- Database automatically seeded

**Expected output:**

```bat
🚀 Starting Testbook in development mode...

🔧 Setting up backend...
📦 Creating Python virtual environment...
📦 Installing backend dependencies with uv (fast!)...
🌱 Seeding database...
🚀 Starting backend server on port 8000...
✅ Backend is ready!

⚛️  Setting up frontend...
📦 Installing frontend dependencies...
🚀 Starting frontend server on port 3000...
✅ Frontend is ready!

==========================================
✅ Testbook is running in development mode!
==========================================

📱 Frontend:    http://localhost:3000
🔌 Backend API: http://localhost:8000/api
📚 API Docs:    http://localhost:8000/docs

Test accounts:
  • sarah.johnson@testbook.com / Sarah2024!
  • mike.chen@testbook.com / MikeRocks88

🎯 What to do now:
  1. Open http://localhost:3000 in your browser
  2. Login with: sarah.johnson@testbook.com / Sarah2024!
  3. Explore the app for 5 minutes
  4. Then start learning: docs\INDEX.md#learning-path

Ready to start? → learn\README.md
```

**Why development mode?**

- No Docker required
- All tests pre-configured for port 3000
- Hot reload enabled
- Perfect for learning!

### Windows Step 3: Open Browser

Frontend: <http://localhost:3000> ← Open this!
Backend API: <http://localhost:8000/api>
API Docs: <http://localhost:8000/docs>

### Windows Step 4: Login

```text
Email: sarah.johnson@testbook.com
Password: Sarah2024!
```

✅ **Done!** You're ready to test!

</details>

---

## 🔧 Environment Configuration (Optional)

**For beginners:** The `start-dev` scripts handle everything automatically. Skip this section unless you want to run commands manually.

<details>
<summary><b>Manual Setup: Using .env file</b></summary>

If you want to run `uvicorn` or `pytest` directly without the start scripts:

### Step 1: Copy the Environment Template

```bash
# Linux/Mac
cp backend/env.example backend/.env

# Windows (PowerShell)
Copy-Item backend\env.example backend\.env

# Windows (Command Prompt)
copy backend\env.example backend\.env
```

### Step 2: Verify the Defaults

The file already has good defaults for development:

```env
TESTING=true          # Enables dev endpoints and higher rate limits
LOG_LEVEL=INFO        # Standard logging (change to DEBUG for more details)
ENVIRONMENT=development
```

### Step 3: Run Commands Without Env Vars

Now you can run commands without typing environment variables:

```bash
# Instead of: TESTING=true uvicorn main:app --reload
# Just run:
cd backend
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
uvicorn main:app --reload --port 8000
```

### What Each Variable Does

| Variable       | Default                   | Purpose                                                                    |
| -------------- | ------------------------- | -------------------------------------------------------------------------- |
| `TESTING`      | `true`                    | Enables dev endpoints (`/api/dev/*`) and increases rate limits to 1000/min |
| `LOG_LEVEL`    | `INFO`                    | Controls logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)         |
| `ENVIRONMENT`  | `development`             | Sets the runtime environment                                               |
| `DATABASE_URL` | `sqlite:///./testbook.db` | Database connection string                                                 |

### When to Override

You can still override any setting with command-line environment variables:

```bash
# Linux/Mac
TESTING=false LOG_LEVEL=DEBUG uvicorn main:app --reload

# Windows (PowerShell)
$env:TESTING='false'; $env:LOG_LEVEL='DEBUG'; uvicorn main:app --reload
```

Command-line variables always take precedence over `.env` file settings.

</details>

---

## 🧪 Run Your First Test

### Option 1: Python (pytest) - Backend Testing

<details>
<summary><b>macOS / Linux</b></summary>

```bash
cd backend
# Linux/Mac
source .venv/bin/activate
pytest -v

# Windows (PowerShell)
.venv\Scripts\activate
pytest -v
```

**Expected:** 180 tests pass in ~72 seconds ✅

</details>

<details>
<summary><b>Windows</b></summary>

```bat
cd backend
.venv\Scripts\activate
pytest -v
```

**Expected:** 180 tests pass in ~72 seconds ✅

</details>

### Option 2: JavaScript (Playwright) - E2E Testing

<details>
<summary><b>All Platforms</b></summary>

**⚠️ Before running:** stop `start-dev.sh` if it's running without a
`backend/.env` file, and restart the backend with `TESTING=true` set — a
handful of E2E tests use the dev-only `/api/dev/reset` endpoint, which is
disabled unless `TESTING=true`. See [Playwright Quick Start](PLAYWRIGHT_QUICKSTART.md)
for the full setup.

```bash
cd tests
npm install
npx playwright install chromium
npm test
```

**Expected:** 59 E2E tests pass ✅

</details>

---

## 🎯 Next Steps

### ⭐ New to Testing?

**→ [learn/README.md](../../learn/README.md)** - Start here! Choose your track and
learning style

### 🧪 Want Hands-On Labs?

**→ [learn/stage_1_unit/exercises/](../../learn/stage_1_unit/exercises/)** - Write first
test in 30 min

### 📚 Want Structured Learning?

**→ [Learning Path](../../README.md#learning-path)** - Complete 5-stage curriculum
overview

### 📖 Want to Run Tests?

**→ [docs/guides/RUNNING_TESTS.md](RUNNING_TESTS.md)** - Complete guide

---

## 🌍 Cross-Platform Notes

### setup_images.py

This script **automatically detects your OS** and uses appropriate fonts:

- Windows: Arial, Calibri, Segoe UI
- macOS: Helvetica, Arial
- Linux: DejaVu, Liberation

Just run: `python3 setup_images.py` (or `python` on Windows)

### Virtual Environment Commands

**Activate:** See [Quick Commands](../reference/QUICK_COMMANDS.md#virtual-environment)
for all platforms

**Deactivate:** `deactivate` (all platforms)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] App loads at **<http://localhost:3000>** (development mode)
- [ ] Can login with test account
- [ ] Can create a post
- [ ] Backend tests run: `cd backend && pytest -v`
- [ ] See 180 tests pass

**⚠️ Common Mistake:** Don't open port 8000 - that's the API! The app is on port 3000.

---

## 🚨 Still Having Issues?

- **Technical problems?** → [Troubleshooting Guide](../reference/TROUBLESHOOTING.md)
- **Learning questions?** → [FAQ](FAQ.md)
- **Windows-specific?** → [Windows Setup Guide](WINDOWS_SETUP.md)
