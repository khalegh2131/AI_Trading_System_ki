# D:\AI\AI_Trading_System_ki\api\connectors\binance_connector.py

import hashlib
import hmac
import time
import requests
from urllib.parse import urlencode

class BinanceConnector:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binance.vision" if testnet else "https://api.binance.com"
        
    def _generate_signature(self, params: dict) -> str:
        """تولید امضای HMAC-SHA256"""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list:
        """دریافت داده‌های کندل"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        url = self.base_url + '/api/v3/klines'
        response = requests.get(url, params=params)
        return response.json()

# مثال استفاده:
if __name__ == "__main__":
    # برای تست، کلیدهای واقعی نیاز داری
    # connector = BinanceConnector("YOUR_API_KEY", "YOUR_API_SECRET")
    # klines = connector.get_klines("BTCUSDT", "1h", 10)
    # print(klines)