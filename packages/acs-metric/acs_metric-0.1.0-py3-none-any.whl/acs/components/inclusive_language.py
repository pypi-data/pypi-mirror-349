import re
from ..utils import CommonWords

def cultural_bias_score(summary):
    if not summary.strip():
        return 1.0
        
    # Expanded culture-specific references
    culture_specific = [
        'Thanksgiving', 'Christmas', 'Easter', 'Halloween',
        'Super Bowl', 'World Series', 'NBA', 'NFL',
        'Fourth of July', 'Independence Day', 'Boxing Day',
        'Diwali', 'Ramadan', 'Hanukkah'
    ]
    
    words = summary.lower().split()
    found = sum(1 for c in culture_specific if c.lower() in words)
    return max(0, 1 - found/2)  # More lenient threshold

def universal_reference_ratio(summary):
    if not summary.strip():
        return 1.0
        
    universal_terms = [
        'people', 'everyone', 'anybody', 'community',
        'global', 'worldwide', 'universal', 'common',
        'all', 'together', 'collaborate', 'participate',
        'team', 'group', 'member', 'person'
    ]
    
    words = summary.lower().split()
    found = sum(1 for term in universal_terms if term in words)
    return min(1, found / 3)  # Adjusted threshold

def inclusive_terminology_ratio(summary):
    if not summary.strip():
        return 1.0
        
    gendered = set([
        'he', 'she', 'his', 'her', 'him', 'hers', 'himself', 'herself',
        'chairman', 'mankind', 'manpower', 'businessman', 'policeman',
        'stewardess', 'mailman', 'saleswoman', 'actress'
    ])
    
    inclusive = CommonWords.INCLUSIVE_TERMS
    
    words = summary.lower().split()
    gen_count = sum(1 for w in words if w in gendered)
    inc_count = sum(1 for w in words if w in inclusive)
    
    if gen_count + inc_count == 0:
        return 0.5  # Neutral score if no relevant terms found
        
    return min(1, (inc_count * 2) / (gen_count + inc_count + 1))

def compute_ila(summary, w10=0.3, w11=0.3, w12=0.4):
    if not summary.strip():
        return 1.0
        
    cbs = cultural_bias_score(summary)
    urr = universal_reference_ratio(summary)
    itr = inclusive_terminology_ratio(summary)
    return w10 * cbs + w11 * urr + w12 * itr