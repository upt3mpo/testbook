# 🚀 Which Start Script Should I Use?

**Quick Answer:** Use `start-dev.sh` (or `start-dev.bat` on Windows) for learning and testing!

---

## 🎯 Two Modes, Two Scripts

Testbook has two different deployment modes, each with its own start script:

### 1. Development Mode (For Learning) ✅ **← USE THIS**

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

### 2. Production Mode (For Deployment) ⚠️

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

## 📊 Side-by-Side Comparison

| Feature | Development Mode (`start-dev`) | Production Mode (`start`) |
|---------|-------------------------------|---------------------------|
| **Frontend Port** | 3000 | 8000 |
| **Backend Port** | 8000 | 8000 |
| **Docker Required** | No | Yes |
| **Hot Reload** | Yes | No |
| **Test Compatibility** | All tests work | Tests need modification |
| **Startup Time** | ~10 seconds | ~60 seconds |
| **Debugging** | Easy | Harder |
| **Use Case** | Learning, testing | Production deployment |

---

## 🎓 For Students

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

## 🏗️ How Development Mode Works

```
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

## 🐳 How Production Mode Works

```
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

## 🔧 Troubleshooting

### "I ran start-dev.sh but can't see the app"

**Check:**

1. Did you open `http://localhost:3000` (not 8000)?
2. Are both terminals running (backend and frontend)?
3. Any error messages in the terminals?

### "I want to switch from dev to production mode"

**Do this:**

1. Stop both terminals (Ctrl+C in each)
2. Run: `./start.sh` (with Docker running)
3. Open: `http://localhost:8000`
4. **Note:** Tests will need port changes!

### "Tests are failing after switching modes"

**Reason:** Tests expect development mode ports (3000 for frontend, 8000 for backend)

**Fix:** Switch back to development mode:

```bash
./start-dev.sh
```

---

## ✅ Verification Checklist

After starting in development mode, verify:

- [ ] Backend running at `http://localhost:8000/docs` (API docs load)
- [ ] Frontend running at `http://localhost:3000` (app loads)
- [ ] Can login with: `sarah.johnson@testbook.com` / `Sarah2024!`
- [ ] Can create a post
- [ ] Tests pass: `cd backend && pytest -v`

---

## 🎯 Quick Decision Tree

```
Are you learning/testing?
├─ YES → Use start-dev.sh ✅
└─ NO → Are you deploying to production?
    ├─ YES → Use start.sh with Docker
    └─ NO → You probably want start-dev.sh ✅
```

---

## 📚 Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - How to get started
- [docs/guides/RUNNING_TESTS.md](docs/guides/RUNNING_TESTS.md) - Running all tests
- [README.md](README.md) - Project overview

---

**🎓 Remember:** When in doubt, use development mode (`start-dev.sh`)!
