# D:\AI\AI_Trading_System_ki\backtester\data_loader.py

import pandas as pd
import json
from typing import List, Dict
import os
from utils.logger import get_logger

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.logger = get_logger("DataLoader")
        
    def load_csv_data(self, filename: str) -> pd.DataFrame:
        """بارگذاری داده‌های CSV"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            self.logger.info(f"داده‌های {filename} بارگذاری شد")
            return df
        else:
            self.logger.error(f"فایل {filename} یافت نشد")
            return pd.DataFrame()
    
    def load_json_data(self, filename: str) -> Dict:
        """بارگذاری داده‌های JSON"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.logger.info(f"داده‌های {filename} بارگذاری شد")
            return data
        else:
            self.logger.error(f"فایل {filename} یافت نشد")
            return {}

# مثال استفاده:
if __name__ == "__main__":
    # تست بارگذاری
    pass