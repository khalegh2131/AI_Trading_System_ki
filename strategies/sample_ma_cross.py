# D:\AI\AI_Trading_System_ki\strategies\sample_ma_cross.py
import backtrader as bt

class MACrossStrategy(bt.Strategy):
    params = dict(
        pfast=20,
        pslow=50,
    )

    def __init__(self):
        self.fast = bt.ind.EMA(period=self.p.pfast)
        self.slow = bt.ind.EMA(period=self.p.pslow)
        self.cross = bt.ind.CrossOver(self.fast, self.slow)

    def next(self):
        if self.cross > 0:
            self.buy()
        elif self.cross < 0:
            self.close()