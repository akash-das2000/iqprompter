def normalize_text(text: str) -> str:
    """Lowercase & strip extra whitespace."""
    return " ".join(text.lower().split())
