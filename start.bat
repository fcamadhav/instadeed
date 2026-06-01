@echo off
echo ====================================
echo  Instadeed Legal Drafting Suite
echo ====================================
echo.
echo [1/3] Checking build...
if not exist "out.js" (
    echo Building frontend...
    python build.py
    if errorlevel 1 (
        echo Build failed!
        pause
        exit /b 1
    )
)
echo Build OK.
echo.
echo [2/3] Starting server on http://localhost:8000
echo.
echo Default Admin: admin@instadeed.local / admin123
echo.
python server.py
if errorlevel 1 (
    echo Server exited with error code %errorlevel%
    pause
)
