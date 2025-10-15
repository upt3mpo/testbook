#!/bin/bash
set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔄 Resetting Testbook Database..."
echo ""

# Validation: Check if we're in the project root
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Must run from project root directory${NC}"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Validation: Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python not found${NC}"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD=$(command -v python3 &> /dev/null && echo "python3" || echo "python")

# Confirmation prompt for production-like environments
if [ -n "$DATABASE_URL" ] && [[ ! "$DATABASE_URL" =~ "test" ]]; then
    echo -e "${YELLOW}⚠️  Warning: DATABASE_URL is set and doesn't contain 'test'${NC}"
    echo -e "${YELLOW}   This might be a production database!${NC}"
    read -p "   Are you sure you want to reset? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
fi

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    # Backend is running - use API
    echo "📦 Resetting database via API..."

    # Check if TESTING mode is enabled
    health_response=$(curl -s http://localhost:8000/api/health)
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to connect to backend${NC}"
        exit 1
    fi

    # Attempt reset
    reset_response=$(curl -s -w "%{http_code}" -X POST http://localhost:8000/api/dev/reset)
    http_code="${reset_response: -3}"

    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Database reset successfully via API!${NC}"
    elif [ "$http_code" -eq 403 ]; then
        echo -e "${RED}❌ API reset failed: TESTING mode not enabled${NC}"
        echo "   Set environment variable: export TESTING=true"
        exit 1
    else
        echo -e "${RED}❌ API reset failed with HTTP code: $http_code${NC}"
        exit 1
    fi
else
    # Backend is not running - reset manually
    echo "📦 Backend not running. Resetting database manually..."

    # Backup existing database (optional)
    if [ -f "backend/testbook.db" ]; then
        backup_file="backend/testbook.db.backup.$(date +%Y%m%d_%H%M%S)"
        cp backend/testbook.db "$backup_file"
        echo "   📋 Backed up to: $backup_file"
        rm backend/testbook.db
        echo "   🗑️  Deleted old database"
    fi

    # Also clean test database
    if [ -f "backend/test_testbook.db" ]; then
        rm backend/test_testbook.db
        echo "   🗑️  Deleted test database"
    fi

    # Delete uploaded files (posts and avatars)
    if [ -d "backend/static/uploads" ]; then
        file_count=$(find backend/static/uploads -type f ! -name '.gitignore' ! -name '.gitkeep' | wc -l)
        find backend/static/uploads -type f ! -name '.gitignore' ! -name '.gitkeep' -delete 2>/dev/null
        echo "   🧹 Cleaned $file_count uploaded files"
    fi
    if [ -d "backend/static/uploads/avatars" ]; then
        find backend/static/uploads/avatars -type f ! -name '.gitignore' ! -name '.gitkeep' -delete 2>/dev/null
    fi

    # Run seed script
    cd backend

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        echo "   🐍 Activating virtual environment..."
        source .venv/bin/activate
    else
        echo -e "${YELLOW}   ⚠️  Virtual environment not found, using system Python${NC}"
    fi

    # Check if seed.py exists
    if [ ! -f "seed.py" ]; then
        echo -e "${RED}❌ Error: seed.py not found${NC}"
        exit 1
    fi

    # Run seeding
    echo "   🌱 Seeding database..."
    if $PYTHON_CMD seed.py; then
        echo -e "${GREEN}✅ Database reset successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to seed database${NC}"
        exit 1
    fi

    cd ..
fi

echo ""
echo "📊 Fresh test data loaded:"
echo "   - 9 test users"
echo "   - 21 sample posts"
echo "   - Comments, reactions, and relationships"
echo ""
echo "🔐 Test accounts ready:"
echo "   - sarah.johnson@testbook.com / Sarah2024!"
echo "   - mike.chen@testbook.com / MikeRocks88"
echo "   - emma.davis@testbook.com / EmmaLovesPhotos"
echo ""
echo "🎯 You can now test with a clean database!"
echo ""

