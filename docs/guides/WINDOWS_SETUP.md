# Windows Setup Guide

This guide helps Windows users set up and run Testbook from scratch, even if you have no development environment installed.

There are three approaches you can use:

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

### Complete Prerequisites Checklist

Before starting, you need to install these tools:

#### 1. Python 3.11+ (Required)

**Download:** [python.org/downloads](https://www.python.org/downloads/)

**Installation Steps:**
1. Download Python 3.11+ for Windows
2. **CRITICAL:** Check "Add Python to PATH" during installation
3. Choose "Install for all users" if prompted
4. Verify installation:

```powershell
python --version
# Should show: Python 3.11.x or higher
```

**If Python not found:**
- Reinstall Python and check "Add to PATH"
- Or manually add Python to PATH:
  - Windows Settings → System → About → Advanced system settings
  - Environment Variables → System Variables → Path → Edit
  - Add: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\`
  - Add: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\Scripts\`

#### 2. Node.js 18+ and npm (Required)

**Download:** [nodejs.org](https://nodejs.org/) (choose LTS version)

**Installation Steps:**
1. Download Node.js LTS for Windows
2. Run installer with default settings
3. Verify installation:

```powershell
node --version
npm --version
# Should show: Node v18.x.x+ and npm 9.x.x+
```

**If npm not found:**
- Node.js includes npm automatically
- If still missing, reinstall Node.js
- Check PATH: `C:\Program Files\nodejs\`

#### 3. Git for Windows (Required)

**Download:** [git-scm.com/download/win](https://git-scm.com/download/win)

**Installation Steps:**
1. Download Git for Windows
2. Use default installation settings
3. Choose "Git from the command line and also from 3rd-party software"
4. Verify installation:

```powershell
git --version
# Should show: git version 2.x.x.windows.x
```

#### 4. curl (Optional but Recommended)

**For health checks and API testing:**

```powershell
# Install via Windows Package Manager (winget)
winget install curl

# Or download from: https://curl.se/windows/
```

**Verify:**
```powershell
curl --version
```

#### 5. Code Editor (Recommended)

**Visual Studio Code:** [code.visualstudio.com](https://code.visualstudio.com/)

**Essential Extensions:**
- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- GitLens

### Verification Commands

Run these commands to verify your setup:

```powershell
# Check all prerequisites
python --version
node --version
npm --version
git --version
curl --version

# All should return version numbers without errors
```

### Setup Steps

1. **Clone the repository:**

   ```powershell
   git clone https://github.com/upt3mpo/testbook.git
   cd testbook
   ```

2. **Run the start script:**

   ```powershell
   .\start-dev.bat
   ```

The script will:

- ✅ Check if ports 8000 and 3000 are available
- ✅ Create Python virtual environment (if needed)
- ✅ Install dependencies only if not already present (idempotent)
- ✅ Health check both services before reporting success
- ✅ Provide clear error messages if startup fails

### Common Issues and Solutions

#### Issue 1: "Python not found" or "python is not recognized"

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Reinstall Python with PATH:** Download from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH"
2. **Manual PATH setup:**
   - Windows Settings → System → About → Advanced system settings
   - Environment Variables → System Variables → Path → Edit
   - Add: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\`
   - Add: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\Scripts\`
3. **Restart terminal** after PATH changes

#### Issue 2: "npm is not recognized" or "node is not recognized"

**Symptoms:**
```
'npm' is not recognized as an internal or external command
'node' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Node.js:** Download from [nodejs.org](https://nodejs.org/) (LTS version)
2. **Check installation:** `node --version` and `npm --version`
3. **Reinstall if needed:** Node.js includes npm automatically
4. **Check PATH:** `C:\Program Files\nodejs\`

#### Issue 3: "git is not recognized"

**Symptoms:**
```
'git' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Git:** Download from [git-scm.com/download/win](https://git-scm.com/download/win)
2. **Choose "Git from the command line"** during installation
3. **Restart terminal** after installation

#### Issue 4: "curl is not recognized"

**Symptoms:**
```
'curl' is not recognized as an internal or external command
```

**Solutions:**
```powershell
# Install via Windows Package Manager
winget install curl

# Or download from: https://curl.se/windows/
```

#### Issue 5: Port already in use

**Symptoms:**
```
Port 8000 is already in use by another process
Port 3000 is already in use by another process
```

**Solutions:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual number)
taskkill /PID <PID> /F

# Or kill all processes on port 8000
netstat -ano | findstr :8000 | ForEach-Object { $pid = ($_ -split '\s+')[-1]; taskkill /PID $pid /F }
```

#### Issue 6: Database connection errors

**Symptoms:**
```
sqlite3.OperationalError: unable to open database file
```

**Solutions:**
1. **Delete existing database directory:** The script will recreate it as a file
2. **Check file permissions:** Ensure the backend directory is writable
3. **Run as administrator** if needed (though not recommended)

#### Issue 7: Permission denied errors

**Symptoms:**
```
Permission denied
Access is denied
```

**Solutions:**
1. **Run PowerShell as Administrator** (temporarily)
2. **Check antivirus software** - it might be blocking file operations
3. **Add project folder to antivirus exclusions**
4. **Use WSL** as alternative (see Option 2 below)

#### Issue 8: Script execution policy errors

**Symptoms:**
```
execution of scripts is disabled on this system
```

**Solutions:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (temporary)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run batch file directly
.\start-dev.bat
```

#### Issue 9: PowerShell profile helper (Optional Enhancement)

**Want a faster way to activate the virtual environment?**

Create a custom PowerShell command called `testbook` that automatically activates your Testbook virtual environment:

```powershell
# Create PowerShell profile (one-time setup)
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }

# Add Testbook helper to your profile
Add-Content -Path $PROFILE -Value @'
# Testbook Development Helper
function Activate-Testbook {
    if (Test-Path "D:\Projects\testbook\backend\.venv\Scripts\Activate.ps1") {
        & "D:\Projects\testbook\backend\.venv\Scripts\Activate.ps1"
        Write-Host "Testbook backend virtual environment activated!" -ForegroundColor Green
    } else {
        Write-Host "Virtual environment not found. Run start-dev.bat first." -ForegroundColor Red
    }
}

Set-Alias -Name testbook -Value Activate-Testbook
Write-Host "Testbook helper loaded. Type `"testbook`" to activate the virtual environment." -ForegroundColor Cyan
'@
```

**After setup, restart PowerShell and you can simply type:**
```powershell
testbook
```

**Benefits:**
- ✅ No more execution policy issues
- ✅ One command to activate virtual environment
- ✅ Works in any PowerShell window
- ✅ Clear visual feedback

**Note:** Adjust the path `"D:\Projects\testbook\backend\.venv\Scripts\Activate.ps1"` to match your actual project location.

### Advanced Troubleshooting

#### Check System Requirements

```powershell
# Check Windows version (need 10/11)
winver

# Check available disk space (need ~2GB)
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace/1GB,2)}}

