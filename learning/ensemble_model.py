# D:\AI\AI_Trading_System_ki\learning\ensemble_model.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging
from learning.advanced_rl import AdvancedRLAgent
from learning.adaptive_strategy import AdaptiveStrategy

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

class EnsembleModel:
    def __init__(self, state_size: int = 20, action_size: int = 3):
        self.logger = get_logger("EnsembleModel")
        self.state_size = state_size
        self.action_size = action_size
        
        # مدل‌های مختلف
        self.rl_agent = AdvancedRLAgent(state_size, action_size)
        self.adaptive_strategy = AdaptiveStrategy()
        
        # وزن‌های مدل‌ها
        self.weights = {
            'rl': 0.4,
            'adaptive': 0.4,
            'technical': 0.2
        }
        
        self.performance_history = []
        
    def prepare_state(self, market_data: pd.DataFrame) -> np.ndarray:
        """آماده‌سازی ورودی برای مدل‌ها"""
        if len(market_data) < 10:
            return np.zeros(self.state_size)
            
        # استخراج ویژگی‌ها
        features = []
        
        # قیمت‌های نرمال‌شده
        prices = market_data['close'].tail(5).values
        if len(prices) > 0:
            normalized_prices = (prices - prices.min()) / (prices.max() - prices.min() + 1e-8)
            features.extend(normalized_prices.tolist())
        
        # نوسانات
        returns = market_data['close'].pct_change().tail(3).fillna(0).values
        features.extend(returns.tolist())
        
        # حجم معاملات
        volumes = market_data['volume'].tail(2).fillna(0).values
        if len(volumes) > 0:
            normalized_volumes = (volumes - volumes.min()) / (volumes.max() - volumes.min() + 1e-8)
            features.extend(normalized_volumes.tolist())
        
        # پر کردن با صفر تا اندازه درست شود
        while len(features) < self.state_size:
            features.append(0)
            
        return np.array(features[:self.state_size]).reshape(1, -1)
    
    def get_rl_prediction(self, state: np.ndarray) -> Tuple[str, float]:
        """دریافت پیش‌بینی از مدل RL"""
        try:
            action = self.rl_agent.act(state)
            actions = ['sell', 'hold', 'buy']
            confidence = 1.0 - self.rl_agent.epsilon  # اعتماد بر اساس epsilon
            return actions[action], confidence
        except Exception as e:
            self.logger.error(f"خطا در پیش‌بینی RL: {str(e)}")
            return 'hold', 0.1
    
    def get_adaptive_prediction(self, market_data: pd.DataFrame) -> Tuple[str, float]:
        """دریافت پیش‌بینی از استراتژی تطبیقی"""
        try:
            signal = self.adaptive_strategy.generate_signal(market_data)
            return signal['signal'], signal['confidence']
        except Exception as e:
            self.logger.error(f"خطا در پیش‌بینی تطبیقی: {str(e)}")
            return 'hold', 0.1
    
    def get_technical_prediction(self, market_data: pd.DataFrame) -> Tuple[str, float]:
        """دریافت پیش‌بینی از تحلیل تکنیکال"""
        try:
            if len(market_data) < 14:
                return 'hold', 0.1
                
            # محاسبه RSI
            delta = market_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # تصمیم بر اساس RSI
            if current_rsi > 70:
                return 'sell', 0.7
            elif current_rsi < 30:
                return 'buy', 0.7
            else:
                return 'hold', 0.3
        except Exception as e:
            self.logger.error(f"خطا در پیش‌بینی تکنیکال: {str(e)}")
            return 'hold', 0.1
    
    def predict(self, market_data: pd.DataFrame) -> Dict:
        """پیش‌بینی نهایی با ترکیب مدل‌ها"""
        # آماده‌سازی ورودی
        state = self.prepare_state(market_data)
        
        # دریافت پیش‌بینی‌ها از هر مدل
        rl_action, rl_conf = self.get_rl_prediction(state)
        adaptive_action, adaptive_conf = self.get_adaptive_prediction(market_data)
        tech_action, tech_conf = self.get_technical_prediction(market_data)
        
        # ترکیب پیش‌بینی‌ها
        predictions = {
            'rl': {'action': rl_action, 'confidence': rl_conf},
            'adaptive': {'action': adaptive_action, 'confidence': adaptive_conf},
            'technical': {'action': tech_action, 'confidence': tech_conf}
        }
        
        # محاسبه رأی موزون
        action_scores = {'buy': 0, 'sell': 0, 'hold': 0}
        
        for model_name, pred in predictions.items():
            weight = self.weights.get(model_name, 0)
            confidence = pred['confidence']
            action = pred['action']
            
            if action in action_scores:
                action_scores[action] += weight * confidence
        
        # انتخاب بهترین عمل
        best_action = max(action_scores, key=action_scores.get)
        total_score = sum(action_scores.values())
        final_confidence = action_scores[best_action] / total_score if total_score > 0 else 0
        
        # لاگ کردن تصمیم
        self.logger.info(f"پیش‌بینی نهایی: {best_action} - اعتماد: {final_confidence:.2f}")
        self.logger.info(f"رأی مدل‌ها: {predictions}")
        
        return {
            'action': best_action,
            'confidence': final_confidence,
            'model_votes': predictions,
            'timestamp': market_data['timestamp'].iloc[-1] if 'timestamp' in market_data.columns else None
        }
    
    def update_weights(self, performance_data: Dict):
        """بروزرسانی وزن‌های مدل‌ها بر اساس عملکرد"""
        try:
            # اینجا می‌تونی الگوریتم بهینه‌سازی وزن‌ها رو پیاده کنی
            # برای حالا فقط لاگ می‌کنیم
            self.logger.info("بروزرسانی وزن‌های مدل‌ها")
            self.performance_history.append(performance_data)
        except Exception as e:
            self.logger.error(f"خطا در بروزرسانی وزن‌ها: {str(e)}")

# تست عملی:
if __name__ == "__main__":
    # ایجاد مدل ترکیبی
    ensemble = EnsembleModel(state_size=20, action_size=3)
    print("مدل ترکیبی ایجاد شد")
    
    # ایجاد داده‌های نمونه
    dates = pd.date_range(start='2023-01-01', periods=50, freq='D')
    sample_data = pd.DataFrame({
        'timestamp': dates,
        'open': np.random.uniform(40000, 50000, 50),
        'high': np.random.uniform(41000, 51000, 50),
        'low': np.random.uniform(39000, 49000, 50),
        'close': np.random.uniform(40000, 50000, 50),
        'volume': np.random.uniform(1000, 5000, 50)
    })
    
    # پیش‌بینی
    prediction = ensemble.predict(sample_data)
    print("پیش‌بینی نهایی:", prediction)