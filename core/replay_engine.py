# core/market_replay.py

import threading
import time
import pandas as pd
import os

class MarketReplayEngine:
    def __init__(self, data_dir: str, callback, loop=False):
        self.data_dir = data_dir
        self.callback = callback
        self.loop = loop

        self._running = False
        self._paused = False
        self._thread = None
        self.speed = 1.0  # کندل بر ثانیه
        self.df = None
        self._idx = 0

    def load_data(self, symbol: str, timeframe: str):
        path = os.path.join(self.data_dir, f"{symbol}_{timeframe}.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"⛔ CSV not found: {path}")
        self.df = pd.read_csv(path)
        self.df.fillna(method="ffill", inplace=True)
        self._idx = 0

    def _run(self):
        while self._running and self._idx < len(self.df):
            if self._paused:
                time.sleep(0.1)
                continue

            row = self.df.iloc[self._idx].to_dict()
            self.callback(row)
            self._idx += 1

            time.sleep(1.0 / self.speed)

            if self._idx >= len(self.df) and self.loop:
                self._idx = 0

    def start(self, symbol: str, timeframe: str, speed=1.0):
        self.load_data(symbol, timeframe)
        self.speed = speed
        self._running = True
        self._paused = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
