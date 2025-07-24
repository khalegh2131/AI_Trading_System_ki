# D:\AI\AI_Trading_System_ki\utils\logger.py

import logging
import os
from datetime import datetime

def get_logger(name: str, log_file: str = None) -> logging.Logger:
    """Create uniform logger for system"""
    
    # Create logs folder if not exists
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Use filename if not specified
    if log_file is None:
        log_file = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger