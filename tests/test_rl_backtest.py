# tests/test_rl_backtest.py

import os
import pytest
from core.backtester import RLBacktestEngine

# مسیر نمونه‌ها
MODEL_PATH = "models/crypto/ppo_btcusdt.pkl"
DATA_PATH = "data/feeds/BTCUSDT_1h_sample.csv"
RESULT_PATH = "results/test_output.csv"

@pytest.mark.parametrize("timesteps", [1000])
def test_rl_backtest_integration(timesteps):
    assert os.path.exists(MODEL_PATH), f"Model file not found: {MODEL_PATH}"
    assert os.path.exists(DATA_PATH), f"Data file not found: {DATA_PATH}"

    engine = RLBacktestEngine(model_path=MODEL_PATH, data_path=DATA_PATH, timesteps=timesteps)
    
    # Load model
    engine.load_rl_model()
    assert engine.model is not None
    assert engine.env is not None

    # Run backtest
    engine.run_backtest()
    assert len(engine.results) > 0

    # Export results
    engine.export_results(out_path=RESULT_PATH)
    assert os.path.exists(RESULT_PATH)
