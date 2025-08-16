import pytest

from src.core.lifecycle_orchestrator import gate_pass


def test_gate_pass_basic_operations():
    ctx = {"A": True, "B": False, "C": True}
    assert gate_pass("A and not B", ctx) is True
    assert gate_pass("A and B", ctx) is False
    assert gate_pass("A or B and C", ctx) is True  # "A or (B and C)" -> True


def test_gate_pass_unknown_name_is_false():
    ctx = {"A": True}
    assert gate_pass("A and B", ctx) is False


def test_gate_pass_parse_error_returns_false():
    ctx = {"A": True, "B": True}
    assert gate_pass("A && B", ctx) is False


def test_gate_pass_unsupported_tokens_return_false():
    ctx = {"A": True, "B": True}
    assert gate_pass("A + B", ctx) is False
    assert gate_pass("__import__('os')", ctx) is False
