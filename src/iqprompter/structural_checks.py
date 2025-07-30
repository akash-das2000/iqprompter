# src/iqprompter/structural_checks.py

import json
import re
from difflib import SequenceMatcher
from typing import Any

# Try to import jsonschema for schema validation:
try:
    from jsonschema import validate, ValidationError
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False


def contains(substring: str, text: str) -> bool:
    """
    Return True if `substring` appears anywhere in `text`.
    Exact, case-sensitive match.
    """
    return substring in text


def matches_regex(pattern: str, text: str) -> bool:
    """
    Return True if the regex `pattern` matches anywhere in `text`.
    Uses `re.search()`, so it can match substrings.
    """
    return bool(re.search(pattern, text))


def is_json(text: str) -> bool:
    """
    Return True if `text` is valid JSON (parsable by json.loads).
    """
    try:
        json.loads(text)
        return True
    except (ValueError, TypeError):
        return False


def is_schema_valid(data: Any, schema: dict) -> bool:
    """
    Validate that `data` conforms to the given JSON `schema`.
    Requires the `jsonschema` package; raises ImportError if missing.
    """
    if not _HAS_JSONSCHEMA:
        raise ImportError(
            "JSON Schema validation requires the `jsonschema` library. "
            "Install with `pip install jsonschema`."
        )
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False


def similarity(a: str, b: str) -> float:
    """
    Return a [0.0–1.0] similarity score between two strings,
    based on difflib.SequenceMatcher (1.0 = identical).
    """
    return SequenceMatcher(None, a, b).ratio()
