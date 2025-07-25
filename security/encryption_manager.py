# D:\AI\AI_Trading_System_ki\security\encryption_manager.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging

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

class EncryptionManager:
    def __init__(self, password: str = None):
        self.logger = get_logger("EncryptionManager")
        self.password = password or self._generate_default_password()
        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)
        
    def _generate_default_password(self) -> str:
        """تولید رمز عبور پیش‌فرض"""
        return "AI_Trading_System_Secure_Password_2025"
    
    def _derive_key(self, password: str) -> bytes:
        """استخراج کلید از رمز عبور"""
        salt = b'secure_trading_system_salt_16bytes'  # باید 16 بایت باشه
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data: str) -> str:
        """رمزنگاری داده"""
        try:
            encrypted_data = self.cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            self.logger.error(f"خطا در رمزنگاری: {str(e)}")
            return ""
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """رمزگشایی داده"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            self.logger.error(f"خطا در رمزگشایی: {str(e)}")
            return ""
    
    def encrypt_api_key(self, api_key: str) -> str:
        """رمزنگاری کلید API"""
        return self.encrypt_data(api_key)
    
    def decrypt_api_key(self, encrypted_api_key: str) -> str:
        """رمزگشایی کلید API"""
        return self.decrypt_data(encrypted_api_key)

# تست عملی:
if __name__ == "__main__":
    # ایجاد مدیر رمزنگاری
    enc_manager = EncryptionManager("my_secure_password")
    
    # تست رمزنگاری
    original_key = "sk-1234567890abcdef"
    encrypted = enc_manager.encrypt_api_key(original_key)
    decrypted = enc_manager.decrypt_api_key(encrypted)
    
    print(f"کلید اصلی: {original_key}")
    print(f"رمز شده: {encrypted}")
    print(f"رمزگشایی شده: {decrypted}")
    print(f"درستی: {original_key == decrypted}")