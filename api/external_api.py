# D:\AI\AI_Trading_System_ki\api\external_api.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from api.routes.control_routes import control_bp
from api.routes.status_routes import status_bp
from api.routes.training_routes import training_bp
import logging

# محلی‌سازی logger
def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def create_api_app():
    """ایجاد اپلیکیشن Flask برای API خارجی"""
    app = Flask(__name__)
    logger = get_logger("ExternalAPI")
    
    # ثبت بلوپرینت‌ها
    app.register_blueprint(control_bp, url_prefix='/api')
    app.register_blueprint(status_bp, url_prefix='/api')
    app.register_blueprint(training_bp, url_prefix='/api')
    
    # مسیر اصلی
    @app.route('/')
    def home():
        return jsonify({
            "message": "AI Trading System External API",
            "version": "1.0.0",
            "endpoints": [
                "GET /api/status",
                "POST /api/pause",
                "POST /api/resume",
                "POST /api/retrain",
                "POST /api/strategy/<name>/train",
                "POST /api/strategy/<name>/backtest"
            ]
        })
    
    # مدیریت خطاها
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

# اجرای مستقیم
if __name__ == '__main__':
    app = create_api_app()
    app.run(host='0.0.0.0', port=8000, debug=True)