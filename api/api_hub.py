# D:\AI\AI_Trading_System_ki\api\api_hub.py

import requests
import time
import json
from typing import List, Dict, Optional
import logging
from utils.logger import get_logger

class APIHub:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("APIHub")
        self.apis = self._load_apis()
        self.current_api = None
        self.switch_api()
        
    def _load_apis(self) -> List[Dict]:
        """Load API list from config"""
        apis = []
        
        # Load Forex APIs
        for forex_api in self.config.get('apis', {}).get('forex', []):
            apis.append({
                'name': forex_api['name'],
                'base_url': forex_api.get('base_url', ''),
                'key': forex_api['key'],
                'secret': forex_api['secret'],
                'type': 'forex',
                'ping_url': forex_api.get('ping_url', '')
            })
            
        # Load Crypto APIs
        for crypto_api in self.config.get('apis', {}).get('crypto', []):
            apis.append({
                'name': crypto_api['name'],
                'base_url': crypto_api.get('base_url', ''),
                'key': crypto_api['key'],
                'secret': crypto_api['secret'],
                'type': 'crypto',
                'ping_url': crypto_api.get('ping_url', 'https://api.binance.com/api/v3/ping')
            })
            
        return apis

    def switch_api(self) -> bool:
        """Switch to best available API"""
        self.logger.info("Testing APIs for connection...")
        
        for api in self.apis:
            try:
                ping_url = api.get('ping_url')
                if not ping_url:
                    continue
                    
                # Test connection with short timeout
                response = requests.get(ping_url, timeout=5)
                if response.status_code == 200:
                    self.current_api = api
                    self.logger.info(f"✅ Connected to: {api['name']}")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"❌ {api['name']} not available: {str(e)}")
                continue
                
        self.logger.error("⚠️ No API available!")
        return False

    def fetch_ohlcv(self, symbol: str = "BTCUSDT", timeframe: str = "1h", limit: int = 100) -> Optional[List]:
        """Fetch OHLCV data from current API"""
        if not self.current_api:
            if not self.switch_api():
                return None
                
        try:
            # Binance candle data path
            if 'binance' in self.current_api['name'].lower():
                url = f"{self.current_api['base_url']}/klines"
                params = {
                    'symbol': symbol,
                    'interval': timeframe,
                    'limit': limit
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # Convert to standard format
                    ohlcv = []
                    for item in data:
                        ohlcv.append({
                            'timestamp': int(item[0]),
                            'open': float(item[1]),
                            'high': float(item[2]),
                            'low': float(item[3]),
                            'close': float(item[4]),
                            'volume': float(item[5])
                        })
                    return ohlcv
                    
        except Exception as e:
            self.logger.error(f"Error fetching data from {self.current_api['name']}: {str(e)}")
            # Try to switch API
            if self.switch_api():
                return self.fetch_ohlcv(symbol, timeframe, limit)
                
        return None

    def place_order(self, symbol: str, side: str, quantity: float, price: float = None) -> Optional[Dict]:
        """Place order (for future versions)"""
        # Implementation for future
        pass

    def get_balance(self) -> Optional[Dict]:
        """Get balance (for future versions)"""
        # Implementation for future
        pass

# Example usage:
if __name__ == "__main__":
    # Load config
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # Create API Hub
    api_hub = APIHub(config)
    
    # Fetch BTC data
    data = api_hub.fetch_ohlcv("BTCUSDT", "1h", 10)
    if data:
        print(f"Fetched {len(data)} candles")
        print(data[0])  # Show first candle
    else:
        print("No data fetched")