# D:\AI\AI_Trading_System_ki\learning\feature_engineering.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from typing import Dict, List
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

class FeatureEngineer:
    def __init__(self):
        self.logger = get_logger("FeatureEngineer")
        
    def create_technical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """ایجاد ویژگی‌های تکنیکال"""
        df = data.copy()
        
        # قیمت‌های نرمال‌شده
        df['price_change'] = df['close'].pct_change()
        df['price_change_2'] = df['close'].pct_change(periods=2)
        df['price_change_5'] = df['close'].pct_change(periods=5)
        
        # Moving Averages
        for window in [5, 10, 20, 50]:
            df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
            df[f'ma_{window}_ratio'] = df['close'] / df[f'ma_{window}']
        
        # RSI
        df['rsi'] = self._calculate_rsi(df['close'])
        
        # MACD
        df['macd'], df['macd_signal'] = self._calculate_macd(df['close'])
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_upper'], df['bb_lower'] = self._calculate_bollinger_bands(df['close'])
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # Volume Features
        df['volume_change'] = df['volume'].pct_change()
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Volatility
        df['volatility'] = df['close'].pct_change().rolling(window=20).std()
        df['volatility_ma'] = df['volatility'].rolling(window=20).mean()
        df['volatility_ratio'] = df['volatility'] / df['volatility_ma']
        
        return df
    
    def create_market_regime_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """ایجاد ویژگی‌های رژیم بازار"""
        df = data.copy()
        
        # روند قیمت
        df['trend_5'] = self._calculate_trend(df['close'], 5)
        df['trend_20'] = self._calculate_trend(df['close'], 20)
        df['trend_50'] = self._calculate_trend(df['close'], 50)
        
        # نوسان بازار
        df['market_regime_volatility'] = self._classify_volatility(df['close'])
        
        # قدرت روند
        df['trend_strength'] = self._calculate_trend_strength(df['close'])
        
        return df
    
    def create_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """ایجاد ویژگی‌های زمانی"""
        df = data.copy()
        
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['hour'] = df['datetime'].dt.hour
            df['day_of_week'] = df['datetime'].dt.dayofweek
            df['day_of_month'] = df['datetime'].dt.day
            df['month'] = df['datetime'].dt.month
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
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
    
    def _calculate_trend(self, prices: pd.Series, window: int = 20) -> pd.Series:
        """محاسبه روند"""
        return (prices / prices.shift(window)) - 1
    
    def _classify_volatility(self, prices: pd.Series, window: int = 20) -> pd.Series:
        """طبقه‌بندی نوسان"""
        volatility = prices.pct_change().rolling(window=window).std() * np.sqrt(252)
        
        # طبقه‌بندی نوسان
        conditions = [
            volatility < 0.2,      # کم
            volatility < 0.4,      # متوسط
            volatility >= 0.4      # زیاد
        ]
        choices = [0, 1, 2]
        return np.select(conditions, choices, default=1)
    
    def _calculate_trend_strength(self, prices: pd.Series, window: int = 20) -> pd.Series:
        """محاسبه قدرت روند"""
        # استفاده از شیب رگرسیون خطی
        def linear_slope(series):
            if len(series) < 2:
                return 0
            x = np.arange(len(series))
            slope = np.polyfit(x, series, 1)[0]
            return slope
        
        return prices.rolling(window=window).apply(linear_slope, raw=True)

# تست عملی:
if __name__ == "__main__":
    # ایجاد داده‌های نمونه
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    sample_data = pd.DataFrame({
        'timestamp': dates.astype(np.int64) // 10**9 * 1000,  # میلی‌ثانیه
        'open': np.random.uniform(40000, 50000, 100),
        'high': np.random.uniform(41000, 51000, 100),
        'low': np.random.uniform(39000, 49000, 100),
        'close': np.random.uniform(40000, 50000, 100),
        'volume': np.random.uniform(1000, 5000, 100)
    })
    
    engineer = FeatureEngineer()
    
    # ایجاد ویژگی‌ها
    technical_features = engineer.create_technical_features(sample_data)
    regime_features = engineer.create_market_regime_features(technical_features)
    time_features = engineer.create_time_features(regime_features)
    
    print(f"تعداد ویژگی‌ها: {len(time_features.columns)}")
    print("ویژگی‌های ایجاد شده:")
    print(time_features.columns.tolist()[-10:])  # 10 تای آخر