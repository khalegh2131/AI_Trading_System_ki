# D:\AI\AI_Trading_System_ki\vpn\connectivity_tester.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from typing import Dict, List
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

class ConnectivityTester:
    def __init__(self):
        self.logger = get_logger("ConnectivityTester")
        # لیست سرورهای تست
        self.test_endpoints = {
            'binance': 'https://api.binance.com/api/v3/ping',
            'coindesk': 'https://www.coindesk.com',
            'google': 'https://www.google.com',
            'github': 'https://api.github.com'
        }
        
    def test_endpoint(self, name: str, url: str, timeout: int = 5) -> Dict:
        """تست یک endpoint خاص"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            end_time = time.time()
            
            result = {
                'name': name,
                'url': url,
                'status': 'reachable' if response.status_code == 200 else 'unreachable',
                'status_code': response.status_code,
                'response_time': (end_time - start_time) * 1000,
                'error': None
            }
            
            return result
            
        except Exception as e:
            return {
                'name': name,
                'url': url,
                'status': 'unreachable',
                'status_code': None,
                'response_time': None,
                'error': str(e)
            }
    
    def test_all_endpoints(self) -> List[Dict]:
        """تست همه endpointها"""
        results = []
        self.logger.info("شروع تست دسترسی به سرورها...")
        
        for name, url in self.test_endpoints.items():
            result = self.test_endpoint(name, url)
            results.append(result)
            status = "✅" if result['status'] == 'reachable' else "❌"
            self.logger.info(f"{status} {name}: {result['status']}")
            
        return results
    
    def get_summary(self, results: List[Dict]) -> Dict:
        """دریافت خلاصه نتایج"""
        reachable = sum(1 for r in results if r['status'] == 'reachable')
        total = len(results)
        
        avg_response_time = 0
        reachable_results = [r for r in results if r['response_time'] is not None]
        if reachable_results:
            avg_response_time = sum(r['response_time'] for r in reachable_results) / len(reachable_results)
        
        return {
            'reachable_count': reachable,
            'total_count': total,
            'success_rate': (reachable / total) * 100 if total > 0 else 0,
            'average_response_time': avg_response_time,
            'details': results
        }

# تست عملی:
if __name__ == "__main__":
    tester = ConnectivityTester()
    results = tester.test_all_endpoints()
    summary = tester.get_summary(results)
    
    print(f"\nخلاصه تست:")
    print(f"دسترسی موفق: {summary['reachable_count']}/{summary['total_count']}")
    print(f"نرخ موفقیت: {summary['success_rate']:.1f}%")
    print(f"میانگین زمان پاسخ: {summary['average_response_time']:.2f}ms")