# D:\AI\AI_Trading_System_ki\backtester\exceptions.py

class BacktestError(Exception):
    """خطای پایه برای بک‌تست"""
    pass

class DataLoadError(BacktestError):
    """خطای بارگذاری داده"""
    pass

class StrategyError(BacktestError):
    """خطای استراتژی"""
    pass

class InsufficientDataError(BacktestError):
    """خطای کمبود داده"""
    pass