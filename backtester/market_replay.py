# D:\AI\AI_Trading_System_ki\backtester\market_replay.py

import pandas as pd
import time
from typing import List, Dict
import logging
from utils.logger import get_logger

class MarketReplay:
    def __init__(self, data: pd.DataFrame):
        self.data = data.sort_values('timestamp')
        self.logger = get_logger("MarketReplay")
        
    def replay(self, speed: float = 1.0, callback=None):
        """اجرای شبیه‌سازی بازار به صورت زنده"""
        self.logger.info("شروع شبیه‌سازی بازار...")
        
        for i, row in self.data.iterrows():
            if callback:
                callback(row)
            
            # تاخیر برای شبیه‌سازی زمان واقعی
            time.sleep(1.0 / speed)
            
        self.logger.info("شبیه‌سازی بازار به پایان رسید")

# مثال استفاده:
if __name__ == "__main__":
    # تست شبیه‌سازی
    pass