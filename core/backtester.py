# D:\AI\AI_Trading_System_ki\core\backtester.py
import backtrader as bt
import ccxt
import pandas as pd
import yaml
from strategies.sample_ma_cross import MACrossStrategy
from utils.logger import get_logger

log = get_logger("backtest")

class BacktestEngine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.exchange = ccxt.binance({
            "sandbox": cfg["exchanges"]["binance"]["sandbox"]
        })

    def fetch_ohlcv(self, symbol, timeframe="15m", limit=1000):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["datetime", "open", "high", "low", "close", "volume"])
        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
        df.set_index("datetime", inplace=True)
        return df

    def run(self, symbol, initial_cash=10000):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initial_cash)
        cerebro.addstrategy(MACrossStrategy)

        df = self.fetch_ohlcv(symbol)
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")

        results = cerebro.run()
        strat = results[0]

        stats = {
            "Final Value": cerebro.broker.getvalue(),
            "Sharpe": strat.analyzers.sharpe.get_analysis(),
            "Drawdown": strat.analyzers.drawdown.get_analysis(),
        }
        log.info("Backtest finished for %s", symbol)
        return stats