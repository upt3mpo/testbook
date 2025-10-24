# 📱 Testbook - Automation Testing Platform

![CI Status](https://github.com/upt3mpo/testbook/actions/workflows/testbook-ci.yml/badge.svg)
![Backend Coverage](https://img.shields.io/badge/backend_coverage-87%25-brightgreen)
![Frontend Coverage](https://img.shields.io/badge/frontend_coverage-95%25-brightgreen)
![Total Tests](https://img.shields.io/badge/tests-220%2B-blue)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Node](https://img.shields.io/badge/node-20-green)

A production-grade social media application built for learning and practicing
automation testing. Features 180+ backend tests, 40+ frontend tests,
comprehensive E2E coverage, and structured hands-on labs.

Perfect for individual learners, junior developers exploring testing, or manual QA professionals transitioning to automation.

**✅ 220+ Tests | Complete Testing Pyramid | 87% Backend Coverage | Production-Ready**

<h2 id="table-of-contents">📋 Table of Contents</h2>

- [🚀 Quick Start](#quick-start)
- [🎓 Learning Path](#learning-path)
- [🖥️ Development Mode](#development-mode)
- [🧪 Complete Testing Pyramid](#complete-testing-pyramid)
- [📚 Documentation](#documentation)
- [✨ Features](#features)
- [🎯 Quick Commands](#quick-commands)
- [👥 Test Accounts](#test-accounts)
- [🏗️ Tech Stack](#tech-stack)
- [🐛 Troubleshooting](#troubleshooting)
- [📞 Getting Help](#getting-help)

---

<h2 id="quick-start">🚀 Quick Start</h2>

**3 simple steps to get started:**

```bash
# 1. Clone and start
git clone https://github.com/upt3mpo/testbook.git
cd testbook
./start-dev.sh  # macOS/Linux
start-dev.bat   # Windows

# 2. Open browser
# http://localhost:3000

# 3. Login
# Email: sarah.johnson@testbook.com
# Password: Sarah2024!
```

**✅ Done!** You're ready to test!

**📖 Need detailed setup?** → [Complete Quick Start Guide](docs/guides/QUICK_START.md)

---

<h2 id="learning-path">🎓 Learning Path</h2>

**Choose your track and master automation testing:**

| Track             | Language   | Time        | Best For            | Start Here                     |
| ----------------- | ---------- | ----------- | ------------------- | ------------------------------ |
| **🐍 Python**     | Python     | 24-34 hours | Backend developers  | [Stage 1](learn/stage_1_unit/) |
| **🟨 JavaScript** | JavaScript | 26-36 hours | Frontend developers | [Stage 1](learn/stage_1_unit/) |
| **🔄 Hybrid**     | Both       | 28-38 hours | Full-stack QA       | [Stage 1](learn/stage_1_unit/) |

**📚 Detailed curriculum:** [Complete Learning Guide](learn/README.md)

### 🧪 The 5 Stages

1. **Stage 1:** Unit Testing (4-6 hours) - Test individual functions
2. **Stage 2:** Integration Testing (5-7 hours) - Test components together
3. **Stage 3:** E2E Testing (5-7 hours) - Test complete user workflows
4. **Stage 4:** Performance & Security (6-8 hours) - Load testing & OWASP
5. **Stage 5:** Portfolio Capstone (4-6 hours) - Build job-ready artifacts

**Total: 20-30 hours** | **Result: Job-ready testing skills**

---

<h2 id="development-mode">🖥️ Development Mode</h2>

**Use `start-dev.sh` for learning and testing!**

- **Frontend:** `http://localhost:3000` ← Open this!
- **Backend API:** `http://localhost:8000`
- **API Docs:** `http://localhost:8000/docs`

**Why development mode?**

- No Docker required
- All tests pre-configured
- Hot reload enabled
- Perfect for learning

**📖 Full explanation:** [Development vs Production Guide](docs/guides/DEPLOYMENT_MODES.md)

---

<h2 id="complete-testing-pyramid">🧪 Complete Testing Pyramid</h2>

Testbook demonstrates the complete testing pyramid with real, production-quality tests:

### 🧪 Unit Tests (Stage 1)

**Backend:** 180 tests with pytest

```python
def test_user_creation():
    user = create_user("test@example.com", "password123")
    assert user.email == "test@example.com"
    assert user.is_active is True
```

**Frontend:** 40 tests with Vitest

```javascript
test("should render login form", () => {
  render(<LoginForm />);
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
});
```

### 🧱 Integration Tests (Stage 2)

**API Endpoints:** TestClient + pytest

```python
def test_create_post_integration():
    response = client.post("/api/posts", json={"content": "Test post"})
    assert response.status_code == 201
    assert response.json()["content"] == "Test post"
```

**Component Testing:** Vitest + React Testing Library

```javascript
test("should create post when form submitted", async () => {
  render(<CreatePost onPostCreated={mockCallback} />);
  await user.type(screen.getByRole("textbox"), "Test post");
  await user.click(screen.getByRole("button", { name: /post/i }));
  expect(mockCallback).toHaveBeenCalledWith(
    expect.objectContaining({
      content: "Test post",
    })
  );
});
```

### 🌐 E2E Tests (Stage 3)

**Complete User Workflows:** Playwright

```javascript
test("user can create and view posts", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[data-testid="email"]', "sarah.johnson@testbook.com");
  await page.fill('[data-testid="password"]', "Sarah2024!");
  await page.click('[data-testid="login-button"]');

  await page.click('[data-testid="create-post"]');
  await page.fill('[data-testid="post-content"]', "My first post!");
  await page.click('[data-testid="submit-post"]');

  await expect(page.locator('[data-testid="post-content"]')).toContainText(
    "My first post!"
  );
});
```

### 🚀 Performance & Security (Stage 4)

**Load Testing:** k6

```javascript
import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    { duration: "2m", target: 100 },
    { duration: "5m", target: 100 },
    { duration: "2m", target: 0 },
  ],
};

export default function () {
  let response = http.get("http://localhost:8000/api/posts");
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
  });
}
```

**Security Testing:** OWASP Top 10

```python
def test_sql_injection_prevention():
    malicious_payload = "'; DROP TABLE users; --"
    response = client.post("/api/posts", json={"content": malicious_payload})
    assert response.status_code == 201  # Should be sanitized, not crash
    assert "DROP TABLE" not in response.json()["content"]
```

---

<h2 id="documentation">📚 Documentation</h2>

### 🎯 Quick Start

- **[Complete Setup Guide](docs/guides/QUICK_START.md)** - Detailed platform-specific instructions
- **[Development vs Production](docs/guides/DEPLOYMENT_MODES.md)** - Understanding the two modes
- **[FAQ](docs/guides/FAQ.md)** - Common questions and answers

### 🧪 Testing Guides

- **[Running Tests](docs/guides/RUNNING_TESTS.md)** - How to run all test types
- **[Testing Guide](docs/guides/TESTING_GUIDE.md)** - Comprehensive examples
- **[Troubleshooting](docs/reference/TROUBLESHOOTING.md)** - Fix common issues

### 📖 Learning Materials

- **[Learning Path](learn/README.md)** - Complete 5-stage curriculum
- **[Stage 1: Unit Tests](learn/stage_1_unit/)** - Start here!
- **[All Documentation](docs/INDEX.md)** - Complete documentation index

---

<h2 id="features">✨ Features</h2>

### 🧪 Testing Features

- **180+ Backend Tests** - pytest with 87% coverage
- **40+ Frontend Tests** - Vitest + React Testing Library
- **15+ E2E Tests** - Playwright (Python & JavaScript)
- **Performance Tests** - k6 load testing
- **Security Tests** - OWASP Top 10 coverage
- **API Tests** - Postman collection + Python examples

### 🎓 Learning Features

- **5-Stage Curriculum** - Progressive skill building
- **Dual Language Support** - Python and JavaScript tracks
- **Real Code Examples** - Production-quality test patterns
- **Hands-on Labs** - Step-by-step exercises
- **Portfolio Ready** - Build artifacts for job applications

### 🏗️ Application Features

- **User Authentication** - JWT-based auth with bcrypt
- **Social Media Posts** - Create, view, like posts
- **Real-time Updates** - WebSocket integration
- **File Uploads** - Image and video support
- **Rate Limiting** - Production-ready API protection
- **Database** - SQLite with SQLAlchemy ORM

---

<h2 id="quick-commands">🎯 Quick Commands</h2>

### 🚀 Start Application

```bash
# Development mode (recommended for learning)
./start-dev.sh        # macOS/Linux
start-dev.bat         # Windows

# Production mode (Docker required)
./start.sh            # macOS/Linux
start.bat             # Windows
```

### 🧪 Run Tests

```bash
# Backend tests (pytest)
cd backend
# Linux/Mac
source .venv/bin/activate
pytest -v

# Windows (PowerShell)
.venv\Scripts\activate
pytest -v

# Frontend tests (Vitest)
cd frontend
npm test

# E2E tests (Playwright)
cd tests
npm install
npx playwright test
```

### 🔧 Environment Configuration (Optional)

**For easier development** - avoid typing `TESTING=true` every time:

```bash
# Copy the environment template
cp backend/env.example backend/.env

# The defaults are ready to use! Just run:
uvicorn main:app --reload --port 8000
```

**What the .env file does:**

- ✅ Sets `TESTING=true` automatically (enables dev endpoints, higher rate limits)
- ✅ Configures logging, CORS, and other settings
- ✅ No need to type environment variables manually

**Note:** The `start-dev` scripts already handle this automatically! This is only needed if you want to run commands manually.

<details>
<summary><b>Windows PowerShell Instructions</b></summary>

```powershell
# Copy the environment template
Copy-Item backend\env.example backend\.env

# Run the backend
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

</details>

### 🔧 Development

```bash
# Reset database
./reset-database.sh   # macOS/Linux
reset-database.bat    # Windows

# Install dependencies
cd backend && uv sync
cd frontend && npm install
```

---

<h2 id="test-accounts">👥 Test Accounts</h2>

Use these accounts to test the application:

| Email                        | Password      | Role | Description            |
| ---------------------------- | ------------- | ---- | ---------------------- |
| `sarah.johnson@testbook.com` | `Sarah2024!`  | User | Primary test account   |
| `mike.chen@testbook.com`     | `MikeRocks88` | User | Secondary test account |

**Note:** These accounts are automatically created when you start the application.

---

<h2 id="tech-stack">🏗️ Tech Stack</h2>

### Backend

- **Python 3.13** - Modern Python with type hints
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database ORM
- **pytest** - Testing framework
- **uv** - Fast Python package manager

### Frontend

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool
- **Vitest** - Testing framework
- **React Testing Library** - Component testing

### Testing

- **Playwright** - E2E testing (Python & JavaScript)
- **k6** - Performance testing
- **MSW** - API mocking
- **Postman** - API testing

### DevOps

- **GitHub Actions** - CI/CD
- **Docker** - Containerization
- **SQLite** - Development database

---

<h2 id="troubleshooting">🐛 Troubleshooting</h2>

### Common Issues

**App won't start?**

- Make sure ports 3000 and 8000 are free
- Use `start-dev.sh` (not `start.sh`)
- Check both terminals are running

**Tests failing?**

- Make sure app is running (`start-dev.sh`)
- Check you're in the right directory
- See [Troubleshooting Guide](docs/reference/TROUBLESHOOTING.md)

**Can't find the app?**

- Open `http://localhost:3000` (not 8000!)
- Port 8000 is the API, port 3000 is the app

**📖 More help:** [Complete Troubleshooting Guide](docs/reference/TROUBLESHOOTING.md) | [FAQ](docs/guides/FAQ.md)

---

<h2 id="getting-help">📞 Getting Help</h2>

**Having issues?**

1. **Check the guides:** [Quick Start](docs/guides/QUICK_START.md) | [Troubleshooting](docs/reference/TROUBLESHOOTING.md) | [FAQ](docs/guides/FAQ.md)
2. **GitHub Discussions:** [Ask questions](https://github.com/upt3mpo/testbook/discussions)
3. **GitHub Issues:** [Report bugs](https://github.com/upt3mpo/testbook/issues)

**Learning questions?**

- **Start here:** [Learning Path](learn/README.md)
- **Stage 1:** [Unit Testing](learn/stage_1_unit/)
- **All docs:** [Documentation Index](docs/INDEX.md)

---

**🎓 Ready to master automation testing? Start with [Stage 1: Unit Tests](learn/stage_1_unit/)! 🚀**
