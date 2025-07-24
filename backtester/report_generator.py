# D:\AI\AI_Trading_System_ki\backtester\report_generator.py

import pandas as pd
from datetime import datetime
import json
from typing import Dict

class ReportGenerator:
    def __init__(self):
        pass
        
    def generate_html_report(self, results: Dict, filename: str = None) -> str:
        """تولید گزارش HTML"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>گزارش بک‌تست</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .result-item {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .metric {{ font-weight: bold; color: #333; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>گزارش بک‌تست - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}</h1>
                <div class="result-item">
                    <div class="metric">موجودی اولیه: {results.get('initial_balance', 0)}</div>
                    <div class="metric">موجودی نهایی: {results.get('final_balance', 0):.2f}</div>
                    <div class="metric">بازده کل: {results.get('total_return', 0):.2f}%</div>
                    <div class="metric">تعداد معاملات: {results.get('total_trades', 0)}</div>
                    <div class="metric">درصد برد: {results.get('win_rate', 0):.2f}%</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return filename

# مثال استفاده:
if __name__ == "__main__":
    # تست گزارش
    pass