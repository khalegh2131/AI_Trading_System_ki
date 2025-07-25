# D:\AI\AI_Trading_System_ki\integration\data_pipeline.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import time

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

class DataPipeline:
    def __init__(self, api_hub=None):
        self.logger = get_logger("DataPipeline")
        self.api_hub = api_hub
        self.cache = {}  # کش داده‌ها
        
    def fetch_market_data(self, symbol: str = "BTCUSDT", timeframe: str = "1h", 
                         limit: int = 100) -> Optional[pd.DataFrame]:
        """دریافت داده‌های بازار"""
        cache_key = f"{symbol}_{timeframe}_{limit}"
        
        # بررسی کش
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 60:  # کش 1 دقیقه
                self.logger.info("داده‌ها از کش بارگذاری شد")
                return cached_data
        
        try:
            # استفاده از API Hub اگر موجود باشد
            if self.api_hub:
                raw_data = self.api_hub.fetch_ohlcv(symbol, timeframe, limit)
                if raw_data:
                    df = self._convert_to_dataframe(raw_data)
                    # ذخیره در کش
                    self.cache[cache_key] = (df, time.time())
                    return df
            
            # در غیر اینصورت داده‌های نمونه
            df = self._generate_sample_data(symbol, timeframe, limit)
            self.cache[cache_key] = (df, time.time())
            return df
            
        except Exception as e:
            self.logger.error(f"خطا در دریافت داده‌های بازار: {str(e)}")
            return None
    
    def _convert_to_dataframe(self, raw_data: List) -> pd.DataFrame:
        """تبدیل داده‌های خام به DataFrame"""
        df = pd.DataFrame(raw_data)
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
    
    def _generate_sample_data(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        """تولید داده‌های نمونه"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=limit)
        dates = pd.date_range(start=start_time, end=end_time, periods=limit)
        
        # تولید داده‌های شبه واقعی
        base_price = 50000 + np.random.normal(0, 1000)
        prices = [base_price]
        
        for i in range(1, limit):
            change = np.random.normal(0, 0.02)  # تغییر 2% در هر کندل
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        df = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
            'close': prices,
            'volume': np.random.uniform(1000, 5000, limit)
        })
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """پیش‌پردازش داده‌ها"""
        if df is None or df.empty:
            return df
            
        df_processed = df.copy()
        
        # محاسبه بازده
        df_processed['return'] = df_processed['close'].pct_change()
        
        # میانگین‌های متحرک
        df_processed['ma_10'] = df_processed['close'].rolling(window=10).mean()
        df_processed['ma_50'] = df_processed['close'].rolling(window=50).mean()
        
        # RSI
        df_processed['rsi'] = self._calculate_rsi(df_processed['close'])
        
        # MACD
        df_processed['macd'], df_processed['macd_signal'] = self._calculate_macd(df_processed['close'])
        
        # حذف ردیف‌های NaN
        df_processed = df_processed.dropna()
        
        self.logger.info(f"داده‌ها پیش‌پردازش شدند: {len(df_processed)} ردیف")
        return df_processed
    
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
    
    def get_latest_features(self, symbol: str = "BTCUSDT") -> Optional[np.ndarray]:
        """دریافت ویژگی‌های آخرین داده برای مدل"""
        df = self.fetch_market_data(symbol, "1h", 50)
        if df is None or len(df) < 20:
            return None
            
        df_processed = self.preprocess_data(df)
        if df_processed is None or df_processed.empty:
            return None
            
        # استخراج ویژگی‌های آخرین ردیف
        latest_row = df_processed.iloc[-1]
        features = [
            latest_row['close'] / latest_row['ma_10'],
            latest_row['close'] / latest_row['ma_50'],
            latest_row['rsi'] / 100,
            latest_row['macd'],
            latest_row['macd_signal'],
            latest_row['return'],
            latest_row['volume'] / df_processed['volume'].mean()
        ]
        
        return np.array(features).reshape(1, -1)

# تست عملی:
if __name__ == "__main__":
    pipeline = DataPipeline()
    
    # دریافت داده‌های نمونه
    data = pipeline.fetch_market_data("BTCUSDT", "1h", 20)
    print(f"داده‌های دریافت شده: {len(data)} ردیف")
    print(data.head())
    
    # پیش‌پردازش
    processed_data = pipeline.preprocess_data(data)
    print(f"داده‌های پیش‌پردازش شده: {len(processed_data)} ردیف")
    
    # ویژگی‌های مدل
    features = pipeline.get_latest_features("BTCUSDT")
    if features is not None:
        print(f"ویژگی‌های مدل: {features.shape}")