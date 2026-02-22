@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo 🔥 ZaunGit (祖安Git) 安装程序 🔥
echo ==========================================

cd /d "%~dp0"

if not exist ".venv" (
    echo 📦 创建虚拟环境...
    python -m venv .venv
)

echo 📥 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ⚙️  运行配置程序...
python src\setup.py

echo.
echo ✅ 安装完成！
pause
