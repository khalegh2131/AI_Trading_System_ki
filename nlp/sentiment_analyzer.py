# D:\AI\AI_Trading_System_ki\nlp\sentiment_analyzer.py

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
import logging
from utils.logger import get_logger

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.logger = get_logger("SentimentAnalyzer")
        
    def analyze_text(self, text: str) -> Dict:
        """تحلیل احساسات یک متن"""
        try:
            scores = self.analyzer.polarity_scores(text)
            sentiment = 'positive' if scores['compound'] >= 0.05 else 'negative' if scores['compound'] <= -0.05 else 'neutral'
            
            result = {
                'text': text,
                'sentiment': sentiment,
                'score': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
            
            return result
        except Exception as e:
            self.logger.error(f"خطا در تحلیل متن: {str(e)}")
            return {'sentiment': 'error', 'score': 0}
    
    def analyze_news_batch(self, news_list: List[str]) -> List[Dict]:
        """تحلیل دسته‌ای اخبار"""
        results = []
        for news in news_list:
            result = self.analyze_text(news)
            results.append(result)
        return results

# تست عملی:
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # تست با متن‌های مختلف
    test_texts = [
        "بیت کوین قیمت خوبی دارد",
        "قیمت بیت کوین به شدت کاهش یافت",
        "اخبار خنثی درباره اتریوم"
    ]
    
    for text in test_texts:
        result = analyzer.analyze_text(text)
        print(f"متن: {text}")
        print(f"احساس: {result['sentiment']} - امتیاز: {result['score']}\n")