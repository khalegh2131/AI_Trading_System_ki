# D:\AI\AI_Trading_System_ki\vpn\subscription_parser.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import base64
import json
from typing import List, Dict
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

class SubscriptionParser:
    def __init__(self):
        self.logger = get_logger("SubscriptionParser")
        
    def fetch_subscription(self, url: str) -> List[str]:
        """دریافت لینک‌های اشتراک از URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # decode base64
                decoded = base64.b64decode(response.text).decode('utf-8')
                links = decoded.strip().split('\n')
                self.logger.info(f"دریافت شد {len(links)} لینک از {url}")
                return links
            else:
                self.logger.error(f"خطا در دریافت {url}: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"خطا در دریافت {url}: {str(e)}")
            return []
    
    def parse_vmess_link(self, link: str) -> Dict:
        """پارس کردن لینک vmess"""
        try:
            if not link.startswith('vmess://'):
                return {}
                
            encoded = link[8:]  # حذف 'vmess://'
            decoded = base64.b64decode(encoded).decode('utf-8')
            config = json.loads(decoded)
            return config
        except Exception as e:
            self.logger.error(f"خطا در پارس کردن لینک: {str(e)}")
            return {}
    
    def parse_all_links(self, links: List[str]) -> List[Dict]:
        """پارس کردن همه لینک‌ها"""
        parsed_configs = []
        for link in links:
            if link.startswith('vmess://'):
                config = self.parse_vmess_link(link)
                if config:
                    config['raw_link'] = link
                    parsed_configs.append(config)
            # می‌تونی برای vless و دیگری‌ها هم اضافه کنی
                    
        self.logger.info(f"پارس شد {len(parsed_configs)} کانفیگ")
        return parsed_configs

# تست عملی:
if __name__ == "__main__":
    parser = SubscriptionParser()
    
    # لینک نمونه (می‌تونی عوض کنی)
    test_links = [
        "vmess://eyJhZGQiOiIxMjcuMC4wLjEiLCJhaWQiOiIwIiwiaG9zdCI6IiIsImlkIjoiMTExMTExMTEtMTExMS0xMTExLTExMTEtMTExMTExMTExMTExIiwibmV0Ijoid3MiLCJwYXRoIjoiLyIsInBvcnQiOiI4MCIsInBzIjoiVGVzdCIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ=="
    ]
    
    configs = parser.parse_all_links(test_links)
    print(f"پارس شد {len(configs)} کانفیگ")
    if configs:
        print("اولین کانفیگ:", configs[0])