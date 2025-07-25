# D:\AI\AI_Trading_System_ki\learning\utils.py

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

def normalize_data(data: np.ndarray) -> np.ndarray:
    """نرمال‌سازی داده‌ها"""
    if len(data) == 0:
        return data
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val - min_val == 0:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)

def create_sequences(data: np.ndarray, seq_length: int) -> Tuple[np.ndarray, np.ndarray]:
    """ایجاد سکانس‌های زمانی"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """محاسبه نسبت شارپ"""
    if len(returns) < 2:
        return 0.0
        
    excess_returns = [r - risk_free_rate/252 for r in returns]
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def calculate_max_drawdown(equity_curve: List[float]) -> float:
    """محاسبه حداکثر افت"""
    if not equity_curve:
        return 0.0
        
    peak = equity_curve[0]
    max_drawdown = 0.0
    
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            
    return max_drawdown * 100

def format_performance_metrics(metrics: Dict) -> str:
    """فرمت‌بندی معیارهای عملکرد"""
    return f"""
📊 عملکرد استراتژی:
   - بازده کل: {metrics.get('total_return', 0):.2f}%
   - نسبت شارپ: {metrics.get('sharpe_ratio', 0):.2f}
   - حداکثر افت: {metrics.get('max_drawdown', 0):.2f}%
   - تعداد معاملات: {metrics.get('total_trades', 0)}
   - درصد موفقیت: {metrics.get('win_rate', 0):.1f}%
    """.strip()

def load_market_data(file_path: str) -> pd.DataFrame:
    """بارگذاری داده‌های بازار"""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError("فرمت فایل پشتیبانی نمی‌شود")
    except Exception as e:
        logging.error(f"خطا در بارگذاری داده‌ها: {str(e)}")
        return pd.DataFrame()

# تست عملی:
if __name__ == "__main__":
    # تست نرمال‌سازی
    test_data = np.array([1, 2, 3, 4, 5])
    normalized = normalize_data(test_data)
    print("داده‌های اصلی:", test_data)
    print("داده‌های نرمال‌شده:", normalized)
    
    # تست محاسبه شارپ
    returns = [0.01, -0.02, 0.03, -0.01, 0.02]
    sharpe = calculate_sharpe_ratio(returns)
    print(f"نسبت شارپ: {sharpe:.2f}")