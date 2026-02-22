#!/usr/bin/env python3
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

LOG_FILE = Path.home() / '.zaun_git.log'

def log(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'[{datetime.now()}] {msg}\n')
    except:
        pass

def get_git_diff():
    try:
        result = subprocess.run(
            ['git', 'show', 'HEAD', '--format=', '--unified=0'],
            capture_output=True,
            text=True,
            timeout=30
        )
        log(f'git show returncode: {result.returncode}')
        if result.returncode != 0:
            log(f'git show stderr: {result.stderr[:200]}')
            return None
        diff = result.stdout.strip()
        if not diff:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--unified=0'],
                capture_output=True,
                text=True,
                timeout=30
            )
            diff = result.stdout.strip()
        return diff if diff else None
    except Exception as e:
        log(f'get_git_diff exception: {e}')
        return None

def load_config():
    config_path = Path.home() / '.zaun_git_config.json'
    if not config_path.exists():
        log(f'Config file not found: {config_path}')
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log(f'Load config error: {e}')
        return None

def call_llm(config, diff_content):
    if not config:
        return None
    
    api_key = config.get('api_key', '')
    base_url = config.get('base_url', 'https://api.deepseek.com').rstrip('/')
    model = config.get('model', 'deepseek-chat')
    
    if not api_key:
        return None
    
    try:
        import requests
        
        from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        user_prompt = USER_PROMPT_TEMPLATE.format(diff_content=diff_content[:8000])
        
        payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ],
            'max_tokens': 500,
            'temperature': 0.9
        }
        
        response = requests.post(
            f'{base_url}/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        log(f'API error: {response.status_code} - {response.text[:200]}')
        return None
    except Exception as e:
        log(f'LLM exception: {e}')
        return None

def sanitize_message(msg, max_len=200):
    msg = msg.replace('\\', '\\\\')
    msg = msg.replace('"', '\\"')
    msg = msg.replace("'", "\\'")
    msg = msg.replace('\n', ' ')
    msg = msg.replace('\r', ' ')
    msg = msg.replace('`', "'")
    msg = msg.replace('$', '\\$')
    msg = ''.join(c for c in msg if c.isprintable() or c in ' ')
    return msg[:max_len].strip()

def send_notification_macos(message):
    title = "🤡 祖安 Code Review"
    safe_msg = sanitize_message(message, 200)
    
    try:
        result = subprocess.run(
            ['which', 'terminal-notifier'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            subprocess.run(
                ['terminal-notifier', '-title', title, '-message', safe_msg, '-sound', 'Basso', '-timeout', '30'],
                capture_output=True,
                timeout=35
            )
            log('macOS notification sent via terminal-notifier')
            return True
    except Exception as e:
        log(f'terminal-notifier failed: {e}')
    
    try:
        safe_msg_dialog = safe_msg.replace('\\', '\\\\').replace('"', '\\"')
        script = f'''
        display dialog "{safe_msg_dialog}" with title "{title}" buttons {{"行了行了"}} default button "行了行了" with icon caution
        '''
        subprocess.Popen(
            ['osascript', '-e', script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log('macOS dialog sent via osascript (requires click to dismiss)')
        return True
    except Exception as e:
        log(f'osascript dialog failed: {e}')
    
    return False

def send_notification_windows(message):
    title = "🤡 祖安 Code Review"
    safe_msg = sanitize_message(message, 200)
    
    safe_msg_ps = safe_msg.replace("'", "''").replace('"', "'").replace('\n', ' ')
    title_ps = title.replace("'", "''").replace('"', "'")
    
    ps_script = f'''
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show('{safe_msg_ps}', '{title_ps}', 'OK', 'Warning')
'''
    
    try:
        subprocess.Popen(
            ['powershell', '-Command', ps_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log('Windows MessageBox sent (requires click to dismiss)')
        return True
    except Exception as e:
        log(f'Windows MessageBox failed: {e}')
        try:
            subprocess.Popen(
                ['mshta', 'vbscript:Execute("MsgBox """ + safe_msg_ps + """,48,"" + title_ps + """:close")'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log('Windows fallback popup sent')
            return True
        except Exception as e2:
            log(f'Windows fallback failed: {e2}')
    
    return False

def send_notification_linux(message):
    title = "🤡 祖安 Code Review"
    safe_msg = sanitize_message(message, 200)
    
    try:
        subprocess.Popen(
            ['zenity', '--info', '--title', title, '--text', safe_msg, '--no-markup'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log('Linux dialog sent via zenity (requires click to dismiss)')
        return True
    except Exception as e:
        log(f'Linux zenity failed: {e}')
        try:
            subprocess.run(
                ['notify-send', '-u', 'critical', '-t', '0', title, safe_msg],
                capture_output=True,
                timeout=10
            )
            log('Linux notification sent via notify-send')
            return True
        except Exception as e2:
            log(f'Linux notify-send failed: {e2}')
    
    return False

def send_notification(message):
    try:
        platform = sys.platform.lower()
        
        if platform == 'darwin':
            send_notification_macos(message)
        elif platform == 'win32' or platform == 'cygwin':
            send_notification_windows(message)
        else:
            send_notification_linux(message)
    except Exception as e:
        log(f'send_notification error: {e}')

def main():
    log('=== Hook triggered ===')
    
    diff = get_git_diff()
    log(f'Diff result: {len(diff) if diff else 0} chars')
    if not diff:
        log('No diff, exiting')
        sys.exit(0)
    
    config = load_config()
    log(f'Config loaded: {bool(config)}')
    if not config:
        log('No config, exiting')
        sys.exit(0)
    
    log('Calling LLM...')
    response = call_llm(config, diff)
    log(f'LLM response: {bool(response)}')
    if response:
        log(f'Response: {response[:100]}...')
        send_notification(response)
        log('Notification sent')
    else:
        log('No response from LLM')
    
    sys.exit(0)

if __name__ == '__main__':
    main()