# Check available memory
Get-WmiObject -Class Win32_ComputerSystem | Select-Object TotalPhysicalMemory
```

#### Environment Variables Check

```powershell
# Check PATH environment variable
$env:PATH -split ';' | Where-Object { $_ -match '(python|node|git)' }

# Check specific program locations
where python
where node
where npm
where git
```

#### Network and Firewall Issues

If the app starts but you can't access it in browser:

1. **Check Windows Firewall:** Allow Python and Node.js through firewall
2. **Check antivirus:** Temporarily disable to test
3. **Try different ports:** Modify `start-dev.bat` to use different ports
4. **Use localhost instead of 0.0.0.0:** Change `--host 0.0.0.0` to `--host localhost`

---

## Option 2: WSL (Windows Subsystem for Linux) ⭐ Recommended for Developers

**Best for:** Developers comfortable with Linux, or those who want full bash script compatibility and better performance.

### Why WSL?

- ✅ Native Linux environment on Windows
- ✅ Better compatibility with shell scripts
- ✅ Same experience as macOS/Linux users
- ✅ Access to Linux tools and packages
- ✅ Better performance for development tools
- ✅ Avoids Windows-specific issues
- ✅ Perfect for learning cross-platform development

### Requirements

- Windows 10 version 2004+ or Windows 11
- At least 4GB RAM (8GB+ recommended)
- At least 1GB free disk space

### Complete WSL Setup

#### Step 1: Enable WSL Feature

```powershell
# Run PowerShell as Administrator
# Enable WSL feature
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer when prompted
```

#### Step 2: Install WSL 2

```powershell
# After restart, run as Administrator
wsl --install
```

This will:
- Install WSL 2
- Download and install Ubuntu (default distro)
- Set WSL 2 as default

#### Step 3: Set up Ubuntu

1. **Launch Ubuntu** from Start Menu or run `wsl`
2. **Create user account** when prompted
3. **Update system:**

```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 4: Install Development Tools

