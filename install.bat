@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo ==========================================
echo ZaunGit Install Script
echo ==========================================

cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    if not exist ".venv\Scripts\activate.bat" (
        echo [!] Failed to create virtual environment
        echo [!] Please make sure Python is installed and in PATH
        pause
        exit /b 1
    )
)

echo [*] Activating virtual environment...
call "%~dp0.venv\Scripts\activate.bat"

echo [*] Installing dependencies...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [*] Running setup...
python src\setup.py

echo.
echo [*] Installation complete!
pause
