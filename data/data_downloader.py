# D:\AI\AI_Trading_System_ki\data\data_downloader.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pandas as pd
import requests
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

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

class DataDownloader:
    def __init__(self, data_dir: str = "data/historical"):
        self.data_dir = data_dir
        self.logger = get_logger("DataDownloader")
        self._create_data_directory()
        
    def _create_data_directory(self):
        """ایجاد پوشه‌های مورد نیاز"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            self.logger.info(f"پوشه داده‌ها ایجاد شد: {self.data_dir}")
            
        # پوشه‌های زیرمجموعه
        sub_dirs = ["crypto", "forex", "stocks", "indices"]
        for sub_dir in sub_dirs:
            full_path = os.path.join(self.data_dir, sub_dir)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                
    def download_binance_data(self, symbol: str, timeframe: str, 
                            start_date: str, end_date: str) -> Optional[str]:
        """دانلود داده‌های Binance"""
        try:
            self.logger.info(f"شروع دانلود {symbol} از {start_date} تا {end_date}")
            
            # تبدیل تاریخ‌ها
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            all_data = []
            current_time = int(start_dt.timestamp() * 1000)
            end_time = int(end_dt.timestamp() * 1000)
            
            # دانلود داده‌ها به صورت چانکی
            while current_time < end_time:
                url = "https://api.binance.com/api/v3/klines"
                params = {
                    'symbol': symbol,
                    'interval': timeframe,
                    'startTime': current_time,
                    'limit': 1000  # حداکثر 1000 کندل
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code != 200:
                    self.logger.error(f"خطا در دریافت داده: {response.status_code}")
                    break
                    
                data = response.json()
                if not data:
                    break
                    
                all_data.extend(data)
                
                # بروزرسانی زمان برای چانک بعدی
                current_time = data[-1][0] + 1
                
                # تاخیر برای جلوگیری از محدودیت‌های API
                time.sleep(0.1)
                
                self.logger.info(f"دانلود شد {len(all_data)} کندل...")
            
            if all_data:
                # تبدیل به DataFrame
                df = pd.DataFrame(all_data)
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
                
                # ذخیره فایل
                filename = f"{symbol}_{timeframe}_{start_date}_{end_date}.csv"
                filepath = os.path.join(self.data_dir, "crypto", filename)
                df.to_csv(filepath, index=False)
                
                self.logger.info(f"✅ داده‌ها ذخیره شدند: {filepath}")
                self.logger.info(f"📊 تعداد کل کندل‌ها: {len(df)}")
                
                return filepath
            else:
                self.logger.warning("داده‌ای یافت نشد")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ خطا در دانلود داده‌های {symbol}: {str(e)}")
            return None
    
    def download_multiple_symbols(self, symbols: List[str], timeframe: str,
                                start_date: str, end_date: str) -> Dict:
        """دانلود داده‌های چندین نماد"""
        results = {}
        
        for symbol in symbols:
            self.logger.info(f"دانلود {symbol}...")
            filepath = self.download_binance_data(symbol, timeframe, start_date, end_date)
            results[symbol] = filepath
            
            # تاخیر بین دانلودها
            time.sleep(1)
            
        return results
    
    def create_dataset_for_ai(self, symbol: str, timeframe: str,
                            start_date: str, end_date: str) -> Optional[str]:
        """ایجاد داده‌های مناسب برای یادگیری AI"""
        try:
            # دانلود داده‌ها
            filepath = self.download_binance_data(symbol, timeframe, start_date, end_date)
            if not filepath:
                return None
                
            # بارگذاری داده‌ها
            df = pd.read_csv(filepath)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # ایجاد ویژگی‌های تکنیکال
            df = self._add_technical_indicators(df)
            
            # ایجاد برچسب‌ها برای یادگیری
            df = self._create_labels(df)
            
            # ذخیره داده‌های آماده برای AI
            ai_filename = f"{symbol}_{timeframe}_ai_ready.csv"
            ai_filepath = os.path.join(self.data_dir, "crypto", ai_filename)
            df.to_csv(ai_filepath, index=False)
            
            self.logger.info(f"✅ داده‌های آماده برای AI: {ai_filepath}")
            return ai_filepath
            
        except Exception as e:
            self.logger.error(f"❌ خطا در ایجاد داده‌های AI: {str(e)}")
            return None
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """افزودن اندیکاتورهای تکنیکال"""
        df = df.copy()
        
        # Moving Averages
        df['ma_10'] = df['close'].rolling(window=10).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()
        df['ma_200'] = df['close'].rolling(window=200).mean()
        
        # RSI
        df['rsi'] = self._calculate_rsi(df['close'])
        
        # MACD
        df['macd'], df['macd_signal'] = self._calculate_macd(df['close'])
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_upper'], df['bb_lower'] = self._calculate_bollinger_bands(df['close'])
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # Volatility
        df['volatility'] = df['close'].pct_change().rolling(window=20).std()
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """محاسبه RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series) -> tuple:
        """محاسبه MACD"""
        exp1 = prices.ewm(span=12).mean()
        exp2 = prices.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        return macd, signal
    
    def _calculate_bollinger_bands(self, prices: pd.Series, window: int = 20) -> tuple:
        """محاسبه باندهای بولینگر"""
        ma = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper = ma + (std * 2)
        lower = ma - (std * 2)
        return upper, lower
    
    def _create_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """ایجاد برچسب‌ها برای یادگیری"""
        df = df.copy()
        
        # برچسب‌های قیمت آینده
        df['future_price_1h'] = df['close'].shift(-1)
        df['future_price_24h'] = df['close'].shift(-24)
        
        # برچسب‌های بازده
        df['return_1h'] = (df['future_price_1h'] - df['close']) / df['close']
        df['return_24h'] = (df['future_price_24h'] - df['close']) / df['close']
        
        # برچسب‌های خرید/فروش
        df['signal_1h'] = df['return_1h'].apply(lambda x: 1 if x > 0.01 else (0 if x < -0.01 else 2))
        df['signal_24h'] = df['return_24h'].apply(lambda x: 1 if x > 0.02 else (0 if x < -0.02 else 2))
        
        return df

# مثال استفاده:
if __name__ == "__main__":
    downloader = DataDownloader()
    
    # دانلود داده‌های یک نماد
    # filepath = downloader.download_binance_data("BTCUSDT", "1h", "2023-01-01", "2023-12-31")
    
    # دانلود داده‌های چند نماد
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    # results = downloader.download_multiple_symbols(symbols, "1h", "2023-01-01", "2023-12-31")
    
    # ایجاد داده‌های آماده برای AI
    ai_data = downloader.create_dataset_for_ai("BTCUSDT", "1h", "2023-01-01", "2023-12-31")
    
    if ai_data:
        print(f"✅ داده‌های AI آماده شد: {ai_data}")
    else:
        print("❌ خطا در ایجاد داده‌های AI")