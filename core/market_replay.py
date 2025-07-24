# D:\AI\AI_Trading_System_ki\core\market_replay.py
import pandas as pd
import time
import threading

class MarketReplay:
    def __init__(self, file_path: str, speed: float = 1.0):
        self.file_path = file_path
        self.speed = speed  # ثانیه بین هر تیک
        self.data = pd.read_csv(file_path)
        self.index = 0
        self.playing = False
        self.lock = threading.Lock()
        self.current_candle = None
        self.thread = None

    def start(self):
        self.playing = True
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def _run(self):
        while self.playing and self.index < len(self.data):
            with self.lock:
                self.current_candle = self.data.iloc[self.index].to_dict()
                self.index += 1
            time.sleep(self.speed)

    def pause(self):
        self.playing = False

    def resume(self):
        self.start()

    def reset(self):
        with self.lock:
            self.index = 0
            self.current_candle = None
            self.playing = False

    def get_current_candle(self):
        with self.lock:
            return self.current_candle
