# AGENTS.md

## 项目概述

**ZaunGit (祖安Git)** 是一个基于 Git Hooks 的"代码审查"工具。当用户提交代码后，它会自动读取代码变动，调用 LLM 进行分析，然后以阴阳怪气、抽象嘴臭的风格通过系统弹窗羞辱用户的代码。

### 核心理念
- **Clone & Run**: 克隆即用，零依赖污染
- **全自动配置**: 自动修改 Git 全局配置
- **跨平台**: 支持 Windows 和 macOS/Linux

## 目录结构

```
ZaunGit/
├── install.sh           # macOS/Linux 安装脚本
├── install.bat          # Windows 安装脚本
├── uninstall.py         # 卸载脚本
├── requirements.txt     # 依赖包 (仅需 requests)
├── README.md            # 项目文档
├── AGENTS.md            # AI Agent 指南
└── src/
    ├── __init__.py
    ├── main.py          # 核心程序：获取 Diff → 调用 API → 弹窗
    ├── prompts.py       # 提示词配置 (核心人设)
    └── setup.py         # 安装配置逻辑
```

## 构建与安装命令

### 安装

```bash
# macOS/Linux
chmod +x install.sh
./install.sh

# Windows
install.bat
```

### 卸载

```bash
python uninstall.py
```

### 手动运行

```bash
# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 运行配置
python src/setup.py

# 手动触发代码审查
python src/main.py
```

## 代码风格指南

### Python 版本
- 目标版本: Python 3.8+
- 使用 pathlib 处理路径，兼容跨平台

### 导入规范
```python
# 标准库
import os
import sys
from pathlib import Path

# 第三方库
import requests

# 本地模块
from prompts import SYSTEM_PROMPT
```

### 格式规范
- 使用 4 空格缩进
- 行宽不超过 100 字符
- 函数之间空一行
- 类方法之间空一行

### 类型注解
- 简单函数可以省略类型注解
- 复杂函数建议添加类型注解

### 命名规范
- 变量/函数: snake_case
- 常量: UPPER_SNAKE_CASE
- 私有函数: _leading_underscore
- 文件名: snake_case.py

### 错误处理
- 静默失败原则: API 调用失败或没网时，不要报错崩溃
- 使用 try-except 捕获异常，返回 None 或 pass

```python
def risky_operation():
    try:
        # 可能失败的操作
        pass
    except Exception:
        return None  # 或 pass
```

### Git Diff 获取
```python
subprocess.run(
    ['git', 'show', 'HEAD', '--format=', '--unified=0'],
    capture_output=True,
    text=True,
    timeout=30
)
```

### 配置文件位置
- 配置文件: `~/.zaun_git_config.json`
- Hook 目录: `~/.zaun_hooks/`

### Hook 文件规范
- Mac/Linux: 必须添加执行权限 (`chmod +x`)
- Windows: 使用 `.bat` 后缀
- Hook 内容必须使用**绝对路径**调用 Python 解释器

### 提示词规范 (prompts.py)
- 必须阴阳怪气，禁止礼貌
- 必须使用抽象话和烂梗
- 每句话结尾必须带表情包
- 字数控制在 50-100 字 (适合弹窗显示)

## 测试

目前无自动化测试。手动测试流程:

1. 安装: `./install.sh`
2. 配置 API Key
3. 在任意 Git 仓库执行 `git commit`
4. 检查是否收到系统弹窗通知

## 注意事项

1. **跨平台路径**: 始终使用 `pathlib.Path` 处理路径
2. **虚拟环境**: `.venv` 目录由安装脚本自动创建
3. **API 兼容**: 使用 OpenAI 格式的 API 接口
4. **通知权限**: 首次运行可能需要授权系统通知权限
5. **通知实现**: 使用原生系统弹窗 (macOS: osascript, Windows: PowerShell, Linux: zenity)
6. **非阻塞设计**: 通知发送失败不能影响 git commit 流程
