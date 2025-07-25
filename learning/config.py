# D:\AI\AI_Trading_System_ki\learning\config.py

LEARNING_CONFIG = {
    'rl_agent': {
        'state_size': 20,
        'action_size': 3,
        'learning_rate': 0.001,
        'gamma': 0.95,
        'epsilon_start': 1.0,
        'epsilon_min': 0.01,
        'epsilon_decay': 0.995,
        'memory_size': 10000,
        'batch_size': 32
    },
    'ensemble': {
        'model_weights': {
            'rl': 0.4,
            'adaptive': 0.4,
            'technical': 0.2
        },
        'prediction_threshold': 0.6
    },
    'feature_engineering': {
        'technical_indicators': ['rsi', 'macd', 'bollinger_bands', 'moving_averages'],
        'market_regime_features': ['trend', 'volatility', 'trend_strength'],
        'time_features': ['hour', 'day_of_week', 'month']
    },
    'training': {
        'epochs': 100,
        'validation_split': 0.2,
        'early_stopping_patience': 10
    }
}