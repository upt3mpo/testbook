#!/bin/bash

echo "🚀 Starting Testbook..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Generate placeholder images if they don't exist
if [ ! -f "backend/static/images/default-avatar.jpg" ]; then
    echo "📸 Generating placeholder images..."
    python3 setup_images.py
    echo ""
fi

# Build and start containers
echo "🔨 Building Docker containers..."
docker-compose up --build -d

echo ""
echo "✅ Testbook is starting!"
echo ""
echo "📱 Frontend: http://localhost:8000"
echo "🔌 Backend API: http://localhost:8000/api"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Test accounts:"
echo "  - sarah.johnson@testbook.com / Sarah2024!"
echo "  - mike.chen@testbook.com / MikeRocks88"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
