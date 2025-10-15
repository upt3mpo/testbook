# Windows Setup Guide

This guide helps Windows users set up and run Testbook. There are three approaches you can use:

---

## 🪟 PowerShell vs Command Prompt

Throughout this guide, we provide commands for both shells:

**PowerShell (Recommended):**

- ✅ Default on Windows 10/11
- ✅ Modern, powerful scripting
- ✅ Better environment variable handling (`$env:VAR="value"`)
- ✅ More consistent with cross-platform workflows

**Command Prompt (Alternative):**

- ✅ Works in corporate environments where PowerShell is restricted
- ✅ Simpler for basic commands
- ✅ Compatible with older Windows systems
- ⚠️ More verbose for environment variables (`set VAR=value`)

💡 **Tip:** If unsure, use PowerShell - it's installed by default and more powerful.

---

## Option 1: Native Windows (Recommended for Beginners)

**Best for:** Windows users who prefer native tools and don't want to install WSL.

### Requirements

- Windows 10/11
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- Git for Windows ([Download](https://git-scm.com/download/win))

### Setup Steps

1. **Clone the repository:**

   ```bat
   git clone https://github.com/upt3mpo/testbook.git
   cd testbook
   ```

2. **Run the start script:**

   ```bat
   start-dev.bat
   ```

The script will:

- ✅ Check if ports 8000 and 3000 are available
- ✅ Create Python virtual environment (if needed)
- ✅ Install dependencies only if not already present (idempotent)
- ✅ Health check both services before reporting success
- ✅ Provide clear error messages if startup fails

### Troubleshooting

**Problem:** `curl` command not found during health checks
**Solution:** Install curl via Windows:

```bat
winget install curl
```

Or download from: <https://curl.se/windows/>

**Problem:** Port already in use
**Solution:** Find and kill the process:

```bat
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Problem:** Python not found
**Solution:** Ensure Python is in your PATH. Reinstall Python and check "Add to PATH" during installation.

---

## Option 2: WSL (Windows Subsystem for Linux)

**Best for:** Developers comfortable with Linux, or those who want full bash script compatibility.

### Why WSL?

- ✅ Native Linux environment on Windows
- ✅ Better compatibility with shell scripts
- ✅ Same experience as macOS/Linux users
- ✅ Access to Linux tools and packages

### Requirements

- Windows 10 version 2004+ or Windows 11
- WSL 2 installed

### Setup Steps

1. **Install WSL 2 (if not already installed):**

   ```powershell
   # Run in PowerShell as Administrator
   wsl --install
   ```

   Restart your computer when prompted.

2. **Install Ubuntu (or your preferred distro):**

   ```powershell
   wsl --install -d Ubuntu
   ```

3. **Open Ubuntu terminal and install dependencies:**

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv nodejs npm git curl
   ```

4. **Clone and run Testbook:**

   ```bash
   git clone https://github.com/upt3mpo/testbook.git
   cd testbook
   chmod +x start-dev.sh
   ./start-dev.sh
   ```

### Accessing from Windows

- Frontend: <http://localhost:3000>
- Backend: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>

WSL 2 automatically forwards ports to Windows, so you can access the app from your Windows browser!

### WSL Tips

**Edit files from Windows:**

- Your WSL files are accessible at: `\\wsl$\Ubuntu\home\<username>\`
- You can use VS Code with the "Remote - WSL" extension

**Performance:**

- Store project files in WSL filesystem (not `/mnt/c/...`) for best performance
- Use `code .` in WSL terminal to open VS Code with WSL integration

**Troubleshooting:**

```bash
# Check WSL version
wsl --list --verbose

# Restart WSL
wsl --shutdown

# Update WSL
wsl --update
```

---

## Option 3: Docker (Cross-Platform)

**Best for:** Production-like environment, or when you want complete isolation.

### Requirements

- Docker Desktop for Windows ([Download](https://www.docker.com/products/docker-desktop))

### Setup Steps

1. **Start Docker Desktop**

2. **Run Testbook:**

   ```bat
   docker-compose up
   ```

3. **Access the app:**
   - Frontend: <http://localhost:80>
   - Backend: <http://localhost:80/api>

**Note:** Docker mode runs in production configuration with different ports than dev mode.

---

## Comparison Table

| Feature | Native Windows | WSL | Docker |
|---------|---------------|-----|--------|
| **Setup Time** | 5-10 minutes | 15-20 minutes | 10-15 minutes |
| **Learning Curve** | Low | Medium | Medium |
| **Performance** | Fast | Fast | Moderate |
| **Port Forwarding** | Direct | Automatic | Configured |
| **Best For** | Beginners | Linux enthusiasts | Production testing |
| **Auto-reload** | ✅ Yes | ✅ Yes | ❌ No |

---

## Development Workflow

### Native Windows or WSL

**Start the app:**

```bat
# Windows
start-dev.bat

# WSL
./start-dev.sh
```

**Stop the app:**

- Press `Ctrl+C` in the terminal

**Reset database:**

```bat
# Windows
reset-database.bat

# WSL
./reset-database.sh
```

**Run tests:**

```bat
# Windows
cd backend
.venv\Scripts\activate
pytest -v

# WSL
cd backend
source .venv/bin/activate
pytest -v
```

---

## Common Issues (All Platforms)

### Port Conflicts

**Symptom:** "Port 8000/3000 is already in use"

**Solution:**

```bat
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# WSL
lsof -ti:8000 | xargs kill
```

### Virtual Environment Issues

**Symptom:** "pip not found" or "module not found"

**Solution:**
Ensure virtual environment is activated:

```bat
# Windows
cd backend
.venv\Scripts\activate

# WSL
cd backend
source .venv/bin/activate
```

### Node Modules Issues

**Symptom:** "Cannot find module..."

**Solution:**
Delete and reinstall:

```bat
cd frontend
rmdir /s /q node_modules  # Windows
rm -rf node_modules       # WSL
npm install
```

---

## IDE Recommendations

### Visual Studio Code (Recommended)

**Extensions:**

- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- Remote - WSL (if using WSL)

**Setup:**

```bat
# Windows
code .

# WSL
code .  # Automatically opens with WSL integration
```

### PyCharm

Works great with native Windows or WSL. Configure interpreters:

- File → Settings → Project → Python Interpreter
- Select the `venv/bin/python` (WSL) or `venv\Scripts\python.exe` (Windows)

---

## Getting Help

**Script not working?**

1. Check you're in the project root directory
2. Verify Python and Node are installed: `python --version` and `node --version`
3. Look at the error messages - the scripts now provide detailed feedback
4. See [FAQ.md](../../FAQ.md) for common issues

**Still stuck?**

- Check [RUNNING_TESTS.md](./RUNNING_TESTS.md)
- Review [START_HERE.md](../../START_HERE.md)
- Ask in the course discussion forum

---

## Next Steps

Once your environment is running:

1. **Verify setup:** Open <http://localhost:3000> and log in
2. **Start learning:** Follow [START_HERE.md](../../START_HERE.md)
3. **Run your first test:** Complete [Lab 1](../../labs/LAB_01_Your_First_Test.md)

**Happy testing!** 🚀
