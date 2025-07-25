# D:\AI\AI_Trading_System_ki\api\controllers\system_controller.py

import logging
import psutil
from datetime import datetime

logger = logging.getLogger("SystemController")

class SystemController:
    def __init__(self):
        self.paused = False
        self.start_time = datetime.now()
    
    def pause_system(self) -> bool:
        """توقف سیستم"""
        try:
            self.paused = True
            logger.info("سیستم متوقف شد")
            return True
        except Exception as e:
            logger.error(f"خطا در توقف سیستم: {str(e)}")
            return False
    
    def resume_system(self) -> bool:
        """ادامه سیستم"""
        try:
            self.paused = False
            logger.info("سیستم ادامه یافت")
            return True
        except Exception as e:
            logger.error(f"خطا در ادامه سیستم: {str(e)}")
            return False
    
    def is_paused(self) -> bool:
        """بررسی توقف سیستم"""
        return self.paused
    
    def get_system_info(self) -> dict:
        """دریافت اطلاعات سیستم"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        uptime = datetime.now() - self.start_time
        
        return {
            "status": "paused" if self.paused else "running",
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / (1024**3):.2f} GB",
            "uptime": str(uptime).split('.')[0]  # حذف میلی‌ثانیه
        }
    
    def restart_system(self) -> bool:
        """راه‌اندازی مجدد سیستم"""
        logger.info("درخواست راه‌اندازی مجدد سیستم")
        # اینجا باید کد واقعی راه‌اندازی مجدد باشه
        return True

# نمونه استفاده:
if __name__ == "__main__":
    controller = SystemController()
    print("کنترل سیستم آماده است")