# D:\AI\AI_Trading_System_ki\api\api_hub.py

import requests
import time
import json
from typing import List, Dict, Optional
import logging
from utils.logger import get_logger

class APIHub:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("APIHub")
        self.apis = self._load_apis()
        self.current_api = None
        self.switch_api()
        
    def _load_apis(self) -> List[Dict]:
        """بارگذاری لیست APIها از فایل تنظیمات"""
        apis = []
        
        # بارگذاری APIهای فارکس
        for forex_api in self.config.get('apis', {}).get('forex', []):
            apis.append({
                'name': forex_api['name'],
                'base_url': forex_api.get('base_url', ''),
                'key': forex_api['key'],
                'secret': forex_api['secret'],
                'type': 'forex',
                'ping_url': forex_api.get('ping_url', '')
            })
            
        # بارگذاری APIهای کریپتو
        for crypto_api in self.config.get('apis', {}).get('crypto', []):
            apis.append({
                'name': crypto_api['name'],
                'base_url': crypto_api.get('base_url', ''),
                'key': crypto_api['key'],
                'secret': crypto_api['secret'],
                'type': 'crypto',
                'ping_url': crypto_api.get('ping_url', 'https://api.binance.com/api/v3/ping')
            })
            
        return apis

    def switch_api(self) -> bool:
        """سوییچ به بهترین API در دسترس"""
        self.logger.info("در حال تست APIها برای اتصال...")
        
        for api in self.apis:
            try:
                ping_url = api.get('ping_url')
                if not ping_url:
                    continue
                    
                # تست اتصال با timeout کم
                response = requests.get(ping_url, timeout=5)
                if response.status_code == 200:
                    self.current_api = api
                    self.logger.info(f"✅ متصل شد به: {api['name']}")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"❌ {api['name']} در دسترس نیست: {str(e)}")
                continue
                
        self.logger.error("⚠️ هیچ APIای در دسترس نیست!")
        return False

    def fetch_ohlcv(self, symbol: str = "BTCUSDT", timeframe: str = "1h", limit: int = 100) -> Optional[List]:
        """دریافت داده OHLCV از API فعلی"""
        if not self.current_api:
            if not self.switch_api():
                return None
                
        try:
            # مسیر داده‌های کندل برای Binance
            if 'binance' in self.current_api['name'].lower():
                url = f"{self.current_api['base_url']}/klines"
                params = {
                    'symbol': symbol,
                    'interval': timeframe,
                    'limit': limit
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # تبدیل به فرمت استاندارد
                    ohlcv = []
                    for item in 
                        ohlcv.append({
                            'timestamp': int(item[0]),
                            'open': float(item[1]),
                            'high': float(item[2]),
                            'low': float(item[3]),
                            'close': float(item[4]),
                            'volume': float(item[5])
                        })
                    return ohlcv
                    
        except Exception as e:
            self.logger.error(f"خطا در دریافت داده از {self.current_api['name']}: {str(e)}")
            # تلاش برای سوییچ API
            if self.switch_api():
                return self.fetch_ohlcv(symbol, timeframe, limit)
                
        return None

# مثال استفاده:
if __name__ == "__main__":
    # بارگذاری config
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # ایجاد API Hub
    api_hub = APIHub(config)
    
    # دریافت داده‌های BTC
    data = api_hub.fetch_ohlcv("BTCUSDT", "1h", 10)
    if data:
        print(f"دریافت شد {len(data)} کندل")
        print(data[0])  # نمایش اولین کندل
    else:
        print("داده‌ای دریافت نشد")