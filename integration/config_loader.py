# D:\AI\AI_Trading_System_ki\integration\config_loader.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import json
import logging
from typing import Dict, Any

# محلی‌سازی logger
def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class ConfigLoader:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.logger = get_logger("ConfigLoader")
        self.config = {}
        
    def load_config(self) -> Dict[str, Any]:
        """بارگذاری تنظیمات از فایل"""
        try:
            # ابتدا YAML
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            # سپس JSON
            elif self.config_path.endswith('.json'):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                raise ValueError("فرمت فایل پشتیبانی نمی‌شود")
                
            self.logger.info(f"تنظیمات از {self.config_path} بارگذاری شد")
            return self.config
            
        except FileNotFoundError:
            self.logger.warning(f"فایل {self.config_path} یافت نشد. ایجاد تنظیمات پیش‌فرض...")
            return self._create_default_config()
        except Exception as e:
            self.logger.error(f"خطا در بارگذاری تنظیمات: {str(e)}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """ایجاد تنظیمات پیش‌فرض"""
        default_config = {
            "app": {
                "name": "AI Trading System",
                "version": "1.0.0",
                "debug": True,
                "host": "0.0.0.0",
                "port": 8050
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000
            },
            "apis": {
                "crypto": [
                    {
                        "name": "Binance",
                        "base_url": "https://api.binance.com",
                        "key": "ENCRYPTED_KEY",
                        "secret": "ENCRYPTED_SECRET",
                        "ping_url": "https://api.binance.com/api/v3/ping"
                    }
                ],
                "forex": []
            },
            "vpn": {
                "subscription_urls": [
                    "https://raw.githubusercontent.com/freefq/free/master/v2"
                ],
                "default_region": "DE",
                "auto_switch": True
            },
            "learning": {
                "rl_agent": {
                    "state_size": 20,
                    "action_size": 3,
                    "learning_rate": 0.001,
                    "gamma": 0.95
                }
            },
            "nlp": {
                "use_chatgpt": False,
                "sentiment_threshold": 0.3
            },
            "security": {
                "session_timeout": 3600
            }
        }
        
        # ذخیره تنظیمات پیش‌فرض
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """ذخیره تنظیمات در فایل"""
        config_to_save = config or self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(config_to_save, f, allow_unicode=True, indent=2)
                elif self.config_path.endswith('.json'):
                    json.dump(config_to_save, f, ensure_ascii=False, indent=2)
                    
            self.logger.info(f"تنظیمات در {self.config_path} ذخیره شد")
        except Exception as e:
            self.logger.error(f"خطا در ذخیره تنظیمات: {str(e)}")
    
    def get(self, key_path: str, default=None):
        """دریافت مقدار با مسیر کلید"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value):
        """تنظیم مقدار با مسیر کلید"""
        keys = key_path.split('.')
        config_ref = self.config
        
        # ایجاد کلیدها اگر وجود نداشته باشند
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        # تنظیم مقدار نهایی
        config_ref[keys[-1]] = value

# تست عملی:
if __name__ == "__main__":
    # تست بارگذاری تنظیمات
    loader = ConfigLoader("test_config.yaml")
    config = loader.load_config()
    print("تنظیمات بارگذاری شد:")
    print(f"نام اپ: {config.get('app', {}).get('name', 'N/A')}")
    
    # تست ذخیره تنظیمات
    loader.set('app.version', '1.0.1')
    loader.save_config()
    print("تنظیمات به‌روزرسانی و ذخیره شد")