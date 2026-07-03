@echo off
title Cerberus DeepCrystal - Frontend
echo.
echo   ╔═══════════════════════════════════════╗
echo   ║  CERBERUS DEEPCRYSTAL - FRONTEND      ║
echo   ║  React + Vite Development Server      ║
echo   ╚═══════════════════════════════════════╝
echo.
cd /d "%~dp0frontend"
echo Installing frontend dependencies...
call npm install
echo.
echo Starting frontend on http://localhost:5173 ...
echo.
call npm run dev
pause
