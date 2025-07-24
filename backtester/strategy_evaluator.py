# D:\AI\AI_Trading_System_ki\backtester\strategy_evaluator.py

from typing import Dict, List
import pandas as pd
from backtester.backtester import Backtester

class StrategyEvaluator:
    def __init__(self):
        pass
        
    def evaluate_multiple_strategies(self, strategies: List, data: pd.DataFrame, config: dict) -> Dict:
        """ارزیابی چندین استراتژی"""
        results = {}
        
        for strategy in strategies:
            strategy_name = strategy.__class__.__name__
            backtester = Backtester(config)
            result = backtester.run(strategy, data)
            results[strategy_name] = result
            
        return results

# مثال استفاده:
if __name__ == "__main__":
    # تست ارزیابی
    pass