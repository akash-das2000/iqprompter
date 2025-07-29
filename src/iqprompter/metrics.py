"""
Metrics for IQPrompter.
"""

from .utils import normalize_text


def hallucination_score(generated: str, reference: str) -> float:
    """
    Placeholder: lower is better.
    """
    return 0.0


def relevance_score(generated: str, reference: str) -> float:
    """
    Placeholder relevance metric.
    """
    return 1.0
