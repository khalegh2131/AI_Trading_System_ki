# D:\AI\AI_Trading_System_ki\security\key_manager.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging
from security.encryption_manager import EncryptionManager

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

class KeyManager:
    def __init__(self, keys_file: str = "keys.json"):
        self.logger = get_logger("KeyManager")
        self.keys_file = keys_file
        self.encryption_manager = EncryptionManager()
        self.keys = self._load_keys()
        
    def _load_keys(self) -> dict:
        """بارگذاری کلیدها از فایل"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r') as f:
                    encrypted_data = json.load(f)
                    decrypted_data = {}
                    for key, value in encrypted_data.items():
                        decrypted_data[key] = self.encryption_manager.decrypt_data(value)
                    return decrypted_data
            else:
                return {}
        except Exception as e:
            self.logger.error(f"خطا در بارگذاری کلیدها: {str(e)}")
            return {}
    
    def _save_keys(self):
        """ذخیره کلیدها در فایل"""
        try:
            encrypted_data = {}
            for key, value in self.keys.items():
                encrypted_data[key] = self.encryption_manager.encrypt_data(value)
            
            with open(self.keys_file, 'w') as f:
                json.dump(encrypted_data, f, indent=2)
                
            self.logger.info("کلیدها ذخیره شدند")
        except Exception as e:
            self.logger.error(f"خطا در ذخیره کلیدها: {str(e)}")
    
    def add_api_key(self, name: str, key: str, exchange: str = "unknown"):
        """افزودن کلید API"""
        self.keys[name] = {
            'key': key,
            'exchange': exchange,
            'type': 'api_key'
        }
        self._save_keys()
        self.logger.info(f"کلید API {name} اضافه شد")
    
    def get_api_key(self, name: str) -> str:
        """دریافت کلید API"""
        if name in self.keys:
            return self.keys[name].get('key', '')
        return ''
    
    def remove_api_key(self, name: str) -> bool:
        """حذف کلید API"""
        if name in self.keys:
            del self.keys[name]
            self._save_keys()
            self.logger.info(f"کلید API {name} حذف شد")
            return True
        return False
    
    def list_keys(self) -> list:
        """لیست کلیدها"""
        return list(self.keys.keys())
    
    def get_key_info(self, name: str) -> dict:
        """دریافت اطلاعات کلید"""
        return self.keys.get(name, {})

# تست عملی:
if __name__ == "__main__":
    key_manager = KeyManager("test_keys.json")
    
    # افزودن کلید نمونه
    key_manager.add_api_key("binance_test", "sk-test-1234567890", "binance")
    
    # دریافت کلید
    key = key_manager.get_api_key("binance_test")
    print(f"کلید دریافت شد: {key}")
    
    # لیست کلیدها
    keys = key_manager.list_keys()
    print(f"کلیدهای موجود: {keys}")