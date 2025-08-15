"""Utilities for extracting conversation data from rendered pages.

This module currently provides a helper for pulling the latest assistant
response from a DOM tree.  It is designed to work with Playwright's
``Page`` object but can also accept raw HTML strings for testing.
"""

from __future__ import annotations

from html import unescape
from typing import Any, Dict, List, Union

try:  # Optional dependency for HTML parsing
    from bs4 import BeautifulSoup, NavigableString, Tag  # type: ignore
except Exception:  # pragma: no cover - fall back to minimal parser
    BeautifulSoup = None  # type: ignore
    NavigableString = None  # type: ignore
    Tag = None  # type: ignore


# ---------------------------------------------------------------------------
def _get_html(page: Union[str, Any]) -> str:
    """Return HTML content from a Playwright ``Page`` or raw string.

    Parameters
    ----------
    page:
        Either a Playwright :class:`~playwright.sync_api.Page` instance or an
        HTML string.  The function attempts to call ``page.content`` when
        ``page`` exposes such a method; otherwise it assumes ``page`` is a
        string containing HTML markup.
    """

    if hasattr(page, "content") and callable(page.content):
        return page.content()
    if isinstance(page, str):
        return page
    raise TypeError("page must be an HTML string or provide a .content() method")


# ---------------------------------------------------------------------------
def _normalise_node_text(node: Any) -> str:
    """Return normalised text content for a DOM node.

    This helper strips surrounding whitespace, decodes HTML entities and
    preserves code blocks by wrapping them in triple backticks.  When
    ``BeautifulSoup`` is unavailable the function falls back to a very simple
    tag removal strategy.
    """

    if BeautifulSoup and isinstance(node, Tag):
        pieces: List[str] = []
        for child in node.descendants:
            if isinstance(child, Tag) and child.name in {"pre", "code"}:
                text = child.get_text("", strip=False)
                if text:
                    pieces.append("\n```\n" + text.strip() + "\n```\n")
            elif isinstance(child, NavigableString):
                pieces.append(str(child))
        text = "".join(pieces)
    else:  # Fallback: naive tag removal
        text = str(node)
        # remove HTML tags
        import re

        text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(lines).strip()


# ---------------------------------------------------------------------------
def get_last_response(page: Union[str, Any], structured: bool = False) -> Union[str, Dict[str, str]]:
    """Extract the most recent assistant response from the page.

    The function searches the DOM for elements that are likely to contain an
    assistant's reply.  Candidates are selected using a collection of common
    attributes used by chat interfaces (e.g. ``data-testid="assistant-message"``
    or classes containing ``assistant``).  Among all candidates the longest
    normalised message is returned, which typically corresponds to the final
    complete response.

    Parameters
    ----------
    page:
        Playwright :class:`Page` object or raw HTML string to search.
    structured:
        When ``True`` a dictionary containing both the text and raw HTML of the
        selected node is returned.  Otherwise just the normalised text is
        returned.
    """

    html = _get_html(page)

    if BeautifulSoup is None:  # pragma: no cover - dependency missing
        # Minimal fallback: return raw text stripped of tags
        text = _normalise_node_text(html)
        return {"text": text} if structured else text

    soup = BeautifulSoup(html, "html.parser")

    # Common selectors for assistant messages across chat UIs
    selectors = [
        '[data-testid="assistant-message"]',
        '[data-message-author-role="assistant"]',
        '.assistant',
        '[data-role="assistant"]',
    ]

    candidates: List[Tag] = []
    for sel in selectors:
        candidates.extend(soup.select(sel))

    if not candidates:
        return {"text": ""} if structured else ""

    # Choose the candidate with the longest normalised text
    best_node = max(candidates, key=lambda n: len(_normalise_node_text(n)))
    text = _normalise_node_text(best_node)

    if structured:
        return {"text": text, "html": str(best_node)}
    return text


__all__ = ["get_last_response"]
