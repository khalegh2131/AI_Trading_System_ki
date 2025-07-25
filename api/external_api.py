# D:\AI\AI_Trading_System_ki\api\external_api.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from api.routes.control_routes import control_bp
from api.routes.status_routes import status_bp
from api.routes.training_routes import training_bp

def create_api_app():
    app = Flask(__name__)
    
    # ثبت بلوپرینت‌ها
    app.register_blueprint(control_bp, url_prefix='/api')
    app.register_blueprint(status_bp, url_prefix='/api')
    app.register_blueprint(training_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "AI Trading System External API",
            "version": "1.0.0",
            "endpoints": [
                "GET /api/status",
                "POST /api/pause",
                "POST /api/resume"
            ]
        })
    
    return app

if __name__ == '__main__':
    app = create_api_app()
    app.run(host='0.0.0.0', port=8000, debug=True)