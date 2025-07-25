# D:\AI\AI_Trading_System_ki\analysis\technical_analyzer.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime

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

class TechnicalAnalyzer:
    def __init__(self):
        self.logger = get_logger("TechnicalAnalyzer")
        
    def calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """محاسبه RSI"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            self.logger.error(f"خطا در محاسبه RSI: {str(e)}")
            return pd.Series([0] * len(prices))
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """محاسبه MACD"""
        try:
            exp1 = prices.ewm(span=fast).mean()
            exp2 = prices.ewm(span=slow).mean()
            macd = exp1 - exp2
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            return macd, signal_line, histogram
        except Exception as e:
            self.logger.error(f"خطا در محاسبه MACD: {str(e)}")
            return pd.Series([0] * len(prices)), pd.Series([0] * len(prices)), pd.Series([0] * len(prices))
    
    def calculate_moving_averages(self, prices: pd.Series, windows: List[int] = [10, 20, 50]) -> Dict:
        """محاسبه میانگین‌های متحرک"""
        try:
            mas = {}
            for window in windows:
                mas[f'SMA_{window}'] = prices.rolling(window=window).mean()
                mas[f'EMA_{window}'] = prices.ewm(span=window).mean()
            return mas
        except Exception as e:
            self.logger.error(f"خطا در محاسبه Moving Averages: {str(e)}")
            return {}
    
    def calculate_bollinger_bands(self, prices: pd.Series, window: int = 20, num_std: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """محاسبه باندهای بولینگر"""
        try:
            ma = prices.rolling(window=window).mean()
            std = prices.rolling(window=window).std()
            upper = ma + (std * num_std)
            lower = ma - (std * num_std)
            return upper, ma, lower
        except Exception as e:
            self.logger.error(f"خطا در محاسبه Bollinger Bands: {str(e)}")
            return pd.Series([0] * len(prices)), pd.Series([0] * len(prices)), pd.Series([0] * len(prices))
    
    def calculate_atr(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """محاسبه ATR (Average True Range)"""
        try:
            high = df['high']
            low = df['low']
            close = df['close']
            
            tr0 = abs(high - low)
            tr1 = abs(high - close.shift())
            tr2 = abs(low - close.shift())
            tr = pd.DataFrame({'tr0': tr0, 'tr1': tr1, 'tr2': tr2}).max(axis=1)
            
            atr = tr.rolling(window=window).mean()
            return atr
        except Exception as e:
            self.logger.error(f"خطا در محاسبه ATR: {str(e)}")
            return pd.Series([0] * len(df))
    
    def calculate_pivot_points(self, df: pd.DataFrame) -> Dict:
        """محاسبه نقاط پیوت"""
        try:
            # برای سادگی، از آخرین داده استفاده می‌کنیم
            if len(df) < 2:
                return {}
                
            prev_high = df['high'].iloc[-2]
            prev_low = df['low'].iloc[-2]
            prev_close = df['close'].iloc[-2]
            
            pivot = (prev_high + prev_low + prev_close) / 3
            resistance1 = (2 * pivot) - prev_low
            support1 = (2 * pivot) - prev_high
            resistance2 = pivot + (prev_high - prev_low)
            support2 = pivot - (prev_high - prev_low)
            
            return {
                'pivot': pivot,
                'r1': resistance1,
                's1': support1,
                'r2': resistance2,
                's2': support2
            }
        except Exception as e:
            self.logger.error(f"خطا در محاسبه Pivot Points: {str(e)}")
            return {}
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        """تولید سیگنال‌های تکنیکال"""
        try:
            signals = []
            if df.empty or len(df) < 20:
                return signals
                
            prices = df['close']
            
            # محاسبه اندیکاتورها
            rsi = self.calculate_rsi(prices)
            macd, signal_line, _ = self.calculate_macd(prices)
            upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands(prices)
            
            # سیگنال RSI
            current_rsi = rsi.iloc[-1]
            if current_rsi > 70:
                signals.append({
                    'indicator': 'RSI',
                    'value': round(current_rsi, 2),
                    'signal': 'SELL',
                    'confidence': 0.7,
                    'reason': f'RSI اشباع خرید ({current_rsi:.2f})'
                })
            elif current_rsi < 30:
                signals.append({
                    'indicator': 'RSI',
                    'value': round(current_rsi, 2),
                    'signal': 'BUY',
                    'confidence': 0.7,
                    'reason': f'RSI اشباع فروش ({current_rsi:.2f})'
                })
            
            # سیگنال MACD
            current_macd = macd.iloc[-1]
            current_signal = signal_line.iloc[-1]
            prev_macd = macd.iloc[-2]
            prev_signal = signal_line.iloc[-2]
            
            # MACD Crossover
            if prev_macd <= prev_signal and current_macd > current_signal:
                signals.append({
                    'indicator': 'MACD',
                    'value': round(current_macd, 4),
                    'signal': 'BUY',
                    'confidence': 0.8,
                    'reason': 'MACD Crossover صعودی'
                })
            elif prev_macd >= prev_signal and current_macd < current_signal:
                signals.append({
                    'indicator': 'MACD',
                    'value': round(current_macd, 4),
                    'signal': 'SELL',
                    'confidence': 0.8,
                    'reason': 'MACD Crossover نزولی'
                })
            
            # سیگنال بولینگر
            current_price = prices.iloc[-1]
            current_upper = upper_bb.iloc[-1]
            current_lower = lower_bb.iloc[-1]
            
            if current_price > current_upper:
                signals.append({
                    'indicator': 'Bollinger Bands',
                    'value': round(current_price, 2),
                    'signal': 'SELL',
                    'confidence': 0.6,
                    'reason': 'شکست بالای باند بالایی'
                })
            elif current_price < current_lower:
                signals.append({
                    'indicator': 'Bollinger Bands',
                    'value': round(current_price, 2),
                    'signal': 'BUY',
                    'confidence': 0.6,
                    'reason': 'شکست پایین باند پایینی'
                })
            
            return signals
        except Exception as e:
            self.logger.error(f"خطا در تولید سیگنال‌ها: {str(e)}")
            return []
    
    def get_analysis_summary(self, df: pd.DataFrame) -> Dict:
        """دریافت خلاصه تحلیل تکنیکال"""
        try:
            if df.empty or len(df) < 20:
                return {'error': 'داده کافی وجود ندارد'}
                
            prices = df['close']
            
            # محاسبه اندیکاتورها
            rsi = self.calculate_rsi(prices).iloc[-1]
            macd, signal_line, _ = self.calculate_macd(prices)
            current_macd = macd.iloc[-1]
            current_signal = signal_line.iloc[-1]
            upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands(prices)
            atr = self.calculate_atr(df).iloc[-1]
            pivot_points = self.calculate_pivot_points(df)
            
            # وضعیت روند
            short_ma = prices.tail(10).mean()
            long_ma = prices.tail(50).mean()
            trend = 'BULLISH' if short_ma > long_ma else 'BEARISH' if short_ma < long_ma else 'NEUTRAL'
            
            return {
                'timestamp': datetime.now().isoformat(),
                'indicators': {
                    'rsi': round(rsi, 2),
                    'macd': round(current_macd, 4),
                    'macd_signal': round(current_signal, 4),
                    'upper_bb': round(upper_bb.iloc[-1], 2),
                    'middle_bb': round(middle_bb.iloc[-1], 2),
                    'lower_bb': round(lower_bb.iloc[-1], 2),
                    'atr': round(atr, 4),
                    'pivot_points': pivot_points
                },
                'trend': trend,
                'current_price': round(prices.iloc[-1], 2),
                'price_change_24h': round(((prices.iloc[-1] / prices.iloc[-24]) - 1) * 100, 2) if len(prices) >= 24 else 0
            }
        except Exception as e:
            self.logger.error(f"خطا در خلاصه تحلیل: {str(e)}")
            return {'error': str(e)}

# مثال استفاده:
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
    
    analyzer = TechnicalAnalyzer()
    
    # تحلیل خلاصه
    summary = analyzer.get_analysis_summary(sample_data)
    print("خلاصه تحلیل تکنیکال:")
    print(summary)
    
    # سیگنال‌ها
    signals = analyzer.generate_signals(sample_data)
    print(f"\nتعداد سیگنال‌ها: {len(signals)}")
    for signal in signals:
        print(f"  {signal['indicator']}: {signal['signal']} - {signal['reason']}")