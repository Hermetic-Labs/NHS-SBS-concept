@echo off
title NHS SBS CQ Portal

echo ==========================================
echo NHS SBS Healthcare AI Solutions (SBS10523)
echo Clarification Question Portal
echo ==========================================

cd /d "%~dp0"

echo.
echo [1/2] Starting local AI backend spine...
start cmd /k ".\venv\Scripts\activate.bat && python backend\main.py"

echo.
echo [2/2] Launching Cockpit frontend server...
start cmd /k "python -m http.server 8000"
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:8000/frontend/index.html"

echo.
echo All systems operational. Close this window to exit (backend cmd will remain open).
