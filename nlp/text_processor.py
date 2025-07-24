# D:\AI\AI_Trading_System_ki\nlp\text_processor.py

import re
import string
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextProcessor:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text: str) -> str:
        """پاک‌سازی متن"""
        # حذف URL
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # حذف ایمیل
        text = re.sub(r'\S+@\S+', '', text)
        
        # حذف اعداد
        text = re.sub(r'\d+', '', text)
        
        # حذف علائم نگارشی
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # حذف فضای خالی اضافی
        text = ' '.join(text.split())
        
        return text.lower()
    
    def tokenize_and_filter(self, text: str) -> List[str]:
        """توکن‌سازی و فیلتر کلمات"""
        cleaned = self.clean_text(text)
        tokens = word_tokenize(cleaned)
        filtered_tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        return filtered_tokens

# تست عملی:
if __name__ == "__main__":
    processor = TextProcessor()
    sample_text = "This is a sample text with URLs https://example.com and emails test@email.com!"
    cleaned = processor.clean_text(sample_text)
    tokens = processor.tokenize_and_filter(sample_text)
    print("متن پاک‌سازی شده:", cleaned)
    print("توکن‌ها:", tokens)