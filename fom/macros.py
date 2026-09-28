"""Explicit surface expansions; open predicates are never ontology-refined."""
from __future__ import annotations

from dataclasses import dataclass, replace

from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from .parser import parse


class MacroError(ValueError):
    def __init__(self, message: str, expr: Expr):
        super().__init__(f"{expr.loc.line}:{expr.loc.col}: {message}")
        self.message = message
        self.loc = expr.loc


@dataclass(frozen=True)
class Expansion:
    macro: str
    source: Expr
    target: str


def expand_macros(root: Expr) -> tuple[Expr, list[Expansion]]:
    expansions: list[Expansion] = []
    centers: dict[str, Atom | None] = {}

    def declared_center(expr: ListExpr) -> Atom | None:
        if len(expr.items) > 2 and isinstance(expr.items[2], MapExpr):
            for key, value in expr.items[2].items:
                if key.value == "center" and isinstance(value, Atom) and value.kind == "symbol":
                    return value
        return None

    def collect(expr: Expr) -> None:
        if isinstance(expr, Atom):
            return
        if isinstance(expr, MapExpr):
            for _, value in expr.items:
                collect(value)
            return
        if (isinstance(expr, ListExpr) and len(expr.items) >= 2
                and isinstance(expr.items[0], Atom) and expr.items[0].kind == "symbol"
                and expr.items[0].value == "scope"
                and isinstance(expr.items[1], Atom) and expr.items[1].kind == "symbol"):
            centers[str(expr.items[1].value)] = declared_center(expr)
        for item in expr.items:
            collect(item)

    collect(root)

    def walk(expr: Expr, center: Atom | None = None) -> Expr:
        if isinstance(expr, Atom):
            return expr
        if isinstance(expr, VectorExpr):
            return replace(expr, items=tuple(walk(item, center) for item in expr.items))
        if isinstance(expr, MapExpr):
            return replace(expr, items=tuple((key, walk(value, center)) for key, value in expr.items))
        if not expr.items:
            return expr
        head = expr.items[0]
        name = head.value if isinstance(head, Atom) and head.kind == "symbol" else None
        if name == "self":
            if len(expr.items) != 1:
                raise MacroError("SELF takes no arguments", expr)
            if center is None:
                raise MacroError("SELF requires a current scope with a symbolic :center", expr)
            expansions.append(Expansion("self", expr, str(center.value)))
            return Atom("symbol", center.value, expr.loc, expr.end)
        if name == "scope":
            # A new perspective never silently borrows the outer center or owner.
            center = declared_center(expr)
        elif (name in {"accept", "reject"} and len(expr.items) in {3, 4}
              and isinstance(expr.items[1], Atom) and expr.items[1].kind == "symbol"
              and not isinstance(expr.items[2], MapExpr)):
            # Explicit status scope is equivalent to lexical status shorthand.
            center = centers.get(str(expr.items[1].value))
        return replace(expr, items=tuple(walk(item, center) for item in expr.items))

    return walk(root), expansions


def parse_expanded(text: str) -> Expr:
    return expand_macros(parse(text))[0]
