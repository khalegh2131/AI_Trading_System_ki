# D:\AI\AI_Trading_System_ki\vpn\utils.py

import base64
import json
from typing import Dict, List
import logging

def decode_subscription(content: str) -> List[str]:
    """decode کردن محتوای اشتراک"""
    try:
        decoded = base64.b64decode(content).decode('utf-8')
        links = decoded.strip().split('\n')
        return [link for link in links if link.strip()]
    except Exception as e:
        logging.error(f"خطا در decode اشتراک: {str(e)}")
        return []

def is_valid_vmess_link(link: str) -> bool:
    """بررسی اعتبار لینک vmess"""
    return link.startswith('vmess://') and len(link) > 8

def is_valid_vless_link(link: str) -> bool:
    """بررسی اعتبار لینک vless"""
    return link.startswith('vless://')

def extract_server_info(config: Dict) -> Dict:
    """استخراج اطلاعات سرور از کانفیگ"""
    return {
        'address': config.get('add', ''),
        'port': config.get('port', ''),
        'id': config.get('id', ''),
        'network': config.get('net', 'tcp'),
        'security': config.get('tls', ''),
        'remark': config.get('ps', 'Unknown')
    }

def format_server_list(servers: List[Dict]) -> str:
    """فرمت‌بندی لیست سرورها برای نمایش"""
    if not servers:
        return "هیچ سروری یافت نشد"
        
    formatted = []
    for i, server in enumerate(servers[:10], 1):  # فقط 10 تا اولی
        info = extract_server_info(server)
        formatted.append(
            f"{i}. {info['remark']} - {info['address']}:{info['port']}"
        )
        
    return "\n".join(formatted)