```bash
# Install all required tools
sudo apt install -y python3 python3-pip python3-venv nodejs npm git curl build-essential

# Verify installations
python3 --version    # Should show Python 3.8+
node --version       # Should show Node.js 18+
npm --version        # Should show npm 9+
git --version        # Should show Git 2.x+
curl --version       # Should show curl 7.x+
```

#### Step 5: Install Testbook

```bash
# Clone repository
git clone https://github.com/upt3mpo/testbook.git
cd testbook

# Make script executable
chmod +x start-dev.sh

# Run the application
./start-dev.sh
```

### Accessing from Windows

- Frontend: <http://localhost:3000>
- Backend: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>

WSL 2 automatically forwards ports to Windows, so you can access the app from your Windows browser!

### WSL Development Tips

#### VS Code Integration (Highly Recommended)

```bash
# Install VS Code Remote - WSL extension
# Then from WSL terminal:
code .
```

This opens VS Code with full WSL integration:
- Terminal runs in WSL
- Extensions work in WSL context
- File operations are WSL-native
- IntelliSense works with WSL Python/Node

#### File Management

**Best Practice:** Keep files in WSL filesystem for performance

```bash
# Good: Store in WSL home directory
cd ~
git clone https://github.com/upt3mpo/testbook.git

# Avoid: Working in Windows filesystem from WSL
cd /mnt/c/Users/...  # Slower performance
```

**Access WSL files from Windows:**
- File Explorer: `\\wsl$\Ubuntu\home\<username>\`
- VS Code: `\\wsl$\Ubuntu\home\<username>\testbook`

#### Performance Optimization

```bash
# Create .wslconfig file in Windows user directory
# C:\Users\<username>\.wslconfig
[wsl2]
memory=8GB          # Adjust based on your RAM
processors=4        # Adjust based on your CPU cores
swap=2GB           # Optional: set swap size
```

#### WSL Troubleshooting

```bash
# Check WSL version and status
wsl --list --verbose

# Restart WSL if issues occur
wsl --shutdown
wsl

# Update WSL
wsl --update

# Check Ubuntu version
lsb_release -a

# Check available disk space
df -h

# Check memory usage
free -h
```

#### Common WSL Issues

**Issue:** "WSL 2 requires an update"

```powershell
# Download and install WSL 2 Linux kernel update
# From: https://aka.ms/wsl2kernel
```

**Issue:** "Virtual Machine Platform not enabled"

```powershell
# Enable in Windows Features
# Control Panel → Programs → Turn Windows features on or off
# Check: Virtual Machine Platform
```

**Issue:** Slow file operations

```bash
# Keep files in WSL filesystem, not /mnt/c/
# Use VS Code Remote - WSL extension
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

## Quick Start Comparison

### 🚀 Fastest Setup (Choose One)

