import re
from ..utils import TextUtils

def jargon_ratio(summary):
    # Expanded common words list
    common_words = set([
        "the", "is", "in", "it", "of", "and", "to", "a", "was", "for", "on", "with", "as", "by",
        "at", "from", "that", "be", "this", "which", "or", "have", "had", "what", "when", "where",
        "who", "will", "way", "about", "many", "then", "them", "would", "like", "so", "these",
        "her", "him", "but", "there", "can", "out", "other", "were", "all", "your", "we", "they"
    ])
    
    # Consider word length in complexity
    words = re.findall(r"\b\w+\b", summary.lower())
    if not words:
        return 1.0
    
    complex_words = [w for w in words if (w not in common_words or len(w) > 8)]
    return 1 - (len(complex_words) / len(words))

def sentence_complexity(summary):
    sentences = TextUtils.split_into_sentences(summary)
    if not sentences:
        return 1.0
    
    total_penalty = 0
    for sentence in sentences:
        words = sentence.split()
        # Penalize for:
        # 1. Long sentences
        length_penalty = len(words) / 20.0  # normalized by ideal length
        # 2. Complex punctuation
        punct_penalty = (sentence.count(",") + sentence.count(";")) * 0.2
        # 3. Long words
        long_words = len([w for w in words if len(w) > 8])
        word_penalty = long_words * 0.1
        
        total_penalty += (length_penalty + punct_penalty + word_penalty)
    
    avg_penalty = total_penalty / len(sentences)
    return max(0, 1 - avg_penalty)

def active_voice_ratio(summary):
    passive_patterns = [
        r'\b(is|are|was|were|be|been|being)\b\s+\w+ed\b',
        r'\b(is|are|was|were|be|been|being)\b\s+\w+en\b',
        r'\b(has|have|had)\b\s+been\b\s+\w+ed\b',
        r'\b(has|have|had)\b\s+been\b\s+\w+en\b'
    ]
    
    sentences = TextUtils.split_into_sentences(summary)
    if not sentences:
        return 1.0
    
    passive_count = 0
    for sentence in sentences:
        if any(re.search(pattern, sentence.lower()) for pattern in passive_patterns):
            passive_count += 1
    
    return 1 - (passive_count / len(sentences))

def compute_pla(summary, w1=0.4, w2=0.4, w3=0.2):
    if not summary.strip():
        return 1.0
        
    jr = jargon_ratio(summary)
    sc = sentence_complexity(summary)
    av = active_voice_ratio(summary)
    return w1 * jr + w2 * sc + w3 * av