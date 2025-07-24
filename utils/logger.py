# D:\AI\AI_Trading_System_ki\utils\logger.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

COLORS = {
    logging.DEBUG:    "\033[36m",   # cyan
    logging.INFO:     "\033[32m",   # green
    logging.WARNING:  "\033[33m",   # yellow
    logging.ERROR:    "\033[31m",   # red
    logging.CRITICAL: "\033[35m",   # magenta
}
RESET = "\033[0m"

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{COLORS.get(record.levelno, '')}{record.levelname}{RESET}"
        return super().format(record)

def setup_logger(log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
    """
    ساخت یک logger سراسری با دو handler:
    1) چرخشی 10MB در log_dir
    2) خروجی رنگی در کنسول
    """
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # پاک‌سازی handlerهای قبلی (برای جلوگیری از دوبار اضافه شدن)
    logger.handlers.clear()

    # --- File Handler (چرخشی 10MB) ---
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    # --- Console Handler (رنگی) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_fmt = ColoredFormatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    return logger


def get_logger(name=None):
    """
    دریافت logger برای ماژول‌های دیگر
    """
    return logging.getLogger(name)