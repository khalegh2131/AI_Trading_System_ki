# D:\AI\AI_Trading_System_ki\security\utils.py

import re
import secrets
from typing import bool

def is_strong_password(password: str) -> bool:
    """بررسی قوی بودن رمز عبور"""
    if len(password) < 8:
        return False
    
    # حداقل یک حرف بزرگ
    if not re.search(r'[A-Z]', password):
        return False
    
    # حداقل یک حرف کوچک
    if not re.search(r'[a-z]', password):
        return False
    
    # حداقل یک عدد
    if not re.search(r'\d', password):
        return False
    
    # حداقل یک کاراکتر خاص
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def generate_secure_token(length: int = 32) -> str:
    """تولید توکن امن"""
    return secrets.token_urlsafe(length)

def mask_api_key(api_key: str) -> str:
    """ماسک کردن کلید API"""
    if len(api_key) <= 8:
        return "*" * len(api_key)
    
    # نمایش فقط 4 کاراکتر اول و آخر
    return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]

def validate_ip_address(ip: str) -> bool:
    """اعتبارسنجی آدرس IP"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

# تست عملی:
if __name__ == "__main__":
    # تست قوی بودن رمز عبور
    test_passwords = [
        "123456",           # ضعیف
        "Password123",      # ضعیف (بدون کاراکتر خاص)
        "Password123!",     # قوی
        "MySecure@Pass123"  # قوی
    ]
    
    for pwd in test_passwords:
        result = is_strong_password(pwd)
        print(f"رمز عبور '{pwd}': {'قوی' if result else 'ضعیف'}")
    
    # تست ماسک کردن کلید API
    api_key = "sk-1234567890abcdef1234567890abcdef"
    masked = mask_api_key(api_key)
    print(f"کلید اصلی: {api_key}")
    print(f"کلید ماسک شده: {masked}")