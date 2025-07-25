# D:\AI\AI_Trading_System_ki\integration\main_system.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import time
import logging
from datetime import datetime
from api.external_api import create_api_app
from ui.dashboard_main import run_dashboard
from integration.module_connector import ModuleConnector
from integration.performance_monitor import PerformanceMonitor
import yaml

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

class MainSystem:
    def __init__(self, config_path: str = "config.yaml"):
        self.logger = get_logger("MainSystem")
        self.config = self._load_config(config_path)
        self.modules = {}
        self.running = False
        self.performance_monitor = PerformanceMonitor()
        
    def _load_config(self, config_path: str) -> dict:
        """بارگذاری تنظیمات"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"خطا در بارگذاری تنظیمات: {str(e)}")
            return {}
    
    def initialize_modules(self):
        """مقداردهی اولیه ماژول‌ها"""
        self.logger.info("در حال مقداردهی اولیه ماژول‌ها...")
        
        try:
            # اتصال ماژول‌ها
            connector = ModuleConnector(self.config)
            self.modules = connector.connect_all_modules()
            
            self.logger.info("✅ همه ماژول‌ها مقداردهی شدند")
            return True
        except Exception as e:
            self.logger.error(f"❌ خطا در مقداردهی ماژول‌ها: {str(e)}")
            return False
    
    def start_api_server(self):
        """شروع سرور API"""
        def run_api():
            try:
                app = create_api_app()
                app.run(
                    host=self.config.get('api', {}).get('host', '0.0.0.0'),
                    port=self.config.get('api', {}).get('port', 8000),
                    debug=False
                )
            except Exception as e:
                self.logger.error(f"خطا در شروع API: {str(e)}")
        
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        self.logger.info("✅ سرور API شروع شد")
    
    def start_dashboard(self):
        """شروع داشبورد"""
        def run_dashboard_app():
            try:
                run_dashboard(self.config)
            except Exception as e:
                self.logger.error(f"خطا در شروع داشبورد: {str(e)}")
        
        dashboard_thread = threading.Thread(target=run_dashboard_app, daemon=True)
        dashboard_thread.start()
        self.logger.info("✅ داشبورد شروع شد")
    
    def start_trading_engine(self):
        """شروع موتور معاملاتی"""
        self.logger.info("در حال شروع موتور معاملاتی...")
        # اینجا کد واقعی موتور معاملاتی می‌آید
        self.running = True
    
    def monitor_performance(self):
        """مانیتور عملکرد"""
        def monitor_loop():
            while self.running:
                try:
                    metrics = self.performance_monitor.get_system_metrics()
                    self.logger.info(f"Metrics: CPU={metrics['cpu']}%, Memory={metrics['memory']}%")
                    time.sleep(60)  # هر 1 دقیقه
                except Exception as e:
                    self.logger.error(f"خطا در مانیتور: {str(e)}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def run(self):
        """اجرای سیستم"""
        self.logger.info("🚀 شروع سیستم AI Trading...")
        
        # مقداردهی اولیه
        if not self.initialize_modules():
            return False
        
        # شروع سرورها
        self.start_api_server()
        self.start_dashboard()
        self.start_trading_engine()
        self.monitor_performance()
        
        # حلقه اصلی
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("در حال توقف سیستم...")
            self.stop()
    
    def stop(self):
        """توقف سیستم"""
        self.running = False
        self.logger.info("🛑 سیستم متوقف شد")

# اجرای مستقیم
if __name__ == "__main__":
    # بارگذاری تنظیمات پیش‌فرض
    default_config = {
        "app": {
            "name": "AI Trading System",
            "debug": True,
            "host": "0.0.0.0",
            "port": 8050
        },
        "api": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }
    
    # ذخیره تنظیمات
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(default_config, f, allow_unicode=True)
    
    # اجرای سیستم
    system = MainSystem("config.yaml")
    system.run()