# PowerShell script to reset Testbook database

Write-Host ""
Write-Host "🔄 Resetting Testbook Database..." -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -ErrorAction Stop -TimeoutSec 2
    $backendRunning = $true
} catch {
    $backendRunning = $false
}

if ($backendRunning) {
    # Backend is running - use API
    Write-Host "📦 Resetting database via API..."
    try {
        $resetResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/dev/reset" -Method POST -UseBasicParsing -ErrorAction Stop
        Write-Host "✅ Database reset successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to reset database via API" -ForegroundColor Red
        exit 1
    }
} else {
    # Backend is not running - reset manually
    Write-Host "📦 Backend not running. Resetting database manually..."

    # Delete database file
    if (Test-Path "backend\testbook.db") {
        Remove-Item "backend\testbook.db" -Force
        Write-Host "   Deleted old database"
    }

    # Delete uploaded files (posts and avatars)
    if (Test-Path "backend\static\uploads") {
        Get-ChildItem "backend\static\uploads" -File | Where-Object {
            $_.Name -ne ".gitignore" -and $_.Name -ne ".gitkeep"
        } | Remove-Item -Force
        Write-Host "   Cleaned uploaded files"
    }
    if (Test-Path "backend\static\uploads\avatars") {
        Get-ChildItem "backend\static\uploads\avatars" -File | Where-Object {
            $_.Name -ne ".gitignore" -and $_.Name -ne ".gitkeep"
        } | Remove-Item -Force
    }

    # Run seed script
    Push-Location backend
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
    }
    python seed.py
    Pop-Location

    Write-Host "✅ Database reset successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "📊 Fresh test data loaded:"
Write-Host "   - 9 test users"
Write-Host "   - 21 sample posts"
Write-Host "   - Comments, reactions, and relationships"
Write-Host ""
Write-Host "🔐 Test accounts ready:"
Write-Host "   - sarah.johnson@testbook.com / Sarah2024!"
Write-Host "   - mike.chen@testbook.com / MikeRocks88"
Write-Host "   - emma.davis@testbook.com / EmmaLovesPhotos"
Write-Host ""
Write-Host "🎯 You can now test with a clean database!" -ForegroundColor Green
Write-Host ""

