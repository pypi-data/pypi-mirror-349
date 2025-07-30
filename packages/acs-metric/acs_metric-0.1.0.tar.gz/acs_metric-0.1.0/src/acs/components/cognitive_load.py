import re
from ..utils import TextUtils

def information_density(summary):
    """Calculate information density based on word count per sentence."""
    if not summary.strip():
        return 1.0
        
    sentences = [s.strip() for s in re.split(r'[.!?]', summary) if s.strip()]
    if not sentences:
        return 1.0
        
    avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
    return max(0, 1 - (avg_length-12)/24)  # scale: 12 words/sentence is ideal

def referential_distance(summary):
    """Measure distance between pronouns and their likely referents."""
    if not summary.strip():
        return 1.0
        
    sentences = [s.strip() for s in re.split(r'[.!?]', summary) if s.strip()]
    pronouns = ['it', 'they', 'this', 'that', 'these', 'those', 'he', 'she']
    total = 0
    distant = 0
    for i, s in enumerate(sentences):
        for p in pronouns:
            if p in s.lower():
                total += 1
                if i > 1:
                    distant += 1
    if not total:
        return 1.0
    return max(0, 1 - distant/total)

def example_presence(summary):
    """Check for presence of examples and illustrations."""
    if not summary.strip():
        return 1.0
        
    triggers = ['for example', 'such as', 'e.g.', 'like', 'for instance']
    count = sum(summary.lower().count(t) for t in triggers)
    sentences = max(1, len(re.split(r'[.!?]', summary.strip())))
    return min(1, count / sentences * 3)

def compute_cle(summary, w7=0.4, w8=0.3, w9=0.3):
    """Compute Cognitive Load Estimation score."""
    if not summary.strip():
        return 1.0
        
    iden = information_density(summary)
    rd = referential_distance(summary)
    ep = example_presence(summary)
    return w7 * iden + w8 * rd + w9 * ep