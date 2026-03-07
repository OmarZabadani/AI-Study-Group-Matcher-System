import re
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in text.split() if word not in stop_words])