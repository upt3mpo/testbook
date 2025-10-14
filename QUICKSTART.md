# 🚀 Quick Start Guide

Get Testbook running in 5 minutes on any platform!

**⚠️ IMPORTANT:** Use the **development mode** scripts below (`start-dev.sh` / `start-dev.bat`). These run the app on port 3000 and work with all tests. Do NOT use `start.sh` - it's for production deployment only!

> **🪟 Windows Users:** We show both PowerShell (recommended) and Command Prompt alternatives. Use PowerShell unless you have a specific reason to use Command Prompt. See [Windows Setup Guide](docs/guides/WINDOWS_SETUP.md) for details.

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

**Why development mode?**

- No Docker required
- All tests pre-configured for port 3000
- Hot reload enabled
- Perfect for learning!

### Step 3: Open Browser

Frontend: <http://localhost:3000>  ← Open this!
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

**Why development mode?**

- No Docker required
- All tests pre-configured for port 3000
- Hot reload enabled
- Perfect for learning!

### Windows Step 3: Open Browser

Frontend: <http://localhost:3000>  ← Open this!
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

## 🧪 Run Your First Test

### Option 1: Python (pytest) - Backend Testing

<details>
<summary><b>macOS / Linux</b></summary>

```bash
cd backend
source .venv/bin/activate
pytest -v
```

**Expected:** 166 tests pass in ~51 seconds ✅

</details>

<details>
<summary><b>Windows</b></summary>

```bat
cd backend
.venv\Scripts\activate
pytest -v
```

**Expected:** 166 tests pass in ~51 seconds ✅

</details>

### Option 2: JavaScript (Playwright) - E2E Testing

<details>
<summary><b>All Platforms</b></summary>

```bash
cd tests
npm install
npx playwright install chromium
npm test
```

**Expected:** E2E tests run in browser ✅

</details>

---

## 🎯 Next Steps

### ⭐ New to Testing?

**→ [START_HERE.md](START_HERE.md)** - Choose your learning path

### 🧪 Want Hands-On Labs?

**→ [labs/LAB_01_Your_First_Test.md](labs/LAB_01_Your_First_Test.md)** - Write first test in 30 min

### 📚 Want Structured Learning?

**→ [docs/course/COURSE_AUTOMATION_TESTING_101.md](docs/course/COURSE_AUTOMATION_TESTING_101.md)** - Progressive curriculum

### 📖 Want to Run Tests?

**→ [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md)** - Complete guide

---

## 🖥️ Understanding The Two Start Scripts

### Development Mode (`start-dev.sh` / `start-dev.bat`) ✅ For Learning

**Ports:**

- Frontend: <http://localhost:3000>
- Backend: <http://localhost:8000>

**Use for:**

- ✅ Learning and testing
- ✅ All labs and tutorials
- ✅ No Docker required
- ✅ Hot reload enabled
- ✅ Easy debugging

### Production Mode (`start.sh` / `start.bat`) ⚠️ For Deployment

**Ports:**

- Frontend: <http://localhost:8000>
- Backend: <http://localhost:8000>

**Use for:**

- Production deployment only
- Requires Docker
- ⚠️ Tests need reconfiguration

**Always use `start-dev.sh` for learning!**

---

## 🌍 Cross-Platform Notes

### setup_images.py

This script **automatically detects your OS** and uses appropriate fonts:

- Windows: Arial, Calibri, Segoe UI
- macOS: Helvetica, Arial
- Linux: DejaVu, Liberation

Just run: `python3 setup_images.py` (or `python` on Windows)

### Virtual Environment Commands

**Activate:**

- macOS/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

**Deactivate:** `deactivate` (all platforms)

---

## 🐛 Troubleshooting

### Port Already in Use

**macOS / Linux:**

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Windows:**

```bat
REM Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

REM Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Python/Node Not Found

**Install Python 3.11+:**

- macOS: `brew install python@3.11`
- Linux: `sudo apt install python3 python3-pip python3-venv`
- Windows: Download from [python.org](https://www.python.org/)

**Install Node.js 20+:**

- All platforms: Download from [nodejs.org](https://nodejs.org/)

### Permission Denied (macOS/Linux only)

```bash
chmod +x *.sh
./start-dev.sh
```

### Wrong Port Opened

**Common mistake:** Opening <http://localhost:8000> after running `start-dev.sh`

**Fix:** Open <http://localhost:3000> (that's the frontend!)

Port 8000 is the backend API - it won't show the app interface.

---

## 🎯 Platform Comparison

| Task | macOS/Linux | Windows |
|------|-------------|---------|
| **Start app** | `./start-dev.sh` | `start-dev.bat` |
| **Reset DB** | `./reset-database.sh` | `reset-database.bat` |
| **Activate venv** | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| **Run tests** | `pytest -v` | `pytest -v` (same!) |
| **Path separator** | `/` | `\` |
| **Shell** | bash/zsh | CMD/PowerShell |

---

## ✅ Verification Checklist

After setup, verify:

- [ ] App loads at **<http://localhost:3000>** (development mode)
- [ ] Can login with test account
- [ ] Can create a post
- [ ] Backend tests run: `cd backend && pytest -v`
- [ ] See 166 tests pass

**⚠️ Common Mistake:** Don't open port 8000 - that's the API! The app is on port 3000.

---

## 📚 Documentation

**All docs organized in [`docs/`](docs/) directory:**

- [`docs/INDEX.md`](docs/INDEX.md) - Complete documentation index
- [`docs/course/`](docs/course/) - Learning materials
- [`docs/guides/`](docs/guides/) - How-to guides
- [`docs/reference/`](docs/reference/) - Reference docs

---

**🎉 You're ready! Choose your next step above!**
