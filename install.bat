@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo ==========================================
echo ZaunGit Install Script
echo ==========================================

cd /d "%~dp0"

if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
)

echo [*] Installing dependencies...
call .venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo [*] Running setup...
python src\setup.py

echo.
echo [*] Installation complete!
pause