#### Option A: Native Windows (5 minutes)
```powershell
# Prerequisites: Python 3.11+, Node.js 18+, Git
git clone https://github.com/upt3mpo/testbook.git
cd testbook
.\start-dev.bat
```

#### Option B: WSL (10 minutes)
```powershell
# One-time setup
wsl --install
# After restart:
wsl
sudo apt update && sudo apt install -y python3 python3-pip python3-venv nodejs npm git
git clone https://github.com/upt3mpo/testbook.git
cd testbook
chmod +x start-dev.sh
./start-dev.sh
```

#### Option C: Docker (5 minutes)
```powershell
# Prerequisites: Docker Desktop
git clone https://github.com/upt3mpo/testbook.git
cd testbook
docker-compose up
```

### Detailed Comparison Table

| Feature | Native Windows | WSL | Docker |
|---------|---------------|-----|--------|
| **Setup Time** | 5-10 minutes | 15-20 minutes | 10-15 minutes |
| **Learning Curve** | Low | Medium | Medium |
| **Performance** | Fast | Fast | Moderate |
| **Port Forwarding** | Direct | Automatic | Configured |
| **Best For** | Beginners | Developers | Production testing |
| **Auto-reload** | ✅ Yes | ✅ Yes | ❌ No |
| **File Permissions** | Windows | Linux | Container |
| **Package Management** | pip/npm | apt/pip/npm | Container |
| **IDE Integration** | Good | Excellent | Limited |
| **Cross-platform** | ❌ No | ✅ Yes | ✅ Yes |
| **Resource Usage** | Low | Medium | High |
| **Troubleshooting** | Windows-specific | Linux | Container logs |

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

## Recommendations by User Type

### 🎯 New to Programming/Testing
**Choose:** Native Windows
- Easiest setup
- Familiar Windows environment
- Good for learning basics

### 💻 Experienced Developer
**Choose:** WSL
- Better development experience
- Cross-platform compatibility
- Access to Linux tools
- VS Code Remote - WSL integration

### 🏢 Corporate Environment
**Choose:** Native Windows or WSL
- Check with IT for WSL policies
- May need admin rights for WSL setup
- Docker might be restricted

### 🐳 DevOps/Container Focused
**Choose:** Docker
- Production-like environment
- Container orchestration learning
- CI/CD pipeline practice

## Verification Checklist

After setup, verify everything works:

### ✅ Basic Functionality
- [ ] App loads at **<http://localhost:3000>** (development mode)
- [ ] Can login with test account: `sarah.johnson@testbook.com` / `Sarah2024!`
- [ ] Can create a post
- [ ] Can view other users' posts

### ✅ Backend Testing
- [ ] Backend tests run: `cd backend && pytest -v`
- [ ] See 166+ tests pass
- [ ] No database errors

### ✅ Frontend Testing
- [ ] Frontend tests run: `cd frontend && npm test`
- [ ] All tests pass
- [ ] No console errors in browser

### ✅ E2E Testing (Optional)
- [ ] E2E tests run: `cd tests && npm test`
- [ ] Browser opens and tests execute

## Next Steps

Once your environment is running:

1. **Verify setup:** Complete the checklist above
2. **Start learning:** Follow [START_HERE.md](../../START_HERE.md)
3. **Run your first test:** Complete [Lab 1](../../labs/LAB_01_Your_First_Test.md)
4. **Explore the codebase:** Check out [docs/INDEX.md](../../docs/INDEX.md)

## Getting Help

**Script not working?**
1. Check you're in the project root directory
2. Verify all prerequisites are installed (see verification commands above)
3. Look at the error messages - the scripts provide detailed feedback
4. Try the troubleshooting sections above

**Still stuck?**
- Check [FAQ.md](../../FAQ.md) for common issues
- Review [RUNNING_TESTS.md](./RUNNING_TESTS.md)
- Try WSL if Native Windows has issues
- Ask in the course discussion forum

**Happy testing!** 🚀
