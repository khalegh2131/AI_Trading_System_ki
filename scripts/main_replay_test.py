# scripts/main_replay_test.py

from core.market_replay import MarketReplayEngine
import time

def on_candle(row):
    print(f"[REPLAY] ⏱️ {row['timestamp']} | Close: {row['close']}")

engine = MarketReplayEngine(data_dir="data/feeds", callback=on_candle)
engine.start(symbol="BTCUSDT", timeframe="1m", speed=2.0)

time.sleep(5)
engine.pause()
print("⏸️ Paused for 3s...")
time.sleep(3)
engine.resume()
print("▶️ Resumed for 5s...")
time.sleep(5)
engine.stop()
print("🛑 Replay Stopped.")
