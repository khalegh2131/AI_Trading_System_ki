"""
ماژول downloader حرفه‌ای برای پروژه Market Replay
نویسنده: Kimi + ChatGPT
مسیر: data_manager/downloader.py
"""
import os
import requests
from datetime import datetime, timedelta
import zipfile
import hashlib
from pathlib import Path

# مسیر پایه فایل‌ها
BASE_DIR = Path("data/market")
BASE_URL = "https://data.binance.vision/data/spot/daily/klines"
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_INTERVAL = "1m"

# اطمینان از وجود مسیر ذخیره‌سازی
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# محاسبه هش SHA256 فایل برای بررسی صحت
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# بررسی checksum
def verify_checksum(zip_path, checksum_path):
    try:
        with open(checksum_path, 'r') as f:
            checksum_content = f.read().strip()
            expected_hash = checksum_content.split()[0]
        calculated_hash = calculate_sha256(zip_path)
        return calculated_hash == expected_hash
    except:
        return False

# دانلود فایل از URL
def download_file(url, save_path):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            print(f"❌ Error {r.status_code}: {url}")
            return False
    except Exception as e:
        print(f"⚠️ Exception while downloading {url}: {e}")
        return False

# اکسترکت فایل ZIP و حذف آن
def extract_and_delete(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)
    except Exception as e:
        print(f"⚠️ Failed to extract {zip_path}: {e}")

# دانلود دیتای یک نماد و تایم‌فریم در بازه مشخص
def download_klines(symbol=DEFAULT_SYMBOL, interval=DEFAULT_INTERVAL, start_date="2025-06-01", end_date="2025-06-05"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    folder = BASE_DIR / symbol / interval
    ensure_dir(folder)

    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        file_name = f"{symbol}-{interval}-{date_str}.zip"
        url = f"{BASE_URL}/{symbol}/{interval}/{file_name}"
        save_path = folder / file_name

        # اگر فایل CSV قبلاً وجود دارد، عبور کن
        csv_file = save_path.with_suffix(".csv")
        if csv_file.exists():
            print(f"✅ Already downloaded: {csv_file.name}")
        else:
            print(f"⬇️ Downloading: {file_name}")
            if download_file(url, save_path):
                extract_and_delete(save_path, folder)
            else:
                print(f"❌ Failed: {file_name}")

        current += timedelta(days=1)

# مثال تستی در صورت اجرا مستقیم
if __name__ == "__main__":
    download_klines(symbol="BTCUSDT", interval="1m", start_date="2025-06-01", end_date="2025-06-03")
