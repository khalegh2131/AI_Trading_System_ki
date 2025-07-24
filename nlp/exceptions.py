# D:\AI\AI_Trading_System_ki\nlp\exceptions.py

class NLPErro(Exception):
    """خطای پایه برای NLP"""
    pass

class SentimentAnalysisError(NLPErro):
    """خطای تحلیل احساسات"""
    pass

class NewsScrapingError(NLPErro):
    """خطای جمع‌آوری اخبار"""
    pass

class APIIntegrationError(NLPErro):
    """خطای اتصال به APIهای متنی"""
    pass