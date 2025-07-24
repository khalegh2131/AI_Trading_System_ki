# D:\AI\AI_Trading_System_ki\vpn\vpn_scanner.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
import json
from typing import List, Dict, Optional
import subprocess
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

class VPNScanner:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.logger = get_logger("VPNScanner")
        self.subscription_urls = self.config.get('vpn', {}).get('subscription_urls', [])
        self.servers = []
        self.current_server = None
        
    def load_subscriptions(self) -> List[Dict]:
        """بارگذاری لینک‌های اشتراک V2Ray"""
        all_servers = []
        
        for url in self.subscription_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # فرض: لینک‌ها در فرمت base64 هستند
                    import base64
                    decoded = base64.b64decode(response.text).decode('utf-8')
                    servers = decoded.strip().split('\n')
                    
                    for server in servers:
                        if server.startswith('vmess://') or server.startswith('vless://'):
                            all_servers.append({
                                'config': server,
                                'source': url,
                                'status': 'unknown'
                            })
                            
            except Exception as e:
                self.logger.error(f"خطا در بارگذاری {url}: {str(e)}")
                
        self.servers = all_servers
        self.logger.info(f"بارگذاری شد {len(all_servers)} سرور")
        return all_servers
    
    def test_server_speed(self, server_config: str) -> float:
        """تست سرعت سرور (واحد: ms)"""
        try:
            start_time = time.time()
            # تست با یک سرور عمومی (می‌تونی تغییر بدی)
            test_url = "https://httpbin.org/delay/1"
            response = requests.get(test_url, timeout=5)
            end_time = time.time()
            
            if response.status_code == 200:
                return (end_time - start_time) * 1000  # تبدیل به میلی‌ثانیه
            else:
                return float('inf')  # ناموفق
                
        except Exception:
            return float('inf')  # ناموفق
    
    def find_best_server(self) -> Optional[Dict]:
        """پیدا کردن بهترین سرور بر اساس سرعت"""
        if not self.servers:
            self.load_subscriptions()
            
        best_server = None
        best_time = float('inf')
        
        self.logger.info("در حال تست سرورها...")
        for server in self.servers[:10]:  # فقط 10 تا اولی رو تست کن
            speed = self.test_server_speed(server['config'])
            server['response_time'] = speed
            
            if speed < best_time:
                best_time = speed
                best_server = server
                
        if best_server:
            self.current_server = best_server
            self.logger.info(f"بهترین سرور: {best_time:.2f}ms")
            
        return best_server
    
    def connect_to_server(self, server: Dict) -> bool:
        """اتصال به سرور (شبیه‌سازی)"""
        try:
            self.logger.info(f"در حال اتصال به سرور...")
            # اینجا باید کد واقعی اتصال به V2Ray باشه
            # برای حالا فقط شبیه‌سازی
            time.sleep(2)  # شبیه‌سازی زمان اتصال
            self.current_server = server
            self.logger.info("✅ اتصال موفق")
            return True
        except Exception as e:
            self.logger.error(f"❌ خطا در اتصال: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """قطع اتصال (شبیه‌سازی)"""
        try:
            self.logger.info("در حال قطع اتصال...")
            time.sleep(1)
            self.current_server = None
            self.logger.info("✅ اتصال قطع شد")
            return True
        except Exception as e:
            self.logger.error(f"❌ خطا در قطع اتصال: {str(e)}")
            return False
    
    def get_status(self) -> Dict:
        """دریافت وضعیت فعلی VPN"""
        return {
            'connected': self.current_server is not None,
            'current_server': self.current_server,
            'total_servers': len(self.servers)
        }

# تست عملی:
if __name__ == "__main__":
    # تنظیمات نمونه
    config = {
        'vpn': {
            'subscription_urls': [
                'https://raw.githubusercontent.com/freefq/free/master/v2'
            ]
        }
    }
    
    scanner = VPNScanner(config)
    servers = scanner.load_subscriptions()
    print(f"تعداد سرورها: {len(servers)}")
    
    if servers:
        best = scanner.find_best_server()
        if best:
            print(f"بهترین سرور: {best.get('response_time', 'N/A')}ms")