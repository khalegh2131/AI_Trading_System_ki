from core.market_replay import MarketReplay
import time

replay = MarketReplay(file_path="data/BTCUSDT_15m.csv", speed=0.5)
replay.start()

for _ in range(10):
    print(replay.get_current_candle())
    time.sleep(1)

replay.pause()
print("⏸ Paused")
time.sleep(2)
replay.resume()
print("▶️ Resumed")
