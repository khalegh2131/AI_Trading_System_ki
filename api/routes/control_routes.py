# D:\AI\AI_Trading_System_ki\api\routes\control_routes.py

from flask import Blueprint, jsonify, request
import logging

control_bp = Blueprint('control', __name__)
logger = logging.getLogger("ControlRoutes")

# متغیرهای حالت سیستم
system_paused = False
active_strategy = None

@control_bp.route('/pause', methods=['POST'])
def pause_system():
    """توقف سیستم"""
    global system_paused
    system_paused = True
    logger.info("سیستم متوقف شد")
    return jsonify({
        "status": "paused",
        "message": "سیستم با موفقیت متوقف شد"
    })

@control_bp.route('/resume', methods=['POST'])
def resume_system():
    """ادامه سیستم"""
    global system_paused
    system_paused = False
    logger.info("سیستم ادامه یافت")
    return jsonify({
        "status": "running",
        "message": "سیستم با موفقیت ادامه یافت"
    })

@control_bp.route('/strategy/<strategy_name>/activate', methods=['POST'])
def activate_strategy(strategy_name):
    """فعال‌سازی استراتژی"""
    global active_strategy
    active_strategy = strategy_name
    logger.info(f"استراتژی {strategy_name} فعال شد")
    return jsonify({
        "status": "activated",
        "strategy": strategy_name
    })

@control_bp.route('/strategy/deactivate', methods=['POST'])
def deactivate_strategy():
    """غیرفعال‌سازی استراتژی"""
    global active_strategy
    previous_strategy = active_strategy
    active_strategy = None
    logger.info(f"استراتژی {previous_strategy} غیرفعال شد")
    return jsonify({
        "status": "deactivated",
        "previous_strategy": previous_strategy
    })