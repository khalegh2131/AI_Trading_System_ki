# D:\AI\AI_Trading_System_ki\security\auth_manager.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import secrets
import time
from typing import Dict, Optional
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

class AuthManager:
    def __init__(self):
        self.logger = get_logger("AuthManager")
        self.users = {}  # ذخیره کاربران (در عمل باید در دیتابیس باشه)
        self.active_sessions = {}  # جلسات فعال
        self.session_timeout = 3600  # 1 ساعت
        
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """هش کردن رمز عبور"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                      password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash_hex = pwdhash.hex()
        return pwdhash_hex, salt
    
    def register_user(self, username: str, password: str) -> bool:
        """ثبت نام کاربر"""
        try:
            if username in self.users:
                self.logger.warning(f"کاربر {username} قبلاً ثبت شده")
                return False
                
            pwdhash, salt = self.hash_password(password)
            self.users[username] = {
                'password_hash': pwdhash,
                'salt': salt,
                'created_at': time.time()
            }
            
            self.logger.info(f"کاربر {username} ثبت نام کرد")
            return True
        except Exception as e:
            self.logger.error(f"خطا در ثبت نام {username}: {str(e)}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """احراز هویت کاربر"""
        if username not in self.users:
            self.logger.warning(f"کاربر {username} یافت نشد")
            return None
            
        user = self.users[username]
        pwdhash, _ = self.hash_password(password, user['salt'])
        
        if pwdhash == user['password_hash']:
            # ایجاد جلسه
            session_token = secrets.token_urlsafe(32)
            self.active_sessions[session_token] = {
                'username': username,
                'created_at': time.time(),
                'last_access': time.time()
            }
            
            self.logger.info(f"کاربر {username} وارد شد")
            return session_token
        else:
            self.logger.warning(f"رمز عبور اشتباه برای {username}")
            return None
    
    def validate_session(self, session_token: str) -> bool:
        """اعتبارسنجی جلسه"""
        if session_token not in self.active_sessions:
            return False
            
        session = self.active_sessions[session_token]
        current_time = time.time()
        
        # بررسی انقضای جلسه
        if current_time - session['last_access'] > self.session_timeout:
            del self.active_sessions[session_token]
            self.logger.info("جلسه منقضی شد")
            return False
            
        # بروزرسانی زمان دسترسی
        session['last_access'] = current_time
        return True
    
    def logout_user(self, session_token: str) -> bool:
        """خروج کاربر"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            self.logger.info("کاربر خارج شد")
            return True
        return False
    
    def get_user_from_session(self, session_token: str) -> Optional[str]:
        """دریافت نام کاربری از جلسه"""
        if self.validate_session(session_token):
            return self.active_sessions[session_token]['username']
        return None

# تست عملی:
if __name__ == "__main__":
    auth = AuthManager()
    
    # ثبت نام
    auth.register_user("admin", "secure_password_123")
    
    # ورود
    token = auth.authenticate_user("admin", "secure_password_123")
    if token:
        print(f"ورود موفق! توکن: {token}")
        
        # بررسی جلسه
        user = auth.get_user_from_session(token)
        print(f"کاربر فعال: {user}")
        
        # خروج
        auth.logout_user(token)
        print("خروج انجام شد")