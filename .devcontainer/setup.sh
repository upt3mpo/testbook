#!/bin/bash
# Dev Container Setup Script
# Runs automatically when container is created

echo "🚀 Setting up Testbook Testing Platform..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd /workspaces/Testbook/backend
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd /workspaces/Testbook/frontend
npm install

# Install test dependencies
echo "📦 Installing test dependencies..."
cd /workspaces/Testbook/tests
npm install

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
npx playwright install chromium

# Install E2E Python dependencies
echo "📦 Installing E2E Python dependencies..."
cd /workspaces/Testbook/tests/e2e-python
pip install -r requirements.txt
npx playwright install chromium

# Seed database
echo "🌱 Seeding database..."
cd /workspaces/Testbook/backend
python seed.py

echo "✅ Setup complete!"
echo ""
echo "🎯 Quick Start:"
echo "  1. Start backend: cd backend && uvicorn main:app --reload"
echo "  2. Start frontend: cd frontend && npm run dev"
echo "  3. Run tests: cd backend && pytest -v"
echo ""
echo "📚 Documentation:"
echo "  - START_HERE.md - Choose your learning path"
echo "  - FAQ.md - Troubleshooting"
echo "  - labs/LAB_01_Your_First_Test.md - Begin learning"
echo ""
echo "🎉 Ready to learn automation testing!"

