# 🤡 ZaunGit (祖安 Git)

> 一个基于 Git Hooks 的"嘴臭代码审查"工具。当你提交代码后，它会用最阴阳怪气、最抽象的方式羞辱你的代码。

## 🎯 项目简介

ZaunGit 是一个独特的代码审查工具，它不是温和地给你建议，而是用**互联网喷子**的语言风格，通过系统弹窗狠狠地羞辱你写的烂代码。

**为什么做这个？**
- 普通的 Code Review 太无聊了
- 需要一点"刺激"来提高代码质量
- 纯属娱乐，请勿当真 😅

## ✨ 功能特点

- 🔥 **阴阳怪气的代码审查** - 基于 LLM 生成极具攻击性的评价
- 💬 **系统级弹窗通知** - 必须手动点击才能关闭，想不看都不行
- 🚀 **Clone & Run** - 克隆即用，零配置污染
- 🌍 **跨平台支持** - macOS / Windows / Linux 全覆盖
- ⚙️ **全局接管** - 自动配置 Git 全局 Hooks，一次安装，全机生效
- 🔐 **隐私安全** - 配置文件存储在本地，不上传任何数据

## 📦 安装

### 前置要求

- Python 3.8+
- Git
- LLM API Key (支持 OpenAI 格式的接口，默认 DeepSeek)

### macOS / Linux

```bash
# 克隆项目
git clone https://github.com/your-repo/ZaunGit.git
cd ZaunGit

# 运行安装脚本
chmod +x install.sh
./install.sh
```

安装脚本会自动：
1. 创建 Python 虚拟环境 `.venv`
2. 安装 Python 依赖
3. 检测并安装 `terminal-notifier` (macOS)
4. 运行配置向导

### Windows

```batch
# 克隆项目
git clone https://github.com/your-repo/ZaunGit.git
cd ZaunGit

# 运行安装脚本
install.bat
```

### 手动安装

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行配置
python src/setup.py
```

## ⚙️ 配置

### 安装时配置

安装时会提示是否配置 LLM API：

```
是否现在配置 LLM API？
  1. 现在配置 (推荐)
  2. 稍后配置
```

选择"稍后配置"后，可随时通过命令更新配置。

### 配置管理命令

```bash
# 更新 LLM API 配置
python src/setup.py --config

# 查看当前配置
python src/setup.py --show

# 安装时跳过配置
python src/setup.py --skip-config
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| API Key | LLM 接口的 API Key | 无 (必填) |
| Base URL | API 接口地址 | `https://api.deepseek.com` |
| Model | 模型名称 | `deepseek-chat` |

配置文件存储位置：`~/.zaun_git_config.json`

### 支持的 LLM 服务

任何兼容 OpenAI 格式的 API 都可以使用：

- DeepSeek (推荐，便宜好用)
- OpenAI
- Claude (通过兼容接口)
- 本地部署的 LLM (如 Ollama)
- 其他第三方 API

## 🚀 使用

安装完成后，在**任意 Git 仓库**执行 `git commit`：

```bash
cd /your/any/project
git add .
git commit -m "修复了一个 bug"
# 稍等片刻... 弹窗出现 🤡
```

### 查看日志

```bash
cat ~/.zaun_git.log
```

## 🗑️ 卸载

```bash
cd ZaunGit
python uninstall.py
```

卸载会：
1. 删除 `~/.zaun_hooks/` 目录
2. 删除 `~/.zaun_git_config.json` 配置
3. 恢复 Git 默认 Hooks 配置

## 🖥️ 平台支持

| 平台 | 通知方式 | 需点击关闭 |
|------|----------|------------|
| macOS | `terminal-notifier` + `osascript dialog` | ✅ |
| Windows | PowerShell MessageBox | ✅ |
| Linux | `zenity` / `notify-send` | ✅ (zenity) |

### macOS 额外依赖

```bash
brew install terminal-notifier
```

安装脚本会自动检测并安装。

## 🎭 提示词风格

ZaunGit 的核心是一个精心设计的 System Prompt，让 LLM 变成一个：

- 互联网顶级喷子
- 抽象话大师
- 阴阳怪气艺术家

**示例输出：**

> 这代码只有你和**阎王爷**看得懂，建议你把注释写在黄纸上，烧给他让他给你 Code Review。💀

> 写出这种代码，你是不是**胎教肄业**啊？👶

> 往键盘上撒把米，**鸡啄出来的**都比你这有逻辑。🐔

## 📁 项目结构

```
ZaunGit/
├── install.sh           # macOS/Linux 安装脚本
├── install.bat          # Windows 安装脚本
├── uninstall.py         # 卸载脚本
├── requirements.txt     # Python 依赖 (仅需 requests)
├── AGENTS.md            # AI Agent 指南
├── README.md            # 项目文档
└── src/
    ├── __init__.py
    ├── main.py          # 核心逻辑：获取 Diff → 调用 API → 弹窗
    ├── prompts.py       # 提示词配置 (核心人设)
    └── setup.py         # 安装配置逻辑
```

## 🔧 高级配置

### 修改提示词

编辑 `src/prompts.py` 文件中的 `SYSTEM_PROMPT` 变量，自定义你的"喷子"风格。

### 修改通知样式

编辑 `src/main.py` 中的 `send_notification_*` 函数。

### 仅对特定仓库生效

```bash
# 取消全局配置
git config --global --unset core.hooksPath

# 在特定仓库设置
cd /your/project
git config core.hooksPath ~/.zaun_hooks
```

## ❓ 常见问题

### Q: 如何更换 LLM API？

```bash
# 更新配置
python src/setup.py --config

# 或直接编辑配置文件
cat ~/.zaun_git_config.json
```

### Q: 为什么没有收到通知？

1. 检查日志：`cat ~/.zaun_git.log`
2. 检查配置：`cat ~/.zaun_git_config.json`
3. macOS 确保安装了 `terminal-notifier`
4. 检查系统通知权限设置

### Q: 通知有延迟？

LLM API 调用需要时间（通常 2-5 秒），属于正常现象。

### Q: 可以自定义提示词吗？

可以！编辑 `src/prompts.py` 文件。

### Q: 会在所有 Git 仓库生效吗？

是的，默认配置为全局生效。如果想只在特定仓库生效，参考上方"高级配置"。

### Q: 会影响 commit 的内容吗？

不会。ZaunGit 只是读取 diff 进行分析，不会修改任何代码或 commit 信息。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本项目纯属娱乐目的，输出的"骂人"内容均由 AI 生成，不代表开发者观点。

请勿将本项目用于：
- 骚扰他人
- 制造职场矛盾
- 任何恶意目的

使用本工具即表示你理解并接受其娱乐性质。

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供优秀的 LLM API

---

**如果这个项目让你笑了，给个 ⭐ Star 吧！**

*Made with 😅 and 🤡*
