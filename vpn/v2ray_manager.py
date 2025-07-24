# D:\AI\AI_Trading_System_ki\vpn\v2ray_manager.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import json
import base64
import tempfile
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

class V2RayManager:
    def __init__(self):
        self.logger = get_logger("V2RayManager")
        self.process = None
        self.config_file = None
        
    def parse_vmess_link(self, vmess_link: str) -> dict:
        """پارس کردن لینک vmess"""
        try:
            # حذف پیشوند
            if vmess_link.startswith('vmess://'):
                encoded = vmess_link[8:]  # حذف 'vmess://'
            else:
                raise ValueError("لینک vmess نامعتبر")
                
            # decode base64
            decoded = base64.b64decode(encoded).decode('utf-8')
            config = json.loads(decoded)
            return config
        except Exception as e:
            self.logger.error(f"خطا در پارس کردن لینک: {str(e)}")
            return {}
    
    def create_config_file(self, server_config: dict) -> str:
        """ایجاد فایل کانفیگ برای V2Ray"""
        try:
            # فرمت کانفیگ V2Ray
            v2ray_config = {
                "inbounds": [{
                    "port": 10808,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    }
                }],
                "outbounds": [{
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [{
                            "address": server_config.get("add", ""),
                            "port": server_config.get("port", 443),
                            "users": [{
                                "id": server_config.get("id", ""),
                                "alterId": server_config.get("aid", 0),
                                "security": server_config.get("scy", "auto")
                            }]
                        }]
                    },
                    "streamSettings": {
                        "network": server_config.get("net", "tcp"),
                        "security": "tls" if server_config.get("tls") == "tls" else "",
                        "tlsSettings": {
                            "serverName": server_config.get("host", "")
                        } if server_config.get("tls") == "tls" else {},
                        "wsSettings": {
                            "path": server_config.get("path", ""),
                            "headers": {
                                "Host": server_config.get("host", "")
                            }
                        } if server_config.get("net") == "ws" else {}
                    }
                }]
            }
            
            # ایجاد فایل موقت
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            json.dump(v2ray_config, temp_file, indent=2)
            temp_file.close()
            
            self.config_file = temp_file.name
            self.logger.info(f"فایل کانفیگ ایجاد شد: {self.config_file}")
            return self.config_file
            
        except Exception as e:
            self.logger.error(f"خطا در ایجاد کانفیگ: {str(e)}")
            return ""
    
    def start_v2ray(self, config_path: str) -> bool:
        """شروع V2Ray با کانفیگ داده شده"""
        try:
            # بررسی وجود v2ray
            result = subprocess.run(['v2ray', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error("V2Ray نصب نیست یا در PATH نیست")
                return False
                
            # شروع V2Ray
            self.process = subprocess.Popen([
                'v2ray', 'run', '-c', config_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.logger.info("✅ V2Ray شروع شد")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ خطا در شروع V2Ray: {str(e)}")
            return False
    
    def stop_v2ray(self) -> bool:
        """توقف V2Ray"""
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.logger.info("✅ V2Ray متوقف شد")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ خطا در توقف V2Ray: {str(e)}")
            return False

# تست عملی:
if __name__ == "__main__":
    # این تست نیاز به نصب V2Ray داره
    manager = V2RayManager()
    print("مدیریت V2Ray آماده است")