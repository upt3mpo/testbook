@echo off
echo.
echo 🚀 Starting Testbook...
echo.

REM Check if Docker is installed
where docker >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    echo.
    echo Download Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Check if docker-compose is available
where docker-compose >nul 2>&1
if errorlevel 1 (
    echo ⚠️  docker-compose not found, trying 'docker compose' instead...
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)

REM Generate placeholder images if they don't exist
if not exist "backend\static\images\default-avatar.jpg" (
    echo 📸 Generating placeholder images...
    python setup_images.py
    echo.
)

REM docker-compose.yml bind-mounts backend\testbook.db into the container so
REM data survives a restart. On a fresh clone that file doesn't exist yet -
REM and Docker's behavior for a missing bind-mount *file* source is to
REM create an empty *directory* there instead, which then makes the app
REM crash trying to open a directory as a SQLite database. Creating the
REM file first avoids that; the app's own startup seeds it if it's empty.
if not exist "backend\testbook.db" (
    echo 🗄️  Creating database file...
    type nul > backend\testbook.db
    echo.
)

REM Build and start containers
echo 🔨 Building Docker containers...
%COMPOSE_CMD% up --build -d

echo.
echo ✅ Testbook is starting!
echo.
echo 📱 Frontend: http://localhost:8000
echo 🔌 Backend API: http://localhost:8000/api
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 🔐 Test accounts:
echo   - sarah.johnson@testbook.com / Sarah2024!
echo   - mike.chen@testbook.com / MikeRocks88
echo   - emma.davis@testbook.com / EmmaLovesPhotos
echo.
echo 🛑 To stop: docker-compose down
echo 📋 View logs: docker-compose logs -f
echo.
pause
