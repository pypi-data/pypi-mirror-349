import pytest
from acs import ACS
from acs.utils import TextUtils, ValidationUtils, calculate_text_stats

class TestACSMetric:
    @pytest.fixture
    def acs(self):
        return ACS()
    
    def test_basic_summary(self, acs):
        summary = "This is a simple test. It uses basic language."
        result = acs.score(summary)
        assert all(0 <= score <= 1 for score in result.values())
    
    def test_complex_summary(self, acs):
        summary = """
        The implementation methodology necessitates complex paradigms vis-à-vis
        instantiation of hierarchical structures. Furthermore, it requires
        extensive cognitive processing capabilities through metaphysical constructs.
        """
        result = acs.score(summary)
        assert result["PLA"] < 0.5  # Should score low on plain language due to complexity
    
    def test_inclusive_summary(self, acs):
        summary = """
        People worldwide contribute to this project together.
        Team members collaborate effectively across all communities.
        The group ensures universal participation and accessibility.
        Everyone has equal opportunities to participate.
        """
        result = acs.score(summary)
        assert result["ILA"] > 0.7  # Should score high on inclusive language
    
    def test_empty_summary(self, acs):
        result = acs.score("")
        assert all(score == 1.0 for score in result.values()), \
            f"Empty summary should return 1.0 for all metrics, got: {result}"
    
    def test_weight_validation(self):
        with pytest.raises(AssertionError):
            ACS(alpha=0.5, beta=0.5, gamma=0.5, delta=0.5)
    
    def test_utils(self):
        text = "This is a test. This is another test!"
        sentences = TextUtils.split_into_sentences(text)
        assert len(sentences) == 2
        stats = calculate_text_stats(text)
        assert stats['sentence_count'] == 2
        assert stats['word_count'] > 0
