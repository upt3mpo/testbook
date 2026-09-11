@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 Starting Testbook in development mode...
echo.

REM Check if ports are already in use. This used to warn and continue, but
REM that let uvicorn/vite crash or silently switch ports while the
REM readiness check below still reported success (it only polls the URL,
REM not whether this run's own process is the one answering it) - so you'd
REM see "Testbook is running!" while the backend that's supposed to reload
REM your code changes was actually dead. Exiting here means you see the
REM real problem once, immediately, instead of a misleading success banner.
echo ⏳ Checking if ports are available...
set PORT_CONFLICT=0

netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo ❌ Error: Port 8000 is already in use
    echo    This might be an existing backend instance, or something else entirely.
    echo    Find it: netstat -ano ^| findstr :8000
    echo    Stop it: taskkill /PID ^<pid^> /F
    echo.
    set PORT_CONFLICT=1
)

netstat -ano | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo ❌ Error: Port 3000 is already in use
    echo    This might be an existing frontend instance, or something else entirely.
    echo    Find it: netstat -ano ^| findstr :3000
    echo    Stop it: taskkill /PID ^<pid^> /F
    echo.
    set PORT_CONFLICT=1
)

if "%PORT_CONFLICT%"=="1" (
    echo Startup stopped - free the port^(s^) above and try again.
    pause
    exit /b 1
)

REM Generate placeholder images if they don't exist
if not exist "backend\static\images\default-avatar.jpg" (
    echo 📸 Generating placeholder images...
    python setup_images.py
    echo.
)

REM Backend setup
echo 🔧 Setting up backend...
cd backend

REM Create venv if it doesn't exist
if not exist ".venv\Scripts\activate.bat" (
    echo 📦 Creating Python virtual environment...
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Check if dependencies need installation (idempotent check)
if not exist ".venv\Lib\site-packages\fastapi\__init__.py" (
    REM Check for uv
    where uv >nul 2>&1
    if not errorlevel 1 (
        echo 📦 Installing backend dependencies with uv ^(fast!^)...
        call uv pip install -r requirements.txt
    ) else (
        echo 📦 Installing backend dependencies with pip...
        pip install -q -r requirements.txt
    )
) else (
    echo ✓ Backend dependencies already installed
)

REM Seed database
echo 🌱 Seeding database...
python seed.py

REM Start backend
echo 🚀 Starting backend server on port 8000...
start /B python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM Wait for backend to be healthy
echo ⏳ Waiting for backend to be ready...
set /a attempts=0
:wait_backend
set /a attempts+=1
if %attempts% GTR 30 (
    echo ❌ Backend failed to start within 30 seconds
    echo    Check for errors above
    goto :error_exit
)

curl -s -f http://localhost:8000/docs >nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto :wait_backend
)
echo ✅ Backend is ready!

cd ..

REM Frontend setup
echo.
echo ⚛️  Setting up frontend...
cd frontend

REM Check if node_modules exists (idempotent check)
if not exist "node_modules\" (
    echo 📦 Installing frontend dependencies...
    call npm install
) else (
    echo ✓ Frontend dependencies already installed
)

REM Start frontend
echo 🚀 Starting frontend server on port 3000...
start /B npm run dev

REM Wait for frontend to be healthy
echo ⏳ Waiting for frontend to be ready...
set /a attempts=0
:wait_frontend
set /a attempts+=1
if %attempts% GTR 30 (
    echo ❌ Frontend failed to start within 30 seconds
    echo    Check for errors above
    goto :error_exit
)

curl -s -f http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto :wait_frontend
)
echo ✅ Frontend is ready!

cd ..

echo.
echo ==========================================
echo ✅ Testbook is running in development mode!
echo ==========================================
echo.
echo 📱 Frontend:    http://localhost:3000
echo 🔌 Backend API: http://localhost:8000/api
echo 📚 API Docs:    http://localhost:8000/docs
echo.
echo Test accounts:
echo   • sarah.johnson@testbook.com / Sarah2024!
echo   • mike.chen@testbook.com / MikeRocks88
echo.
echo 🎯 What to do now:
echo   1. Open http://localhost:3000 in your browser
echo   2. Login with: sarah.johnson@testbook.com / Sarah2024!
echo   3. Explore the app for 5 minutes
echo   4. Then start learning: docs\INDEX.md#learning-path
echo.
echo Ready to start? → learn\README.md
echo.
echo Press Ctrl+C to stop all services
echo ==========================================
echo.

pause
goto :eof

:error_exit
echo.
echo ❌ Startup failed. Please check the errors above.
cd ..
pause
exit /b 1
