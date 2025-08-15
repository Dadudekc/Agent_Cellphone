"""Utilities for navigating the ChatGPT web interface using Playwright.

This module provides a small helper class that can be used by other
components to open a ChatGPT conversation in a new page and wait until
the interface is ready for interaction.  The class keeps a reference to
an active :class:`playwright.async_api.Page` instance so that callers can
continue interacting with the page after navigation.
"""

from __future__ import annotations

from typing import Optional

from playwright.async_api import BrowserContext, Page

# Default URL used when no specific conversation is supplied.  This loads a
# fresh "new chat" conversation in the ChatGPT interface.
CHATGPT_NEW_CHAT_URL = "https://chat.openai.com/"


class ChatGPTNavigator:
    """Helper for navigating to ChatGPT conversations.

    The class is intentionally lightweight – it simply opens a new page
    within the provided browser context, navigates to the desired
    conversation (or a fresh chat if none is provided) and waits for the
    message input box to become available.  Callers can then retrieve the
    :class:`Page` object for further scripted interactions.
    """

    def __init__(self) -> None:
        self._page: Optional[Page] = None

    async def navigate_to_chat(
        self,
        context: BrowserContext,
        conversation_url: Optional[str] = None,
    ) -> Page:
        """Navigate to a ChatGPT conversation and wait until ready.

        Parameters
        ----------
        context:
            The Playwright :class:`BrowserContext` in which to create the
            page.
        conversation_url:
            Optional URL to a specific conversation.  If ``None`` a new
            chat is opened using :data:`CHATGPT_NEW_CHAT_URL`.

        Returns
        -------
        Page
            The Playwright page that was created and navigated.
        """

        url = conversation_url or CHATGPT_NEW_CHAT_URL

        # Open a new page within the provided context and navigate to the URL
        self._page = await context.new_page()
        await self._page.goto(url)

        # The ChatGPT interface is considered ready once the message input
        # textarea is present.  Waiting for it avoids race conditions where
        # subsequent actions would fail because the page is not fully loaded.
        await self._page.wait_for_selector("textarea", timeout=60_000)
        return self._page

    def get_active_page(self) -> Page:
        """Return the active page created by :meth:`navigate_to_chat`.

        Raises
        ------
        RuntimeError
            If :meth:`navigate_to_chat` has not been called yet.
        """

        if self._page is None:
            raise RuntimeError("No active page – call navigate_to_chat first")
        return self._page


__all__ = ["ChatGPTNavigator", "CHATGPT_NEW_CHAT_URL"]
