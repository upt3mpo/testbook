#!/bin/bash
set -e

echo "🚀 Setting up Testbook development environment..."

# Backend setup
echo "📦 Installing Python dependencies..."
cd /workspace/backend
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend setup
echo "📦 Installing Node dependencies..."
cd /workspace/frontend
npm install

# Test dependencies
echo "📦 Installing test dependencies..."
cd /workspace/tests
npm install

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
npx playwright install chromium

# E2E Python dependencies
if [ -f "/workspace/tests/e2e-python/requirements.txt" ]; then
    echo "📦 Installing E2E Python dependencies..."
    cd /workspace/tests/e2e-python
    pip install -r requirements.txt
fi

# Database setup
echo "🗄️ Setting up database..."
cd /workspace/backend
python seed.py

# Generate placeholder images
echo "🖼️ Generating placeholder images..."
cd /workspace
python setup_images.py

echo ""
echo "✅ Development environment ready!"
echo ""
echo "🎯 To start development:"
echo "  Backend:  cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0"
echo "  Frontend: cd frontend && npm run dev -- --host 0.0.0.0"
echo "  Tests:    cd backend && pytest -v"
echo ""
echo "📚 Begin learning:"
echo "  - Open START_HERE.md to choose your learning path"
echo "  - Check labs/LAB_01_Your_First_Test.md to begin"
