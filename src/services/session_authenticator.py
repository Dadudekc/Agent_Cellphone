from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from playwright.sync_api import BrowserContext


class SessionAuthenticator:
    """Handle authenticated browser sessions via cookie or credential login.

    This utility attempts to reuse saved cookies to establish a session. If
    cookies are missing or invalid, it can fall back to credential-based login
    or wait for a manual login. After a successful login the current cookies can
    be persisted for future runs.
    """

    def __init__(self, cookie_path: str = "cookies.json", login_url: str = "https://chat.openai.com") -> None:
        self.cookie_path = Path(cookie_path)
        self.login_url = login_url
        self.context: Optional[BrowserContext] = None

    # ------------------------------------------------------------------
    def load_cookies(self, path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load cookies from *path*.

        Returns an empty list if the file does not exist or cannot be read.
        """
        file_path = Path(path) if path else self.cookie_path
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception:
            return []

    # ------------------------------------------------------------------
    def save_cookies(self, path: Optional[str] = None) -> None:
        """Persist current context cookies to *path*.

        If no browser context has been assigned, this is a no-op.
        """
        if self.context is None:
            return
        file_path = Path(path) if path else self.cookie_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        cookies = self.context.cookies()
        file_path.write_text(json.dumps(cookies), encoding="utf-8")

    # ------------------------------------------------------------------
    def cookie_login(self, context: BrowserContext, path: Optional[str] = None) -> bool:
        """Inject cookies into *context* if available.

        Returns ``True`` if cookies were loaded and applied, ``False`` otherwise.
        """
        self.context = context
        cookies = self.load_cookies(path)
        if not cookies:
            return False
        context.add_cookies(cookies)
        return True

    # ------------------------------------------------------------------
    def credential_login(self, context: BrowserContext, email: str, password: str) -> bool:
        """Attempt credential-based login as a fallback.

        The implementation is generic and may need adjustment for specific
        authentication flows. It navigates to ``login_url`` and tries a simple
        email/password form submission.
        """
        self.context = context
        page = context.new_page()
        try:
            page.goto(self.login_url)
            page.fill('input[type="email"]', email)
            page.click('button:has-text("Continue")')
            page.fill('input[type="password"]', password)
            page.click('button:has-text("Continue")')
            page.wait_for_url("**/chat")
            return True
        except Exception:
            return False
        finally:
            page.close()

    # ------------------------------------------------------------------
    def await_manual_login(self, context: BrowserContext, success_path: str = "/chat", timeout: int = 120) -> bool:
        """Wait for the user to complete login manually.

        A new page is opened and navigated to ``login_url``. The method blocks
        until a URL containing ``success_path`` is detected or ``timeout``
        seconds elapse.
        """
        self.context = context
        page = context.new_page()
        try:
            page.goto(self.login_url)
            page.wait_for_url(f"**{success_path}**", timeout=timeout * 1000)
            return True
        except Exception:
            return False
        finally:
            page.close()
