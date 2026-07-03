@echo off
setlocal EnableDelayedExpansion
title Cerberus DeepCrystal
color 0A

echo.
echo  =====================================================
echo     CERBERUS DEEPCRYSTAL v2.0
echo     AI-Powered Mineral ^& Gemstone Forensic Lab
echo  =====================================================
echo.

REM ── Verify install was run ─────────────────────────────
if not exist venv (
    echo [ERROR] Environment not set up. Please run install.bat first!
    pause
    exit /b 1
)

if not exist frontend\dist (
    echo [ERROR] Frontend not built. Please run install.bat first!
    pause
    exit /b 1
)

echo [OK] Starting Cerberus DeepCrystal...
echo      The app will open in your browser automatically.
echo      URL: http://localhost:8000
echo.
echo      Press Ctrl+C to shut down the application.
echo.

call venv\Scripts\activate.bat

REM Open browser after 2-second delay
start /min "" cmd /c "timeout /t 2 >nul && start http://localhost:8000"

REM Start the unified backend server (serves both API and frontend)
cd backend
python main.py
