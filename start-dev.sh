#!/bin/bash
set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🚀 Starting Testbook in development mode..."
echo ""

# Validation: Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Must run from project root directory${NC}"
    echo "   Current directory: $(pwd)"
    echo "   Expected structure: backend/ and frontend/ subdirectories"
    exit 1
fi

# Check for required commands
for cmd in python3 node npm curl; do
    if ! command -v $cmd &> /dev/null; then
        echo -e "${RED}❌ Error: $cmd is not installed${NC}"
        exit 1
    fi
done

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Function to check if URL is responding
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=0

    echo "⏳ Waiting for $service_name to be ready..."

    while [ $attempt -lt $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done

    echo "❌ $service_name failed to start within 30 seconds"
    return 1
}

# Check if port is already in use
check_port() {
    local port=$1
    local service_name=$2

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}❌ Error: Port $port is already in use${NC}"
        echo "   This might be an existing $service_name instance, or something else entirely."
        echo "   Find it:  lsof -i :$port"
        echo "   Stop it:  lsof -ti:$port | xargs kill"
        return 1
    fi
    return 0
}

# Generate placeholder images if they don't exist
if [ ! -f "backend/static/images/default-avatar.jpg" ]; then
    echo "📸 Generating placeholder images..."
    python3 setup_images.py
    echo ""
fi

# Check both ports before starting anything. Continuing past a port conflict
# used to just print a warning and proceed - but uvicorn/vite then either
# crash outright or (for vite) silently pick a different port, while the
# readiness check below still reports success because it only polls the
# URL, not whether *this run's* process is the one answering it. The result
# was a "Testbook is running!" banner while the backend that's supposed to
# reload your code changes was actually dead. Exiting here means the error
# is the first and only thing you see, not the first of several confusing
# ones.
PORT_CONFLICT=false
check_port 8000 "backend" || PORT_CONFLICT=true
check_port 3000 "frontend" || PORT_CONFLICT=true
if [ "$PORT_CONFLICT" = true ]; then
    exit 1
fi

# Start backend
echo "🔧 Setting up backend..."
cd backend

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Check if dependencies need installation (idempotent check)
NEEDS_INSTALL=false
if [ ! -f ".venv/lib/python*/site-packages/fastapi/__init__.py" ] && \
   [ ! -f ".venv/lib/python3.*/site-packages/fastapi/__init__.py" ]; then
    NEEDS_INSTALL=true
fi

if [ "$NEEDS_INSTALL" = true ]; then
    # Use uv if available, otherwise fall back to pip
    if command -v uv &> /dev/null; then
        echo "📦 Installing backend dependencies with uv (fast!)..."
        uv pip install -r requirements.txt
    else
        echo "📦 Installing backend dependencies with pip..."
        pip install -q -r requirements.txt
    fi
else
    echo "✓ Backend dependencies already installed"
fi

# Seed database
echo "🌱 Seeding database..."
python3 seed.py

# Start backend
echo "🚀 Starting backend server on port 8000..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be healthy
if ! wait_for_service "http://localhost:8000/docs" "Backend"; then
    echo "❌ Backend failed to start. Check the logs above for errors."
    cleanup
fi

cd ..

# Start frontend
echo ""
echo "⚛️  Setting up frontend..."
cd frontend

# Check if node_modules exists and is not empty (idempotent check)
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
else
    echo "✓ Frontend dependencies already installed"
fi

# Start frontend
echo "🚀 Starting frontend server on port 3000..."
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to be healthy
if ! wait_for_service "http://localhost:3000" "Frontend"; then
    echo "❌ Frontend failed to start. Check the logs above for errors."
    cleanup
fi

cd ..

echo ""
echo "=========================================="
echo "✅ Testbook is running in development mode!"
echo "=========================================="
echo ""
echo "📱 Frontend:    http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000/api"
echo "📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "Test accounts:"
echo "  • sarah.johnson@testbook.com / Sarah2024!"
echo "  • mike.chen@testbook.com / MikeRocks88"
echo ""
echo "🎯 What to do now:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Login with: sarah.johnson@testbook.com / Sarah2024!"
echo "  3. Explore the app for 5 minutes"
echo "  4. Then start learning: ./docs/INDEX.md#learning-path"
echo ""
echo "Ready to start? → learn/README.md"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="
echo ""

# Wait for processes
wait
