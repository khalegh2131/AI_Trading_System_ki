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
        """Generate HMAC-SHA256 signature"""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    def _send_signed_request(self, http_method: str, url_path: str, payload: dict = {}) -> dict:
        """Send signed request"""
        payload['timestamp'] = int(time.time() * 1000)
        payload['signature'] = self._generate_signature(payload)
        
        url = self.base_url + url_path
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        if http_method == 'GET':
            response = requests.get(url, headers=headers, params=payload)
        elif http_method == 'POST':
            response = requests.post(url, headers=headers, params=payload)
            
        return response.json()
        
    def get_account_info(self) -> dict:
        """Get account information"""
        return self._send_signed_request('GET', '/api/v3/account')
        
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list:
        """Get candle data"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        url = self.base_url + '/api/v3/klines'
        response = requests.get(url, params=params)
        return response.json()

# Example usage:
if __name__ == "__main__":
    # For testing, you need real keys
    # connector = BinanceConnector("YOUR_API_KEY", "YOUR_API_SECRET")
    # klines = connector.get_klines("BTCUSDT", "1h", 10)
    # print(klines)