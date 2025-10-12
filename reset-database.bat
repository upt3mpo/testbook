@echo off
echo.
echo 🔄 Resetting Testbook Database...
echo.

REM Check if backend is running
curl -s http://localhost:8000/api/health >nul 2>&1
if not errorlevel 1 (
    REM Backend is running - use API
    echo 📦 Resetting database via API...
    curl -s -X POST http://localhost:8000/api/dev/reset >nul

    if not errorlevel 1 (
        echo ✅ Database reset successfully!
    ) else (
        echo ❌ Failed to reset database via API
        exit /b 1
    )
) else (
    REM Backend is not running - reset manually
    echo 📦 Backend not running. Resetting database manually...

    REM Delete database file
    if exist "backend\testbook.db" (
        del /Q "backend\testbook.db"
        echo    Deleted old database
    )

    REM Delete uploaded files (posts)
    if exist "backend\static\uploads\*.*" (
        for %%F in (backend\static\uploads\*.*) do (
            if not "%%~nxF"==".gitignore" if not "%%~nxF"==".gitkeep" (
                del /Q "%%F"
            )
        )
        echo    Cleaned uploaded files
    )

    REM Delete uploaded avatars
    if exist "backend\static\uploads\avatars\*.*" (
        for %%F in (backend\static\uploads\avatars\*.*) do (
            if not "%%~nxF"==".gitignore" if not "%%~nxF"==".gitkeep" (
                del /Q "%%F"
            )
        )
    )

    REM Run seed script
    cd backend
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    )
    python seed.py
    cd ..

    echo ✅ Database reset successfully!
)

echo.
echo 📊 Fresh test data loaded:
echo    - 9 test users
echo    - 21 sample posts
echo    - Comments, reactions, and relationships
echo.
echo 🔐 Test accounts ready:
echo    - sarah.johnson@testbook.com / Sarah2024!
echo    - mike.chen@testbook.com / MikeRocks88
echo    - emma.davis@testbook.com / EmmaLovesPhotos
echo.
echo 🎯 You can now test with a clean database!
echo.
pause

