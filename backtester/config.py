# D:\AI\AI_Trading_System_ki\backtester\config.py

BACKTEST_CONFIG = {
    'initial_balance': 10000,
    'commission': 0.001,  # 0.1%
    'slippage': 0.0005,   # 0.05%
    'start_date': '2022-01-01',
    'end_date': '2024-01-01',
    'symbols': ['BTCUSDT', 'ETHUSDT'],
    'timeframes': ['1h', '4h', '1d']
}