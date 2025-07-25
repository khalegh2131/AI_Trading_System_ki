# D:\AI\AI_Trading_System_ki\learning\market_analyzer.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List

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

class MarketAnalyzer:
    def __init__(self):
        self.logger = get_logger("MarketAnalyzer")
        
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """محاسبه اندیکاتورهای تکنیکال"""
        df = data.copy()
        
        # Moving Averages
        df['MA_10'] = df['close'].rolling(window=10).mean()
        df['MA_50'] = df['close'].rolling(window=50).mean()
        
        # RSI
        df['RSI'] = self._calculate_rsi(df['close'])
        
        # MACD
        df['MACD'], df['MACD_signal'] = self._calculate_macd(df['close'])
        
        # Bollinger Bands
        df['BB_upper'], df['BB_lower'] = self._calculate_bollinger_bands(df['close'])
        
        # Volume MA
        df['Volume_MA'] = df['volume'].rolling(window=20).mean()
        
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
    
    def detect_market_regimes(self, data: pd.DataFrame) -> Dict:
        """تشخیص رژیم‌های بازار"""
        df = self.calculate_technical_indicators(data)
        
        regimes = []
        for i in range(len(df)):
            if pd.isna(df['RSI'].iloc[i]):
                regimes.append('unknown')
                continue
                
            rsi = df['RSI'].iloc[i]
            if rsi > 70:
                regimes.append('overbought')
            elif rsi < 30:
                regimes.append('oversold')
            else:
                regimes.append('neutral')
        
        df['regime'] = regimes
        
        # آمار رژیم‌ها
        regime_counts = df['regime'].value_counts()
        
        return {
            'current_regime': regimes[-1] if regimes else 'unknown',
            'regime_distribution': regime_counts.to_dict(),
            'volatility': df['close'].pct_change().std() * np.sqrt(252) * 100  # سالانه
        }
    
    def analyze_market_trend(self, data: pd.DataFrame) -> Dict:
        """تحلیل روند بازار"""
        if len(data) < 50:
            return {'trend': 'insufficient_data'}
            
        # محاسبه میانگین‌های متحرک
        short_ma = data['close'].tail(10).mean()
        long_ma = data['close'].tail(50).mean()
        
        # محاسبه روند
        price_change = (data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0] * 100
        
        if short_ma > long_ma and price_change > 2:
            trend = 'bullish'
        elif short_ma < long_ma and price_change < -2:
            trend = 'bearish'
        else:
            trend = 'sideways'
            
        return {
            'trend': trend,
            'price_change_pct': round(price_change, 2),
            'short_ma': round(short_ma, 2),
            'long_ma': round(long_ma, 2)
        }

# تست عملی:
if __name__ == "__main__":
    # ایجاد داده‌های نمونه
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    sample_data = pd.DataFrame({
        'timestamp': dates,
        'open': np.random.uniform(40000, 50000, 100),
        'high': np.random.uniform(41000, 51000, 100),
        'low': np.random.uniform(39000, 49000, 100),
        'close': np.random.uniform(40000, 50000, 100),
        'volume': np.random.uniform(1000, 5000, 100)
    })
    
    analyzer = MarketAnalyzer()
    
    # تحلیل روند
    trend_analysis = analyzer.analyze_market_trend(sample_data)
    print("تحلیل روند:", trend_analysis)
    
    # تشخیص رژیم‌ها
    regime_analysis = analyzer.detect_market_regimes(sample_data)
    print("تحلیل رژیم:", regime_analysis)