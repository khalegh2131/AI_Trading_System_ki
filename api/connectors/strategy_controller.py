# D:\AI\AI_Trading_System_ki\api\controllers\strategy_controller.py

import logging
from typing import Dict, Any

logger = logging.getLogger("StrategyController")

class StrategyController:
    def __init__(self):
        self.active_strategy = None
        self.strategies = {}  # ذخیره استراتژی‌ها
    
    def load_strategy(self, name: str, config: Dict) -> bool:
        """بارگذاری استراتژی"""
        try:
            # اینجا باید کد واقعی بارگذاری استراتژی باشه
            self.strategies[name] = config
            logger.info(f"استراتژی {name} بارگذاری شد")
            return True
        except Exception as e:
            logger.error(f"خطا در بارگذاری استراتژی {name}: {str(e)}")
            return False
    
    def activate_strategy(self, name: str) -> bool:
        """فعال‌سازی استراتژی"""
        if name in self.strategies:
            self.active_strategy = name
            logger.info(f"استراتژی {name} فعال شد")
            return True
        else:
            logger.error(f"استراتژی {name} یافت نشد")
            return False
    
    def deactivate_strategy(self) -> bool:
        """غیرفعال‌سازی استراتژی"""
        if self.active_strategy:
            previous = self.active_strategy
            self.active_strategy = None
            logger.info(f"استراتژی {previous} غیرفعال شد")
            return True
        return False
    
    def get_active_strategy(self) -> str:
        """دریافت نام استراتژی فعال"""
        return self.active_strategy
    
    def get_all_strategies(self) -> Dict:
        """دریافت لیست همه استراتژی‌ها"""
        return list(self.strategies.keys())

# نمونه استفاده:
if __name__ == "__main__":
    controller = StrategyController()
    print("کنترل استراتژی‌ها آماده است")