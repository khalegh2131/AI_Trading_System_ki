# D:\AI\AI_Trading_System_ki\ui\utils.py

import json
from datetime import datetime

def format_log_message(message: str, level: str = "INFO") -> str:
    """فرمت‌بندی پیام لاگ"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {level}: {message}"

def load_dashboard_config(config_path: str = "config.yaml") -> dict:
    """بارگذاری تنظیمات داشبورد"""
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {}

def save_dashboard_config(config: dict, config_path: str = "config.yaml"):
    """ذخیره تنظیمات داشبورد"""
    try:
        import yaml
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)
    except Exception as e:
        pass