# D:\AI\AI_Trading_System_ki\integration\performance_monitor.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psutil
import logging
from datetime import datetime
import time
from typing import Dict

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

class PerformanceMonitor:
    def __init__(self):
        self.logger = get_logger("PerformanceMonitor")
        self.start_time = time.time()
        self.metrics_history = []
    
    def get_system_metrics(self) -> Dict:
        """دریافت معیارهای عملکرد سیستم"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory
            memory = psutil.virtual_memory()
            
            # Disk
            disk = psutil.disk_usage('/')
            
            # Network
            net_io = psutil.net_io_counters()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time() - self.start_time,
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0
                },
                'memory': {
                    'percent': memory.percent,
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2)
                },
                'disk': {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'percent': round((disk.used / disk.total) * 100, 2)
                },
                'network': {
                    'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                    'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2)
                }
            }
            
            # ذخیره در تاریخچه
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1000:  # حفظ 1000 ردیف آخر
                self.metrics_history = self.metrics_history[-1000:]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"خطا در دریافت معیارهای سیستم: {str(e)}")
            return {}
    
    def get_process_metrics(self) -> Dict:
        """دریافت معیارهای فرآیند فعلی"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'pid': process.pid,
                'name': process.name(),
                'cpu_percent': process.cpu_percent(),
                'memory_rss_mb': round(memory_info.rss / (1024**2), 2),
                'memory_vms_mb': round(memory_info.vms / (1024**2), 2),
                'num_threads': process.num_threads(),
                'create_time': datetime.fromtimestamp(process.create_time()).isoformat()
            }
        except Exception as e:
            self.logger.error(f"خطا در دریافت معیارهای فرآیند: {str(e)}")
            return {}
    
    def get_resource_usage_summary(self) -> str:
        """دریافت خلاصه مصرف منابع"""
        system_metrics = self.get_system_metrics()
        process_metrics = self.get_process_metrics()
        
        if not system_metrics or not process_metrics:
            return "خطا در دریافت معیارها"
        
        summary = f"""
📊 خلاصه مصرف منابع - {system_metrics['timestamp']}
{'='*50}

🖥️ سیستم:
  CPU: {system_metrics['cpu']['percent']}%
  RAM: {system_metrics['memory']['percent']}% ({system_metrics['memory']['used_gb']}GB/{system_metrics['memory']['total_gb']}GB)
  دیسک: {system_metrics['disk']['percent']}% ({system_metrics['disk']['used_gb']}GB/{system_metrics['disk']['total_gb']}GB)

sPid فرآیند: {process_metrics['pid']}
  CPU فرآیند: {process_metrics['cpu_percent']}%
  RAM فرآیند: {process_metrics['memory_rss_mb']}MB
  تعداد رشته‌ها: {process_metrics['num_threads']}
        """.strip()
        
        return summary
    
    def log_performance_alert(self, threshold_cpu: float = 80.0, 
                            threshold_memory: float = 80.0) -> bool:
        """ثبت هشدار عملکرد"""
        metrics = self.get_system_metrics()
        if not metrics:
            return False
            
        cpu_percent = metrics['cpu']['percent']
        memory_percent = metrics['memory']['percent']
        
        alerts = []
        if cpu_percent > threshold_cpu:
            alerts.append(f"CPU بیش از {threshold_cpu}%: {cpu_percent}%")
        if memory_percent > threshold_memory:
            alerts.append(f"RAM بیش از {threshold_memory}%: {memory_percent}%")
        
        if alerts:
            alert_msg = "⚠️ هشدار عملکرد: " + ", ".join(alerts)
            self.logger.warning(alert_msg)
            return True
            
        return False

# تست عملی:
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # دریافت معیارهای سیستم
    system_metrics = monitor.get_system_metrics()
    print("معیارهای سیستم:")
    print(f"CPU: {system_metrics['cpu']['percent']}%")
    print(f"RAM: {system_metrics['memory']['percent']}%")
    
    # دریافت معیارهای فرآیند
    process_metrics = monitor.get_process_metrics()
    print(f"\nsPid فرآیند: {process_metrics.get('pid', 'N/A')}")
    print(f"RAM فرآیند: {process_metrics.get('memory_rss_mb', 'N/A')}MB")
    
    # خلاصه مصرف منابع
    summary = monitor.get_resource_usage_summary()
    print(f"\n{summary}")