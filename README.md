# 📱 Testbook - Automation Testing Platform

![CI Status](https://github.com/upt3mpo/testbook/actions/workflows/testbook-ci.yml/badge.svg)
![Backend Coverage](https://img.shields.io/badge/backend_coverage-86%25-brightgreen)
![Frontend Coverage](https://img.shields.io/badge/frontend_coverage-95%25-brightgreen)
![Total Tests](https://img.shields.io/badge/tests-210%2B-blue)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Node](https://img.shields.io/badge/node-20-green)

A production-grade social media application built for learning and practicing automation testing. Features 200+ backend tests, 30 frontend tests, comprehensive E2E coverage, and structured hands-on labs.

Perfect for individual learners, junior developers exploring testing, or manual QA professionals transitioning to automation.

**✅ 200+ Tests | Complete Testing Pyramid | 86% Backend Coverage | Production-Ready**

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start-5-minutes)
- [🎓 Learning Path](#-learning-path)
- [🖥️ Development vs Production Mode](#️-development-vs-production-mode)
- [🧪 Complete Testing Pyramid](#-complete-testing-pyramid)
- [📚 Documentation](#-documentation-organized)
- [✨ Features](#-features)
- [🎯 Quick Commands](#-quick-commands)
- [👥 Test Accounts](#-test-accounts)
- [🏗️ Tech Stack](#️-tech-stack)
- [🐛 Troubleshooting](#-troubleshooting)
- [❓ FAQ](#-frequently-asked-questions)
- [📞 Getting Help](#-getting-help)

---

## 🚀 Quick Start (5 Minutes)

Get Testbook running in 5 minutes on any platform!

**⚠️ IMPORTANT:** Use the **development mode** scripts below (`start-dev.sh` / `start-dev.bat`). These run the app on port 3000 and work with all tests. Do NOT use `start.sh` - it's for production deployment only!

> **🪟 Windows Users:** We show both PowerShell (recommended) and Command Prompt alternatives. Use PowerShell unless you have a specific reason to use Command Prompt. See [Windows Setup Guide](docs/guides/WINDOWS_SETUP.md) for details.

---

### 🖥️ Choose Your Platform

<details>
<summary><b>🍎 macOS / Linux</b> (click to expand)</summary>

#### Step 1: Clone Repository

```bash
git clone https://github.com/upt3mpo/testbook.git
cd testbook
```

#### Step 2: Start Application (Development Mode)

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

#### Step 3: Open Browser

Frontend: <http://localhost:3000> ← Open this!
Backend API: <http://localhost:8000/api>
API Docs: <http://localhost:8000/docs>

#### Step 4: Login

```text
Email: sarah.johnson@testbook.com
Password: Sarah2024!
```

✅ **Done!** You're ready to test!

</details>

<details>
<summary><b>🖥️ Windows</b> (click to expand)</summary>

#### Windows Step 1: Clone Repository

```bat
git clone https://github.com/upt3mpo/testbook.git
cd testbook
```

#### Windows Step 2: Start Application (Development Mode)

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

#### Windows Step 3: Open Browser

Frontend: <http://localhost:3000> ← Open this!
Backend API: <http://localhost:8000/api>
API Docs: <http://localhost:8000/docs>

#### Windows Step 4: Login

```text
Email: sarah.johnson@testbook.com
Password: Sarah2024!
```

✅ **Done!** You're ready to test!

</details>

---

### 🧪 Run Your First Test

#### Option 1: Python (pytest) - Backend Testing

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

#### Option 2: JavaScript (Playwright) - E2E Testing

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

### 🎯 Next Steps

#### ⭐ New to Testing?

**→ [learn/README.md](learn/README.md)** - Start here! Choose your track and learning style

#### 🧪 Want Hands-On Labs?

**→ [learn/stage_1_unit/exercises/](learn/stage_1_unit/exercises/)** - Write first test in 30 min

#### 📚 Want Structured Learning?

**→ [Learning Path](#-learning-path)** - Complete 5-stage curriculum overview

#### 📖 Want to Run Tests?

**→ [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md)** - Complete guide

---

### 🌍 Cross-Platform Notes

#### setup_images.py

This script **automatically detects your OS** and uses appropriate fonts:

- Windows: Arial, Calibri, Segoe UI
- macOS: Helvetica, Arial
- Linux: DejaVu, Liberation

Just run: `python3 setup_images.py` (or `python` on Windows)

#### Virtual Environment Commands

**Activate:** See [Quick Commands](docs/reference/QUICK_COMMANDS.md#virtual-environment) for all platforms

**Deactivate:** `deactivate` (all platforms)

---

### ✅ Verification Checklist

After setup, verify:

- [ ] App loads at **<http://localhost:3000>** (development mode)
- [ ] Can login with test account
- [ ] Can create a post
- [ ] Backend tests run: `cd backend && pytest -v`
- [ ] See 166 tests pass

**⚠️ Common Mistake:** Don't open port 8000 - that's the API! The app is on port 3000.

---

## 🎓 Learning Path

**Welcome to Testbook Automation Testing!**

A comprehensive learning platform for mastering automation testing. Perfect for individual learners, junior developers exploring testing, or manual QA professionals transitioning to automation.

**Your Platform:** 🖥️ Windows | 🍎 macOS | 🐧 Linux - All supported!

---

### 🌟 **Complete 5-Stage Curriculum**

**→ Start here: [learn/](learn/) or jump to [Stage 1: Unit Tests](learn/stage_1_unit/)**

**Duration:** 12-18 hours (self-paced)

- 🎯 Clear progression (Stage 1 → Stage 5)
- 🐍 Python Track OR ☕ JavaScript Track OR 🔄 Hybrid
- 📝 Reflection prompts at each stage
- ✅ Success criteria to track progress
- 💼 Portfolio-ready capstone project
- 🎓 Job interview preparation built in

**5 Stages:** Unit Tests → Integration → API/E2E → Performance/Security → Capstone

---

### 📚 **Learning Resources**

**Hands-On Exercises** - Jump straight into coding

- Start with: [Stage 1 Exercises](learn/stage_1_unit/exercises/)
- Write your first test in 30 minutes!
- Interactive and practical step-by-step instructions

**Reference Materials** - Quick lookups and deep dives

- [Testing Cheat Sheet](docs/reference/TESTING_CHEATSHEET.md) - Quick lookups
- [Running Tests Guide](docs/guides/RUNNING_TESTS.md) - Run all 210+ tests
- [Troubleshooting Guide](docs/reference/TROUBLESHOOTING.md) - Common issues

---

### 🗺️ Choose Your Track

Pick the track that matches your background and goals:

| Path                        | Language Focus      | Tools You'll Master                    | Time        | Best For                         | Start Here                                                                             |
| --------------------------- | ------------------- | -------------------------------------- | ----------- | -------------------------------- | -------------------------------------------------------------------------------------- |
| **🐍 Python Track**         | Python              | pytest, Playwright Python, k6          | 12-15 hours | Backend developers, API testing  | [Stage 1](learn/stage_1_unit/)                                                         |
| **☕ JavaScript Track**     | JavaScript          | Vitest, Playwright JS, MSW             | 14-17 hours | Frontend developers, React teams | [Stage 1 Exercises](learn/stage_1_unit/exercises/) then [Stage 1](learn/stage_1_unit/) |
| **🔄 Hybrid Track**         | Python + JavaScript | All tools from both stacks             | 15-18 hours | Full-stack QA, most realistic    | [Stage 1](learn/stage_1_unit/)                                                         |
| **⚡ Manual QA Transition** | Python-first        | pytest, Playwright, automation mindset | 20-25 hours | Manual testers going automation  | [Manual QA Guide](docs/guides/MANUAL_QA_TO_AUTOMATION.md)                              |

**Not sure?** Try the [Hybrid Track](learn/stage_1_unit/) - it's what most real QA roles need!

---

### 🚦 Recommended Path for Beginners

If you're new to automation testing, follow this progression:

#### Getting Started (Week 1-2)

1. **Read:** [README.md](README.md) - Understand the project (15 min)
2. **Run:** `./start-dev.sh` - Get Testbook running (5 min)
3. **Explore:** Use the app manually (15 min)
4. **Do:** [learn/stage_1_unit/exercises/](learn/stage_1_unit/exercises/) (30 min)

#### Backend Testing (Week 3-4)

1. **Do:** [learn/stage_1_unit/exercises/](learn/stage_1_unit/exercises/) (45 min)
2. **Do:** [learn/stage_2_integration/exercises/](learn/stage_2_integration/exercises/) (60 min)
3. **Practice:** Write 5 more tests on your own
4. **Read:** [backend/tests/README.md](backend/tests/README.md)

#### Frontend Testing (Week 5-6)

1. **Try:** Frontend component tests - `cd frontend && npm test` (30 min) ✨
2. **Try:** Accessibility tests - `npm test -- accessibility` (20 min) ✨
3. **Do:** [learn/stage_3_api_e2e/exercises/](learn/stage_3_api_e2e/exercises/) (90 min)
4. **Read:** [docs/reference/TESTING_PATTERNS.md](docs/reference/TESTING_PATTERNS.md) - Dynamic content
5. **Practice:** Write 3 E2E tests on your own
6. **Read:** [tests/README.md](tests/README.md)

#### Advanced Topics (Week 7-8)

1. **🆕 Do:** [learn/stage_3_api_e2e/exercises/](learn/stage_3_api_e2e/exercises/) - Page objects, fixtures (2 hours)
2. **🆕 Do:** [learn/stage_4_performance_security/exercises/](learn/stage_4_performance_security/exercises/) - MSW, accessibility (2 hours)
3. **🆕 Do:** [learn/stage_4_performance_security/exercises/](learn/stage_4_performance_security/exercises/) - Contract validation (90 min)
4. **Read:** [Contract Testing Guide](docs/guides/CONTRACT_TESTING.md) - Property-based testing (30 min) ✨
5. **Run:** API examples - `python tests/api/python_api_examples.py`
6. **Try:** Performance tests - `k6 run tests/performance/smoke-test.js`
7. **Explore:** Security tests - `pytest tests/security/`
8. **Study:** CI/CD workflows in `.github/workflows/` (5 workflows!) ✨
9. **Read:** [Logging Guide](docs/guides/LOGGING.md) - Observability ✨
10. **Read:** [CI/CD for E2E Testing](learn/stage_5_capstone/README.md#cicd-automation) - Production automation ✨

#### Mastery (Week 9+)

1. **Build:** Add a new feature with tests
2. **Achieve:** 90%+ code coverage
3. **Set up:** CI/CD for your code
4. **Document:** Your learning journey

---

### 📊 Skill Progression

```text
Level 0: "I've never written a test"
    ↓
    → Do Lab 1 (30 min)
    ↓
Level 1: "I can run and modify tests"
    ↓
    → Do Labs 2-3 (2 hours)
    ↓
Level 2: "I can write backend tests"
    ↓
    → Do Lab 4 (90 min)
    ↓
Level 3: "I can write E2E tests"
    ↓
    → Complete advanced topics
    ↓
Level 4: "I can test anything professionally"
```

---

### 🛠️ What You Need

#### Required

- ✅ Computer (Mac, Windows, or Linux)
- ✅ Terminal/Command Prompt
- ✅ Code editor (VS Code recommended)
- ✅ Testbook installed ([Quick Start](#-quick-start-5-minutes))
- ✅ 30 minutes to start

**Having setup issues?** → [Troubleshooting Guide](#-troubleshooting) (technical errors) | [FAQ](#-frequently-asked-questions) (learning questions)

#### Optional (For Later)

- Node.js (for E2E tests)
- K6 (for performance tests)
- Postman (for API testing)
- Git/GitHub (for CI/CD)

---

### 🎯 Your First 30 Minutes

**Right now, do this:**

1. **Read this page** (you're doing it!) - 5 min
2. **Choose your track** above - 1 min
3. **Open the learning path** - 1 min
4. **Follow first exercise** - 30 min

**That's it!** You'll have written your first test!

---

### 🎬 Let's Begin

**Ready to start your testing journey?**

#### 🌟 **Start Here: [learn/](learn/)**

**Complete 5-stage curriculum:**

1. **Choose your track** → Python, JavaScript, or Hybrid
2. **Start with Stage 1** → [Unit Tests](learn/stage_1_unit/)
3. **Progress through stages** → Stage 1 → Stage 2 → ... → Stage 5
4. **Build your portfolio** → Complete capstone project

**Time:** 12-18 hours self-paced | **Result:** Job-ready testing skills

#### 🚀 **Want to jump straight into coding?**

**Start with hands-on exercises:**

1. **Open** → [Stage 1 Exercises](learn/stage_1_unit/exercises/)
2. **Pick** → [Lab 1: Your First Test](learn/stage_1_unit/exercises/LAB_01_Your_First_Test.md)
3. **Code** → Follow step-by-step instructions
4. **Learn** → Gain hands-on experience immediately

---

### 🚀 One Final Thing

**You're about to learn skills that:**

- Companies pay $80k-$150k+ for
- Are in high demand (SDET, QA Automation)
- Give you confidence in your code
- Make you a better developer

**Let's do this! 🎓**

---

## 🖥️ Development vs Production Mode

**Quick Answer:** Use `start-dev.sh` (or `start-dev.bat` on Windows) for learning and testing!

### 🎯 Two Modes, Two Scripts

Testbook has two different deployment modes, each with its own start script:

#### 1. Development Mode (For Learning) ✅ **← USE THIS**

**Scripts:**

- macOS/Linux: `./start-dev.sh`
- Windows: `start-dev.bat`
- WSL: `./start-dev.sh` (see [Windows Setup Guide](docs/guides/WINDOWS_SETUP.md))

**What it does:**

- Starts backend on `http://localhost:8000`
- Starts frontend on `http://localhost:3000` ← **Open this in your browser!**
- Uses local file system (no Docker)
- Hot reload enabled (changes update automatically)
- **Idempotent:** Skips installs if dependencies already present
- **Health checks:** Waits for services to be ready before continuing
- Easy to debug

**Ports:**

- Frontend: `http://localhost:3000` (React dev server with Vite)
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

**Use for:**

- ✅ All labs and tutorials
- ✅ Running tests (all tests expect these ports)
- ✅ Learning and experimentation
- ✅ Development work
- ✅ Debugging

---

#### 2. Production Mode (For Deployment) ⚠️

**Scripts:**

- macOS/Linux: `./start.sh`
- Windows: `start.bat`

**What it does:**

- Runs everything in Docker containers
- Frontend and backend both on `http://localhost:8000`
- Production-optimized build
- Mimics real deployment

**Ports:**

- Everything: `http://localhost:8000` (Dockerized)

**Use for:**

- ⚠️ Testing production deployment
- ⚠️ Docker practice
- ⚠️ NOT recommended for learning

**Why NOT for learning:**

- Requires Docker installation
- Tests need reconfiguration (different ports)
- Harder to debug
- Slower to start up
- More complex setup

---

### 📊 Side-by-Side Comparison

| Feature                | Development Mode (`start-dev`) | Production Mode (`start`) |
| ---------------------- | ------------------------------ | ------------------------- |
| **Frontend Port**      | 3000                           | 8000                      |
| **Backend Port**       | 8000                           | 8000                      |
| **Docker Required**    | No                             | Yes                       |
| **Hot Reload**         | Yes                            | No                        |
| **Test Compatibility** | All tests work                 | Tests need modification   |
| **Startup Time**       | ~10 seconds                    | ~60 seconds               |
| **Debugging**          | Easy                           | Harder                    |
| **Use Case**           | Learning, testing              | Production deployment     |

---

### 🎓 For Students

**Always use development mode:**

```bash
# macOS/Linux
./start-dev.sh

# Windows
start-dev.bat
```

**Then open:** `http://localhost:3000`

**Common mistake:** Opening `http://localhost:8000` after starting dev mode. That's the API, not the app! Use port 3000.

---

### 🏗️ How Development Mode Works

```text
start-dev.sh runs:
├── Pre-checks
│   ├── Check if ports 8000 and 3000 are available
│   └── Generate placeholder images (if missing)
│
├── Backend Setup
│   ├── cd backend
│   ├── Create venv (if doesn't exist)
│   ├── source .venv/bin/activate
│   ├── Install dependencies (ONLY if not already present)
│   ├── Seed database
│   ├── uvicorn main:app --reload
│   ├── Health check: Wait for http://localhost:8000/docs
│   └── ✅ Runs on: localhost:8000
│
└── Frontend Setup
    ├── cd frontend
    ├── Install node_modules (ONLY if not already present)
    ├── npm run dev
    ├── Health check: Wait for http://localhost:3000
    └── ✅ Runs on: localhost:3000
```

**Result:**

- Frontend at 3000 talks to Backend at 8000
- All tests configured for this setup
- Scripts are **idempotent** - safe to run multiple times
- Health checks ensure services are ready before reporting success
- Clear error messages if something fails

---

### 🐳 How Production Mode Works

```text
start.sh runs:
├── docker-compose up
│   ├── Builds backend container
│   ├── Builds frontend container
│   ├── Sets up networking
│   └── Everything on: localhost:8000
```

**Result:**

- Isolated containers
- Production-like environment
- Single port (8000)

---

### 🔧 Troubleshooting

#### "I ran start-dev.sh but can't see the app"

**Check:**

1. Did you open `http://localhost:3000` (not 8000)?
2. Are both terminals running (backend and frontend)?
3. Any error messages in the terminals?

#### "I want to switch from dev to production mode"

**Do this:**

1. Stop both terminals (Ctrl+C in each)
2. Run: `./start.sh` (with Docker running)
3. Open: `http://localhost:8000`
4. **Note:** Tests will need port changes!

#### "Tests are failing after switching modes"

**Reason:** Tests expect development mode ports (3000 for frontend, 8000 for backend)

**Fix:** Switch back to development mode:

```bash
./start-dev.sh
```

---

### ✅ Verification Checklist

After starting in development mode, verify:

- [ ] Backend running at `http://localhost:8000/docs` (API docs load)
- [ ] Frontend running at `http://localhost:3000` (app loads)
- [ ] Can login with: `sarah.johnson@testbook.com` / `Sarah2024!`
- [ ] Can create a post
- [ ] Tests pass: `cd backend && pytest -v`

---

### 🎯 Quick Decision Tree

```text
Are you learning/testing?
├─ YES → Use start-dev.sh ✅
└─ NO → Are you deploying to production?
    ├─ YES → Use start.sh with Docker
    └─ NO → You probably want start-dev.sh ✅
```

---

### 📚 Related Documentation

- [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md) - Running all tests

---

**🎓 Remember:** When in doubt, use development mode (`start-dev.sh`)!

---

## 🧪 Complete Testing Pyramid

We test at every level - backend, frontend, E2E, API, security, and performance!

![Testbook Dashboard](docs/screenshots/testbook-dashboard.png)
_Testbook running in development mode with seeded test data_

### Backend Testing (Python + pytest)

**166+ tests covering:**

- ✅ Unit tests (models, auth, utilities)
- ✅ Integration tests (database operations)
- ✅ API tests (all endpoints)
- ✅ Contract tests (property-based with Schemathesis)\*
- ✅ Security tests

\*Contract test currently skipped pending OpenAPI 3.1.0 support. See [Contract Testing Guide](docs/guides/CONTRACT_TESTING.md) to learn about this powerful testing technique.

```bash
cd backend
pytest -v                    # Run all 180 tests (1 skipped)
```

![Backend Tests Passing](docs/screenshots/backend-tests-passing.png)
_180 backend tests running with 86% code coverage_

![Coverage Report](docs/screenshots/coverage_report.png)
_Detailed HTML coverage report showing tested code paths_

### Frontend Component Testing (JavaScript + Vitest)

**30+ tests covering:**

- ✅ React component rendering
- ✅ User interactions
- ✅ Form validation
- ✅ Accessibility (WCAG compliance)
- ✅ Keyboard navigation
- ✅ Contract validation

```bash
cd frontend
npm test                     # Run component tests
npm run test:a11y            # Accessibility tests
```

![Frontend Tests](docs/screenshots/frontend-tests.png)
_30 frontend tests with Vitest, React Testing Library, and MSW_

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

![E2E Test Running](docs/screenshots/e2e-test-running.gif)
_Playwright automating browser interactions - login flow in action_

**Both?** - Recommended for well-rounded testers! 🚀

- Try Python version first
- Then JavaScript version
- Compare and learn both!

**Other Tools:**

- **Selenium** - Supported (any language)
- **Cypress** - Supported (JavaScript only)

### Platform-Specific Notes

| Platform    | Start Command    | Python Activation         | Notes                 |
| ----------- | ---------------- | ------------------------- | --------------------- |
| **macOS**   | `./start-dev.sh` | source .venv/bin/activate | Use Terminal          |
| **Linux**   | `./start-dev.sh` | source .venv/bin/activate | Use Terminal          |
| **Windows** | `start-dev.bat`  | .venv\Scripts\activate    | Use CMD or PowerShell |

See [Quick Commands](docs/reference/QUICK_COMMANDS.md#virtual-environment) for more commands!

---

## 📚 Documentation (Organized!)

### Essential (Start Here)

- **[Learning Path](#-learning-path)** - Choose your track ⭐
- **[Quick Start](#-quick-start-5-minutes)** - Get app running in 5 minutes
- **[FAQ](#-frequently-asked-questions)** - Learning questions and quick setup guidance
- **[Development vs Production Mode](#️-development-vs-production-mode)** - Dev vs production explained
- **This file** - Project overview

### For Learning

- **[Learning Path](learn/README.md)** - Structured curriculum
- **[Learn Exercises](learn/)** - Hands-on tutorials
- **[Choose Your Track](learn/README.md#choose-your-track)** - Choose track for your background
- **[Running Tests Guide](docs/guides/RUNNING_TESTS.md)** - How to run everything
- **[Troubleshooting](docs/reference/TROUBLESHOOTING.md)** - Avoid common errors

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

**📋 Quick Reference:** [Quick Commands](docs/reference/QUICK_COMMANDS.md) - Common commands without task runners

### Platform-Specific Commands

**macOS / Linux:**

```bash
# Start app
./start-dev.sh

# Reset database
./reset-database.sh

# Run tests
cd backend && source .venv/bin/activate && pytest -v
# See [Quick Commands](docs/reference/QUICK_COMMANDS.md) for all commands
```

**Windows:**

```bat
REM Start app
start-dev.bat

REM Reset database
reset-database.bat

REM Run tests
cd backend
.venv\Scripts\activate
pytest -v
REM See Quick Commands for all commands
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

| Email                        | Password        | Platform |
| ---------------------------- | --------------- | -------- |
| <sarah.johnson@testbook.com> | Sarah2024!      | All      |
| <mike.chen@testbook.com>     | MikeRocks88     | All      |
| <emma.davis@testbook.com>    | EmmaLovesPhotos | All      |
| <newuser@testbook.com>       | NewUser123!     | All      |

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
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

# See [Quick Commands](docs/reference/QUICK_COMMANDS.md#virtual-environment) for all platforms
```

See [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md) for complete troubleshooting.

---

## ❓ Frequently Asked Questions

**Quick answers to common learning and setup questions**

---

### 🚀 Getting Started

#### Q: Which start script should I use?

**A:** Use `start-dev.sh` (or `start-dev.bat` on Windows) for learning!

- ✅ **Development mode** (`start-dev.sh`): Port 3000, no Docker, perfect for testing
- ⚠️ **Production mode** (`start.sh`): Port 8000, requires Docker, for deployment only

See [Development vs Production Mode](#️-development-vs-production-mode) for full details.

---

#### Q: What port should I open in my browser?

**A:** `http://localhost:3000` for development mode!

Common mistake: Opening port 8000 (that's the API, not the app).

---

#### Q: Do I need Docker?

**A:** Not for learning! Only for production mode.

Development mode works without Docker and is recommended for all labs.

---

#### Q: Is it safe to run start-dev.sh multiple times?

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

#### Q: The script says "Port already in use" - what do I do?

**A:** You might have a previous instance running. See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick fix:** Let the script continue anyway - it might work if the existing process is the one you want!

---

#### Q: I'm on Windows - which approach should I use?

**A:** See the [Windows Setup Guide](docs/guides/WINDOWS_SETUP.md) for three options:

1. **Native Windows** (`start-dev.bat`) - Easiest for beginners
2. **WSL** (`start-dev.sh` in WSL) - Best Linux compatibility
3. **Docker** - Production-like environment

Most students prefer Native Windows or WSL.

---

### 🐍 Python & Virtual Environment

#### Q: "pytest: command not found" or "ModuleNotFoundError"

**A:** Your virtual environment isn't activated or dependencies aren't installed. See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick check:** Look for `(venv)` in your terminal prompt:

```bash
(venv) $ pytest    # ✅ Activated
$ pytest           # ❌ Not activated
```

---

### 🧪 Running Tests

#### Q: "Tests not found" or "collected 0 items"

**A:** Make sure you're in the right directory:

```bash
# For backend tests
cd backend
pytest tests/

# Check you're in the right place
pwd  # Should show .../Testbook/backend
```

---

#### Q: Tests pass individually but fail together

**A:** Test data pollution. See [TESTING_ANTIPATTERNS.md](docs/reference/TESTING_ANTIPATTERNS.md) for solutions.

---

#### Q: "Database is locked" or E2E tests failing

**A:** See [Troubleshooting](#-troubleshooting) for detailed solutions.

---

### 🌐 Connection Issues

#### Q: "Connection refused" or port conflicts

**A:** See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick check:** Make sure backend is running:

```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

---

### 🎭 Playwright Issues

#### Q: Playwright tests failing or timing out

**A:** See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick tip:** Avoid `waitForTimeout()` - use proper element waits instead.

---

### 📂 File & Directory Issues

#### Q: "No such file or directory" or can't find test files

**A:** Check you're in the right directory and test files start with `test_`:

```bash
# See where you are
pwd
# Should be in Testbook root for most commands

# For pytest
cd backend
pytest tests/
```

---

### 🔒 Permission Issues

#### Q: "Permission denied" or "Access denied"

**A:** See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick fixes:**

- macOS/Linux: `chmod +x *.sh`
- Windows: Run as Administrator

---

### 💾 Database Issues

#### Q: Database problems or need to reset

**A:** Use the reset script:

```bash
# From Testbook root
./reset-database.sh  # macOS/Linux
reset-database.bat   # Windows
```

---

### 🎓 Learning & Labs

#### Q: I'm stuck on a lab. What should I do?

**A:** Follow this checklist:

1. **Re-read instructions** - Carefully
2. **Check error message** - It usually tells you what's wrong
3. **Look at [TROUBLESHOOTING.md](docs/reference/TROUBLESHOOTING.md)** - Your issue is probably there
4. **Check [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Learn to debug
5. **Look at working examples** - Check existing tests
6. **Take a break** - Fresh eyes help!

---

#### Q: Where are the lab solutions?

**A:** In `learn/solutions/` (for instructors).

Students should try exercises first, then check solutions if really stuck.

---

#### Q: Which exercises should I do first?

**A:** Follow this order:

1. **Stage 1 Exercises** - Your first test (30 min)
2. **Stage 1 Exercises** - Testing real functions (45 min)
3. **Stage 1 Exercises** - Understanding fixtures (45 min) ← Important!
4. **Stage 1 Exercises** - Reading errors (30 min) ← Very helpful!
5. **Stage 2 Exercises** - API endpoints (60 min)
6. Continue with Stages 3-4...

---

#### Q: How long will this take?

**A:** Approximate times:

- **Stage 1 exercises**: 2-3 hours
- **Stage 2 exercises**: 1 hour
- **Stage 3 exercises**: 3-4 hours
- **Full course**: 30-40 hours

Go at your own pace!

---

### 🛠️ Tool-Specific Issues

#### Q: Python version, npm, or coverage issues

**A:** See [Troubleshooting](#-troubleshooting) for detailed solutions.

**Quick checks:**

- Python version: `python --version` (should be 3.13+)
- Node version: `node --version` (should be 20+)

---

### 🔍 Debugging Tips

#### Q: How do I debug failing tests?

**A:** See [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md) for comprehensive debugging strategies.

**Quick tips:**

- Use `pytest -v -s` to see print statements
- Use `pytest --pdb` to drop into debugger
- Run single test: `pytest tests/test_file.py::test_name -v`

---

### 📚 Documentation

#### Q: Where do I find information about X?

**A:** Check the docs structure:

- **Getting started**: `README.md`, [Learning Path](#-learning-path)
- **Running tests**: `docs/guides/RUNNING_TESTS.md`
- **Learning curriculum**: `learn/README.md`
- **Quick reference**: `docs/reference/QUICK_REFERENCE_*.md`
- **Common mistakes**: `docs/reference/TROUBLESHOOTING.md`
- **Anti-patterns**: `docs/reference/TESTING_ANTIPATTERNS.md`
- **Learning path**: [Learning Path](#-learning-path)

Full index: `docs/INDEX.md`

---

#### Q: Can I use this for teaching or mentoring?

**A:** Yes! While Testbook is designed for individual learning, it works great for:

- Staff engineers guiding junior developers
- Mentors introducing testing to manual QA professionals
- Tech leads onboarding team members

See:

- `learn/solutions/` - Sample solutions for guidance
- `learn/README.md` - Structured curriculum
- [Learning Path](#-learning-path) - Choose your track and get started

---

### 🚨 Still Stuck?

If your issue isn't here:

1. **Check [Troubleshooting](#-troubleshooting)** - Comprehensive technical solutions ⭐
2. **Check [TROUBLESHOOTING.md](docs/reference/TROUBLESHOOTING.md)** - 24+ common errors
3. **Check [DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Debug strategies
4. **Search GitHub Issues** - Someone might have asked
5. **Create an Issue** - We'll help you!

---

### 💡 Pro Tips

#### Tip 1: Keep Two Terminals Open

```text
Terminal 1: Backend running
Terminal 2: Run tests
```

#### Tip 2: Use Quick References

Bookmark these for fast lookups:

- `docs/reference/QUICK_REFERENCE_PYTEST.md`
- `docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md`

#### Tip 3: Read Error Messages Carefully

90% of issues are explained in the error message. Read it!

#### Tip 4: Start Fresh

When really stuck:

```bash
# Reset everything
./reset-database.sh
cd backend && deactivate && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

#### Tip 5: Use Verbose Mode

Always use `-v` for better output:

```bash
pytest -v  # Shows test names and results
```

---

**Still have questions? Create an issue on GitHub!** 🚀

---

## 📞 Getting Help

### Quick Troubleshooting

- **[TROUBLESHOOTING.md](docs/reference/TROUBLESHOOTING.md)** - Technical errors with exact fixes
- **[FAQ](#-frequently-asked-questions)** - Learning questions and quick setup guidance
- **[DEBUGGING_GUIDE.md](docs/reference/DEBUGGING_GUIDE.md)** - Step-by-step debugging
- **[Scripts Guide](scripts/README.md)** - Development and maintenance utilities

### Learning Resources

1. **Starting out?** → [Learning Path](#-learning-path)

2. **Running tests?** → [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md)
3. **Learning?** → [learn/](learn/)
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

**→ [Learning Path](#-learning-path)** - Begin your testing journey!

**→ [learn/stage_1_unit/exercises/](learn/stage_1_unit/exercises/)** - Write your first test in 30 minutes!
