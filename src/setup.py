#!/usr/bin/env python3
import json
import os
import sys
import stat
import argparse
from pathlib import Path

def get_project_root():
    return Path(__file__).parent.parent.resolve()

def get_venv_python():
    root = get_project_root()
    if sys.platform == 'win32':
        venv_python = root / '.venv' / 'Scripts' / 'python.exe'
    else:
        venv_python = root / '.venv' / 'bin' / 'python'
    return venv_python

def get_hooks_dir():
    return Path.home() / '.zaun_hooks'

def get_config_path():
    return Path.home() / '.zaun_git_config.json'

def load_config():
    config_path = get_config_path()
    if not config_path.exists():
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def save_config(api_key, base_url, model):
    config = {
        'api_key': api_key,
        'base_url': base_url.rstrip('/'),
        'model': model
    }
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f'✅ 配置已保存到: {config_path}')

def create_hook_file():
    hooks_dir = get_hooks_dir()
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    hook_file = hooks_dir / 'post-commit'
    main_py = get_project_root() / 'src' / 'main.py'
    venv_python = get_venv_python()
    
    if sys.platform == 'win32':
        hook_content = f'''@echo off
"{venv_python}" "{main_py}"
'''
        hook_file = hooks_dir / 'post-commit.bat'
    else:
        hook_content = f'''#!/bin/sh
"{venv_python}" "{main_py}"
'''
    
    with open(hook_file, 'w', encoding='utf-8') as f:
        f.write(hook_content)
    
    if sys.platform != 'win32':
        st = os.stat(hook_file)
        os.chmod(hook_file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    print(f'✅ Hook 文件已创建: {hook_file}')
    return hook_file

def configure_git_hooks():
    hooks_dir = get_hooks_dir()
    os.system(f'git config --global core.hooksPath "{hooks_dir}"')
    print(f'✅ Git 全局配置已设置: core.hooksPath = {hooks_dir}')

def show_current_config():
    config = load_config()
    if config:
        print('\n📋 当前配置：')
        print(f'   Base URL: {config.get("base_url", "未设置")}')
        print(f'   Model: {config.get("model", "未设置")}')
        api_key = config.get('api_key', '')
        if api_key:
            masked = api_key[:8] + '***' + api_key[-4:] if len(api_key) > 12 else '***'
            print(f'   API Key: {masked}')
    else:
        print('\n⚠️  未找到配置文件')
    return config

def prompt_for_config(existing=None):
    print('\n请输入 LLM 配置信息：')
    print('(直接回车保持当前值)\n')
    
    if existing:
        print(f'当前 Base URL: {existing.get("base_url", "未设置")}')
        base_url = input(f'Base URL [{existing.get("base_url", "https://api.deepseek.com")}]: ').strip()
        if not base_url:
            base_url = existing.get('base_url', 'https://api.deepseek.com')
        
        print(f'当前 Model: {existing.get("model", "未设置")}')
        model = input(f'Model Name [{existing.get("model", "deepseek-chat")}]: ').strip()
        if not model:
            model = existing.get('model', 'deepseek-chat')
        
        print('API Key (留空保持原值): ', end='')
        api_key = input().strip()
        if not api_key:
            api_key = existing.get('api_key', '')
            if not api_key:
                print('❌ API Key 不能为空！')
                return None
    else:
        api_key = input('API Key: ').strip()
        if not api_key:
            print('❌ API Key 不能为空！')
            return None
        
        base_url = input('Base URL [https://api.deepseek.com]: ').strip()
        if not base_url:
            base_url = 'https://api.deepseek.com'
        
        model = input('Model Name [deepseek-chat]: ').strip()
        if not model:
            model = 'deepseek-chat'
    
    return api_key, base_url, model

def setup_hooks():
    create_hook_file()
    configure_git_hooks()

def interactive_setup(skip_config=False):
    print('\n' + '=' * 50)
    print('🔥 ZaunGit (祖安Git) 安装配置 🔥')
    print('=' * 50)
    
    existing = load_config()
    if existing:
        print('\n检测到已有配置文件。')
    
    if skip_config:
        print('\n⏭️  跳过 API 配置，稍后可通过以下命令配置：')
        print('   python src/setup.py --config')
        setup_hooks()
    else:
        print('\n是否现在配置 LLM API？')
        print('  1. 现在配置 (推荐)')
        print('  2. 稍后配置')
        
        choice = input('\n请选择 [1]: ').strip()
        
        if choice == '2':
            print('\n⏭️  跳过配置，稍后可通过以下命令配置：')
            print('   python src/setup.py --config')
            setup_hooks()
        else:
            result = prompt_for_config(existing)
            if result:
                api_key, base_url, model = result
                print('\n' + '-' * 50)
                print('正在配置...\n')
                save_config(api_key, base_url, model)
                setup_hooks()
    
    print('\n' + '=' * 50)
    print('🎉 ZaunGit 安装完成！')
    if not load_config():
        print('⚠️  请记得配置 API Key：python src/setup.py --config')
    else:
        print('现在每次 git commit 后都会收到"亲切"的代码审查。')
    print('=' * 50 + '\n')

def config_only():
    print('\n' + '=' * 50)
    print('🔧 ZaunGit 配置管理')
    print('=' * 50)
    
    show_current_config()
    
    existing = load_config()
    result = prompt_for_config(existing)
    
    if result:
        api_key, base_url, model = result
        print('\n' + '-' * 50)
        print('正在保存配置...\n')
        save_config(api_key, base_url, model)
        print('\n✅ 配置已更新，立即生效！')
    
    print('=' * 50 + '\n')

def main():
    parser = argparse.ArgumentParser(
        description='ZaunGit 安装配置工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python src/setup.py           # 交互式安装
  python src/setup.py --config  # 仅更新 API 配置
  python src/setup.py --show    # 显示当前配置
'''
    )
    parser.add_argument('--config', '-c', action='store_true', help='更新 LLM API 配置')
    parser.add_argument('--show', '-s', action='store_true', help='显示当前配置')
    parser.add_argument('--skip-config', action='store_true', help='安装时跳过 API 配置')
    
    args = parser.parse_args()
    
    if args.show:
        show_current_config()
    elif args.config:
        config_only()
    else:
        interactive_setup(skip_config=args.skip_config)

if __name__ == '__main__':
    main()
