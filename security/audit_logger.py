# D:\AI\AI_Trading_System_ki\security\audit_logger.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from datetime import datetime
import json
from typing import Dict, Any

class AuditLogger:
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """راه‌اندازی logger امنیتی"""
        logger = logging.getLogger("AuditLogger")
        logger.setLevel(logging.INFO)
        
        # جلوگیری از تکرار handlerها
        if not logger.handlers:
            # File Handler
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # فرمت
            formatter = logging.Formatter(
                '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            # اضافه کردن handler
            logger.addHandler(file_handler)
            
        return logger
    
    def log_event(self, event_type: str, user: str, details: Dict[str, Any] = None):
        """ثبت رویداد امنیتی"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user': user,
            'details': details or {}
        }
        
        # لاگ به فایل
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))
        
        # نمایش در کنسول
        print(f"🛡️ [امنیت] {event_type} - کاربر: {user}")
    
    def log_login_attempt(self, user: str, success: bool, ip_address: str = "unknown"):
        """ثبت تلاش ورود"""
        self.log_event(
            "LOGIN_ATTEMPT",
            user,
            {
                "success": success,
                "ip_address": ip_address
            }
        )
    
    def log_api_key_access(self, user: str, key_name: str, action: str):
        """ثبت دسترسی به کلید API"""
        self.log_event(
            "API_KEY_ACCESS",
            user,
            {
                "key_name": key_name,
                "action": action
            }
        )
    
    def log_system_change(self, user: str, change_type: str, details: str):
        """ثبت تغییرات سیستم"""
        self.log_event(
            "SYSTEM_CHANGE",
            user,
            {
                "change_type": change_type,
                "details": details
            }
        )
    
    def log_security_violation(self, user: str, violation_type: str, details: str):
        """ثبت نقض امنیتی"""
        self.log_event(
            "SECURITY_VIOLATION",
            user,
            {
                "violation_type": violation_type,
                "details": details
            }
        )

# تست عملی:
if __name__ == "__main__":
    audit = AuditLogger("test_audit.log")
    
    # ثبت رویدادهای مختلف
    audit.log_login_attempt("admin", True, "192.168.1.100")
    audit.log_api_key_access("admin", "binance_key", "READ")
    audit.log_system_change("admin", "CONFIG_UPDATE", "Updated trading pairs")
    audit.log_security_violation("unknown", "UNAUTHORIZED_ACCESS", "Failed API access attempt")
    
    print("رویدادهای امنیتی ثبت شدند")