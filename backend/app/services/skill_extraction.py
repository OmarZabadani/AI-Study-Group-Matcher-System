# services/skill_extractor.py

import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords if not already
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def extract_skills_from_text(text, top_n=20):
    """
    Extract potential skills from any text dynamically.
    Returns a list of keywords ranked by frequency.
    
    Args:
        text (str): Resume or job description text
        top_n (int): Number of top frequent words to return
    
    Returns:
        List[str]: List of potential skills/keywords
    """
    if not text:
        return []

    # Lowercase and remove non-alphabetic characters
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = text.split()

    # Remove stopwords and single-character words
    words = [w for w in words if w not in stop_words and len(w) > 1]

    # Count frequency
    word_counts = Counter(words)

    # Return top N most common words as "skills"
    skills_sorted = [w for w, _ in word_counts.most_common(top_n)]
    return skills_sorted

def compare_skills(resume_skills, job_skills):
    """
    Compare dynamic skills lists from resume and job description.
    
    Args:
        resume_skills (List[str])
        job_skills (List[str])
    
    Returns:
        matched (List[str]): Skills both have
        missing (List[str]): Skills in job but not in resume
    """
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))
    return matched, missing