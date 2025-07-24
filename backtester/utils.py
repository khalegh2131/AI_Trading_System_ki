# D:\AI\AI_Trading_System_ki\backtester\utils.py

import pandas as pd
from datetime import datetime

def timestamp_to_datetime(timestamp: int) -> datetime:
    """تبدیل timestamp به datetime"""
    return datetime.fromtimestamp(timestamp / 1000)

def calculate_returns(prices: List[float]) -> List[float]:
    """محاسبه بازده روزانه"""
    if len(prices) < 2:
        return []
    return [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """نرمال‌سازی داده‌ها"""
    normalized = df.copy()
    for col in ['open', 'high', 'low', 'close']:
        if col in normalized.columns:
            normalized[col] = (normalized[col] - normalized[col].min()) / (normalized[col].max() - normalized[col].min())
    return normalized