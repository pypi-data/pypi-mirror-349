from .components.plain_language import compute_pla
from .components.structure import compute_scm
from .components.cognitive_load import compute_cle
from .components.inclusive_language import compute_ila

class ACS:
    """
    Accessibility Comprehension Score (ACS) Metric
    """
    def __init__(self, alpha=0.25, beta=0.25, gamma=0.25, delta=0.25):
        assert abs((alpha + beta + gamma + delta) - 1.0) < 1e-6, "Weights must sum to 1."
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

    def score(self, summary: str) -> dict:
        """
        Compute ACS and sub-metric scores for a given summary.
        Returns a dict with ACS and all sub-metrics.
        """
        # Handle empty summary
        if not summary.strip():
            return {
                "ACS": 1.0,
                "PLA": 1.0,
                "SCM": 1.0,
                "CLE": 1.0,
                "ILA": 1.0
            }
            
        pla = compute_pla(summary)
        scm = compute_scm(summary)
        cle = compute_cle(summary)
        ila = compute_ila(summary)
        
        acs = (
            self.alpha * pla
            + self.beta * scm
            + self.gamma * cle
            + self.delta * ila
        )
        
        return {
            "ACS": acs,
            "PLA": pla,
            "SCM": scm,
            "CLE": cle,
            "ILA": ila
        }