"""Utilities for interacting with web based chat prompts.

This module encapsulates the logic required to reliably enter text into a
prompt text area on a web page and submit it.  It is written with
Playwright-style ``Page`` objects in mind but only relies on a minimal
subset of the API so it can be easily mocked for unit testing.  The
functions try multiple selectors for locating the input box and send
button, simulate human typing with randomized delays, and fall back to a
JavaScript snippet if the standard submission paths fail.  Optionally the
class can block until response streaming has completed before returning
control to the caller.
"""

from __future__ import annotations

import random
import time
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - optional Playwright typing
    from playwright.sync_api import Locator, Page


class PromptInteractor:
    """Interact with a chat style prompt on a web page."""

    # Candidate selectors for locating elements.  ARIA and ``data-*``
    # attributes are used where possible for robustness across updates to
    # the UI being automated.
    input_selectors: Sequence[str] = (
        "textarea[aria-label='Message']",
        "textarea[aria-label='Enter your message']",
        "textarea[data-id='prompt-textarea']",
        "textarea[data-testid='chat-input']",
    )

    send_button_selectors: Sequence[str] = (
        "button[aria-label='Send message']",
        "button[data-testid='send-button']",
        "button[type='submit']",
    )

    # Selector that indicates streaming output from the assistant.  When
    # present we wait for it to detach before returning to the caller.
    streaming_selector: str = "[data-streaming='true']"

    def __init__(self, page: "Page") -> None:
        self.page = page

    # ------------------------------------------------------------------
    def locate_input(self):
        """Locate the prompt input element using known selectors."""

        for selector in self.input_selectors:
            element = self.page.query_selector(selector)
            if element:
                return element
        raise RuntimeError("Prompt input box could not be found")

    # ------------------------------------------------------------------
    def type_text(
        self, text: str, min_delay: float = 0.03, max_delay: float = 0.15
    ) -> None:
        """Type ``text`` into the input element using random delays."""

        field = self.locate_input()
        field.click()
        for char in text:
            field.type(char)
            time.sleep(random.uniform(min_delay, max_delay))

    # ------------------------------------------------------------------
    def _press_enter(self, field) -> bool:
        """Attempt to submit by pressing the Enter key."""

        try:
            field.press("Enter")
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    def _click_send(self) -> bool:
        """Attempt to submit by clicking a send button."""

        for selector in self.send_button_selectors:
            button = self.page.query_selector(selector)
            if not button:
                continue
            try:
                button.click()
                return True
            except Exception:
                continue
        return False

    # ------------------------------------------------------------------
    def _fallback_submit(self, field) -> None:
        """Last resort: execute a JS snippet to submit the form."""

        try:
            self.page.evaluate("el => el.form && el.form.submit()", field)
        except Exception:
            # Nothing else we can do; swallow the error so control is
            # returned to the caller.
            pass

    # ------------------------------------------------------------------
    def _wait_for_streaming_to_finish(self, timeout: float) -> None:
        """Block until assistant response streaming has finished."""

        try:
            # First wait briefly for streaming to begin.  If the selector is
            # never attached the subsequent wait with state="detached" will
            # return immediately.
            self.page.wait_for_selector(
                self.streaming_selector, state="attached", timeout=1000
            )
            self.page.wait_for_selector(
                self.streaming_selector, state="detached", timeout=timeout
            )
        except Exception:
            # Timeouts or missing selector shouldn't raise to caller
            # because the best effort was made to detect completion.
            pass

    # ------------------------------------------------------------------
    def submit(self, wait_for_response: bool = True, timeout: float = 120.0) -> None:
        """Submit the currently typed text and optionally wait for a reply."""

        field = self.locate_input()
        if not self._press_enter(field):
            if not self._click_send():
                self._fallback_submit(field)

        if wait_for_response:
            self._wait_for_streaming_to_finish(timeout)

    # ------------------------------------------------------------------
    def interact(self, text: str, wait_for_response: bool = True) -> None:
        """High level helper that types text then submits it."""

        self.type_text(text)
        self.submit(wait_for_response=wait_for_response)


__all__ = ["PromptInteractor"]
