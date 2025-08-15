from __future__ import annotations

from typing import Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext

from .session_authenticator import SessionAuthenticator


class BrowserManager:
    """Launch and manage a Playwright browser instance.

    The manager ensures an authenticated session is available before any
    conversation logic is executed by leveraging :class:`SessionAuthenticator`.
    """

    def __init__(self, cookie_path: str = "cookies.json", headless: bool = True) -> None:
        self.cookie_path = cookie_path
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.auth = SessionAuthenticator(cookie_path)

    # ------------------------------------------------------------------
    def start(self, email: Optional[str] = None, password: Optional[str] = None) -> BrowserContext:
        """Launch browser and authenticate session.

        Cookie-based login is attempted first. If it fails, credential-based
        login is tried when ``email`` and ``password`` are provided. Otherwise,
        the user is prompted to log in manually.
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()

        if not self.auth.cookie_login(self.context):
            success = False
            if email and password:
                success = self.auth.credential_login(self.context, email, password)
            if not success:
                self.auth.await_manual_login(self.context)
            self.auth.save_cookies()

        return self.context

    # ------------------------------------------------------------------
    def stop(self) -> None:
        """Close browser resources."""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        finally:
            if self.playwright:
                self.playwright.stop()

