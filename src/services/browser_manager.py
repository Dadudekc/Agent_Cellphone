"""Browser management utilities built on Playwright.

This module provides a lightweight wrapper around Playwright's synchronous
API that is tailored for agent usage.  The :class:`BrowserManager` handles
browser launch, creation of isolated contexts with optional cookie loading,
and cleanup of all resources.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

try:  # pragma: no cover - optional dependency during documentation builds
    from playwright.sync_api import Browser, BrowserContext, sync_playwright
except Exception:  # pragma: no cover
    Browser = BrowserContext = None  # type: ignore
    sync_playwright = None  # type: ignore


class BrowserManager:
    """Utility class for managing a Playwright browser instance.

    Parameters
    ----------
    headless:
        Whether to run the browser in headless mode.  Defaults to ``True``.
    viewport:
        Optional viewport dictionary with ``width`` and ``height`` keys used
        for all created contexts.
    user_agent:
        Optional user agent string applied to created contexts.
    """

    def __init__(
        self,
        headless: bool = True,
        viewport: Optional[Dict[str, int]] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        self.headless = headless
        self.viewport = viewport
        self.user_agent = user_agent
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._contexts: List[BrowserContext] = []

    # ------------------------------------------------------------------
    def launch(self) -> None:
        """Launch the underlying browser if not already running."""

        if self._browser is not None:
            return
        if sync_playwright is None:  # pragma: no cover - missing dependency
            raise RuntimeError("playwright is not installed")

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)

    # ------------------------------------------------------------------
    def new_context(self, cookie_path: Optional[str] = None) -> BrowserContext:
        """Create a new browser context.

        If ``cookie_path`` points to a JSON file containing cookies in
        Playwright's storage state format, they are loaded into the context
        before any navigation occurs.
        """

        if self._browser is None:
            self.launch()
        assert self._browser is not None  # for type checkers

        kwargs: Dict = {}
        if self.viewport:
            kwargs["viewport"] = self.viewport
        if self.user_agent:
            kwargs["user_agent"] = self.user_agent
        if cookie_path and Path(cookie_path).exists():
            kwargs["storage_state"] = str(cookie_path)

        context = self._browser.new_context(**kwargs)
        self._contexts.append(context)
        return context

    # ------------------------------------------------------------------
    def close(self) -> None:
        """Close all contexts and the browser."""

        for ctx in list(self._contexts):
            try:
                ctx.close()
            except Exception:  # pragma: no cover - best effort cleanup
                pass
        self._contexts.clear()

        if self._browser is not None:
            try:
                self._browser.close()
            finally:
                self._browser = None

        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None


__all__ = ["BrowserManager"]

