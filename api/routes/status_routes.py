# D:\AI\AI_Trading_System_ki\api\routes\status_routes.py

from flask import Blueprint, jsonify
import psutil
import logging
from datetime import datetime

status_bp = Blueprint('status', __name__)
logger = logging.getLogger("StatusRoutes")

# متغیرهای حالت سیستم
system_paused = False
active_strategy = None

@status_bp.route('/status', methods=['GET'])
def get_system_status():
    """دریافت وضعیت کلی سیستم"""
    # اطلاعات سیستم
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "status": "paused" if system_paused else "running",
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / (1024**3):.2f} GB"
        },
        "trading": {
            "active_strategy": active_strategy,
            "is_trading": not system_paused and active_strategy is not None
        },
        "network": {
            "vpn_connected": False,  # باید از ماژول VPN بگیریم
            "api_connected": True    # باید از ماژول API بگیریم
        }
    }
    
    logger.info("وضعیت سیستم ارسال شد")
    return jsonify(status)

@status_bp.route('/health', methods=['GET'])
def health_check():
    """چک سلامت سیستم"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "online",
            "database": "online",
            "trading_engine": "online"
        }
    })