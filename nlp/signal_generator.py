# D:\AI\AI_Trading_System_ki\nlp\signal_generator.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

class SignalGenerator:
    def __init__(self):
        self.logger = get_logger("SignalGenerator")
        
    def generate_trading_signal(self, sentiment_result: Dict) -> Dict:
        """تبدیل نتیجه احساس به سیگنال معاملاتی"""
        sentiment = sentiment_result.get('sentiment', 'neutral')
        score = sentiment_result.get('score', 0)
        
        if sentiment == 'positive' and score > 0.3:
            signal = 'buy'
            strength = 'strong' if score > 0.6 else 'moderate'
        elif sentiment == 'negative' and score < -0.3:
            signal = 'sell'
            strength = 'strong' if score < -0.6 else 'moderate'
        else:
            signal = 'hold'
            strength = 'weak'
            
        result = {
            'signal': signal,
            'strength': strength,
            'confidence': abs(score),
            'reason': f"Sentiment: {sentiment}, Score: {score}"
        }
        
        self.logger.info(f"سیگنال تولید شد: {signal} - قدرت: {strength}")
        return result

# تست عملی:
if __name__ == "__main__":
    generator = SignalGenerator()
    
    # تست با نتایج مختلف
    test_results = [
        {'sentiment': 'positive', 'score': 0.7},
        {'sentiment': 'negative', 'score': -0.5},
        {'sentiment': 'neutral', 'score': 0.1}
    ]
    
    for result in test_results:
        signal = generator.generate_trading_signal(result)
        print(f"نتیجه: {result} → سیگنال: {signal}")