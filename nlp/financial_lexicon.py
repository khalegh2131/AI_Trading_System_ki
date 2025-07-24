# D:\AI\AI_Trading_System_ki\nlp\financial_lexicon.py

# واژگان مالی کلیدی برای تحلیل بهتر
FINANCIAL_KEYWORDS = {
    'positive': [
        'increase', 'rise', 'gain', 'boost', 'surge', 'jump', 'climb', 'grow',
        'bullish', 'optimistic', 'confidence', 'strong', 'profit', 'success',
        'buy', 'bull', 'up', 'green', 'positive'
    ],
    'negative': [
        'decrease', 'fall', 'drop', 'decline', 'plunge', 'crash', 'collapse',
        'bearish', 'pessimistic', 'fear', 'weak', 'loss', 'failure',
        'sell', 'bear', 'down', 'red', 'negative', 'crisis'
    ],
    'cryptocurrency': [
        'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain',
        'coin', 'token', 'wallet', 'exchange', 'mining'
    ]
}

def get_sentiment_from_keywords(text: str) -> str:
    """تحلیل احساسات بر اساس واژگان کلیدی"""
    text_lower = text.lower()
    positive_count = sum(1 for word in FINANCIAL_KEYWORDS['positive'] if word in text_lower)
    negative_count = sum(1 for word in FINANCIAL_KEYWORDS['negative'] if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

# تست عملی:
if __name__ == "__main__":
    test_text = "Bitcoin price is rising and investors are bullish"
    sentiment = get_sentiment_from_keywords(test_text)
    print(f"احساس کلیدواژه‌ای: {sentiment}")