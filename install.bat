@echo off
setlocal EnableDelayedExpansion
title Cerberus DeepCrystal - Installer
color 0A

echo.
echo  =====================================================
echo     CERBERUS DEEPCRYSTAL - ONE-CLICK INSTALLER
echo     AI-Powered Mineral ^& Gemstone Forensic Lab
echo  =====================================================
echo.

REM ── Check Python ──────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python found.

REM ── Check Node.js ─────────────────────────────────────
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js found.

echo.
echo [1/5] Creating Python virtual environment...
if exist venv (
    echo      venv already exists, skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

echo.
echo [2/5] Installing Python dependencies (this may take a few minutes)...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r backend\requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies.
    echo Trying without --quiet for more info...
    pip install -r backend\requirements.txt
    pause
    exit /b 1
)
echo [OK] Python dependencies installed.

echo.
echo [3/5] Pre-downloading AI Vision Model (openai/clip-vit-base-patch32)...
echo      This will cache the model locally so the app starts instantly.
echo      Download size: ~600 MB. Please wait...
python -c "from transformers import CLIPProcessor, CLIPModel; CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32'); print('Model cached successfully.')"
if errorlevel 1 (
    echo [WARNING] Could not pre-download model. It will download on first run.
)
echo [OK] AI model ready.

echo.
echo [4/5] Installing frontend dependencies...
cd frontend
call npm install --silent
if errorlevel 1 (
    echo [ERROR] Failed to install frontend npm packages.
    pause
    exit /b 1
)
echo [OK] Frontend packages installed.

echo.
echo [5/5] Building frontend (React ^> static files)...
call npm run build
if errorlevel 1 (
    echo [ERROR] Frontend build failed.
    pause
    exit /b 1
)
echo [OK] Frontend built successfully.
cd ..

echo.
echo  =====================================================
echo   INSTALLATION COMPLETE!
echo.
echo   To start the application, double-click:
echo   ^> Start_DeepCrystal.bat
echo  =====================================================
echo.
pause
