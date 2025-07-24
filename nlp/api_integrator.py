# D:\AI\AI_Trading_System_ki\nlp\api_integrator.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import openai
import requests
import json
from typing import Dict, Optional
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

class APIIntegrator:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("APIIntegrator")
        self.chatgpt_key = config.get('nlp', {}).get('chatgpt_api_key', '')
        
    def analyze_with_chatgpt(self, text: str) -> Optional[Dict]:
        """تحلیل متن با ChatGPT API"""
        if not self.chatgpt_key:
            self.logger.warning("کلید ChatGPT API تنظیم نشده")
            return None
            
        try:
            openai.api_key = self.chatgpt_key
            
            prompt = f"""
            Analyze the sentiment of this financial news text and provide:
            1. Sentiment (positive/negative/neutral)
            2. Confidence score (0-100)
            3. Trading signal (buy/sell/hold)
            
            Text: {text}
            
            Respond in JSON format.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            self.logger.error(f"خطا در تحلیل ChatGPT: {str(e)}")
            return None

# تست عملی (نیاز به کلید API):
if __name__ == "__main__":
    # config = {"nlp": {"chatgpt_api_key": "YOUR_KEY_HERE"}}
    # integrator = APIIntegrator(config)
    # result = integrator.analyze_with_chatgpt("Bitcoin price is rising rapidly")
    # print(result)
    pass