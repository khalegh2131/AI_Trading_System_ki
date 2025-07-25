# D:\AI\AI_Trading_System_ki\integration\module_connector.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from api.api_hub import APIHub
from vpn.vpn_scanner import VPNScanner
from security.key_manager import KeyManager
from learning.ensemble_model import EnsembleModel

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

class ModuleConnector:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("ModuleConnector")
        self.modules = {}
    
    def connect_all_modules(self) -> dict:
        """اتصال همه ماژول‌ها به هم"""
        self.logger.info("در حال اتصال ماژول‌ها...")
        
        # اتصال API Hub
        self.modules['api_hub'] = self._connect_api_hub()
        
        # اتصال VPN Scanner
        self.modules['vpn_scanner'] = self._connect_vpn_scanner()
        
        # اتصال Key Manager
        self.modules['key_manager'] = self._connect_key_manager()
        
        # اتصال Ensemble Model
        self.modules['ensemble_model'] = self._connect_ensemble_model()
        
        self.logger.info("✅ همه ماژول‌ها متصل شدند")
        return self.modules
    
    def _connect_api_hub(self):
        """اتصال API Hub"""
        try:
            api_hub = APIHub(self.config)
            self.logger.info("API Hub متصل شد")
            return api_hub
        except Exception as e:
            self.logger.error(f"خطا در اتصال API Hub: {str(e)}")
            return None
    
    def _connect_vpn_scanner(self):
        """اتصال VPN Scanner"""
        try:
            vpn_scanner = VPNScanner(self.config)
            self.logger.info("VPN Scanner متصل شد")
            return vpn_scanner
        except Exception as e:
            self.logger.error(f"خطا در اتصال VPN Scanner: {str(e)}")
            return None
    
    def _connect_key_manager(self):
        """اتصال Key Manager"""
        try:
            key_manager = KeyManager()
            self.logger.info("Key Manager متصل شد")
            return key_manager
        except Exception as e:
            self.logger.error(f"خطا در اتصال Key Manager: {str(e)}")
            return None
    
    def _connect_ensemble_model(self):
        """اتصال Ensemble Model"""
        try:
            ensemble_model = EnsembleModel(
                state_size=self.config.get('learning', {}).get('rl_agent', {}).get('state_size', 20),
                action_size=self.config.get('learning', {}).get('rl_agent', {}).get('action_size', 3)
            )
            self.logger.info("Ensemble Model متصل شد")
            return ensemble_model
        except Exception as e:
            self.logger.error(f"خطا در اتصال Ensemble Model: {str(e)}")
            return None

# تست عملی:
if __name__ == "__main__":
    # تنظیمات نمونه
    sample_config = {
        "apis": {
            "crypto": [
                {
                    "name": "Binance",
                    "base_url": "https://api.binance.com",
                    "key": "test_key",
                    "secret": "test_secret",
                    "ping_url": "https://api.binance.com/api/v3/ping"
                }
            ]
        },
        "learning": {
            "rl_agent": {
                "state_size": 20,
                "action_size": 3
            }
        }
    }
    
    connector = ModuleConnector(sample_config)
    modules = connector.connect_all_modules()
    print("ماژول‌های متصل شده:", list(modules.keys()))