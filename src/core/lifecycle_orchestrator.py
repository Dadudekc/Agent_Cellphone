"""Lifecycle orchestration utilities."""
from __future__ import annotations

import ast
import logging
from typing import Mapping


logger = logging.getLogger(__name__)


class _GateEvaluator(ast.NodeVisitor):
    """Safely evaluate a boolean gate expression.

    Only a minimal subset of Python's AST is supported:
    - Boolean operations: ``and`` / ``or``
    - Unary negation: ``not``
    - Parentheses (handled by AST structure)
    - Boolean constants: ``True`` / ``False``
    - Names mapped to boolean values supplied via ``context``

    Any other syntax results in a ``ValueError``.
    """

    def __init__(self, context: Mapping[str, bool]):
        self.context = context

    # Entry point
    def visit_Expression(self, node: ast.Expression) -> bool:  # pragma: no cover - delegator
        return self.visit(node.body)

    # Boolean operations: and / or
    def visit_BoolOp(self, node: ast.BoolOp) -> bool:
        if isinstance(node.op, ast.And):
            return all(self.visit(v) for v in node.values)
        if isinstance(node.op, ast.Or):
            return any(self.visit(v) for v in node.values)
        raise ValueError("Unsupported boolean operator")

    # Unary operations: not
    def visit_UnaryOp(self, node: ast.UnaryOp) -> bool:
        if isinstance(node.op, ast.Not):
            return not self.visit(node.operand)
        raise ValueError("Unsupported unary operator")

    # Names -> lookup in context
    def visit_Name(self, node: ast.Name) -> bool:
        if node.id in self.context:
            return bool(self.context[node.id])
        raise ValueError(f"Unknown gate: {node.id}")

    # Boolean constants
    def visit_Constant(self, node: ast.Constant) -> bool:
        if isinstance(node.value, bool):
            return node.value
        raise ValueError("Only boolean constants allowed")

    # Disallow all other nodes
    def generic_visit(self, node: ast.AST):  # pragma: no cover - error path
        raise ValueError(f"Unsupported expression: {type(node).__name__}")


def gate_pass(expr: str, context: Mapping[str, bool]) -> bool:
    """Return ``True`` if the gate expression evaluates to truthy.

    Parameters
    ----------
    expr:
        A string containing a boolean expression referencing gates in ``context``.
    context:
        Mapping of gate names to boolean values.

    Returns
    -------
    bool
        Result of the evaluated expression. If parsing fails or unsupported
        tokens are encountered, ``False`` is returned.
    """

    try:
        tree = ast.parse(expr, mode="eval")
        evaluator = _GateEvaluator(context)
        return bool(evaluator.visit(tree))
    except Exception as exc:
        logger.debug("gate_pass parse error: %s", exc)
        return False
