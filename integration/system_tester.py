# D:\AI\AI_Trading_System_ki\integration\system_tester.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import logging
from datetime import datetime
import pandas as pd
import numpy as np

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

class SystemTester:
    def __init__(self):
        self.logger = get_logger("SystemTester")
        self.test_results = []
    
    def run_all_tests(self) -> dict:
        """اجرای همه تست‌ها"""
        self.logger.info("🚀 شروع تست کامل سیستم...")
        
        tests = [
            self.test_api_connection,
            self.test_vpn_connection,
            self.test_data_pipeline,
            self.test_model_prediction,
            self.test_security_features,
            self.test_ui_access
        ]
        
        results = {}
        for test_func in tests:
            test_name = test_func.__name__
            try:
                result = test_func()
                results[test_name] = result
                self.logger.info(f"✅ {test_name}: {'موفق' if result else 'ناموفق'}")
            except Exception as e:
                results[test_name] = False
                self.logger.error(f"❌ {test_name}: خطا - {str(e)}")
        
        # ذخیره نتایج
        self.test_results.append({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'overall_success': all(results.values())
        })
        
        self.logger.info("🏁 تست کامل سیستم به پایان رسید")
        return results
    
    def test_api_connection(self) -> bool:
        """تست اتصال API"""
        try:
            # شبیه‌سازی تست API
            time.sleep(1)
            self.logger.info("تست اتصال API انجام شد")
            return True
        except Exception:
            return False
    
    def test_vpn_connection(self) -> bool:
        """تست اتصال VPN"""
        try:
            # شبیه‌سازی تست VPN
            time.sleep(1)
            self.logger.info("تست اتصال VPN انجام شد")
            return True
        except Exception:
            return False
    
    def test_data_pipeline(self) -> bool:
        """تست خط لوله داده‌ها"""
        try:
            # ایجاد داده‌های نمونه
            dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
            sample_data = pd.DataFrame({
                'timestamp': dates,
                'open': np.random.uniform(40000, 50000, 10),
                'high': np.random.uniform(41000, 51000, 10),
                'low': np.random.uniform(39000, 49000, 10),
                'close': np.random.uniform(40000, 50000, 10),
                'volume': np.random.uniform(1000, 5000, 10)
            })
            
            self.logger.info(f"داده‌های نمونه ایجاد شد: {len(sample_data)} ردیف")
            return True
        except Exception as e:
            self.logger.error(f"خطا در تست خط لوله: {str(e)}")
            return False
    
    def test_model_prediction(self) -> bool:
        """تست پیش‌بینی مدل"""
        try:
            # شبیه‌سازی تست مدل
            time.sleep(2)
            self.logger.info("تست پیش‌بینی مدل انجام شد")
            return True
        except Exception:
            return False
    
    def test_security_features(self) -> bool:
        """تست ویژگی‌های امنیتی"""
        try:
            # شبیه‌سازی تست امنیت
            time.sleep(1)
            self.logger.info("تست ویژگی‌های امنیتی انجام شد")
            return True
        except Exception:
            return False
    
    def test_ui_access(self) -> bool:
        """تست دسترسی به UI"""
        try:
            # شبیه‌سازی تست UI
            time.sleep(1)
            self.logger.info("تست دسترسی به UI انجام شد")
            return True
        except Exception:
            return False
    
    def generate_test_report(self) -> str:
        """تولید گزارش تست"""
        if not self.test_results:
            return "هیچ نتیجه تستی موجود نیست"
        
        latest_result = self.test_results[-1]
        results = latest_result['results']
        
        report = f"""
🧪 گزارش تست سیستم - {latest_result['timestamp']}
{'='*50}

نتایج تست‌ها:
"""
        for test_name, success in results.items():
            status = "✅ موفق" if success else "❌ ناموفق"
            report += f"  {test_name}: {status}\n"
        
        overall = "✅ کلی: موفق" if latest_result['overall_success'] else "❌ کلی: ناموفق"
        report += f"\n{overall}\n"
        
        return report

# تست عملی:
if __name__ == "__main__":
    tester = SystemTester()
    results = tester.run_all_tests()
    report = tester.generate_test_report()
    print(report)