# D:\AI\AI_Trading_System_ki\nlp\utils.py

import re
from datetime import datetime
from typing import List, Dict

def extract_symbols_from_text(text: str) -> List[str]:
    """استخراج نمادهای ارز دیجیتال از متن"""
    # الگوهای رایج برای نمادها
    patterns = [
        r'\b(BTC|ETH|XRP|ADA|DOGE|SOL|DOT|AVAX|LINK|UNI)\b',
        r'\b([A-Z]{2,8})\b'  # نمادهای عمومی
    ]
    
    symbols = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        symbols.extend([match.upper() for match in matches])
        
    return list(set(symbols))  # حذف تکراری‌ها

def format_news_for_display(news_item: Dict) -> str:
    """فرمت‌بندی خبر برای نمایش"""
    return f"""
📰 {news_item.get('title', 'بدون عنوان')}
📅 {news_item.get('published', 'بدون تاریخ')}
🔗 {news_item.get('link', 'بدون لینک')}
    """.strip()