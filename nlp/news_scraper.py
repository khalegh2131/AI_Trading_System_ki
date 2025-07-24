# D:\AI\AI_Trading_System_ki\nlp\news_scraper.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
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

class NewsScraper:
    def __init__(self):
        self.logger = get_logger("NewsScraper")
        self.news_sources = [
            'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'https://cointelegraph.com/rss',
            'https://news.google.com/rss/search?q=cryptocurrency'
        ]
        
    def scrape_rss_feeds(self, hours_back: int = 24) -> List[Dict]:
        """جمع‌آوری اخبار از فید RSS"""
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for source in self.news_sources:
            try:
                feed = feedparser.parse(source)
                for entry in feed.entries:
                    pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
                    
                    if pub_date >= cutoff_time:
                        news_item = {
                            'title': entry.title,
                            'summary': getattr(entry, 'summary', ''),
                            'link': entry.link,
                            'published': pub_date.isoformat(),
                            'source': source
                        }
                        all_news.append(news_item)
                        
            except Exception as e:
                self.logger.error(f"خطا در جمع‌آوری از {source}: {str(e)}")
                continue
                
        self.logger.info(f"جمع‌آوری شد {len(all_news)} خبر")
        return all_news

# تست عملی:
if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.scrape_rss_feeds(hours_back=2)
    print(f"جمع‌آوری شد {len(news)} خبر")
    if news:
        print("آخرین خبر:", news[0]['title'])