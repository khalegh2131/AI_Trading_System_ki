# D:\AI\AI_Trading_System_ki\api\utils.py

import json
from datetime import datetime
from typing import Dict, Any

def format_response(data: Dict, success: bool = True) -> Dict:
    """فرمت‌بندی پاسخ API"""
    return {
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

def format_error(message: str, code: int = 400) -> Dict:
    """فرمت‌بندی خطا"""
    return {
        "success": False,
        "timestamp": datetime.now().isoformat(),
        "error": {
            "message": message,
            "code": code
        }
    }

def validate_json_request(request_data: str) -> tuple:
    """اعتبارسنجی درخواست JSON"""
    try:
        data = json.loads(request_data)
        return True, data
    except json.JSONDecodeError as e:
        return False, {"error": f"JSON نامعتبر: {str(e)}"}

def get_client_ip(request) -> str:
    """دریافت IP کلاینت"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '127.0.0.1'