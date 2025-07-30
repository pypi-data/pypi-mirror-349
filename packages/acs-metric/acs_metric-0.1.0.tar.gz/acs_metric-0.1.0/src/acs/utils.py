import re
from typing import List, Set, Dict, Union, Optional
from datetime import datetime

class TextUtils:
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences, handling common abbreviations."""
        # Handle common abbreviations to avoid false sentence splits
        text = re.sub(r'(?<=Mr)\.', '@', text)
        text = re.sub(r'(?<=Dr)\.', '@', text)
        text = re.sub(r'(?<=Mrs)\.', '@', text)
        text = re.sub(r'(?<=Ms)\.', '@', text)
        text = re.sub(r'(?<=Prof)\.', '@', text)
        text = re.sub(r'(?<=Ph)\.D\.', '@D@', text)
        
        # Split sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Restore periods in abbreviations
        sentences = [s.replace('@', '.').replace('@D@', '.D.') for s in sentences]
        
        return sentences

    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return paragraphs

    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text."""
        return len(re.findall(r'\b\w+\b', text))

    @staticmethod
    def unique_words(text: str) -> Set[str]:
        """Get set of unique words in text."""
        return set(re.findall(r'\b\w+\b', text.lower()))

class ValidationUtils:
    @staticmethod
    def validate_weights(weights: Dict[str, float]) -> bool:
        """
        Validate that weights sum to 1.0 (within floating point precision).
        """
        return abs(sum(weights.values()) - 1.0) < 1e-6

    @staticmethod
    def validate_score(score: float) -> float:
        """
        Ensure score is between 0 and 1.
        """
        return max(0.0, min(1.0, score))

class MetricLogger:
    def __init__(self):
        self.log_entries: List[Dict] = []

    def log_metric_calculation(self, 
                             metric_name: str, 
                             score: float, 
                             text: str,
                             details: Optional[Dict] = None) -> None:
        """
        Log metric calculations for debugging and analysis.
        """
        entry = {
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'metric': metric_name,
            'score': score,
            'text_length': len(text),
            'sentence_count': len(TextUtils.split_into_sentences(text)),
            'details': details or {}
        }
        self.log_entries.append(entry)

    def get_logs(self) -> List[Dict]:
        """
        Retrieve logged entries.
        """
        return self.log_entries

class CommonWords:
    """
    Common word lists for various purposes.
    """
    TRANSITION_WORDS: Set[str] = {
        'however', 'therefore', 'thus', 'hence', 'consequently',
        'furthermore', 'moreover', 'in addition', 'besides', 'alternatively',
        'meanwhile', 'nonetheless', 'nevertheless', 'in contrast',
        'for example', 'for instance', 'specifically', 'in particular',
        'first', 'second', 'third', 'finally', 'lastly'
    }

    INCLUSIVE_TERMS: Set[str] = {
        'person', 'people', 'they', 'them', 'their', 'theirs',
        'everyone', 'everybody', 'humanity', 'humankind',
        'staff', 'team', 'crew', 'workforce', 'personnel'
    }

    GENDERED_TERMS: Dict[str, str] = {
        'mankind': 'humanity',
        'manpower': 'workforce',
        'chairman': 'chair',
        'policeman': 'police officer',
        'fireman': 'firefighter',
        'stewardess': 'flight attendant',
        'businessman': 'business person',
        'mailman': 'mail carrier'
    }

def calculate_text_stats(text: str) -> Dict[str, Union[int, float]]:
    """
    Calculate various statistics about the text.
    """
    sentences = TextUtils.split_into_sentences(text)
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = len(set(words))
    
    stats = {
        'sentence_count': len(sentences),
        'word_count': len(words),
        'unique_words': unique_words,
        'avg_words_per_sentence': len(words) / max(len(sentences), 1),
        'lexical_diversity': unique_words / max(len(words), 1),
        'paragraph_count': len(TextUtils.split_into_paragraphs(text))
    }
    
    return stats

def get_version() -> str:
    """
    Return the current version of the ACS metric.
    """
    return "0.1.0"

# Example usage:
if __name__ == "__main__":
    # Test the utilities
    sample_text = """
    This is a sample paragraph. It contains multiple sentences!
    This is another paragraph. For example, it demonstrates the usage.
    """
    
    # Test text utils
    sentences = TextUtils.split_into_sentences(sample_text)
    paragraphs = TextUtils.split_into_paragraphs(sample_text)
    word_count = TextUtils.word_count(sample_text)
    
    # Test validation
    weights = {'w1': 0.3, 'w2': 0.3, 'w3': 0.4}
    is_valid = ValidationUtils.validate_weights(weights)
    
    # Test logger
    logger = MetricLogger()
    logger.log_metric_calculation('test_metric', 0.85, sample_text)
    
    # Test stats
    stats = calculate_text_stats(sample_text)
    
    print(f"Sentences: {len(sentences)}")
    print(f"Paragraphs: {len(paragraphs)}")
    print(f"Word count: {word_count}")
    print(f"Weights valid: {is_valid}")
    print(f"Stats: {stats}")