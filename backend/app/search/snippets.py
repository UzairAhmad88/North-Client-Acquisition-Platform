"""Secure Search Snippet Generator with Safe Highlighting and Information Leakage Defense."""

import re
from typing import List, Optional


class SnippetGenerator:
    """Generates contextual preview snippets strictly from authorized text fields."""

    @classmethod
    def generate(
        cls,
        text: Optional[str],
        query_terms: List[str],
        max_length: int = 160,
        is_restricted: bool = False,
    ) -> str:
        """Construct highlighted snippet without leaking restricted information."""
        if is_restricted:
            return "Content preview restricted by authorization policy."

        if not text or not text.strip():
            return "No preview available."

        clean_text = re.sub(r"\s+", " ", text).strip()
        if len(clean_text) <= max_length:
            return cls._highlight_terms(clean_text, query_terms)

        # Locate first matching term index
        first_idx = -1
        lower_text = clean_text.lower()
        for term in query_terms:
            if term:
                pos = lower_text.find(term.lower())
                if pos != -1 and (first_idx == -1 or pos < first_idx):
                    first_idx = pos

        if first_idx == -1:
            snippet = clean_text[:max_length] + "..."
            return cls._highlight_terms(snippet, query_terms)

        # Center window around first matching term
        start = max(0, first_idx - 40)
        end = min(len(clean_text), start + max_length)
        if start > 0:
            start_space = clean_text.find(" ", start)
            if start_space != -1 and start_space < first_idx:
                start = start_space + 1

        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(clean_text) else ""
        snippet = f"{prefix}{clean_text[start:end]}{suffix}"

        return cls._highlight_terms(snippet, query_terms)

    @classmethod
    def _highlight_terms(cls, snippet: str, query_terms: List[str]) -> str:
        """Surround matched query terms with safe <mark> tags."""
        if not query_terms:
            return snippet

        highlighted = snippet
        for term in query_terms:
            if len(term) > 1:
                pattern = re.compile(rf"({re.escape(term)})", re.IGNORECASE)
                highlighted = pattern.sub(r"<mark>\1</mark>", highlighted)

        return highlighted
