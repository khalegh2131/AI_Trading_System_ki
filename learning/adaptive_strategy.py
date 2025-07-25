# D:\AI\AI_Trading_System_ki\learning\adaptive_strategy.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import logging
from learning.market_analyzer import MarketAnalyzer

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

class AdaptiveStrategy:
    def __init__(self):
        self.logger = get_logger("AdaptiveStrategy")
        self.market_analyzer = MarketAnalyzer()
        self.current_strategy = "default"
        self.performance_history = []
        
    def select_strategy(self, market_data: pd.DataFrame) -> str:
        """انتخاب استراتژی مناسب بر اساس شرایط بازار"""
        # تحلیل بازار
        trend_analysis = self.market_analyzer.analyze_market_trend(market_data)
        regime_analysis = self.market_analyzer.detect_market_regimes(market_data)
        
        current_trend = trend_analysis.get('trend', 'unknown')
        current_regime = regime_analysis.get('current_regime', 'unknown')
        volatility = regime_analysis.get('volatility', 0)
        
        # تصمیم‌گیری بر اساس شرایط
        if current_trend == 'bullish' and current_regime == 'neutral':
            strategy = "momentum"
        elif current_trend == 'bearish':
            strategy = "mean_reversion"
        elif volatility > 50:  # نوسان بالا
            strategy = "scalping"
        elif current_regime == 'overbought':
            strategy = "short_swing"
        elif current_regime == 'oversold':
            strategy = "long_swing"
        else:
            strategy = "default"
        
        # لاگ کردن تصمیم
        self.logger.info(f"انتخاب استراتژی: {strategy} - روند: {current_trend}, رژیم: {current_regime}")
        
        self.current_strategy = strategy
        return strategy
    
    def generate_signal(self, market_data: pd.DataFrame, strategy: str = None) -> Dict:
        """تولید سیگنال معاملاتی"""
        if strategy is None:
            strategy = self.select_strategy(market_data)
            
        # آخرین داده
        latest_data = market_data.iloc[-1]
        
        # سیگنال بر اساس استراتژی
        if strategy == "momentum":
            signal = self._momentum_signal(market_data)
        elif strategy == "mean_reversion":
            signal = self._mean_reversion_signal(market_data)
        elif strategy == "scalping":
            signal = self._scalping_signal(market_data)
        elif strategy == "short_swing":
            signal = self._short_swing_signal(market_data)
        elif strategy == "long_swing":
            signal = self._long_swing_signal(market_data)
        else:
            signal = self._default_signal(market_data)
            
        return {
            'strategy': strategy,
            'signal': signal['action'],
            'confidence': signal['confidence'],
            'reason': signal['reason'],
            'timestamp': latest_data['timestamp'] if 'timestamp' in latest_data else None
        }
    
    def _momentum_signal(self, data: pd.DataFrame) -> Dict:
        """سیگنال بر اساس استراتژی مومنتوم"""
        if len(data) < 2:
            return {'action': 'hold', 'confidence': 0, 'reason': 'insufficient data'}
            
        current_price = data['close'].iloc[-1]
        prev_price = data['close'].iloc[-2]
        short_ma = data['close'].tail(10).mean()
        long_ma = data['close'].tail(50).mean()
        
        if current_price > short_ma > long_ma and current_price > prev_price:
            return {
                'action': 'buy',
                'confidence': 0.8,
                'reason': 'مومنتوم صعودی قوی'
            }
        elif current_price < short_ma < long_ma and current_price < prev_price:
            return {
                'action': 'sell',
                'confidence': 0.8,
                'reason': 'مومنتوم نزولی قوی'
            }
        else:
            return {
                'action': 'hold',
                'confidence': 0.3,
                'reason': 'عدم روند مشخص'
            }
    
    def _mean_reversion_signal(self, data: pd.DataFrame) -> Dict:
        """سیگنال بر اساس استراتژی بازگشت به میانگین"""
        if len(data) < 20:
            return {'action': 'hold', 'confidence': 0, 'reason': 'insufficient data'}
            
        current_price = data['close'].iloc[-1]
        ma_20 = data['close'].tail(20).mean()
        std_20 = data['close'].tail(20).std()
        upper_band = ma_20 + (2 * std_20)
        lower_band = ma_20 - (2 * std_20)
        
        if current_price > upper_band:
            return {
                'action': 'sell',
                'confidence': 0.7,
                'reason': 'قیمت بالای باند بالایی'
            }
        elif current_price < lower_band:
            return {
                'action': 'buy',
                'confidence': 0.7,
                'reason': 'قیمت پایین باند پایینی'
            }
        else:
            return {
                'action': 'hold',
                'confidence': 0.2,
                'reason': 'قیمت در محدوده نرمال'
            }
    
    def _scalping_signal(self, data: pd.DataFrame) -> Dict:
        """سیگنال برای استراتژی اسکالپینگ"""
        if len(data) < 5:
            return {'action': 'hold', 'confidence': 0, 'reason': 'insufficient data'}
            
        price_changes = data['close'].pct_change().tail(5)
        avg_change = price_changes.mean()
        
        if avg_change > 0.005:  # 0.5% در 5 کندل
            return {
                'action': 'buy',
                'confidence': 0.6,
                'reason': 'روند صعودی کوتاه‌مدت'
            }
        elif avg_change < -0.005:
            return {
                'action': 'sell',
                'confidence': 0.6,
                'reason': 'روند نزولی کوتاه‌مدت'
            }
        else:
            return {
                'action': 'hold',
                'confidence': 0.1,
                'reason': 'نوسان کم'
            }
    
    def _default_signal(self, data: pd.DataFrame) -> Dict:
        """سیگنال پیش‌فرض"""
        return {
            'action': 'hold',
            'confidence': 0.1,
            'reason': 'استراتژی پیش‌فرض'
        }
    
    # سیگنال‌های دیگر
    def _short_swing_signal(self, data: pd.DataFrame) -> Dict:
        return {
            'action': 'sell',
            'confidence': 0.6,
            'reason': 'بازار اشباع خرید'
        }
    
    def _long_swing_signal(self, data: pd.DataFrame) -> Dict:
        return {
            'action': 'buy',
            'confidence': 0.6,
            'reason': 'بازار اشباع فروش'
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
    
    strategy = AdaptiveStrategy()
    
    # تولید سیگنال
    signal = strategy.generate_signal(sample_data)
    print("سیگنال تولید شده:", signal)