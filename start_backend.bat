@echo off
title Cerberus DeepCrystal - Backend Server
echo.
echo   ╔═══════════════════════════════════════╗
echo   ║     CERBERUS DEEPCRYSTAL v1.0         ║
echo   ║   AI Gemstone Forensic Laboratory     ║
echo   ║   Author: Sudeepa Wanigarathna        ║
echo   ╚═══════════════════════════════════════╝
echo.
echo [1/3] Initializing Python environment...
cd /d "%~dp0backend"
python -m pip install -r requirements.txt --quiet

echo [2/3] Seeding database...
python data/seed_database.py

echo [3/3] Starting FastAPI backend on http://localhost:8000 ...
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
