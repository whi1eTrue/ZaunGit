#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def get_hooks_dir():
    return Path.home() / '.zaun_hooks'

def get_config_path():
    return Path.home() / '.zaun_git_config.json'

def uninstall():
    print('\n' + '=' * 50)
    print('🗑️  ZaunGit 卸载程序')
    print('=' * 50 + '\n')
    
    hooks_dir = get_hooks_dir()
    config_path = get_config_path()
    
    if hooks_dir.exists():
        shutil.rmtree(hooks_dir)
        print(f'✅ 已删除: {hooks_dir}')
    
    if config_path.exists():
        config_path.unlink()
        print(f'✅ 已删除: {config_path}')
    
    os.system('git config --global --unset core.hooksPath')
    print('✅ 已恢复 Git 默认配置')
    
    print('\n' + '=' * 50)
    print('👋 ZaunGit 已卸载')
    print('不会再有人骂你的代码了（也许你应该怀念它）')
    print('=' * 50 + '\n')

if __name__ == '__main__':
    uninstall()
