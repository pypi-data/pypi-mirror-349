"""
ACS Metric - Accessibility Comprehension Score
"""

from .metric import ACS
from .utils import calculate_text_stats, MetricLogger

__version__ = "0.1.0"
__author__ = "Afsal-CP"
__email__ = "your.email@domain.com"

__all__ = ['ACS', 'calculate_text_stats', 'MetricLogger']