import re
from ..utils import TextUtils

def topic_consistency(summary):
    """Measure consistency of topics across sentences."""
    if not summary.strip():
        return 1.0
        
    sentences = [s.strip() for s in re.split(r'[.!?]', summary) if s.strip()]
    if len(sentences) < 2:
        return 1.0
        
    first_words = set(sentences[0].lower().split())
    consistency = 0
    for s in sentences[1:]:
        overlap = first_words.intersection(set(s.lower().split()))
        consistency += bool(overlap)
    return consistency / max(1, (len(sentences)-1))

def transition_quality(summary):
    """Measure the use of transition words and phrases."""
    if not summary.strip():
        return 1.0
        
    transitions = ['however', 'therefore', 'in addition', 'moreover', 'thus', 
                  'furthermore', 'meanwhile', 'consequently', 'nevertheless']
    count = sum(summary.lower().count(t) for t in transitions)
    sentences = max(1, len(re.split(r'[.!?]', summary.strip())))
    return min(1, count / sentences * 2)

def information_hierarchy(summary):
    """Check if paragraphs have clear topic sentences."""
    if not summary.strip():
        return 1.0
        
    paragraphs = [p for p in summary.split('\n') if p.strip()]
    if not paragraphs:
        return 1.0
        
    topic_count = 0
    for p in paragraphs:
        words = set(p.split())
        if words and len(words) > 4:
            topic_count += 1
    return topic_count / len(paragraphs)

def compute_scm(summary, w4=0.34, w5=0.33, w6=0.33):
    """Compute Structural Clarity Measurement score."""
    if not summary.strip():
        return 1.0
        
    tc = topic_consistency(summary)
    tq = transition_quality(summary)
    ih = information_hierarchy(summary)
    return w4 * tc + w5 * tq + w6 * ih