# tests/test_structural_checks.py

import pytest
import json
from iqprompter.structural_checks import (
    contains,
    matches_regex,
    is_json,
    is_schema_valid,
    similarity,
)

# ----- contains() -----
def test_contains_true():
    assert contains("foo", "foobar")

def test_contains_false():
    assert not contains("baz", "foobar")

# ----- matches_regex() -----
@pytest.mark.parametrize("pattern,text,expected", [
    (r"^foo", "foobar", True),
    (r"bar$", "foobar", True),
    (r"\d+", "no digits here", False),
])
def test_matches_regex(pattern, text, expected):
    assert matches_regex(pattern, text) is expected

# ----- is_json() -----
def test_is_json_true():
    assert is_json('{"a": 1, "b": [2,3]}')

def test_is_json_false():
    assert not is_json("not a json")

# ----- similarity() -----
def test_similarity_identical():
    assert similarity("hello", "hello") == 1.0

def test_similarity_different():
    assert similarity("abc", "xyz") < 0.1

# ----- is_schema_valid() -----
def test_schema_validation_pass():
    schema = {"type":"object","properties":{"x":{"type":"number"}},"required":["x"]}
    data = {"x": 10}
    assert is_schema_valid(data, schema)

def test_schema_validation_fail():
    schema = {"type":"object","properties":{"x":{"type":"number"}},"required":["x"]}
    data = {"x": "nope"}
    assert not is_schema_valid(data, schema)

def test_schema_requires_jsonschema(monkeypatch):
    import iqprompter.structural_checks as sc
    monkeypatch.setattr(sc, "_HAS_JSONSCHEMA", False)
    with pytest.raises(ImportError):
        sc.is_schema_valid({"x": 1}, {"type":"object"})
