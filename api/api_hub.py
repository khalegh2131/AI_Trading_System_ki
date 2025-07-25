# D:\AI\AI_Trading_System_ki\api\api_hub.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import requests
import time
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
from utils.logger import get_logger

# بررسی وجود فایل encryption_manager.py
try:
    from security.encryption_manager import EncryptionManager
except ImportError:
    # ایجاد یک کلاس جایگزین برای زمانی که فایل وجود ندارد
    class EncryptionManager:
        def encrypt_data(self, data: str) -> str:
            return data  # بدون رمزنگاری
        def decrypt_data(self,  str) -> str:
            return data  # بدون رمزگشایی

class APIHub:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("APIHub")
        self.encryption_manager = EncryptionManager()
        self.apis = self._load_apis()
        self.active_connections = {}
        self.switch_api()
        
    def _load_apis(self) -> List[Dict]:
        """بارگذاری لیست APIها از config و دیتابیس"""
        apis = []
        
        # بارگذاری از config
        for forex_api in self.config.get('apis', {}).get('forex', []):
            apis.append({
                'name': forex_api['name'],
                'base_url': forex_api.get('base_url', ''),
                'key': self.encryption_manager.decrypt_data(forex_api['key']),
                'secret': self.encryption_manager.decrypt_data(forex_api['secret']),
                'type': 'forex',
                'ping_url': forex_api.get('ping_url', ''),
                'use_vpn': forex_api.get('use_vpn', False),
                'status': 'inactive'
            })
            
        for crypto_api in self.config.get('apis', {}).get('crypto', []):
            apis.append({
                'name': crypto_api['name'],
                'base_url': crypto_api.get('base_url', ''),
                'key': self.encryption_manager.decrypt_data(crypto_api['key']),
                'secret': self.encryption_manager.decrypt_data(crypto_api['secret']),
                'type': 'crypto',
                'ping_url': crypto_api.get('ping_url', 'https://api.binance.com/api/v3/ping'),
                'use_vpn': crypto_api.get('use_vpn', False),
                'status': 'inactive'
            })
            
        return apis

    def add_api(self, name: str, api_type: str, base_url: str, key: str, secret: str, 
                ping_url: str = "", use_vpn: bool = False) -> bool:
        """افزودن API جدید"""
        try:
            # رمزنگاری کلیدها
            encrypted_key = self.encryption_manager.encrypt_data(key)
            encrypted_secret = self.encryption_manager.encrypt_data(secret)
            
            new_api = {
                'name': name,
                'base_url': base_url,
                'key': encrypted_key,
                'secret': encrypted_secret,
                'type': api_type,
                'ping_url': ping_url,
                'use_vpn': use_vpn,
                'status': 'inactive'
            }
            
            self.apis.append(new_api)
            self.logger.info(f"✅ API جدید اضافه شد: {name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ خطا در افزودن API {name}: {str(e)}")
            return False

    def switch_api(self) -> bool:
        """سوییچ به بهترین API در دسترس"""
        self.logger.info("در حال تست APIها برای اتصال...")
        
        for api in self.apis:
            try:
                # بررسی نیاز به VPN
                if api.get('use_vpn', False):
                    # اینجا باید کد بررسی VPN باشه
                    pass
                    
                ping_url = api.get('ping_url')
                if not ping_url:
                    continue
                    
                # تست اتصال با timeout کم
                response = requests.get(ping_url, timeout=5)
                if response.status_code == 200:
                    api['status'] = 'active'
                    self.active_connections[api['name']] = api
                    self.logger.info(f"✅ متصل شد به: {api['name']}")
                    return True
                    
            except Exception as e:
                api['status'] = 'inactive'
                self.logger.warning(f"❌ {api['name']} در دسترس نیست: {str(e)}")
                continue
                
        self.logger.error("⚠️ هیچ APIای در دسترس نیست!")
        return False

    def fetch_ohlcv(self, symbol: str = "BTCUSDT", timeframe: str = "1h", 
                   limit: int = 100, api_name: str = None) -> Optional[pd.DataFrame]:
        """دریافت داده OHLCV از API مشخص یا فعلی"""
        # انتخاب API
        target_api = None
        if api_name and api_name in self.active_connections:
            target_api = self.active_connections[api_name]
        elif self.active_connections:
            target_api = list(self.active_connections.values())[0]
        else:
            if not self.switch_api():
                return None
            target_api = list(self.active_connections.values())[0]
                
        try:
            # رمزگشایی کلیدها
            api_key = self.encryption_manager.decrypt_data(target_api['key'])
            
            # مسیر داده‌های کندل برای Binance
            if 'binance' in target_api['name'].lower():
                url = f"{target_api['base_url']}/api/v3/klines"
                params = {
                    'symbol': symbol,
                    'interval': timeframe,
                    'limit': limit
                }
                
                headers = {'X-MBX-APIKEY': api_key}
                response = requests.get(url, params=params, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # تبدیل به DataFrame
                    df = pd.DataFrame(data)
                    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                 'close_time', 'quote_asset_volume', 'number_of_trades',
                                 'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore']
                    
                    # انتخاب ستون‌های مورد نیاز
                    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
                    
                    # تبدیل انواع داده
                    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
                    for col in numeric_columns:
                        df[col] = pd.to_numeric(df[col])
                    
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    return df
                    
        except Exception as e:
            self.logger.error(f"خطا در دریافت داده از {target_api['name']}: {str(e)}")
            # تلاش برای سوییچ API
            if self.switch_api():
                return self.fetch_ohlcv(symbol, timeframe, limit)
                
        return None

    def download_historical_data(self, symbol: str, timeframe: str, 
                               start_date: str, end_date: str, 
                               api_name: str = None) -> Optional[pd.DataFrame]:
        """دانلود داده‌های تاریخی برای یادگیری"""
        try:
            # تبدیل تاریخ‌ها
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            all_data = []
            current_dt = start_dt
            
            # دانلود داده‌ها به صورت چانکی
            while current_dt < end_dt:
                # محاسبه تعداد کندل‌های مورد نیاز
                if timeframe == '1h':
                    limit = min(1000, int((end_dt - current_dt).total_seconds() / 3600))
                elif timeframe == '1d':
                    limit = min(1000, (end_dt - current_dt).days)
                else:
                    limit = 1000
                    
                # دریافت داده
                df = self.fetch_ohlcv(symbol, timeframe, limit, api_name)
                if df is not None and not df.empty:
                    all_data.append(df)
                    # بروزرسانی تاریخ فعلی
                    current_dt = df['timestamp'].max()
                else:
                    break
                    
                # تاخیر برای جلوگیری از محدودیت‌های API
                time.sleep(0.1)
            
            if all_data:  # ✅ اصلاح شد
                # ترکیب همه داده‌ها
                final_df = pd.concat(all_data, ignore_index=True)
                # حذف تکراری‌ها
                final_df = final_df.drop_duplicates(subset=['timestamp']).sort_values('timestamp')
                
                self.logger.info(f"✅ دانلود شد {len(final_df)} کندل برای {symbol}")
                return final_df
            else:
                self.logger.warning(f"⚠️ داده‌ای برای {symbol} یافت نشد")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ خطا در دانلود داده‌های تاریخی: {str(e)}")
            return None

    def get_api_status(self) -> Dict:
        """دریافت وضعیت همه APIها"""
        status = {}
        for api in self.apis:
            status[api['name']] = {
                'type': api['type'],
                'status': api.get('status', 'unknown'),
                'use_vpn': api.get('use_vpn', False)
            }
        return status

    def place_order(self, symbol: str, side: str, quantity: float, 
                   price: float = None, api_name: str = None) -> Optional[Dict]:
        """ثبت سفارش (برای نسخه‌های بعدی)"""
        # پیاده‌سازی در آینده
        pass

    def get_balance(self, api_name: str = None) -> Optional[Dict]:
        """دریافت موجودی (برای نسخه‌های بعدی)"""
        # پیاده‌سازی در آینده
        pass

# مثال استفاده:
if __name__ == "__main__":
    # بارگذاری config
    import yaml
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        # config پیش‌فرض
        config = {
            "apis": {
                "crypto": [
                    {
                        "name": "Binance",
                        "base_url": "https://api.binance.com",
                        "key": "ENCRYPTED_KEY",
                        "secret": "ENCRYPTED_SECRET",
                        "ping_url": "https://api.binance.com/api/v3/ping",
                        "use_vpn": False
                    }
                ]
            }
        }
        # ذخیره config پیش‌فرض
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    # ایجاد API Hub
    api_hub = APIHub(config)
    
    # دریافت داده‌های BTC
    data = api_hub.fetch_ohlcv("BTCUSDT", "1h", 10)
    if data is not None and not data.empty:
        print(f"دریافت شد {len(data)} کندل")
        print(data.head())
    else:
        print("داده‌ای دریافت نشد")