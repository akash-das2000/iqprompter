# src/iqprompter/metrics.py

import json
from typing import Any, Dict, List, Pattern, Union

from .structural_checks import (
    contains as _contains,
    matches_regex as _matches_regex,
    is_json as _is_json,
    is_schema_valid as _is_schema_valid,
    similarity as _similarity,
)

# ——————————————
# Named‐preset registry
# ——————————————
_STRUCTURE_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_structure(
    name: str,
    *,
    contains_list: List[str] = None,
    regex_list: List[Union[str, Pattern]] = None,
    schema: Dict[str, Any] = None,
    similarity_with: str = None,
) -> None:
    """
    Register a named Layer-1 template. Later you can invoke
    level1_check(preset=name) instead of passing all lists.
    """
    _STRUCTURE_REGISTRY[name] = {
        "contains_list": contains_list or [],
        "regex_list":   regex_list or [],
        "schema":       schema,
        "similarity_with": similarity_with,
    }


def get_structure(name: str) -> Dict[str, Any]:
    """Retrieve a previously registered template by name."""
    try:
        return _STRUCTURE_REGISTRY[name]
    except KeyError:
        raise KeyError(f"No structure registered under name={name!r}")


# ——————————————
# PromptEvaluator
# ——————————————
class PromptEvaluator:
    """
    Wraps a text string and provides both standalone structural checks
    and a one‐shot level1_check(preset=…) API.
    """

    def __init__(self, text: str):
        self.text = text

    # Individual methods
    def contains(self, substring: str) -> bool:
        return _contains(substring, self.text)

    def matches_regex(self, pattern: Union[str, Pattern]) -> bool:
        return _matches_regex(pattern, self.text)

    def is_json(self) -> bool:
        return _is_json(self.text)

    def similarity(self, other: str) -> float:
        return _similarity(self.text, other)

    def is_schema_valid(self, schema: Dict[str, Any]) -> bool:
        if not self.is_json():
            raise ValueError("Cannot validate schema: text is not valid JSON.")
        data = json.loads(self.text)
        return _is_schema_valid(data, schema)

    # One‐shot Layer-1
    def level1_check(
        self,
        *,
        preset: str = None,
        contains_list: List[str] = None,
        regex_list: List[Union[str, Pattern]] = None,
        schema: Dict[str, Any] = None,
        similarity_with: str = None,
    ) -> Dict[str, Any]:
        """
        If `preset` is provided, it overrides the explicit lists/schema.
        Returns a dict of sub‐results.
        """
        if preset:
            cfg = get_structure(preset)
            contains_list    = cfg["contains_list"]
            regex_list       = cfg["regex_list"]
            schema           = cfg["schema"]
            similarity_with  = cfg["similarity_with"]

        results: Dict[str, Any] = {}

        if contains_list is not None:
            results["contains"] = {
                s: self.contains(s) for s in contains_list
            }

        if regex_list is not None:
            results["regex"] = {
                r: self.matches_regex(r) for r in regex_list
            }

        if schema is not None:
            try:
                results["schema_valid"] = self.is_schema_valid(schema)
            except Exception as e:
                results["schema_error"] = str(e)

        if similarity_with is not None:
            results["similarity"] = self.similarity(similarity_with)

        return results
