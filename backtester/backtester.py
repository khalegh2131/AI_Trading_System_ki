# D:\AI\AI_Trading_System_ki\backtester\backtester.py

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
import logging
from utils.logger import get_logger

class Backtester:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("Backtester")
        self.results = []
        self.trades = []
        
    def run(self, strategy, data: pd.DataFrame) -> Dict:
        """اجرای تست تاریخی روی داده‌ها"""
        self.logger.info("شروع بک‌تست...")
        
        # مقداردهی اولیه
        initial_balance = self.config.get('initial_balance', 10000)
        balance = initial_balance
        position = 0
        entry_price = 0
        
        for i in range(1, len(data)):
            row = data.iloc[i]
            signal = strategy.generate_signal(data.iloc[:i+1])
            
            # اجرای سیگنال
            if signal == 1 and position == 0:  # خرید
                position = 1
                entry_price = row['close']
                self.trades.append({
                    'timestamp': row['timestamp'],
                    'action': 'BUY',
                    'price': entry_price,
                    'balance': balance
                })
                
            elif signal == -1 and position == 1:  # فروش
                position = 0
                profit = (row['close'] - entry_price) * (balance / entry_price)
                balance += profit
                self.trades.append({
                    'timestamp': row['timestamp'],
                    'action': 'SELL',
                    'price': row['close'],
                    'profit': profit,
                    'balance': balance
                })
        
        # محاسبه نتایج
        final_result = {
            'initial_balance': initial_balance,
            'final_balance': balance,
            'total_return': ((balance - initial_balance) / initial_balance) * 100,
            'total_trades': len(self.trades),
            'win_rate': self._calculate_win_rate()
        }
        
        self.logger.info(f"بک‌تست به پایان رسید. بازده: {final_result['total_return']:.2f}%")
        return final_result
    
    def _calculate_win_rate(self) -> float:
        """محاسبه درصد معاملات سودآور"""
        if len(self.trades) < 2:
            return 0.0
            
        wins = 0
        for i in range(1, len(self.trades), 2):
            if i < len(self.trades) and self.trades[i].get('profit', 0) > 0:
                wins += 1
                
        return (wins / (len(self.trades) // 2)) * 100 if self.trades else 0.0

# مثال استفاده:
if __name__ == "__main__":
    # اینجا می‌تونی تست کنی
    pass    