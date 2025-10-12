#!/bin/bash
set -e

echo "🚀 Setting up Testbook development environment..."

# Backend setup
echo "📦 Installing Python dependencies..."
cd /workspace/backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend setup
echo "📦 Installing Node dependencies..."
cd /workspace/frontend
npm install

cd /workspace/tests
npm install

# Database setup
echo "🗄️ Setting up database..."
cd /workspace/backend
python seed.py

echo "✅ Development environment ready!"
echo ""
echo "To start development:"
echo "  Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo "  Tests:    cd backend && pytest -v"

