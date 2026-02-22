#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "🔥 ZaunGit (祖安Git) 安装程序 🔥"
echo "=========================================="

if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

echo "📥 激活虚拟环境并安装依赖..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 macOS 平台检测..."
    if ! command -v terminal-notifier &> /dev/null; then
        echo "📦 安装 terminal-notifier (通知工具)..."
        if command -v brew &> /dev/null; then
            brew install terminal-notifier
        else
            echo "⚠️  未检测到 Homebrew，请手动安装 terminal-notifier:"
            echo "   brew install terminal-notifier"
        fi
    else
        echo "✅ terminal-notifier 已安装"
    fi
fi

echo "⚙️  运行配置程序..."
python src/setup.py

echo ""
echo "✅ 安装完成！"
