from __future__ import annotations

import pytest

from src.services.prompt_interactor import PromptInteractor


class FakeElement:
    def __init__(self, *, press_raises: bool = False, click_raises: bool = False):
        self.typed = ""
        self.pressed = []
        self.clicked = False
        self.press_raises = press_raises
        self.click_raises = click_raises

    def click(self) -> None:
        if self.click_raises:
            raise Exception("click failed")
        self.clicked = True

    def type(self, chars: str) -> None:
        self.typed += chars

    def press(self, key: str) -> None:
        if self.press_raises:
            raise Exception("press failed")
        self.pressed.append(key)


class FakePage:
    def __init__(self, elements: dict[str, FakeElement] | None = None):
        self.elements = elements or {}
        self.evaluate_called = False
        self.wait_calls = []

    def query_selector(self, selector: str):  # pragma: no cover - exercised indirectly
        return self.elements.get(selector)

    def evaluate(self, *_):
        self.evaluate_called = True

    def wait_for_selector(self, selector: str, state: str | None = None, timeout: float | None = None):
        self.wait_calls.append((selector, state, timeout))


def test_locate_input_checks_all_selectors():
    inp = FakeElement()
    # Only the last selector from PromptInteractor.input_selectors is present
    selectors = PromptInteractor.input_selectors
    page = FakePage({selectors[-1]: inp})
    interactor = PromptInteractor(page)  # type: ignore[arg-type]
    assert interactor.locate_input() is inp


def test_submit_prefers_enter_then_click_then_fallback(monkeypatch):
    # First scenario: Enter key works
    input_el = FakeElement()
    page = FakePage({PromptInteractor.input_selectors[0]: input_el})
    interactor = PromptInteractor(page)  # type: ignore[arg-type]
    interactor.submit(wait_for_response=False)
    assert input_el.pressed == ["Enter"]
    assert not page.evaluate_called

    # Second scenario: Enter fails, click succeeds
    input_el = FakeElement(press_raises=True)
    send_btn = FakeElement()
    page = FakePage({
        PromptInteractor.input_selectors[0]: input_el,
        PromptInteractor.send_button_selectors[0]: send_btn,
    })
    interactor = PromptInteractor(page)  # type: ignore[arg-type]
    interactor.submit(wait_for_response=False)
    assert send_btn.clicked

    # Third scenario: both Enter and click fail -> JS fallback
    input_el = FakeElement(press_raises=True)
    send_btn = FakeElement(click_raises=True)
    page = FakePage({
        PromptInteractor.input_selectors[0]: input_el,
        PromptInteractor.send_button_selectors[0]: send_btn,
    })
    interactor = PromptInteractor(page)  # type: ignore[arg-type]
    interactor.submit(wait_for_response=False)
    assert page.evaluate_called


def test_wait_for_response_triggers_wait_calls(monkeypatch):
    input_el = FakeElement()
    page = FakePage({PromptInteractor.input_selectors[0]: input_el})
    interactor = PromptInteractor(page)  # type: ignore[arg-type]
    interactor.submit(wait_for_response=True, timeout=5)
    assert (
        (interactor.streaming_selector, "attached", 1000) in page.wait_calls
        and (interactor.streaming_selector, "detached", 5) in page.wait_calls
    )
