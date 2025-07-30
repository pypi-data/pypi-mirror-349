import re
from collections import Counter

def summarize_text(text, max_sentences=2):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return ' '.join(sentences[:max_sentences])

def extract_keywords(text, top_n=5):
    words = re.findall(r'\b\w{4,}\b', text.lower())
    stopwords = {'this', 'that', 'with', 'from', 'your', 'have', 'more', 'just', 'some', 'like'}
    filtered = [word for word in words if word not in stopwords]
    most_common = Counter(filtered).most_common(top_n)
    return [word for word, count in most_common]
