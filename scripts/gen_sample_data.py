# scripts/gen_sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_csv(filepath="data/BTCUSDT_15m.csv", start_price=30000):
    candles = []
    timestamp = datetime(2024, 1, 1, 0, 0)

    for _ in range(100):
        open_price = start_price + np.random.randn() * 50
        close_price = open_price + np.random.randn() * 30
        high_price = max(open_price, close_price) + np.random.rand() * 20
        low_price = min(open_price, close_price) - np.random.rand() * 20
        volume = np.random.randint(500, 3000)

        candles.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume
        })
        timestamp += timedelta(minutes=15)

    df = pd.DataFrame(candles)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"[✅] Generated: {filepath}")

if __name__ == "__main__":
    generate_sample_csv()
