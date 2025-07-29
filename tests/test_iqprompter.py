from iqprompter.core import evaluate
from iqprompter.metrics import hallucination_score, relevance_score


def test_evaluate_returns_dict():
    result = evaluate("What is 2+2?", "It is 4.")
    assert isinstance(result, dict)


def test_hallucination_score_zero_when_equal():
    assert hallucination_score("foo", "foo") == 0.0


def test_relevance_score_max_when_equal():
    assert relevance_score("bar", "bar") == 1.0
