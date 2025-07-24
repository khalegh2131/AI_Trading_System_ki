# D:\AI\AI_Trading_System_ki\backtester\performance_metrics.py

import numpy as np
import pandas as pd
from typing import Dict, List

class PerformanceMetrics:
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """محاسبه نسبت شارپ"""
        if len(returns) < 2:
            return 0.0
            
        excess_returns = [r - risk_free_rate/252 for r in returns]
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    
    @staticmethod
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
    
    @staticmethod
    def calculate_win_loss_ratio(trades: List[Dict]) -> float:
        """محاسبه نسبت برد/باخت"""
        wins = sum(1 for trade in trades if trade.get('profit', 0) > 0)
        losses = len(trades) - wins
        return wins / losses if losses > 0 else float('inf')

# مثال استفاده:
if __name__ == "__main__":
    # تست معیارها
    pass