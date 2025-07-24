# strategies/strategy_manager.py
from strategies.rl_adaptive import RLTrader

class StrategyManager:
    def __init__(self):
        self.mode = "idle"
        self.rl = None

    def load_rl(self):
        if not self.rl:
            self.rl = RLTrader()
            self.rl.load_model()

    def train(self):
        self.load_rl()
        self.mode = "training"
        self.rl.train()

    def backtest(self):
        self.load_rl()
        self.mode = "backtest"
        return self.rl.backtest()

    def replay(self):
        self.load_rl()
        self.mode = "replay"
        return self.rl.replay_market()

    def status(self):
        return {
            "mode": self.mode,
            "loaded": self.rl is not None
        }
